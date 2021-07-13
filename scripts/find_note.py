from optparse import OptionParser

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote.edam.type.ttypes import NoteSortOrder


def main():
  parser = OptionParser()
  parser.add_option("--token", type="string", help="Evernote developer token")
  parser.add_option("--prod", action="store_true", default=False,
                    dest="production", help="Use production")
  parser.add_option("--guid", type="string", help="Notebook GUID")
  parser.add_option("--tag-guid", type="string", dest="tag_guid", help="Tag GUID")

  (options, args) = parser.parse_args()

  token: str = options.token
  sandbox: bool = not options.production
  notebook_guid: str = options.guid
  tag_guid = options.tag_guid
  print(token, sandbox, notebook_guid, tag_guid)

  client = EvernoteClient(token=token, sandbox=sandbox)
  store = client.get_note_store()

  filter = NoteFilter()
  filter.notebookGuid = notebook_guid
  filter.ascending = False
  filter.order = NoteSortOrder.UPDATED

  if tag_guid:
    filter.tagGuids = [tag_guid]

  spec = NotesMetadataResultSpec()
  spec.includeTitle = True
  spec.includeCreated = True
  spec.includeAttributes = True
  spec.includeTagGuids = True

  metadata_list = store.findNotesMetadata(filter, 0, 1, spec)
  print(f'Note Count: {metadata_list.totalNotes}')

  if not metadata_list:
    return

  note_guid = metadata_list.notes[0].guid
  note = store.getNote(note_guid, True, False, False, False)
  print(note.content)


if __name__ == "__main__":
  main()
