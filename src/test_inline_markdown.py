import unittest
from text_node import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_image, extract_markdown_link, split_nodes_image, split_nodes_link


class TestTextNodeSplitting(unittest.TestCase):
    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bolded phrase")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " in the middle")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        
    def test_italic_delimiter(self):
        node = TextNode("This is text with an _italicized phrase_ in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italicized phrase")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " in the middle")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        
    def test_multiple_delimiters_same_type(self):
        node = TextNode("**Bold start** and **bold end**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Bold start")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, " and ")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "bold end")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        
    def test_no_delimiters(self):
        node = TextNode("Plain text with no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Plain text with no delimiters")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        
    def test_empty_content_between_delimiters(self):
        node = TextNode("Text with **** empty delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " empty delimiters")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        
    def test_multiple_node_input(self):
        node1 = TextNode("First node with `code`", TextType.TEXT)
        node2 = TextNode("Already bold text", TextType.BOLD)
        node3 = TextNode("Third node with `more code`", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "First node with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)  # Node preserved as-is
        self.assertEqual(new_nodes[3].text, "Third node with ")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, "more code")
        self.assertEqual(new_nodes[4].text_type, TextType.CODE)
        
    def test_unclosed_delimiter(self):
        node = TextNode("Text with unclosed **bold", TextType.TEXT)
        
        with self.assertRaises(SyntaxError):
            split_nodes_delimiter([node], "**", TextType.BOLD)
            
    def test_delimiter_at_start(self):
        node = TextNode("**Bold start** normal end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Bold start")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, " normal end")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        
    def test_delimiter_at_end(self):
        node = TextNode("Normal start **bold end**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Normal start ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold end")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestExtractMarkdownURLs(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_image(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_link(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


class TestMarkdownNodeSplitting(unittest.TestCase):
    def test_image_single(self):
        """Test case 1: Single image with no text"""
        nodes = [TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        expected = [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")]
        
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), len(expected))
        self.assertEqual(result[0].text, expected[0].text)
        self.assertEqual(result[0].text_type, expected[0].text_type)
        self.assertEqual(result[0].url, expected[0].url)
    
    def test_image_with_surrounding_text(self):
        """Test case 2: Text with an image in the middle"""
        nodes = [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and more text", TextType.TEXT)]
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and more text", TextType.TEXT)
        ]
        
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)
    
    def test_image_with_text_before(self):
        """Test case 3: Text followed by an image"""
        nodes = [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ]
        
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)
    
    def test_image_with_text_after(self):
        """Test case 4: Image followed by text"""
        nodes = [TextNode("![image](https://i.imgur.com/zjjcJKZ.png) and text", TextType.TEXT)]
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and text", TextType.TEXT)
        ]
        
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)
    
    def test_no_images(self):
        """Test case 5: Just text with no images"""
        nodes = [TextNode("This is just text", TextType.TEXT)]
        expected = [TextNode("This is just text", TextType.TEXT)]
        
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), len(expected))
        self.assertEqual(result[0].text, expected[0].text)
        self.assertEqual(result[0].text_type, expected[0].text_type)
        self.assertEqual(result[0].url, expected[0].url)
    
    def test_multiple_images_with_text_between(self):
        """Test case 6: Text with multiple images separated by text"""
        nodes = [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ]
        
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)
    
    def test_adjacent_images_with_text_before(self):
        """Test case 7: Text followed by two adjacent images"""
        nodes = [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ]
        
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)
    
    def test_adjacent_images_with_text_after(self):
        """Test case 8: Two adjacent images followed by text"""
        nodes = [TextNode("![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png) and text", TextType.TEXT)]
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" and text", TextType.TEXT)
        ]
        
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)
    
    def test_adjacent_images_only(self):
        """Test case 9: Just two adjacent images with no text"""
        nodes = [TextNode("![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ]
        
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)
    
    def test_non_text_nodes_preserved(self):
        """Test that non-TEXT nodes are preserved in the output"""
        nodes = [
            TextNode("link text", TextType.LINK, "https://example.com"),
            TextNode("This has an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        ]
        expected = [
            TextNode("link text", TextType.LINK, "https://example.com"),
            TextNode("This has an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ]
        
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)

# Similar tests for split_nodes_link function
class TestLinkNodeSplitting(unittest.TestCase):
    def test_link_single(self):
        """Test case for single link with no text"""
        nodes = [TextNode("[link](https://example.com)", TextType.TEXT)]
        expected = [TextNode("link", TextType.LINK, "https://example.com")]
        
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), len(expected))
        self.assertEqual(result[0].text, expected[0].text)
        self.assertEqual(result[0].text_type, expected[0].text_type)
        self.assertEqual(result[0].url, expected[0].url)
    
    def test_link_with_surrounding_text(self):
        """Test case for text with a link in the middle"""
        nodes = [TextNode("This is text with a [link](https://example.com) and more text", TextType.TEXT)]
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and more text", TextType.TEXT)
        ]
        
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)
    
    def test_image_not_matched_as_link(self):
        """Test that images are not matched as links"""
        nodes = [TextNode("This has an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        expected = [TextNode("This has an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), len(expected))
        self.assertEqual(result[0].text, expected[0].text)
        self.assertEqual(result[0].text_type, expected[0].text_type)
        self.assertEqual(result[0].url, expected[0].url)
    
    def test_link_and_image(self):
        """Test case for text with both a link and an image"""
        nodes = [TextNode("This has a [link](https://example.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        expected = [
            TextNode("This has a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        ]
        
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)

# Run the tests
if __name__ == "__main__":
    unittest.main()
