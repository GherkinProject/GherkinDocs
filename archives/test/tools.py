from xml.dom.minidom import Document

doc = Document()

root = doc.createElement('root')
doc.appendChild(root)
main = doc.createElement('Text')
main.setAttribute('id', "1")
root.appendChild(main)

text = doc.createTextNode('Some text here')
main.appendChild(text)

main2 = doc.createElement('Text')
main2.setAttribute('id', "2")
root.appendChild(main2)

l = [e.getAttribute('id') for e in doc.getElementsByTagName('Text')]
print l
print doc.toprettyxml(indent='\t')
