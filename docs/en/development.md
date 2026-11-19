> Preserved 0.1.0 documentation. Current status: [0.2 handbook](handbook-0.2.md) and [0.2 matrix](capabilities-0.2.md).

# Development, plugins and release preparation
[العربية](../ar/development.md) · [Contribution policy](../../CONTRIBUTING.md)

## Implement a real capability
```python
from alfarouqai import Client, Capability, Result

def word_count(*, text, config):
    return Result('custom.words', {'count':len(text.split())}, 'my-plugin')

client = Client()
client.registry.register(Capability('custom.words', word_count, 'Word count', ('text',)))
print(client.run('custom.words',text='Hello AlFarouq AI').data)
```
Use explicit keyword parameters; unknown inputs and duplicate capability names are
rejected. Honor Config, lazy imports, consent policy, resource limits and provenance.
Ship Arabic/English documentation and real success/failure tests. Do not register
names that merely raise NotImplementedError or return hard-coded model results.

For a separate installed distribution:
```toml
[project.entry-points."alfarouqai.plugins"]
counter = "my_plugin:register"
```
`register(registry)` calls registry.register(Capability(...)). Load trusted installed
plugins only with `client.registry.load_plugins(consent=True)`. Discovery does not
confer trust: loading runs Python with your process privileges, not in a sandbox.

## Tests and packaging
```bash
python -m pip install -e '.[dev,ml,vision,documents]'
python -m pytest
python -m build
python -m twine check dist/*
```
The PDF fixture test also needs reportlab; without it that test explicitly skips.
Actual model-weight inference tests are not yet supplied. reports/environment.json
and verified-requirements.txt record the tested environment, not a portable hash
lock or vulnerability audit. CI templates target multiple OS/Python versions but
have not run on GitHub in this delivery.

## Publication is explicitly deferred
Repository files, templates, CI, package metadata, wheel and sdist are prepared.
No external repository was created, no namespace reserved and no public upload made.
After owner approval: decide a compatible license, verify PyPI/GitHub/trademark
availability, review public disclosure of email/photo/age, create a repository in
your account, run CI, build a new release and test TestPyPI with your credentials.
Only publish the final release after another explicit approval. There are no tokens
or publishing workflows here. Library version is maintained in pyproject.toml,
core.__version__ and CHANGELOG; pre-1.0 minor releases may change APIs.

The current all-rights-reserved terms require written permission for contributions
and reuse. Do not silently apply MIT while retaining a contradictory no-copying
restriction. Third-party licenses always apply to their own works separately.
