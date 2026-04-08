import xml.etree.ElementTree as ET
import re
import scripts

def parse(path):
    with open(path, "r") as f:
        text = f.read()

        scripts.scripts[:] = re.findall(r'<Script>(.*?)</Script>', text, re.DOTALL)

        clean = re.sub(r'<Script>.*?</Script>', '<Script/>', text, flags=re.DOTALL)

    root = ET.fromstring(clean)
    
    return root
