# Contributing | المساهمة
Current license reserves all rights; obtain written contribution/reuse terms
from Khalid Salman before submitting or redistributing original work.
التواصل: khalidsalman7140@gmail.com. لا تفترض وجود ترخيص مفتوح المصدر.

## Development
python -m venv .venv
python -m pip install -e '.[dev,ml,vision,documents]'
python -m pytest
python -m build
python -m twine check dist/*

Run with the virtual environment's interpreter (activate it first).
Every capability must declare inputs, return Result, be deterministic where
appropriate, use lazy imports, honor resource/network policy, avoid hidden
installation, and ship tests plus Arabic/English examples. Document weights
separately from library licenses. Never execute generated/untrusted code.

SemVer: pre-1.0 minor versions may break APIs; patches fix defects.
Maintain CHANGELOG, public schemas and migration notes. A release needs all
tests passing, a reviewed dependency lock per target platform, license review,
owner approval and confirmation of PyPI/GitHub namespace availability.
