from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_children

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    for i in range (len(blocks)):
        blocks[i] = blocks[i].strip()

    return blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        if not block.strip(): continue
        
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            paragraph_string = " ".join(line.strip() for line in block.split("\n") if line.strip())
            node = ParentNode('p', text_to_children(paragraph_string))
            children.append(node)

        if block_type == BlockType.HEADING:
            i = 0
            while block[i] == '#' and i < len(block):
                i += 1
            level = i
            if 1 <= level <= 6 and i < len(block) and block[i] == " ":
                content = block[i+1:].strip()
                tag = f"h{level}"
                node = ParentNode(tag, text_to_children(content))
                children.append(node)
        
        if block_type == BlockType.QUOTE:
            clean = []
            for line in block.splitlines():
                if line.startswith(">"):
                    line = line[1:].lstrip()  # remove '>' then spaces
                clean.append(line.strip())
            joined = " ".join(l for l in clean if l)
            node = ParentNode("blockquote", text_to_children(joined))
            children.append(node)

        if block_type == BlockType.UNORDERED_LIST:
            li_nodes = []
            for line in block.splitlines():
                line = line.strip()
                if line.startswith("- "):
                    item = line[2:].strip()
                    li_nodes.append(ParentNode("li", text_to_children(item)))
            children.append(ParentNode("ul", li_nodes))
        
        if block_type == BlockType.ORDERED_LIST:
            li_nodes = []
            for line in block.splitlines():
                line = line.strip()
                j = 0
                while j < len(line) and line[j].isdigit():
                    j += 1
                if j > 0 and j + 1 < len(line) and line[j] == "." and line[j+1] == " ":
                    item = line[j+2:].strip()
                    li_nodes.append(ParentNode("li", text_to_children(item)))
            children.append(ParentNode("ol", li_nodes))
        
        if block_type == BlockType.CODE:
            lines = block.splitlines(keepends=True)
            inner_text = "".join(lines[1:-1])
            children.append(ParentNode("pre", [LeafNode("code", inner_text)]))

    return ParentNode('div', children)
    