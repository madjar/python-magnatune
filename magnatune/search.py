import sys
import logging
import requests
import urllib.parse
import webbrowser
import zipfile
import lxml.etree
from magnatune.api import get_session, Album, Artist


logger = logging.getLogger(__name__)


HANDLED_ALBUM_ATTRS = {'artist', 'name', 'genre', 'description', 'sku'}

# TODO : I'm not sure this abstraction is usefull
def search_album(**kw):
    """Searchs for albums matching the arguments."""
    if not HANDLED_ALBUM_ATTRS.issuperset(kw):
        raise TypeError(
            'unhandled search on attributes : {0}'
            .format(', '.join(set(kw.keys()).difference(HANDLED_ALBUM_ATTRS))))

    session = get_session()

    # TODO : case sensitivity might be a problem
    query = session.query(Album)
    for attr, value in kw.items():
        if value:
            if attr == 'genre':
                # TODO : useless without a documentation of available genres
                query = query.filter(Album.genres.contains(value))
            elif attr == 'artist':
                query = query.join(Artist).filter(Artist.name.like('%' + value + '%'))
            else:
                query = query.filter(getattr(Album, attr).like('%' + value + '%'))
    return query.all()


def auth_url(url, login):
    """Adds authentification to a streaming url"""
    return (url.replace('http://he3', 'http://{}@download'.format(login))
            .replace('.mp3', '_nospeech.mp3').replace('.ogg', '_nospeech.ogg'))


def stream_url(song, format, login=None):
    """Returns a streaming url for given track, in given format with given
    login."""
    filename = urllib.parse.quote(song.mp3.replace('.mp3', format))
    url = "http://he3.magnatune.com/all/" + filename
    if login:
        return auth_url(url, login)
    else:
        return url


def download(sku, format, extract=False, login=None):
    """Downloads the album with given sku id in given format, with given login.

    If extract is not empty, also extract to the given path."""
    # Preparation for the login
    auth = tuple(login.split(':'))

    # Download of the information file
    url = ("http://download.magnatune.com/buy/"
           "membership_free_dl_xml?id=python&sku={}".format(sku))
    logger.debug("Downloading %s", url)

    content = requests.get(url, auth=auth).content
    content = content.replace(b'<br>', b'')  # Workaround because the xml is malformated
    # TODO : don't use lxml for this one
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
        response = requests.get(urlzip.text, auth=auth, stream=True)
        # This is for the progress bar
        size = int(response.headers.get("Content-Length", -1))
        width = 32
        bs = 1024*8
        blocknum = 0
        output = logging.INFO >= logger.getEffectiveLevel()
        with open(filename, 'wb') as dest:
            for chunk in response.iter_content(bs):
                dest.write(chunk)
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
