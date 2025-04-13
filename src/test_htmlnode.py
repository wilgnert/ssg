import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_initialization(self):
        node = HTMLNode(
            tag="div", value="Hello", children=[], props={"class": "container"}
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), 'class="container" id="main"')

    def test_props_to_html_without_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(
            tag="p", value="Text", children=[], props={"style": "color:red;"}
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=p, value=Text, children=[], props={'style': 'color:red;'})",
        )

    def test_equality_same_attributes(self):
        node1 = HTMLNode(tag="span", value="Test", children=[], props={"class": "test"})
        node2 = HTMLNode(tag="span", value="Test", children=[], props={"class": "test"})
        self.assertEqual(node1, node2)

    def test_equality_different_attributes(self):
        node1 = HTMLNode(tag="span", value="Test", children=[], props={"class": "test"})
        node2 = HTMLNode(tag="div", value="Test", children=[], props={"class": "test"})
        self.assertNotEqual(node1, node2)

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_props(self):
        node = LeafNode(
            tag="a", value="Click here", props={"href": "https://example.com"}
        )
        self.assertEqual(
            node.to_html(), '<a href="https://example.com">Click here</a>'
        )

    def test_to_html_without_props(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_empty_value(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p")

class TestParentNode(unittest.TestCase):
    
    def test_parent_to_html_with_children_and_props(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        parent = ParentNode(
            tag="div",
            children=[child1, child2],
            props={"class": "container"}
        )
        self.assertEqual(
            parent.to_html(),
            '<div class="container"><span>Child 1</span><span>Child 2</span></div>'
        )

    def test_parent_to_html_with_children_without_props(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        parent = ParentNode(tag="div", children=[child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><span>Child 1</span><span>Child 2</span></div>"
        )

    def test_parent_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="div").to_html()

    def test_parent_to_html_no_tag(self):
        child = LeafNode(tag="span", value="Child")
        with self.assertRaises(ValueError):
            ParentNode(children=[child]).to_html()

    def test_parent_to_html_nested_structure(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        nested_parent = ParentNode(tag="section", children=[child1, child2])
        parent = ParentNode(
            tag="div",
            children=[nested_parent],
            props={"id": "main"}
        )
        self.assertEqual(
            parent.to_html(),
            '<div id="main"><section><span>Child 1</span><span>Child 2</span></section></div>'
        )
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )




if __name__ == "__main__":
    unittest.main()
