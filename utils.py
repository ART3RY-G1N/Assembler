import xml.etree.ElementTree as ET

def write_xml_log(filepath, instructions):
  root = ET.Element("log")
  for instruction in instructions:
    instruction_elem = ET.SubElement(root, "instruction")
    for key, value in instruction.items():
      ET.SubElement(instruction_elem, key).text = str(value)
  tree = ET.ElementTree(root)
  tree.write(filepath, encoding="utf-8", xml_declaration=True)

def write_xml_result(filepath, memory):
  root = ET.Element("memory")
  for address, value in memory.items():
    entry = ET.SubElement(root, "entry")
    ET.SubElement(entry, "address").text = str(address)
    ET.SubElement(entry, "value").text = str(value)
  tree = ET.ElementTree(root)
  tree.write(filepath, encoding="utf-8", xml_declaration=True)