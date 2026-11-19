import tempfile
from pathlib import Path
from alfarouqai import Scheduler
with tempfile.TemporaryDirectory() as temp:
    scheduler=Scheduler(Path(temp)/'jobs.sqlite')
    scheduler.add('example','text.analyze',{'text':'Hello students.'},run_at=0)
    print(scheduler.tick().to_dict());print(scheduler.tick().to_dict());scheduler.close()
