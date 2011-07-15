import unittest
import mock


class TestSearchAlbum(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch('magnatune.api.get_database')
        self.db = patcher.start()()
        self.addCleanup(patcher.stop)

    def test_searching_with_all_params(self):
        album = mock.Mock()
        self.db.getroot().Album = [album]

        album.find().text.lower.return_value = mock.MagicMock()
        album.find().text.lower().__contains__.return_value = True

        attrs = ('artist', 'albumname', 'magnatunegenres', 'artistdesc')
        call = {att: att + 'called' for att in attrs}

        from magnatune.search import search_album
        list(search_album(**call))

        self.assertEqual(album.find().text.lower().__contains__.call_args_list,
            [((value,), {}) for value in call.values()])

    def test_wrong_arg(self):
        from magnatune.search import search_album
        with self.assertRaises(TypeError):
            list(search_album(ratatouille='plonk'))


class TestAuthUrl(unittest.TestCase):
    def test_adding_the_auth_to_urls_works(self):
        from magnatune.search import auth_url

        data = [('http://he3.magnatune.com/all/'
                 '01-Ouverture%20Le%20bourgeois%20gentilhomme%20(JB%20Lully)-'
                 'The%20Bach%20Players.{0}'.format(ext),
                 'http://tagada:test@download.magnatune.com/all/'
                 '01-Ouverture%20Le%20bourgeois%20gentilhomme%20(JB%20Lully)-'
                 'The%20Bach%20Players_nospeech.{0}'.format(ext))
        for ext in ('mp3', 'ogg')]

        for input, output in data:
            self.assertEqual(auth_url(input, 'tagada:test'), output)
