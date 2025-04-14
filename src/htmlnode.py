class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list["HTMLNode"] = None,
        props: dict[str, str] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def props_to_html(self):
        if self.props:
            return " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        return ""

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return (
                self.tag == other.tag
                and self.value == other.value
                and self.children == other.children
                and self.props == other.props
            )
        return False


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str = None, value: str = None, props: dict[str, str] = None
    ):
        super().__init__(tag, value, None, props)
        if None is value:
            raise ValueError("LeafNode must have a value.")

    def to_html(self):
        props_html = self.props_to_html()
        if self.tag is None:
            return self.value
        if props_html:
            return f"<{self.tag} {props_html}>{self.value if self.value else ""}</{self.tag}>"
        return f"<{self.tag}>{self.value if self.value else ""}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str = None,
        children: list[HTMLNode] = None,
        props: dict[str, str] = None,
    ):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if not self.children:
            raise ValueError("ParentNode must have children.")
        if not self.tag:
            raise ValueError("ParentNode must have a tag.")
        children_html = "".join([child.to_html() for child in self.children])
        props_html = self.props_to_html()
        if props_html:
            return f"<{self.tag} {props_html}>{children_html}</{self.tag}>"
        return f"<{self.tag}>{children_html}</{self.tag}>"
        