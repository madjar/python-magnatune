import argparse
import logging
import magnatune.search
import magnatune.config

# TODO : not in the right place
FORMATS = {'ogg': '.ogg',
           'mp3': '.mp3',
           'mp3lofi': '-lofi.mp3'}

# TODO : the arg parsing could be improved

def main():
    parser = argparse.ArgumentParser(description="Search an album.")

    verbose = parser.add_mutually_exclusive_group()
    verbose.add_argument('--verbose', '-v', action='store_true',
                         help='Print informative output.')
    verbose.add_argument('--quiet', '-q', action='store_true',
                         help='Supress all non-warning informational output.')

    action = parser.add_mutually_exclusive_group()
    action.add_argument('--stream', '-s', action='store_true',
                        help='Output the streaming url of the track.')

    stream = parser.add_argument_group('Streaming options')
    stream.add_argument('--format', '-f', nargs='?', choices=FORMATS.keys(),
                        help='The format to use for streaming url.')

    action.add_argument('--download', '-d', action='store_true',
                        help='Download the albums.')

    download = parser.add_argument_group('Download options')
    download.add_argument('--dlformat', nargs='?',
                        choices=('web', 'wav', '128kmp3', 'ogg', 'vbr', 'flac'),
                        help='The format to use for downloading albums.')
    # TODO : add opus
    download.add_argument('--extract', '-e', nargs='?', const='.',
                        help='Extract downloaded albums to path (. by default).')

    parser.add_argument('--login', '-l',
                        help='The magnatune login and password in the '
                        '"login:passwd" format.')

    search = parser.add_argument_group('Search arguments')
    search.add_argument('--artist', '-a', help='Filter by artist name.')
    search.add_argument('--albumname', '-n', help='Filter by album name.')
    search.add_argument('--artistdesc', help='Filter by artist description.')
    search.add_argument('--genre', '-g', help='Filter by genre.')
    search.add_argument('--albumid', '-i', help='Filter by album id.')
    args = magnatune.config.ConfigArgs(parser.parse_args())

    if args.verbose:
        loglevel = logging.DEBUG
    elif args.quiet:
        loglevel = logging.WARN
    else:
        loglevel = logging.INFO
    logging.basicConfig(level=loglevel)
    logging.getLogger('requests').setLevel(logging.WARNING)

    if not (args.artist or args.albumname or args.genre or args.artistdesc or args.albumid):
        parser.error('no search filter given')

    if args.download and not args.login:
        parser.error('cannot download an album without subscription login')

    results = magnatune.search.search_album(artist=args.artist,
                                            name=args.albumname,
                                            genre=args.genre,
                                            description=args.artistdesc,
                                            sku=args.albumid)
    for a in results:
        if args.stream:
            format = FORMATS[args.format]
            for s in a.songs:
                print(magnatune.search.stream_url(s, format, args.login))
        elif args.download:
            magnatune.search.download(a.sku, args.dlformat, args.extract, args.login)
        else:
            print(a.artist.name, '--', a.name)
