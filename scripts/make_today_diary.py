from datetime import datetime
from optparse import OptionParser
from evernote.api.client import EvernoteClient, Store
from evernote.edam.type import ttypes
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec


def main() -> None:
  parser = OptionParser()
  parser.add_option("--token", type="string", help="Evernote developer token")
  parser.add_option("--prod", action="store_true", default=False,
                    dest="production", help="Use production")
  parser.add_option("--guid", type="string", help="Notebook GUID")
  parser.add_option("--tag-guid", type="string", dest="tag_guid", help="Tag GUID")
  parser.add_option("--dry-run", action="store_true", default=False,
                    dest="dry_run", help="Execute as DryRun mode.")

  (options, args) = parser.parse_args()

  token: str = options.token
  sandbox: bool = not options.production
  notebook_guid: str = options.guid
  tag_guid = options.tag_guid
  dry_run = options.dry_run
  print(f'\nArgs: {token}, {sandbox}, {notebook_guid}, {tag_guid}, {dry_run}')

  client = EvernoteClient(token=token, sandbox=sandbox)
  store = client.get_note_store()

  metadata, note = find_note(store, notebook_guid, tag_guid)
  ret = create_note(store, token, metadata, note, dry_run)
  print('')
  print(ret)


def find_note(store: Store, notebook_guid: str, tag_guid: str) -> []:
  filter = NoteFilter()
  filter.notebookGuid = notebook_guid
  filter.ascending = False
  filter.order = ttypes.NoteSortOrder.UPDATED

  if tag_guid:
    filter.tagGuids = [tag_guid]

  spec = NotesMetadataResultSpec()
  spec.includeTitle = True
  spec.includeCreated = True
  spec.includeAttributes = True
  spec.includeTagGuids = True

  metadata_list = store.findNotesMetadata(filter, 0, 1, spec)

  if not metadata_list:
    return [None, None]

  note_guid = metadata_list.notes[0].guid
  note = store.getNote(note_guid, True, False, False, False)

  return [metadata_list.notes[0], note]


def create_note(store, token, src_metadata, src_note, dry_run):

  def create_title():
    return f'{datetime.now().strftime("%y%m%d")} Diary'

  note = ttypes.Note()
  note.notebookGuid = src_metadata.notebookGuid
  note.tagGuids = src_metadata.tagGuids
  note.title = create_title()
  note.content = src_note.content

  if dry_run:
    print('')
    print('DRY-RUN:')
    print(note)
    print('')
    return None

  else:
    note = store.createNote(token, note)
    return note


if __name__ == '__main__':
  main()
