import os
import shutil
from textnode import TextNode, TextType
import sys
from markdown import generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if basepath != "/":
        basepath = "/" + basepath.strip("/") + "/" 
    copy_contents("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)




def copy_contents(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    os.mkdir(destination)

    content_to_copy = os.listdir(source)

    for file in content_to_copy:
        src_path = os.path.join(source, file)
        dst_path = os.path.join(destination, file)
        
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)

        if os.path.isdir(src_path):
            os.mkdir(dst_path)
            copy_contents(src_path, dst_path)

main()