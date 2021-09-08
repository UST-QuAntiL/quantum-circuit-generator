import unittest
from app import create_app
import json


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Running' in response.get_data(as_text=True))

    def test_basis_encoding(self):
        # Test for single number
        response = self.client.post('/encoding/basis', data=json.dumps({'vector': 3.14, 'integral_bits': 3, 'fractional_bits': 3}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(7, response.get_json().get('n_qubits'))
        self.assertTrue('OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[7];\nx q[2];\nx q[3];\nx q[6];\n' in response.get_json().values())

        # Test for list of numbers
        response = self.client.post('/encoding/basis',
                                    data=json.dumps({'vector': [3.14, 2.25], 'integral_bits': 3, 'fractional_bits': 3}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print(response.get_json())
        self.assertEqual(14, response.get_json().get('n_qubits'))
        self.assertTrue(
            'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[14];\nx q[2];\nx q[3];\nx q[6];\nx q[9];\nx q[12];\n' in response.get_json().values())

    def test_angle_encoding(self):
        response = self.client.post('/encoding/angle', data=json.dumps({'vector': 3.14, 'rotationaxis': "x"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_amplitude_encoding(self):
        response = self.client.post('/encoding/amplitude',
                                    data=json.dumps({'vector': 3.14}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def quam_encoding(self):
        response = self.client.post('/encoding/quam',
                                    data=json.dumps({'vector': 3.14}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_schmidt_decomposition(self):
        response = self.client.post('/encoding/schmidt_decomposition',
                                    data=json.dumps({'vector': 3.14}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)