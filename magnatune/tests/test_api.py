import unittest
import mock


class MockDbm(dict):
    def close(self):
        pass


class TestXMLDownload(unittest.TestCase):
    def patch(self, *args, **kwargs):
        patcher = mock.patch(*args, **kwargs)
        mock_object = patcher.start()
        self.addCleanup(patcher.stop)
        return mock_object

    def setUp(self):
        self.download = self.patch('magnatune.api.download')

        self.dbm = MockDbm()
        open = self.patch('dbm.open')
        open.return_value = self.dbm

        self.server_time = 123456789
        time = self.patch('time.time')
        time.return_value = self.server_time

        self.server_crc = 'servercrc'
        self.urlopen = self.patch('urllib.request.urlopen')
        self.urlopen().read.return_value = self.server_crc
        self.urlopen.reset_mock()

        self.patch('magnatune.config.check_config_dir')

    def test_non_existing_file(self):
        from magnatune.api import update_if_needed
        update_if_needed()

        self.download.assert_called_once_with()

    def test_recent_update(self):
        self.dbm['updated'] = '123456788.42'

        from magnatune.api import update_if_needed
        update_if_needed()

        self.assertFalse(self.download.called)

    def test_crc_unchanged(self):
        self.dbm['crc'] = self.server_crc
        self.dbm['updated'] = 1

        from magnatune.api import update_if_needed, CRC_URL
        update_if_needed()

        self.urlopen.assert_called_once_with(CRC_URL)
        self.assertFalse(self.download.called)

    def test_download_needed(self):
        self.dbm['crc'] = self.server_crc + 'changed'
        self.dbm['updated'] = 1

        from magnatune.api import update_if_needed, CRC_URL
        update_if_needed()

        self.download.assert_called_once_with()
        self.urlopen.assert_called_once_with(CRC_URL)
        self.assertEqual(self.dbm['crc'], self.server_crc)
        self.assertEqual(self.dbm['updated'], str(self.server_time))


class TestDownload(unittest.TestCase):
    @mock.patch('urllib.request.urlretrieve')
    def test_download(self, urlretrieve):
        from magnatune.api import download, ALBUM_INFO_URL, album_info_file
        download()
        urlretrieve.assert_called_once_with(ALBUM_INFO_URL, album_info_file)
