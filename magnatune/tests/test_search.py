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

        album.find().text = mock.MagicMock()
        album.find().text.__contains__.return_value = True

        attrs = ('artist', 'albumname', 'magnatunegenres', 'artistdesc')
        call = {att: att + 'called' for att in attrs}

        from magnatune.search import search_album
        list(search_album(**call))

        self.assertEqual(album.find().text.__contains__.call_args_list,
            [((value,), {}) for value in call.values()])

    def test_wrong_arg(self):
        from magnatune.search import search_album
        with self.assertRaises(TypeError):
            list(search_album(ratatouille='plonk'))
