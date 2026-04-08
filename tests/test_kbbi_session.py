import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the current directory to sys.path
sys.path.append(r"d:\Saka-NLP")

from saka.plugins.kbbi_scraper import query_kbbi

class TestKBBISession(unittest.TestCase):
    @patch('requests.get')
    def test_query_kbbi_with_cookies(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><ul class='adjusted-par'><li>Belajar adalah...</li></ul></body></html>"
        mock_get.return_value = mock_response
        
        my_cookies = {"session_id": "12345"}
        query_kbbi("belajar", cookies=my_cookies)
        
        # Verify that requests.get was called with the cookies
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['cookies'], my_cookies)
        print("KBBI Cookie test PASSED")

if __name__ == "__main__":
    unittest.main()
