from optparse import OptionParser

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec


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
  # print(token, sandbox, notebook_guid)

  client = EvernoteClient(token=token, sandbox=sandbox)
  store = client.get_note_store()

  filter = NoteFilter()
  filter.notebookGuid = notebook_guid

  spec = NotesMetadataResultSpec()
  spec.includeTitle = True
  spec.includeCreated = True
  spec.includeAttributes = True

  metadata_list = store.findNotesMetadata(filter, 0, 3, spec)
  print(f'Note Count: {metadata_list.totalNotes}')


if __name__ == "__main__":
  main()
