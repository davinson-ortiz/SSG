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
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)
        
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        
        if self.tag is None:
            return self.value
    
        open_tag = f"<{self.tag}{self.props_to_html()}>"
        close_tag = f"</{self.tag}>"
            
        return f"{open_tag}{self.value}{close_tag}"

    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
 
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[LeafNode], props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        """Create a html tree"""
        if not self.tag:
            raise ValueError("invalid HTML: no tag")
        if not self.children:
            raise ValueError("invalid HTML: no children")
        
        open_tag = f"<{self.tag}{self.props_to_html()}>"
        close_tag = f"</{self.tag}>"
        child_tag = ''.join([child.to_html() for child in self.children])
        
        return f"{open_tag}{child_tag}{close_tag}"
