class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value.")
        
        if self.tag is None:
            return self.value
    
        open_tag = f"<{self.tag}{self.props_to_html()}>"
        close_tag = f"</{self.tag}>"
            
        return f"{open_tag}{self.value}{close_tag}"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
        