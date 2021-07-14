# evernote-tools
My evernote tools

## Setup
```
$ git clone git@github.com:tayutaedomo/evernote-tools.git
$ cd evernote-tools
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Scripts
Sample code is bellow:
```
$ export EVERNOTE_DEV_TOKEN="<Your developer token for Sandbox>"
$ python scripts/get_notes.py
```

My trial codes are following:
```
$ python scripts/find_note.py --token "<Your developer token>" --guid="Target notebook GUID" --tag-guid="<Target tag GUID>"

$ python scripts/find_note.py --token "<Your developer token>" --guid="Target notebook GUID"
```
