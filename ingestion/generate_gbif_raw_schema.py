import zipfile
import xml.etree.ElementTree as ET

namespace = {
    "dwc": "http://rs.tdwg.org/dwc/text/"
}

index_l = [] 
column_names = []

with zipfile.ZipFile("../data/gbif/raw/0021471-260928105237408.zip") as archive:
    with archive.open("meta.xml") as meta_file:
        tree = ET.parse(meta_file)
        root = tree.getroot()

core = root.find("dwc:core", namespace)
print(core.tag)
fields = core.findall("dwc:field", namespace)
print(len(fields))

for field in fields : 
    if field.get("index") is not None :
        index_l.append(field.get('index'))
        term = field.get("term")
        column_name = term.rsplit("/", 1)[-1]
        column_names.append(column_name)

print(len(index_l))
print(len(column_names))
print(column_names[0:10])