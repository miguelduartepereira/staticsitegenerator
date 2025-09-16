from markdown_blocks import markdown_to_html_node
import os

def extract_title(markdown):
    root = markdown_to_html_node(markdown)
    for node in getattr(root, "children", []) or []:
        if getattr(node, "tag", None) == "h1":
            return _text_of(node)
    raise Exception("no header found")

def _text_of(node):
    if hasattr(node, "value") and node.value is not None:
        return node.value
    parts = []
    for c in getattr(node, "children", []) or []:
        parts.append(_text_of(c))
    return "".join(parts)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown_content = f.read()

    with open(template_path, "r") as f:   
        template_content = f.read()

    markdown_file = markdown_to_html_node(markdown_content)

    markdown_string = markdown_file.to_html()

    title = extract_title(markdown_content)

    template_content = template_content.replace("{{ Title }}", title)

    template_content = template_content.replace("{{ Content }}", markdown_string)

    template_content = template_content.replace('href="/', f'href="{basepath}')

    template_content = template_content.replace('src="/', f'src="{basepath}')

    dirpath = os.path.dirname(dest_path)

    os.makedirs(dirpath, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):

    files = os.listdir(dir_path_content)

    for file in files:
        src_path = os.path.join(dir_path_content, file)

        if not os.path.isfile(src_path):
            dest_subdir = os.path.join(dest_dir_path, file)
            os.makedirs(dest_subdir, exist_ok=True)
            generate_pages_recursive(src_path, template_path, dest_subdir, basepath)

        elif os.path.isfile(src_path) and file.endswith(".md"):
            if file == "index.md":
                dest_html = os.path.join(dest_dir_path, "index.html")
            else:
                base, _ = os.path.splitext(file)
                dest_html = os.path.join(dest_dir_path, base + ".html")
            
            parent = os.path.dirname(dest_html)
            os.makedirs(parent, exist_ok=True)
            generate_page(src_path, template_path, dest_html, basepath)
