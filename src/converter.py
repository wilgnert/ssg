from src.htmlnode import LeafNode, ParentNode
from src.textnode import TextNode, TextType
import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    BLOCKQUOTE = 3
    CODE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?:^|[^\!])\[([^\]]+)\]\(([^)]+)\)", text)


def split_nodes_link(nodes):
    new_nodes = []
    for node in nodes:
        text = node.text
        links = extract_markdown_links(text)
        if len(links) > 0:
            for link in links:
                formated_link = f"[{link[0]}]({link[1]})"
                while True:
                    parts = text.split(formated_link, 1)
                    if len(parts) < 2:
                        break
                    if parts[0] != "":
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    text = parts[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            if text != "":
                new_nodes.append(node)
    return new_nodes


def split_nodes_image(nodes):
    new_nodes = []
    for node in nodes:
        text = node.text
        images = extract_markdown_images(text)
        if len(images) > 0:
            for image in images:
                formated_image = f"![{image[0]}]({image[1]})"
                while True:
                    parts = text.split(formated_image, 1)
                    if len(parts) < 2:
                        break
                    if parts[0] != "":
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    text = parts[1]
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            if text != "":
                new_nodes.append(node)
    return new_nodes


def split_nodes_delimiter(nodes, delimiter, text_type):
    """Parses a list of TextNodes and splits them by a delimiter, which
    could be ** for bold, _ for italic, or ` for code"""
    new_nodes = []
    for node in nodes:
        type = node.text_type
        text = node.text
        parts = text.split(delimiter)
        if len(parts) > 1:
            temp = []
            for part in parts:
                if len(temp) % 2 == 0:
                    temp.append(TextNode(part, type))
                else:
                    temp.append(TextNode(part, text_type))
            new_nodes.extend(list(filter(lambda x: x.text != "", temp)))
        else:
            if text != "":
                new_nodes.append(node)
    return new_nodes


def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    if text == "":
        return []
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def text_node_to_html_node(text_node):
    """
    Converts a TextNode to a LeafNode.
    """
    if not isinstance(text_node, TextNode):
        raise TypeError("text_node must be an instance of TextNode")

    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(
            tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
        )
    else:
        raise ValueError("Unknown text type")


def text_to_html_nodes(text):
    return [text_node_to_html_node(text_node) for text_node in text_to_text_nodes(text)]


def markdown_to_blocks(markdown):
    """
    Converts a markdown string to a list of HTMLNode objects.
    """
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a string")

    return list(
        filter(lambda x: x != "", map(lambda y: y.strip(), markdown.split("\n\n")))
    )


def block_to_block_type(block):
    """
    Converts a block of markdown to a block type.
    """
    if not isinstance(block, str):
        raise TypeError("block must be a string")
    lines = block.split("\n")

    if len(re.findall(r"^#{1,6} ", block, re.M)) == len(lines):
        return BlockType.HEADING

    m = re.search(r"^```.*```$", block, re.M | re.S)
    if m and m.pos == 0:
        return BlockType.CODE

    if len(re.findall(r"^>( |\n)", block, re.M)) == len(lines):
        return BlockType.BLOCKQUOTE

    if len(re.findall(r"^- ", block, re.M)) == len(lines):
        return BlockType.UNORDERED_LIST

    for i in range(len(lines)):
        if not lines[i].startswith(f"{i+1}. "):
            break
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        lines = block.split("\n")

        match block_type:
            case BlockType.PARAGRAPH:
                html_nodes.append(
                    ParentNode(
                        tag="p", children=text_to_html_nodes(block.replace("\n", " "))
                    )
                )
            case BlockType.HEADING:
                for line in lines:
                    level = len(re.match(r"^#+", line).group(0))
                    html_nodes.append(
                        ParentNode(
                            tag=f"h{level}",
                            children=text_to_html_nodes(line.split(" ", 1)[1]),
                        )
                    )
            case BlockType.BLOCKQUOTE:
                block = re.sub(r"^>\n", ">  \n", block, 0, re.M)
                # my_lines = [ParentNode(tag="p", children=text_to_html_nodes(line)) for line in block.replace("> ", "").split("\n")]
                html_nodes.append(
                    ParentNode(tag="blockquote", children=text_to_html_nodes(block.replace("> ", "")))
                )
            case BlockType.CODE:
                html_nodes.append(
                    ParentNode(
                        tag="pre",
                        children=[
                            ParentNode(
                                tag="code",
                                children=[
                                    text_node_to_html_node(
                                        TextNode(
                                            text=block[4:-3],
                                            text_type=TextType.TEXT,
                                        )
                                    )
                                ],
                            )
                        ],
                    )
                )
            case BlockType.UNORDERED_LIST:
                items = re.findall(r"^- (.*)", block, re.M)
                children = [
                    ParentNode(tag="li", children=text_to_html_nodes(item))
                    for item in items
                ]
                html_nodes.append(ParentNode(tag="ul", children=children))
            case BlockType.ORDERED_LIST:
                items = re.findall(r"^\d+\. (.*)", block, re.M)
                children = [
                    ParentNode(tag="li", children=text_to_html_nodes(item))
                    for item in items
                ]
                html_nodes.append(ParentNode(tag="ol", children=children))
            case _:
                raise ValueError(f"Unknown block type: {block_type}")

    return ParentNode(tag="div", children=html_nodes if html_nodes else [LeafNode(tag=None, value="")])


def markdown_to_html(markdown):
    """
    Converts a markdown string to a HTMLNode object.
    """
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a string")

    html_node = markdown_to_html_node(markdown)
    return html_node.to_html()
