import requests
import lxml.etree as ET

# Daftar URL sumber EPG yang valid
sources = {
    "MACANTV": "https://cdn.macan.tv/epgtv.xml",
    "ZOZOTV": "https://link.zozotv.xyz/epgtvku.xml"
}

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
    root = ET.Element("tv")

    for provider, url in sources.items():
        xml_data = fetch_xml(url)
        if xml_data is None:
            continue

        for elem in xml_data:
            if elem.tag == "channel" and "id" in elem.attrib:
                elem.attrib["id"] = elem.attrib["id"] + f".{provider}"
            if elem.tag == "programme" and "channel" in elem.attrib:
                elem.attrib["channel"] = elem.attrib["channel"] + f".{provider}"
            root.append(elem)

    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Selesai gabung, hasil: {output_file}")

if __name__ == "__main__":
    merge_epg()
