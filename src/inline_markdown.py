import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception("unmatched delimeter")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            elif i % 2 != 0:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        split_nodes = []

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        if node.text != "":
            
            curr_text = node.text
            for alt, url in matches:
                before, after = curr_text.split(f"[{alt}]({url})", 1)
                if before:
                    split_nodes.append(TextNode(before, TextType.TEXT))
                split_nodes.append(TextNode(alt, TextType.LINK, url))
                curr_text = after  # Get ready for next link

            if curr_text:  # Add any remaining tail text
                split_nodes.append(TextNode(curr_text, TextType.TEXT))
            new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        split_nodes = []

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        if node.text != "":
            
            curr_text = node.text
            for alt, url in matches:
                before, after = curr_text.split(f"![{alt}]({url})", 1)
                if before:
                    split_nodes.append(TextNode(before, TextType.TEXT))
                split_nodes.append(TextNode(alt, TextType.IMAGE, url))
                curr_text = after  # Get ready for next link

            if curr_text:  # Add any remaining tail text
                split_nodes.append(TextNode(curr_text, TextType.TEXT))
            new_nodes.extend(split_nodes)
    return new_nodes

                        
def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    current_nodes = split_nodes_image([text_node])
    current_nodes = split_nodes_link(current_nodes)
    current_nodes = split_nodes_delimiter(current_nodes, "`", TextType.CODE)
    current_nodes = split_nodes_delimiter(current_nodes, "**", TextType.BOLD)
    current_nodes = split_nodes_delimiter(current_nodes, "_",TextType.ITALIC)
    return current_nodes





