from textnode import TextNode

def main():
    some_text_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(some_text_node.__repr__())

if __name__ == "__main__":
    main()
