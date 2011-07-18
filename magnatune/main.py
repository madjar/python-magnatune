import argparse
import logging
import magnatune.search
import magnatune.config

FORMATS = {'ogg': 'oggurl',
           'mp3': 'url',
           'mp3lofi': 'mp3lofi'}


def main():
    parser = argparse.ArgumentParser(description="Search an album.")

    verbose = parser.add_mutually_exclusive_group()
    verbose.add_argument('--verbose', '-v', action='store_true',
                         help='Print informative output.')
    verbose.add_argument('--quiet', '-q', action='store_true',
                         help='Supress all non-warning informational output.')
    parser.add_argument('--stream', '-s', action='store_true',
                        help='Output the streaming url of the track.')
    parser.add_argument('--format', '-f', nargs='?', default='ogg',
                        choices=FORMATS.keys(),
                        help='The format to use for streaming url.')
    parser.add_argument('--login', '-l',
                        help='The magnatune login and password in the '
                        '"login:passwd" format')


    group = parser.add_argument_group('Search arguments')
    group.add_argument('--artist', '-a', help='Filter by artist name.')
    group.add_argument('--albumname', '-n', help='Filter by album name.')
    group.add_argument('--artistdesc', '-d',
                       help='Filter by artist description.')
    group.add_argument('--genre', '-g', help='Filter by genre.')

    args = magnatune.config.ConfigArgs(parser.parse_args())

    if args.verbose:
        loglevel = logging.DEBUG
    elif args.quiet:
        loglevel = logging.WARN
    else:
        loglevel = logging.INFO
    logging.basicConfig(level=loglevel)

    if not (args.artist or args.albumname or args.genre or args.artistdesc):
        parser.error('no search filter given')

    for a in magnatune.search.search_album(artist=args.artist,
                                           albumname=args.albumname,
                                           magnatunegenres=args.genre,
                                           artistdesc=args.artistdesc):
        if args.stream:
            format = FORMATS[args.format]
            for t in a.Track:
                print(magnatune.search.stream_url(t, format, args.login))
        else:
            print(a.albumname, 'by', a.artist)
