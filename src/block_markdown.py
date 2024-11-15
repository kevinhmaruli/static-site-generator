import re


def markdown_to_blocks(markdown):
    line_breaks_regex = r"(?:\r?\n){2,}"
    markdown_blocks = [block.strip() for block in re.split(line_breaks_regex, markdown) if block != ""]

    return markdown_blocks


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")) and re.search(r"\w", block):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"

    block_by_lines = block.split("\n")

    for index, line in enumerate(block_by_lines):
        if index == len(block_by_lines) - 1 and line[0] == ">":
            return "quote"
        elif line[0] == ">":
            continue
        else:
            break

    # LISTS
    first_line = block_by_lines[0]

    ## check if unordered list
    if first_line.startswith("* ") or first_line.startswith("- "):
        tag = first_line[:2]
        for index, line in enumerate(block_by_lines): 
            if line.startswith(tag):
                if index == len(block_by_lines) - 1:
                    return "unordered_list"
                continue
            else:
                break

    ## check if ordered list
    if first_line.startswith("1. "):
        for index, line in enumerate(block_by_lines):
            if line.startswith(f"{index + 1}. "):
                if index == len(block_by_lines) - 1:
                    return "ordered_list"
                continue
            else:
                break

    return "paragraph"

