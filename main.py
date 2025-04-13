from src.textnode import *

def main():
  print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))

if __name__ == "__main__":
  main()