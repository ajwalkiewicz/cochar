#!/usr/bin/python3
import unittest

import cochar.occup
from cochar.error import *


class TestOccupation(unittest.TestCase):
    # def test_get_occupation(self):
    #     occupation = cochar.occup.get_occupation()
    #     self.assertEqual()

    def test_get_hobby_points(self):
        points = cochar.occup.calc_hobby_points(50)
        self.assertEqual(points, 100)
