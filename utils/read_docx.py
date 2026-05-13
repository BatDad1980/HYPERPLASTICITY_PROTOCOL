import zipfile
import xml.etree.ElementTree as ET

def extract_text_from_docx(docx_path):
    text = []
    try:
        with zipfile.ZipFile(docx_path) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.XML(xml_content)
            
            # The namespace for Word XML
            namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            # Find all text nodes
            for paragraph in tree.findall('.//w:p', namespace):
                texts = [node.text for node in paragraph.findall('.//w:t', namespace) if node.text]
                if texts:
                    text.append(''.join(texts))
        return '\n'.join(text)
    except Exception as e:
        return f"Error reading docx: {e}"

if __name__ == '__main__':
    content = extract_text_from_docx("Project HPP, Research Vectors.docx")
    with open("output_docx.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print("Extracted text to output_docx.txt")
