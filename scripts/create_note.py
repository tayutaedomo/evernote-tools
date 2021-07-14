from optparse import OptionParser
from evernote.api.client import EvernoteClient
from evernote.edam.type import ttypes


def main():
  parser = OptionParser()
  parser.add_option("--token", type="string", help="Evernote developer token")
  parser.add_option("--prod", action="store_true", default=False,
                    dest="production", help="Use production")
  parser.add_option("--guid", type="string", help="Notebook GUID")

  (options, args) = parser.parse_args()

  token: str = options.token
  sandbox: bool = not options.production
  notebook_guid: str = options.guid
  print(token, sandbox, notebook_guid)

  client = EvernoteClient(token=token, sandbox=sandbox)
  store = client.get_note_store()

  # Refer: https://dev.evernote.com/doc/articles/creating_notes.php
  note_body = 'Hello, Evernote!'
  note_content = '<?xml version="1.0" encoding="UTF-8"?>'
  note_content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
  note_content += '<en-note>%s</en-note>' % note_body

  note = ttypes.Note()
  note.title = 'Create by script with API'
  note.content = note_content
  note.notebookGuid = notebook_guid

  note = store.createNote(token, note)
  print(note)


if __name__ == "__main__":
  main()
