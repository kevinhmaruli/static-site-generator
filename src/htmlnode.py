class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        prop_string = f''
        if self.props is not None:
            for key in self.props:
                prop_string += f' {key}="{self.props[key]}"'
        return prop_string

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, children: {self.children}, {self.props})'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Invalid HTML: ParentNode must have a tag")
        if self.children == None or self.children == []:
            raise ValueError("Invalid HTML: ParentNode must have children")
        children_str = f''
        for child in self.children:
            children_str += child.to_html() # recursively call the method for all nested nodes
        return f'<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>'
