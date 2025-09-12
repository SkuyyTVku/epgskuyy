import requests
import lxml.etree as ET

# Daftar URL sumber EPG
sources = {
    "IndiHome": "http://www.indihometv.com/epg.xml",
    "Sooka": "http://www.sooka.my/epg.xml",
    "VisionPlus": "http://www.mncvision.id/epg.xml",
    "FirstMedia": "http://www.firstmedia.com/epg.xml"
}

# File output
output_file = "epgtv.xml"

def fetch_xml(url):
    """Download dan parse XML dari URL"""
    try:
        print(f"Fetching {url} ...")
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return ET.fromstring(r.content)
    except Exception as e:
        print(f"Gagal ambil {url}: {e}")
        return None

def merge_epg():
    # Root XMLTV
    root = ET.Element("tv")

    for provider, url in sources.items():
        xml_data = fetch_xml(url)
        if xml_data is None:
            continue

        # Copy semua elemen channel & programme
        for elem in xml_data:
            # Tambahkan suffix provider ke channel id biar unik
            if elem.tag == "channel" and "id" in elem.attrib:
                elem.attrib["id"] = elem.attrib["id"] + f".{provider.upper()}"

            if elem.tag == "programme" and "channel" in elem.attrib:
                elem.attrib["channel"] = elem.attrib["channel"] + f".{provider.upper()}"

            root.append(elem)

    # Simpan ke file
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Selesai gabung, hasil: {output_file}")

if __name__ == "__main__":
    merge_epg()
