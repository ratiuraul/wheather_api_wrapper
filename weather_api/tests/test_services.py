"""Unit tests for our services."""
import unittest
from unittest.mock import patch

import requests_mock
from requests.exceptions import HTTPError, RequestException, Timeout

from weather_api import create_app
from weather_api.services import BASE_URL, get_forecast, get_weather

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
        self.patcher_set = patch(
            'weather_api.services.cache.set', return_value=True)
        self.patcher_get.start()
        self.patcher_set.start()

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


class TestForecast(unittest.TestCase):
    """Test that get forecast feature works as expected."""

    def setUp(self):
        """Set up the tests."""
        # Mock cache.get to always return None (force cache miss)
        self.patcher_get = patch(
            'weather_api.services.cache.get', return_value=None)
        self.patcher_set = patch(
            'weather_api.services.cache.set', return_value=True)
        self.patcher_get.start()
        self.mock_cache_set = self.patcher_set.start()

    def tearDown(self):
        """Stop all mocks after each test."""
        patch.stopall()

    @requests_mock.Mocker()
    def test_get_forecast_succesfull(self, mock_request):
        """test expected response is returned in case of successfull request"""
        mock_request.get(f'{BASE_URL}/Madrid',
                         status_code=200, text='{"address": "Madrid","days": []}')

        response = get_forecast('Madrid')
        self.assertEqual(response.status_code, 200)
        self.assertIn('days', response.text)

    @requests_mock.Mocker()
    def test_get_forecast_raises_exception(self, mock_request):
        """test exception is raised in case of unsuccesfull response."""
        mock_request.get(f'{BASE_URL}/Madrid', status_code=500)
        with self.assertRaises(HTTPError):
            get_forecast('Madrid')

    @patch('weather_api.services.cache.get')
    @patch('weather_api.services.cache.set')
    @patch('weather_api.services.requests.get')
    def test_response_in_cache(self, mock_request_get, mock_set, mock_get):
        """If response is in cache, request.get and cache.set should not be called."""
        mock_get.return_value = {"address": "Madrid", "days": []}
        response = get_forecast('Madrid')
        self.assertEqual(response.status_code, 200)
        self.assertIn("days", response.text)
        mock_set.assert_not_called()
        mock_request_get.assert_not_called()

    @requests_mock.Mocker()
    def test_response_not_in_cache(self, mock_request):
        """If response is not in cache, cache_set and requests.get need to be called"""
        mock_request.get(f'{BASE_URL}/Madrid',
                         status_code=200, text='{"address": "Madrid","days": []}')
        response = get_forecast('Madrid')
        self.assertEqual(response.status_code, 200)
        self.assertIn("days", response.text)
        self.mock_cache_set.assert_called()
        assert mock_request.called


if __name__ == 'main':
    unittest.main()
