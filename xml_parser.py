import xml.etree.ElementTree as ET

def parse(path):
    root = ET.parse(path).getroot()
    
    return root
