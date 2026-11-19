"""In-process explicit plugin registration; no hidden imports."""
from alfarouqai import Client, Capability, Result
def word_count(*,text,config):
    return Result('custom.words',{'count':len(text.split())},'custom.python')
client=Client()
client.registry.register(Capability('custom.words',word_count,'Custom word counter',('text',)))
print(client.run('custom.words',text='Hello AlFarouq AI').to_dict())
# Installed plugin metadata: [project.entry-points."alfarouqai.plugins"]
# example = "your_package:register"; register(registry) must call registry.register.
# Load trusted installed plugins only: client.registry.load_plugins(consent=True)
