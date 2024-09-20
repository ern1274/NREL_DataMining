import unittest
import NREL_DataMining.src.NREL_Methods as NREL


class MyTestCase(unittest.TestCase):
    def test_geocoder(self):
        self.assertEqual(NREL.geocodeAddress('Texas', 'US'), [-98.326329,31.030974])
        self.assertEqual(NREL.geocodeAddress('invalid', 'invalid'), None)

if __name__ == '__main__':
    unittest.main()
