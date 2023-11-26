import unittest
import random
import sys
import pandas as pd
sys.path.insert(0, '../../src/gg')
import prep_and_create_consort as pcc
import consort_prep_functions as pf



class Test_prep_and_create(unittest.TestCase):

    @classmethod
    def setUp(self):
