import unittest
import NREL_DataMining.src.NREL_Methods as NREL


class MyTestCase(unittest.TestCase):
    def test_geocoder(self):
        self.assertEqual(NREL.geocodeAddress('Texas', 'US'), [-98.326329,31.030974])
        self.assertEqual(NREL.geocodeAddress('invalid', 'invalid'), None)
    def test_convertPointsToString(self):
        self.assertEqual(NREL.convertPointsToString([]), [])
        self.assertEqual(NREL.convertPointsToString([[-98.326329,31.030974]]), ['-98.326329%2031.030974'])
        self.assertEqual(NREL.convertPointsToString([[-98.326329,31.030974],[-120.047533,37.229564],[-74.00597, 40.71427]]), ['-98.326329%2031.030974', '-120.047533%2037.229564', '-74.00597%2040.71427'])


if __name__ == '__main__':
    unittest.main()
