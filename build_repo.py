import os
import zipfile
import hashlib
from xml.etree import ElementTree as ET

def build_repo():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    addon_xml_path = os.path.join(src_dir, 'addon.xml')
    
    # Parse addon.xml to get id and version
    tree = ET.parse(addon_xml_path)
    root = tree.getroot()
    addon_id = root.attrib.get('id')
    version = root.attrib.get('version')
    
    print(f"Building for {addon_id} version {version}")
    
    # Create the zip file
    zip_dir = os.path.join(src_dir, addon_id)
    if not os.path.exists(zip_dir):
        os.makedirs(zip_dir)
        
    zip_filename = f"{addon_id}-{version}.zip"
    zip_filepath = os.path.join(zip_dir, zip_filename)
    
    print(f"Creating zip {zip_filepath}")
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root_dir, dirs, files in os.walk(src_dir):
            if '.git' in root_dir or addon_id in root_dir or '__pycache__' in root_dir:
                continue
            for file in files:
                if file.endswith('.zip') or file in ['build_repo.py', 'addons.xml', 'addons.xml.md5']:
                    continue
                file_path = os.path.join(root_dir, file)
                arcname = os.path.join(addon_id, os.path.relpath(file_path, src_dir))
                zipf.write(file_path, arcname)
                
    # Create addons.xml
    addons_xml_content = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<addons>\n"
    with open(addon_xml_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Remove xml declaration if present
        if content.startswith('<?xml'):
            content = content.split('?>\n', 1)[-1]
        addons_xml_content += content
    addons_xml_content += "\n</addons>"
    
    addons_xml_path = os.path.join(src_dir, 'addons.xml')
    with open(addons_xml_path, 'w', encoding='utf-8') as f:
        f.write(addons_xml_content)
        
    # Create addons.xml.md5
    md5_hash = hashlib.md5(addons_xml_content.encode('utf-8')).hexdigest()
    with open(os.path.join(src_dir, 'addons.xml.md5'), 'w') as f:
        f.write(md5_hash)
        
    print("Repository build complete.")

if __name__ == '__main__':
    build_repo()
