import xml.etree.ElementTree as ET
import re
import scripts
import lib

def parse(path):
    with open(path, "r") as f:
        text = f.read()

        scripts.main_scripts[:] = re.findall(r'<Script>(.*?)</Script>', text, re.DOTALL)

        clean = re.sub(r'<Script>.*?</Script>', '<Script/>', text, flags=re.DOTALL)

    root = ET.fromstring(clean)
    
    return root

def parse_library(path):
    with open(path, "r") as f:
        text = f.read()

        library_scripts = re.findall(r'<Script>(.*?)</Script>', text, re.DOTALL)

        clean = re.sub(r'<Script>.*?</Script>', '<Script/>', text, flags=re.DOTALL)

    root = ET.fromstring(clean)
    if root.tag != "Library":
        lib.throw_error("imported file must have a <Library> root tag")

    scripts.library_scripts.extend(library_scripts)
    
    return root
