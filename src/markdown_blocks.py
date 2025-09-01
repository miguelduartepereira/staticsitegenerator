from enum import Enum


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
    if not block: return

    if block[0] == '#':
        heading_characters = 1
        i = 1
        while heading_characters < 6 and i < len(block):
            if block[i] == '#':
                heading_characters += 1
                i += 1
            elif block[i] == ' ':
                break
        if 1 <= heading_characters <= 6 and i < len(block) and block[i] == ' ': return BlockType.HEADING
        else: return BlockType.PARAGRAPH
    
    elif len(block) >= 6 and block[:3] == '```' and block[-3:] == '```': return BlockType.CODE

    elif block[0] == '>':
        lines = block.split("\n")
        for i in range(lines):
            if len(lines) >= 1 and lines[i][0] != '>': return BlockType.PARAGRAPH

            elif lines[i] == "":
                del lines[i]
        return BlockType.QUOTE
    
    elif block[0] == '-':
        lines = block.split("\n")
        for i in range(lines):
            if len(lines) >= 1 and lines[i][:2] != '- ': return BlockType.PARAGRAPH

            elif lines[i] == "":
                del lines[i]
        return BlockType.UNORDERED_LIST
    
    elif block[0].isdigit():
        lines = block.split("\n")
        dot_index = lines[0].find('.')
        start_number = int(lines[0][0][:dot_index])
        if start_number != 1: return BlockType.PARAGRAPH
        for line in lines:
            dot_index = line.find('.')
            number = line[:dot_index]
            if ( number == start_number + 1 and
                line[:dot_index + 2] == f'{number}. '

            ):
                start_number = number
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    