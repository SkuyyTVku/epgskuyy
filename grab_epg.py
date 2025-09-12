import requests
import lxml.etree as ET

# Daftar URL sumber EPG yang valid
sources = {
    "SKUYYTV": "https://cdn.macan.tv/epgtv.xml",  # Ganti MACANTV ke SKUYYTV
    "SKUYYTV": "https://link.zozotv.xyz/epgtvku.xml"  # Ganti ZOZOTV ke SKUYYTV
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
                # Ganti 'MACANTV' atau 'ZOZOTV' menjadi 'SKUYYTV' di channel ID
                elem.attrib["id"] = elem.attrib["id"].replace("MACANTV", "SKUYYTV").replace("ZOZOTV", "SKUYYTV")

            if elem.tag == "programme" and "channel" in elem.attrib:
                # Ambil judul program dan ganti 'MACANTV' atau 'ZOZOTV' jadi 'SKUYYTV'
                title_elem = elem.find("title")
                title_text = title_elem.text if title_elem is not None else "NOPROG"
                suffix = f"SKUYYTV_{title_text.replace(' ', '_')}"
                elem.attrib["channel"] = elem.attrib["channel"].replace("MACANTV", "SKUYYTV").replace("ZOZOTV", "SKUYYTV") + f".{suffix}"

            root.append(elem)

    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Selesai gabung, hasil: {output_file}")

if __name__ == "__main__":
    merge_epg()
