import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leafN_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(
            node.to_html(),
            '<p>This is a paragraph of text.</p>'
        )
        
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node2.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )
        node3 = LeafNode(value="Click me!")
        self.assertEqual(
            node3.to_html(),
            'Click me!'
        )

if __name__ == "__main__":
    unittest.main()