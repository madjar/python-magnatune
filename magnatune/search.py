import logging
import urllib.request
import webbrowser
import lxml.etree
import magnatune.api


logger = logging.getLogger(__name__)


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


def auth_url(url, login):
    return (url.replace('http://he3', 'http://{}@download'.format(login))
            .replace('.mp3', '_nospeech.mp3').replace('.ogg', '_nospeech.ogg'))


def stream_url(track, format, login):
     url = str(track.find(format))
     if login:
        return auth_url(url, login)
     else:
         return url


def download(sku, format, login):
    user, pwd = login.split(':')
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, 'https://download.magnatune.com', user, pwd)
    auth_manager = urllib.request.HTTPBasicAuthHandler(password_manager)
    opener = urllib.request.build_opener(auth_manager)

    url = ("http://download.magnatune.com/buy/"
           "membership_free_dl_xml?id=python&sku={}".format(sku))
    logger.debug("Downloading %s", url)
    content = opener.open(url).read()
    content = content.replace(b'<br>', b'')  # Workaround because the xml is malformated
    response = lxml.etree.fromstring(content)

    if format == 'web':
        url = response.find('DL_PAGE').text
        print(url)
        webbrowser.open(url)
    else:
        urlzip = response.find('URL_{}ZIP'.format(format.upper()))
        if urlzip is None:
            raise Exception('Unknown download format : %s' % format)
        print(urlzip.text)
        # TODO : download the zip file, and maybe even decompress
