import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_attribute(self):
        node = HTMLNode(props={'class': 'test'})
        self.assertEqual(node.props_to_html(), ' class="test"')

    def test_props_to_html_multiple_attributes(self):
        node = HTMLNode(props={'class': 'test', 'id': 'test'})
        self.assertEqual(node.props_to_html(), ' class="test" id="test"')

    def test_props_to_html_no_attributes(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_repr(self):
        node = HTMLNode(tag='div', value='test', children=[], props={'class': 'test'})
        self.assertEqual(repr(node), 'HTMLNode(tag=div, value=test, children=[], props={\'class\': \'test\'})')

    def test_leaf_node_to_html(self):
        node = LeafNode('a', 'Click me!', {'href': 'https://www.google.com'})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_node_to_html_no_tag(self):
        node = LeafNode(value='Click me!', props={'href': 'https://www.google.com'})
        self.assertEqual(node.to_html(), 'Click me!')

    def test_leaf_node_to_html_no_value(self):
        node = LeafNode(tag='a', props={'href': 'https://www.google.com'})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_to_html_no_children(self):
        node = ParentNode('div')
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_to_html_no_tag(self):
        node = ParentNode(children=[LeafNode('a', 'Click me!', {'href': 'https://www.google.com'})])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_to_html_multiple_children(self):
        children = [
            LeafNode('a', 'Click me!', {'href': 'https://www.google.com'}),
            LeafNode('p', 'Hello There!')
        ]
        node = ParentNode('div', children)
        self.assertEqual(node.to_html(),
            '<div>\n<a href="https://www.google.com">Click me!</a>\n<p>Hello There!</p>\n</div>'
        )

    def test_parent_node_to_html_with_leaf_children(self):
        children = [LeafNode('a', 'Click me!', {'href': 'https://www.google.com'})]
        node = ParentNode('div', children)
        self.assertEqual(node.to_html(),
            '<div>\n<a href="https://www.google.com">Click me!</a>\n</div>'
        )

    def test_parent_node_to_html_with_parent_children(self):
        leaf = [LeafNode('a', 'Click me!', {'href': 'https://www.google.com'})]
        children = [ParentNode('div', leaf)]
        node = ParentNode('div', children)
        self.assertEqual(node.to_html(),
            '<div>\n<div>\n<a href="https://www.google.com">Click me!</a>\n</div>\n</div>'
        )

if __name__ == '__main__':
    unittest.main()