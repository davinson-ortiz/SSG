from textnode import TextNode, TextType
from htmlnode import LeafNode


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node) 
    

if __name__ == "__main__":
    main()