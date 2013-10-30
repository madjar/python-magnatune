import unittest


class TestSearchAlbum(unittest.TestCase):
    def test_search_by_album_name(self):
        from magnatune.search import search_album
        results = search_album(name='We Are Complex')

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].artist.name, 'Curl')

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
