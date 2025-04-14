import unittest
from generator import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_valid_title(self):
        markdown = "# My Title\nSome content here."
        self.assertEqual(extract_title(markdown), "My Title")

    def test_no_title(self):
        markdown = "Some content here without a title."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_title_with_extra_spaces(self):
        markdown = "#    My Title   \nSome content here."
        self.assertEqual(extract_title(markdown), "My Title")

    def test_multiple_titles(self):
        markdown = "# First Title\n# Second Title\nSome content here."
        self.assertEqual(extract_title(markdown), "First Title")

    def test_title_in_middle_of_text(self):
        markdown = "Some content here.\n# My Title\nMore content."
        self.assertEqual(extract_title(markdown), "My Title")

if __name__ == "__main__":
    unittest.main()