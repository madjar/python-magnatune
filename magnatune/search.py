import magnatune.api

HANDLED_ALBUM_ATTRS = {'artist', 'albumname', 'magnatunegenres', 'artistdesc'}


def search_album(**kw):
    """Search for albums matching the arguments."""
    if not HANDLED_ALBUM_ATTRS.issuperset(kw):
        raise TypeError(
            'unhandled search on attributes : {0}'
            .format(', '.join(set(kw.keys()).difference(HANDLED_ALBUM_ATTRS))))

    db = magnatune.api.get_database()
    for a in db.getroot().Album:
        for attr, value in kw.items():
            if value and not value.lower() in a.find(attr).text.lower():
                break
        else:
            yield a
