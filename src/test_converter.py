import unittest
from converter import *
from htmlnode import LeafNode
from textnode import TextNode, TextType


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_normal_text_node(self):
        text_node = TextNode(text="Hello", text_type=TextType.TEXT)
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, None)
        self.assertEqual(result.value, "Hello")
        self.assertEqual(result.props, None)

    def test_bold_text_node(self):
        text_node = TextNode(text="Bold Text", text_type=TextType.BOLD)
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "b")
        self.assertEqual(result.value, "Bold Text")
        self.assertEqual(result.props, None)

    def test_italic_text_node(self):
        text_node = TextNode(text="Italic Text", text_type=TextType.ITALIC)
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "i")
        self.assertEqual(result.value, "Italic Text")
        self.assertEqual(result.props, None)

    def test_code_text_node(self):
        text_node = TextNode(text="Code Text", text_type=TextType.CODE)
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "code")
        self.assertEqual(result.value, "Code Text")
        self.assertEqual(result.props, None)

    def test_link_text_node(self):
        text_node = TextNode(
            text="Link Text", text_type=TextType.LINK, url="http://example.com"
        )
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "a")
        self.assertEqual(result.value, "Link Text")
        self.assertEqual(result.props, {"href": "http://example.com"})

    def test_image_text_node(self):
        text_node = TextNode(
            text="Image Alt",
            text_type=TextType.IMAGE,
            url="http://example.com/image.png",
        )
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "img")
        self.assertEqual(result.value, "")
        self.assertEqual(
            result.props, {"href": "http://example.com/image.png", "alt": "Image Alt"}
        )

    def test_invalid_text_node_type(self):
        with self.assertRaises(TypeError):
            text_node_to_html_node("Not a TextNode")

    def test_unknown_text_type(self):
        text_node = TextNode(text="Unknown", text_type="UNKNOWN")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_bold_delimiter(self):
        nodes = [TextNode(text="This is **bold** text", text_type=TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertListEqual(
            result,
            [
                TextNode(text="This is ", text_type=TextType.TEXT),
                TextNode(text="bold", text_type=TextType.BOLD),
                TextNode(text=" text", text_type=TextType.TEXT),
            ],
        )

    def test_split_italic_delimiter(self):
        nodes = [TextNode(text="This is *italic* text", text_type=TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertListEqual(
            result,
            [
                TextNode(text="This is ", text_type=TextType.TEXT),
                TextNode(text="italic", text_type=TextType.ITALIC),
                TextNode(text=" text", text_type=TextType.TEXT),
            ],
        )

    def test_split_code_delimiter(self):
        nodes = [TextNode(text="This is `code` text", text_type=TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertListEqual(
            result,
            [
                TextNode(text="This is ", text_type=TextType.TEXT),
                TextNode(text="code", text_type=TextType.CODE),
                TextNode(text=" text", text_type=TextType.TEXT),
            ],
        )

    def test_no_split_when_no_delimiter(self):
        nodes = [TextNode(text="This is normal text", text_type=TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertListEqual(
            result, [TextNode(text="This is normal text", text_type=TextType.TEXT)]
        )

    def test_empty_text_node(self):
        nodes = [TextNode(text="", text_type=TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 0)

    def test_multiple_delimiters(self):
        nodes = [TextNode(text="**bold** and *italic*", text_type=TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        result = split_nodes_delimiter(result, "*", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertListEqual(
            result,
            [
                TextNode(text="bold", text_type=TextType.BOLD),
                TextNode(text=" and ", text_type=TextType.TEXT),
                TextNode(text="italic", text_type=TextType.ITALIC),
            ],
        )

    def test_split_with_many_bolds(self):
        nodes = [TextNode(text="**bold1** and **bold2**", text_type=TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertListEqual(
            result,
            [
                TextNode(text="bold1", text_type=TextType.BOLD),
                TextNode(text=" and ", text_type=TextType.TEXT),
                TextNode(text="bold2", text_type=TextType.BOLD),
            ],
        )


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "Here is an image ![alt text](http://example.com/image.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "http://example.com/image.png")])

    def test_extract_markdown_images_multiple(self):
        text = "![image1](http://example.com/1.png) and ![image2](http://example.com/2.png)"
        result = extract_markdown_images(text)
        self.assertEqual(
            result,
            [
                ("image1", "http://example.com/1.png"),
                ("image2", "http://example.com/2.png"),
            ],
        )

    def test_extract_markdown_images_no_images(self):
        text = "This text has no images."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links(self):
        text = "Here is a [link](http://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "http://example.com")])

    def test_extract_markdown_links_multiple(self):
        text = "[link1](http://example.com/1) and [link2](http://example.com/2)"
        result = extract_markdown_links(text)
        self.assertEqual(
            result,
            [("link1", "http://example.com/1"), ("link2", "http://example.com/2")],
        )

    def test_extract_markdown_links_no_links(self):
        text = "This text has no links."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links_ignores_images(self):
        text = "Here is an image ![alt text](http://example.com/image.png) and a [link](http://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "http://example.com")])


class TestSplitNodesLink(unittest.TestCase):
    def test_split_single_link(self):
        nodes = [
            TextNode(
                text="This is a [link](http://example.com)", text_type=TextType.TEXT
            )
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 2)
        self.assertListEqual(
            result,
            [
                TextNode(text="This is a ", text_type=TextType.TEXT),
                TextNode(
                    text="link", text_type=TextType.LINK, url="http://example.com"
                ),
            ],
        )

    def test_split_multiple_links(self):
        nodes = [
            TextNode(
                text="[link1](http://example.com/1) and [link2](http://example.com/2)",
                text_type=TextType.TEXT,
            )
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 3)
        self.assertListEqual(
            result,
            [
                TextNode(
                    text="link1", text_type=TextType.LINK, url="http://example.com/1"
                ),
                TextNode(text=" and ", text_type=TextType.TEXT),
                TextNode(
                    text="link2", text_type=TextType.LINK, url="http://example.com/2"
                ),
            ],
        )

    def test_no_links(self):
        nodes = [TextNode(text="This text has no links.", text_type=TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 1)
        self.assertListEqual(
            result, [TextNode(text="This text has no links.", text_type=TextType.TEXT)]
        )

    def test_mixed_text_with_links(self):
        nodes = [
            TextNode(
                text="Start [link](http://example.com) end", text_type=TextType.TEXT
            )
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 3)
        self.assertListEqual(
            result,
            [
                TextNode(text="Start ", text_type=TextType.TEXT),
                TextNode(
                    text="link", text_type=TextType.LINK, url="http://example.com"
                ),
                TextNode(text=" end", text_type=TextType.TEXT),
            ],
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        nodes = [
            TextNode(
                text="This is an image ![alt text](http://example.com/image.png)",
                text_type=TextType.TEXT,
            )
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 2)
        self.assertListEqual(
            result,
            [
                TextNode(text="This is an image ", text_type=TextType.TEXT),
                TextNode(
                    text="alt text",
                    text_type=TextType.IMAGE,
                    url="http://example.com/image.png",
                ),
            ],
        )

    def test_split_multiple_images(self):
        nodes = [
            TextNode(
                text="![image1](http://example.com/1.png) and ![image2](http://example.com/2.png)",
                text_type=TextType.TEXT,
            )
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 3)
        self.assertListEqual(
            result,
            [
                TextNode(
                    text="image1",
                    text_type=TextType.IMAGE,
                    url="http://example.com/1.png",
                ),
                TextNode(text=" and ", text_type=TextType.TEXT),
                TextNode(
                    text="image2",
                    text_type=TextType.IMAGE,
                    url="http://example.com/2.png",
                ),
            ],
        )

    def test_no_images(self):
        nodes = [TextNode(text="This text has no images.", text_type=TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 1)
        self.assertListEqual(
            result, [TextNode(text="This text has no images.", text_type=TextType.TEXT)]
        )

    def test_mixed_text_with_images(self):
        nodes = [
            TextNode(
                text="Start ![alt text](http://example.com/image.png) end",
                text_type=TextType.TEXT,
            )
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 3)
        self.assertListEqual(
            result,
            [
                TextNode(text="Start ", text_type=TextType.TEXT),
                TextNode(
                    text="alt text",
                    text_type=TextType.IMAGE,
                    url="http://example.com/image.png",
                ),
                TextNode(text=" end", text_type=TextType.TEXT),
            ],
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_empty_text(self):
        result = text_to_text_nodes("")
        self.assertEqual(result, [])

    def test_plain_text(self):
        result = text_to_text_nodes("This is plain text.")
        self.assertEqual(len(result), 1)
        self.assertListEqual(
            result, [TextNode(text="This is plain text.", text_type=TextType.TEXT)]
        )

    def test_bold_text(self):
        result = text_to_text_nodes("This is **bold** text.")
        self.assertEqual(len(result), 3)
        self.assertListEqual(
            result,
            [
                TextNode(text="This is ", text_type=TextType.TEXT),
                TextNode(text="bold", text_type=TextType.BOLD),
                TextNode(text=" text.", text_type=TextType.TEXT),
            ],
        )

    def test_italic_text(self):
        result = text_to_text_nodes("This is _italic_ text.")
        self.assertEqual(len(result), 3)
        self.assertListEqual(
            result,
            [
                TextNode(text="This is ", text_type=TextType.TEXT),
                TextNode(text="italic", text_type=TextType.ITALIC),
                TextNode(text=" text.", text_type=TextType.TEXT),
            ],
        )

    def test_code_text(self):
        result = text_to_text_nodes("This is `code` text.")
        self.assertEqual(len(result), 3)
        self.assertListEqual(
            result,
            [
                TextNode(text="This is ", text_type=TextType.TEXT),
                TextNode(text="code", text_type=TextType.CODE),
                TextNode(text=" text.", text_type=TextType.TEXT),
            ],
        )

    def test_link_text(self):
        result = text_to_text_nodes("This is a [link](http://example.com)")
        self.assertEqual(len(result), 2)
        self.assertListEqual(
            result,
            [
                TextNode(text="This is a ", text_type=TextType.TEXT),
                TextNode(
                    text="link", text_type=TextType.LINK, url="http://example.com"
                ),
            ],
        )

    def test_image_text(self):
        result = text_to_text_nodes(
            "This is an image ![alt text](http://example.com/image.png)"
        )
        self.assertEqual(len(result), 2)
        self.assertListEqual(
            result,
            [
                TextNode(text="This is an image ", text_type=TextType.TEXT),
                TextNode(
                    text="alt text",
                    text_type=TextType.IMAGE,
                    url="http://example.com/image.png",
                ),
            ],
        )

    def test_combined_text(self):
        result = text_to_text_nodes(
            "This is **bold**, _italic_, `code`, a [link](http://example.com), and an image ![alt text](http://example.com/image.png)."
        )
        self.assertEqual(len(result), 11)
        self.assertListEqual(
            result,
            [
                TextNode(text="This is ", text_type=TextType.TEXT),
                TextNode(text="bold", text_type=TextType.BOLD),
                TextNode(text=", ", text_type=TextType.TEXT),
                TextNode(text="italic", text_type=TextType.ITALIC),
                TextNode(text=", ", text_type=TextType.TEXT),
                TextNode(text="code", text_type=TextType.CODE),
                TextNode(text=", a ", text_type=TextType.TEXT),
                TextNode(
                    text="link", text_type=TextType.LINK, url="http://example.com"
                ),
                TextNode(text=", and an image ", text_type=TextType.TEXT),
                TextNode(
                    text="alt text",
                    text_type=TextType.IMAGE,
                    url="http://example.com/image.png",
                ),
                TextNode(text=".", text_type=TextType.TEXT),
            ],
        )

    def test_converter(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 10)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_empty_markdown(self):
        result = markdown_to_blocks("")
        self.assertEqual(result, [])

    def test_single_block(self):
        markdown = "This is a single block."
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["This is a single block."])

    def test_multiple_blocks(self):
        markdown = "Block one.\n\nBlock two.\n\nBlock three."
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["Block one.", "Block two.", "Block three."])

    def test_blocks_with_extra_whitespace(self):
        markdown = "  Block one.  \n\n  Block two.  \n\n  Block three.  "
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["Block one.", "Block two.", "Block three."])

    def test_blocks_with_empty_lines(self):
        markdown = "Block one.\n\n\n\nBlock two."
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["Block one.", "Block two."])

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            markdown_to_blocks(123)

    def test_blocks_with_special_characters(self):
        markdown = "Block with **bold** text.\n\nBlock with _italic_ text."
        result = markdown_to_blocks(markdown)
        self.assertEqual(
            result, ["Block with **bold** text.", "Block with _italic_ text."]
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_block(self):
        block = "# Heading 1"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_code_block(self):
        block = "```code block```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_blockquote_block(self):
        block = "> This is a blockquote\n> with multiple lines"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.BLOCKQUOTE)

    def test_unordered_list_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        block = "This is a paragraph with no special formatting."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_empty_block(self):
        block = ""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            block_to_block_type(123)

    def test_mixed_block(self):
        block = "# Heading\n- List item\n> Blockquote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)


class TestMarkdownToHtml(unittest.TestCase):
    def test_empty_markdown(self):
        result = markdown_to_html("")
        self.assertEqual(result, "<div></div>")

    def test_plain_text(self):
        markdown = "This is plain text."
        result = markdown_to_html(markdown)
        self.assertEqual(result, "<div><p>This is plain text.</p></div>")

    def test_bold_text(self):
        markdown = "This is **bold** text."
        result = markdown_to_html(markdown)
        self.assertEqual(result, "<div><p>This is <b>bold</b> text.</p></div>")

    def test_italic_text(self):
        markdown = "This is _italic_ text."
        result = markdown_to_html(markdown)
        self.assertEqual(result, "<div><p>This is <i>italic</i> text.</p></div>")

    def test_code_text(self):
        markdown = "This is `code` text."
        result = markdown_to_html(markdown)
        self.assertEqual(result, "<div><p>This is <code>code</code> text.</p></div>")

    def test_link_text(self):
        markdown = "This is a [link](http://example.com)."
        result = markdown_to_html(markdown)
        self.assertEqual(
            result, '<div><p>This is a <a href="http://example.com">link</a>.</p></div>'
        )

    def test_image_text(self):
        markdown = "This is an image ![alt text](http://example.com/image.png)."
        result = markdown_to_html(markdown)
        self.assertEqual(
            result,
            '<div><p>This is an image <img href="http://example.com/image.png" alt="alt text"></img>.</p></div>',
        )

    def test_combined_text(self):
        markdown = "This is **bold**, _italic_, `code`, a [link](http://example.com), and an image ![alt text](http://example.com/image.png)."
        result = markdown_to_html(markdown)
        self.assertEqual(
            result,
            '<div><p>This is <b>bold</b>, <i>italic</i>, <code>code</code>, a <a href="http://example.com">link</a>, and an image <img href="http://example.com/image.png" alt="alt text"></img>.</p></div>',
        )

    def test_multiple_paragraphs(self):
        markdown = "Paragraph one.\n\nParagraph two."
        result = markdown_to_html(markdown)
        self.assertEqual(
            result, "<div><p>Paragraph one.</p><p>Paragraph two.</p></div>"
        )

    def test_heading(self):
        markdown = "# Heading 1\n## Heading 2"
        result = markdown_to_html(markdown)
        self.assertEqual(result, "<div><h1>Heading 1</h1><h2>Heading 2</h2></div>")

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2"
        result = markdown_to_html(markdown)
        self.assertEqual(result, "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>")

    def test_ordered_list(self):
        markdown = "1. Item 1\n2. Item 2"
        result = markdown_to_html(markdown)
        self.assertEqual(result, "<div><ol><li>Item 1</li><li>Item 2</li></ol></div>")

    def test_blockquote(self):
        markdown = "> This is a blockquote."
        result = markdown_to_html(markdown)
        self.assertEqual(
            result, "<div><blockquote>This is a blockquote.</blockquote></div>"
        )

    def test_code_block(self):
        markdown = "```\nCode block\n```"
        result = markdown_to_html(markdown)
        self.assertEqual(result, "<div><pre><code>Code block\n</code></pre></div>")

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            markdown_to_html(123)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
