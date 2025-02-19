class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ''
        html_att = []
        for attribute in self.props:
            html_att.append(f" {attribute}=\"{self.props[attribute]}\"")
        html_str = "".join(html_att)
        return html_str

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value="", props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag="", children=[], props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == "":
            raise ValueError("ParentNode must have a tag")
        if self.children == []:
            raise ValueError("ParentNode must have children")
        children_html = "\n".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>\n{children_html}\n</{self.tag}>"