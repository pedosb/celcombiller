# Used third-party libraries

* pyst
  Interface with Asterisk using either AGI or Manager interfaces
* sqlalchemy
  Database interface

# Setup developemnt enrironment

```bash
$ virutalenv venv
$ source venv/bin/activate
$ pip install --allow-external pyst --allow-unverified pyst -r requirements.txt
```

## Database setup

Each SIP user must be inserted in the database of users with a balance. The python code snippet bellow is an example of a insertion of two users.

```python
from models import session, User
    session.add_all([User(clid='100000000', name='PSB', balance=100),
                    User(clid='200000000', name='LaPS', balance=100)
                    ])
    session.commit()
```

## Asterisk setup

With a working Asterisk server you must have at least two SIP accounts. An example of the corresponding section of `sip.conf` follows.

```
[1000000000]
type=friend
secret=laps
host=dynamic
context=celcom

[2000000000]
type=friend
secret=laps
host=dynamic
context=celcom
```

The referenced context in `sip.conf` must exist in the `extensions.conf` the code bellow is an example.

```
[celcom]
exten => _ZXXXXXXXX,1,AGI(celcombiller)
same  =>            n,NoOp(${CEL_MAX_DUR})
```

celcombiller is an AGI, implemented in the file [celcombiller.py](celcombiller.py) and it must run in the virtual environment created in the first section, a file with something like the content bellow should be created in `/var/lib/asterisk/agi-bin` with execution permission.

```
#!/bin/bash
/home/psb/Dropbox/git-projects/celcombiller/venv/bin/python /home/psb/git-projects/celcombiller/celcombiller.py
```
