import unittest
from cochar import Character
from unittest.mock import patch

class TestCharacter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dummy(self):
        char = Character()
        char.age = 21
        self.assertEqual(char.age, 21)


if __name__ == "__main__":
    unittest.main()
