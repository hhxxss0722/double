import xml.etree.ElementTree as et

root = et.parse('tboxset.xml')
p=root.findall('.')
xmllist={}
for oneper in p:
    for child in oneper.getchildren():
        xmllist[child.tag] = child.text
print(xmllist)