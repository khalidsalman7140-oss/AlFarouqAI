# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Leakage-aware tabular training with explicit target and problem type."""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from .core import Result, ValidationError, ConsentRequired, require, fingerprint, atomic_write
from .local import read_csv, finite_number


@dataclass
class TrainedModel:
    pipeline: object
    features: list[str]
    target: str
    problem: str
    report: Result

    def predict(self, rows):
        pd = require('pandas', 'ml')
        if not isinstance(rows, list) or not rows or any(not isinstance(r, dict) or set(r) != set(self.features) for r in rows):
            raise ValidationError(f'Every prediction row must have exactly: {self.features}')
        frame = pd.DataFrame(rows, columns=self.features).replace('', float('nan'))
        # Repeat training coercions before the ColumnTransformer.
        for col in self.pipeline.alfarouq_numeric_columns:
            frame[col] = pd.to_numeric(frame[col], errors='raise')
        values = self.pipeline.predict(frame).tolist()
        return Result('ml.predict', {'rows': [{'prediction': v} for v in values]}, 'scikit-learn', provenance={'problem': self.problem, 'target': self.target})

    def save(self, path, *, consent=False):
        if not consent:
            raise ConsentRequired('Persist with skops only after consent=True; keep dependency versions and never trust unknown artifacts.')
        skops = require('skops.io', 'persistence')
        path = Path(path)
        if path.exists():
            raise FileExistsError(path)
        # Reserve output exclusively. Remove only our own incomplete file on error.
        with path.open('xb') as stream:
            try:
                skops.dump({'pipeline': self.pipeline, 'features': self.features, 'target': self.target, 'problem': self.problem}, stream)
            except Exception:
                path.unlink(missing_ok=True)
                raise
        return path


def train(*, data, target, problem, config, test_size=0.25, seed=42, **kwargs):
    if problem not in ('classification', 'regression'):
        raise ValidationError('problem must explicitly be classification or regression')
    if not 0.1 <= float(test_size) <= 0.5:
        raise ValidationError('test_size must be between 0.1 and 0.5')
    pd = require('pandas', 'ml')
    require('sklearn', 'ml')
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, r2_score
    p, rows = read_csv(data, config)
    if target not in rows[0] or len(rows[0]) < 2:
        raise ValidationError('target must exist and at least one feature is required')
    if len(rows) < 12:
        raise ValidationError('Need at least 12 rows for a meaningful train/test workflow')
    if any(not row[target].strip() for row in rows):
        raise ValidationError('Target contains missing labels')
    frame = pd.DataFrame(rows)
    X = frame.drop(columns=[target]).replace('', float('nan'))
    y = frame[target]
    if problem == 'regression':
        try:
            y = pd.to_numeric(y, errors='raise')
        except ValueError as exc:
            raise ValidationError('Regression target must be numeric') from exc
        if any(finite_number(v) is None for v in y):
            raise ValidationError('Regression target must be finite')
    else:
        counts = y.value_counts()
        if len(counts) < 2 or counts.min() < 2:
            raise ValidationError('Classification requires >=2 classes and >=2 rows per class')
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(test_size), random_state=int(seed), stratify=y if problem == 'classification' else None)
    except ValueError as exc:
        raise ValidationError(f'Cannot create a valid split: {exc}') from exc
    # Infer feature types on the TRAIN split only, never on held-out data.
    numeric = []
    for col in X.columns:
        vals = X_train[col].dropna().tolist()
        if vals and all(finite_number(v) is not None for v in vals):
            numeric.append(col)
            try:
                X_train[col] = pd.to_numeric(X_train[col], errors='raise')
                X_test[col] = pd.to_numeric(X_test[col], errors='raise')
            except ValueError as exc:
                raise ValidationError(f'Non-numeric held-out value in numeric training feature {col}') from exc
    categorical = [c for c in X.columns if c not in numeric]
    steps = []
    if numeric:
        steps.append(('numbers', Pipeline([('impute', SimpleImputer(strategy='median')), ('scale', StandardScaler())]), numeric))
    if categorical:
        steps.append(('categories', Pipeline([('impute', SimpleImputer(strategy='most_frequent')), ('encode', OneHotEncoder(handle_unknown='ignore'))]), categorical))
    estimator = (RandomForestClassifier if problem == 'classification' else RandomForestRegressor)(n_estimators=60, random_state=int(seed), n_jobs=1)
    pipe = Pipeline([('preprocess', ColumnTransformer(steps)), ('estimator', estimator)])
    pipe.alfarouq_numeric_columns = numeric
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    metrics = {'accuracy': accuracy_score(y_test, pred), 'f1_weighted': f1_score(y_test, pred, average='weighted', zero_division=0)} if problem == 'classification' else {'mae': mean_absolute_error(y_test, pred), 'r2': r2_score(y_test, pred)}
    import sklearn
    report = Result('ml.train', {'problem': problem, 'target': target, 'features': list(X.columns), 'numeric_features': numeric, 'train_rows': len(X_train), 'test_rows': len(X_test), 'seed': int(seed), 'metrics': metrics, 'rows': [{'actual': a, 'prediction': b} for a, b in zip(y_test.tolist(), pred.tolist())]}, 'scikit-learn.RandomForest', ['Held-out split, not cross-validation. Not suitable evidence for time-series, grouped or causal claims; use domain-specific splits in future versions.'], {'input_sha256': fingerprint(p), 'sklearn_version': sklearn.__version__})
    # Public train returns a Result; train_model returns the usable in-memory object.
    return TrainedModel(pipe, list(X.columns), target, problem, report)


def train_report(*, data, target, problem, config, test_size=0.25, seed=42):
    return train(data=data, target=target, problem=problem, config=config, test_size=test_size, seed=seed).report
