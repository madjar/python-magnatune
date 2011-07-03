import argparse
import logging
import magnatune.search

FORMATS = {'ogg': 'oggurl',
           'mp3': 'url',
           'mp3lofi': 'mp3lofi'}


def get_log_level(args):
    return ({0: logging.WARN, 1: logging.INFO}
                 .get(len(args.verbose), logging.DEBUG))


def main():
    parser = argparse.ArgumentParser(description="Search an album.")

    parser.add_argument('--verbose', '-v', action='append_const',
                        const=None, default=[],
                        help='Print informative output. Twice for debug.')
    parser.add_argument('--stream', '-s', nargs='?', const='ogg',
                        choices=FORMATS.keys(),
                        help='Output the streaming url of the track. Takes an '
                             'optional argument to determine the format.')

    group = parser.add_argument_group('Search arguments')
    group.add_argument('--artist', '-a', help='Filter by artist name.')
    group.add_argument('--albumname', '-n', help='Filter by album name.')
    group.add_argument('--artistdesc', '-d',
                       help='Filter by artist description.')
    group.add_argument('--genre', '-g', help='Filter by genre.')

    args = parser.parse_args()

    logging.basicConfig(level=get_log_level(args))

    if not (args.artist or args.albumname or args.genre or args.artistdesc):
        parser.error('no search filter given')

    for a in magnatune.search.search_album(artist=args.artist,
                                           albumname=args.albumname,
                                           magnatunegenres=args.genre,
                                           artistdesc=args.artistdesc):
        if args.stream:
            for t in a.Track:
                print(t.find(FORMATS[args.stream]))
        else:
            print(a.albumname, 'by', a.artist)
