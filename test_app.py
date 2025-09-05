
import json
import unittest
from unittest.mock import patch, MagicMock

from app import app

class BatteryAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('app.read_json_file')
    def test_get_cars(self, mock_read_json_file):
        mock_read_json_file.return_value = [{'name': 'Tesla Model 3', 'capacity': 75}]
        response = self.app.get('/cars')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'name': 'Tesla Model 3', 'capacity': 75}])

    @patch('app.write_json_file')
    @patch('app.read_json_file')
    def test_add_car(self, mock_read_json_file, mock_write_json_file):
        mock_read_json_file.return_value = []
        car_data = {'name': 'Tesla Model Y', 'capacity': 75}
        response = self.app.post('/cars', data=json.dumps(car_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        mock_write_json_file.assert_called_once_with('cars.json', [car_data])

    def test_add_car_invalid_data(self):
        response = self.app.post('/cars', data=json.dumps({'name': 'Tesla Model S'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    @patch('app.write_json_file')
    def test_calculate(self, mock_write_json_file):
        data = {'capacity': 75, 'current_charge': 20}
        response = self.app.post('/calculate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('kwh_needed', response.json)
        self.assertAlmostEqual(response.json['kwh_needed'], 45.0)
        mock_write_json_file.assert_called_once()

    def test_calculate_invalid_data(self):
        response = self.app.post('/calculate', data=json.dumps({'capacity': 75}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_calculate_invalid_number_format(self):
        data = {'capacity': 'invalid', 'current_charge': 20}
        response = self.app.post('/calculate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_calculate_charge_out_of_range(self):
        data = {'capacity': 75, 'current_charge': 110}
        response = self.app.post('/calculate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
