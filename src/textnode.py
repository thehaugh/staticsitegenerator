class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __str__(self):
        return f"{type(self).__name__}({self.text}, {self.text_type}, {self.url})"


if __name__ == "__main__":
    a = TextNode("test", "bold", "www.test.com")
    print(a)
