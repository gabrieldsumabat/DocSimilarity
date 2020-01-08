import string
import unittest

from code.CleanText import clean_text


class TestCleanText(unittest.TestCase):

    def test_clean_text(self):
        bad_text = string.punctuation
        self.assertEqual(clean_text(bad_text), "%")
        symbol_text = "-- J.R.R. Tolkien, \"The Lord of the Rings\""
        self.assertEqual(clean_text(symbol_text), " JRR Tolkien The Lord of the Rings")
        weird_text = "nef aear, s'i  nef aearon!"
        self.assertEqual(clean_text(weird_text), "nef aear si  nef aearon")
