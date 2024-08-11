import unittest
from app import app

class RatesAPITestCase(unittest.TestCase):

    # Set up the Flask test client
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    # Test for valid port-to-port request
    def test_valid_port_to_port_request(self):
        response = self.client.get('/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=NLRTM')
        self.assertEqual(response.status_code, 200)
        self.assertIn('average_price', response.data.decode('utf-8'))

    # Test for valid region-to-region request
    def test_valid_region_to_region_request(self):
        response = self.client.get('/rates?date_from=2016-01-01&date_to=2016-01-10&origin=china_east_main&destination=north_europe_main')
        self.assertEqual(response.status_code, 200)
        self.assertIn('average_price', response.data.decode('utf-8'))

    # Test for dates with fewer than 3 prices
    def test_dates_with_few_prices(self):
        response = self.client.get('/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=NLRTM')
        data = response.get_json()
        for day_data in data:
            if day_data['day'] == '2021-01-04':
                self.assertIsNone(day_data['average_price'])

    # Test for invalid date format
    def test_invalid_date_format(self):
        response = self.client.get('/rates?date_from=01-01-2016&date_to=01-10-2016&origin=CNSGH&destination=NLRTM')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid date format', response.data.decode('utf-8'))

    # Test for non-existent ports or regions
    def test_non_existent_ports(self):
        response = self.client.get('/rates?date_from=2016-01-01&date_to=2016-01-10&origin=XXXXX&destination=YYYYY')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()