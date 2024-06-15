import unittest
from unittest.mock import patch
import hashlib
from main import get_country_data, encrypt_language, process_country_data

class TestCountryDataProcessing(unittest.TestCase):

    @patch('requests.get')
    def test_get_country_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'name': {'common': 'Country1'}, 'languages': {'en': 'English'}}]
        data = get_country_data()
        self.assertIsInstance(data, list)

    def test_encrypt_language(self):
        language = 'English'
        encrypted = encrypt_language(language)
        self.assertEqual(encrypted, hashlib.sha1(language.encode('utf-8')).hexdigest())

    @patch('requests.get')
    def test_process_country_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'name': {'common': 'Country1'}, 'languages': {'en': 'English'}}]
        records = process_country_data()
        self.assertEqual(len(records), 1)
        self.assertIn('Country', records[0])
        self.assertIn('Language', records[0])
        self.assertIn('Encrypted Language', records[0])
        self.assertIn('Time', records[0])

if __name__ == '__main__':
    unittest.main()