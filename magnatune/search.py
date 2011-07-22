import sys
import logging
import urllib.request
import webbrowser
import zipfile
import lxml.etree
import magnatune.api


logger = logging.getLogger(__name__)


HANDLED_ALBUM_ATTRS = {'artist', 'albumname', 'magnatunegenres', 'artistdesc'}


def search_album(**kw):
    """Searchs for albums matching the arguments."""
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
    """Adds authentification to a streaming url"""
    return (url.replace('http://he3', 'http://{}@download'.format(login))
            .replace('.mp3', '_nospeech.mp3').replace('.ogg', '_nospeech.ogg'))


def stream_url(track, format=None, login=None):
     """Returns a streaming url for given track, in given format with given login."""
     if not format:
         format = 'ogg'
     url = str(track.find(format))
     if login:
        return auth_url(url, login)
     else:
         return url


def download(sku, format=None, extract=False, login=None):
    """Downloads the album with given sku id in given format, with given login.

    If extract is not empty, also extract to the given path."""
    if not format:
        format = 'web'
    # Preparation for the login
    user, pwd = login.split(':')
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, 'https://download.magnatune.com', user, pwd)
    auth_manager = urllib.request.HTTPBasicAuthHandler(password_manager)
    opener = urllib.request.build_opener(auth_manager)

    # Download of the information file
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

        filename = urlzip.text.split('/')[-1]
        logger.debug("Downloading %s", urlzip.text)
        with opener.open(urlzip.text) as source, open(filename, 'wb') as dest:
            headers = source.info()
            width = 32
            bs = 1024*8
            blocknum = 0
            size = int(headers.get("Content-Length", -1))
            output = logging.INFO >= logger.getEffectiveLevel()
            while 1:
                block = source.read(bs)
                if not block:
                    break
                dest.write(block)
                blocknum += 1
                if output and blocknum % 16 == 0:
                    cur = blocknum * bs
                    x = (width + 1) * cur // size
                    bar = '{} [{}{}] {:.1f}/{:.1f}\r'.format(filename, '='*x,
                                                             '-'*(width-x),
                                                             cur/(1024*1024),
                                                             size/(1024*1024))
                    sys.stderr.write(bar)
                    sys.stderr.flush()
            if output:
                sys.stderr.write('\n')

        if extract:
            logger.info("Extracting %s", filename)
            zipfile.ZipFile(filename).extractall(path=extract)
