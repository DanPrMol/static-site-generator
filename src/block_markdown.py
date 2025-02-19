import re

from inline_markdown import *
from textnode import *
from htmlnode import *

def markdown_to_blocks(markdown):
    extra_lines = re.sub(r'\n{3,}', '\n\n', markdown)
    fixed_markdown = "\n".join([line.lstrip() for line in extra_lines.splitlines()])
    blocks = fixed_markdown.split("\n\n")
    return blocks

def block_to_block_type(block):
    if re.search(r'#{1,6} ', block):
        return "heading"
    if re.fullmatch(r'^```.*```$', block):
        return "code"
    if re.fullmatch(r'(>.*\n?)+', block, re.MULTILINE):
        return "quote"
    if re.fullmatch(r'([*-] .*\n?)+', block, re.MULTILINE):
        return "unordered_list"
    for i, line in enumerate(block.splitlines()):
        match = re.fullmatch(r"^(\d+)\. .*$", line)
        if not match:
            return "paragraph"
        number = int(match.group(1))
        if number != i +1:
            return "paragraph"
    return "ordered_list"

def divide_tag_and_children(block):
    block_type = block_to_block_type(block)
    if block_type == "heading":
        return block.replace("#", "")[1:]
    if block_type == "code":
        return block.replace("`", "")
    if block_type == "quote":
        return block.replace(">", "")
    if block_type == "unordered_list":
        return block.replace("- ", "").replace("* ", "")
    if block_type == "ordered_list":
        return re.sub(r'^\d+\.\s+', '', block, flags=re.MULTILINE)
    return block

def text_to_children(text):
    textnodes = []
    textnodes.extend(text_to_textnodes(text))
    children = []
    for node in textnodes:
        children.append(text_node_to_html_node(node))
    return children

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    inner_text = divide_tag_and_children(block)
    children = []
    if block_type == "ordered_list" or block_type == "unordered_list":
        lines = inner_text.split("\n")
        for line in lines:
            new_node = ParentNode("li", text_to_children(line))
            children.append(new_node)
        if block_type == "ordered_list":
            return ParentNode("ol", children)
        else:
            return ParentNode("ul", children)
    else:
        children = text_to_children(inner_text)
        if block_type == "quote":
            return ParentNode("blockquote", children)
        if block_type == "code":
            return ParentNode("pre", [ParentNode("code", children)])
        if block_type == "paragraph":
            return ParentNode("p", children)
        if block_type == "heading":
            match = re.match(r'#+', block)
            number = len(match.group(0))
            return ParentNode(f"h{number}", children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        nodes.append(block_to_html_node(block))
    return ParentNode("div", nodes)
        
def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match = re.match(r'#+', block)
        if len(match.group(0)) == 1:
            return divide_tag_and_children(block)
    raise Exception("No title found")