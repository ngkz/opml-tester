# opml-tester
broken feed checker

## Usage
```sh
$ python3 -m venv env
$ . env/bin/activate
$ pip install -r requirements.txt
$ ./opml-tester.py feedly.opml
Checking feed [REDACTED] (https://[REDACTED])... OK
Checking feed [REDACTED] (http://[REDACTED])... NG (HTTP)
Checking feed [REDACTED] (http://[REDACTED])... OLD (9mo)
Checking feed [REDACTED] (https://[REDACTED])... OLD (2yr)
Checking feed [REDACTED] (http://[REDACTED])... MOVED TO https://[REDACTED]
Checking feed [REDACTED] (http://[REDACTED])... NG (FEED)
Checking page [REDACTED] (https://[REDACTED])... OK
```
