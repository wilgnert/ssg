from enum import Enum

class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url
        if text_type == TextType.LINK and url is None:
            raise ValueError("URL must be provided for LINK text type.")
        elif text_type == TextType.IMAGE and url is None:
            raise ValueError("URL must be provided for IMAGE text type.")
        elif (
            text_type != TextType.LINK
            and text_type != TextType.IMAGE
            and not url is None
        ):
            raise ValueError("URL not used in non LINK or IMAGE text types.")

    def __repr__(self):
        if self.url:
            return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return f"TextNode({self.text}, {self.text_type.value})"

    def __eq__(self, value):
        if isinstance(value, TextNode):
            return (
                self.text == value.text
                and self.text_type == value.text_type
                and self.url == value.url
            )
        return False

    def __ne__(self, value):
        return not self.__eq__(value)
