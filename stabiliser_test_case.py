import unittest

from stabiliser import Stabiliser

class StabiliserTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_should_construct(self):
        stabiliser = Stabiliser()
        self.assertIsInstance(stabiliser, Stabiliser)

