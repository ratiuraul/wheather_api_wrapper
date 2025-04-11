"""Unit tests for our services."""
import unittest
from unittest.mock import patch

import requests_mock
from requests.exceptions import HTTPError, RequestException, Timeout

from weather_api import create_app
from weather_api.services import BASE_URL, get_weather

# python -m unittest weather_api.tests.test_services


class TestGetWeather(unittest.TestCase):
    """Test get weather service works properly."""

    def setUp(self):
        """Set up the Flask app and test client."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

        # Mock cache.get to always return None (force cache miss)
        self.patcher_get = patch(
            'weather_api.services.cache.get', return_value=None)
        self.patcher_get.start()

    def tearDown(self):
        """Stop all mocks after each test."""
        patch.stopall()

    @requests_mock.Mocker()
    def test_get_weather_success(self, mock_request):
        """Test success case."""
        mock_request.get(f'{BASE_URL}/London/today',
                         status_code=200, text='{"weather": "sunny"}')

        result = get_weather('London')
        self.assertEqual(result.status_code, 200)
        self.assertIn('weather', result.text)

    @requests_mock.Mocker()
    def test_get_weather_http_error(self, mock_request):
        """Test HTTPError case."""
        mock_request.get(f'{BASE_URL}/London/today', status_code=500)

        with self.assertRaises(HTTPError):
            get_weather('London')

    @requests_mock.Mocker()
    def test_get_weather_connection_error(self, mock_request):
        """Test Connection Error case."""
        mock_request.get(f'{BASE_URL}/London/today',
                         exc=ConnectionError("Connection error"))

        with self.assertRaises(ConnectionError):
            get_weather('London')

    @requests_mock.Mocker()
    def test_get_weather_timeout_error(self, mock_request):
        """Test Timeout Exception case."""
        mock_request.get(f'{BASE_URL}/London/today',
                         exc=Timeout("Timeout error"))

        with self.assertRaises(Timeout):
            get_weather('London')

    @requests_mock.Mocker()
    def test_get_weather_request_error(self, mock_request):
        """Test Request Exception case."""
        mock_request.get(f'{BASE_URL}/London/today',
                         exc=RequestException("Request error"))

        with self.assertRaises(RequestException):
            get_weather('London')

    @requests_mock.Mocker()
    def test_get_weather_general_exception(self, mock_request):
        """Test Generic Exception case."""
        mock_request.get(f'{BASE_URL}/London/today',
                         exc=Exception("Some general error"))

        with self.assertRaises(Exception):
            get_weather('London')

    @patch('weather_api.services.cache.get', return_value={"weather": "sunny"})
    @patch('weather_api.services.cache.set')
    # pylint: disable=unused-argument
    def test_cache_hit_skips_api_and_set(self, mock_set, mock_get):
        """
            Test that in case of cache hit, we are not setting the cache again
        """
        response = get_weather("Bucharest")

        self.assertEqual(response.status_code, 200)
        self.assertIn("weather", response.text)
        mock_set.assert_not_called()  # Ensure cache.set is not called


if __name__ == 'main':
    unittest.main()
