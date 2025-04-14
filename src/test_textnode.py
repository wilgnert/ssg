import unittest

from textnode import TextNode, TextType
from src.localutil import pass_arguments


class TestTextType(unittest.TestCase):
    def test_type_names(self):
        types = TextType.__members__
        expected = {
            "IMAGE",
            "TEXT",
            "ITALIC",
            "LINK",
            "CODE",
            "BOLD",
        }
        self.assertSetEqual(set(types.keys()), expected)

    def test_type_values(self):
        types = TextType.__members__
        type_values = [type for type in types]
        expected = {
            "IMAGE",
            "TEXT",
            "ITALIC",
            "LINK",
            "CODE",
            "BOLD",
        }
        self.assertSetEqual(set(type_values), expected)


class TestTextNode(unittest.TestCase):
    @pass_arguments(
        ["a", "b"],
        [
            [TextNode("This is a text node", TextType.BOLD), TextNode("This is a text node", TextType.BOLD)],
            [TextNode("This is a text node", TextType.LINK, "url"), TextNode("This is a text node", TextType.LINK, "url")]
        ]
    )
    def test_eq_true(self, a, b):
        self.assertTrue(a == b)
        
    @pass_arguments(
        ["a", "b"],
        [
            [TextNode("This is a text node", TextType.BOLD), TextNode("This is another text node", TextType.BOLD)],
            [TextNode("This is a text node", TextType.TEXT), TextNode("This is a text node", TextType.BOLD)],
            [TextNode("This is a link node", TextType.LINK, "url"), TextNode("This is a link node", TextType.LINK, "link")],
            [TextNode("This is a image node", TextType.IMAGE, "url"), TextNode("This is a image node", TextType.IMAGE, "link")],
        ]
    )
    def test_eq_false(self, a, b):
        self.assertFalse(a == b)

    @pass_arguments(
        ["a", "b"],
        [
            [TextNode("a", TextType.TEXT), TextNode("b", TextType.TEXT)],
            [TextNode("a", TextType.TEXT), TextNode("a", TextType.BOLD)],
            [TextNode("a", TextType.LINK, "a"), TextNode("a", TextType.LINK, "b")],
            [TextNode("a", TextType.IMAGE, "a"), TextNode("a", TextType.IMAGE, "b")],
        ],
    )
    def test_ne_true(self, a, b):
        self.assertTrue(a != b)

    def test_raise_if_no_url_for_link(self):
        with self.assertRaises(ValueError):
            node = TextNode("text", TextType.LINK)

    def test_raise_if_no_url_for_image(self):
        with self.assertRaises(ValueError):
            node = TextNode("text", TextType.IMAGE)


if __name__ == "__main__":
    unittest.main()
