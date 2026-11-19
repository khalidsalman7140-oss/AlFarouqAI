# AlFarouq AI — ml.train

Backend: scikit-learn.RandomForest

```json
{
  "task": "ml.train",
  "data": {
    "problem": "classification",
    "target": "passed",
    "features": [
      "study_hours",
      "attendance",
      "track"
    ],
    "numeric_features": [
      "study_hours",
      "attendance"
    ],
    "train_rows": 75,
    "test_rows": 25,
    "seed": 42,
    "metrics": {
      "accuracy": 1.0,
      "f1_weighted": 1.0
    },
    "rows": [
      {
        "actual": "yes",
        "prediction": "yes"
      },
      {
        "actual": "yes",
        "prediction": "yes"
      },
      {
        "actual": "yes",
        "prediction": "yes"
      },
      {
        "actual": "no",
        "prediction": "no"
      },
      {
        "actual": "yes",
        "prediction": "yes"
      },
      {
        "actual": "yes",
        "prediction": "yes"
      },
      {
        "actual": "no",
        "prediction": "no"
      },
      {
        "actual": "yes",
        "prediction": "yes"
      },
      {
        "actual": "yes",
        "prediction": "yes"
      },
      {
        "actual": "yes",
        "prediction": "yes"
      },
      {
        "actual": "no",
        "prediction": "no"
      },
      {
        "actual": "yes",
        "prediction": "yes"
      },
      {
        "actual": "no",
        "prediction": "no"
      },
      {
        "actual": "no",
        "prediction": "no"
      },
      {
        "actual": "yes",
        "prediction": "yes"
      },
      {
        "actual": "no",
        "prediction": "no"
      },
      {
        "actual": "no",
        "prediction": "no"
      },
      {
        "actual": "yes",
        "prediction": "yes"
      },
      {
        "actual": "no",
        "prediction": "no"
      },
      {
        "actual": "no",
        "prediction": "no"
      },
      {
        "actual": "no",
        "prediction": "no"
      },
      {
        "actual": "no",
        "prediction": "no"
      },
      {
        "actual": "no",
        "prediction": "no"
      },
      {
        "actual": "no",
        "prediction": "no"
      },
      {
        "actual": "yes",
        "prediction": "yes"
      }
    ]
  },
  "backend": "scikit-learn.RandomForest",
  "warnings": [
    "Held-out split, not cross-validation. Not suitable evidence for time-series, grouped or causal claims; use domain-specific splits in future versions.",
    "Synthetic teaching fixture only. A high score is not evidence of real-world generalization."
  ],
  "provenance": {
    "input_sha256": "05d27f1fdd73884ea0e6ed6d9e1a28d1e0d823ec687930afff198a8946b17db2",
    "sklearn_version": "1.9.1"
  },
  "schema_version": "1.0"
}
```
