import datetime
import os

# URL provider (dummy untuk contoh)
PROVIDER_URLS = {
    "IndiHome": "http://www.indihometv.com",
    "Sooka": "http://www.sooka.my",
    "VisionPlus": "http://www.mncvision.id",
    "FirstMedia": "http://www.firstmedia.com"
}

SUFFIX = "(SKUYYTV)"
CHANNEL_IDS = {
    "IndiHome": "IndiHome.SKUYY",
    "Sooka": "Sooka.SKUYY",
    "VisionPlus": "VisionPlus.SKUYY",
    "FirstMedia": "FirstMedia.SKUYY"
}

def generate_dummy_xml(provider, url):
    now = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="EPG Auto">
  <channel id="{CHANNEL_IDS[provider]}">
    <display-name>{provider}</display-name>
  </channel>
  <programme start="{now}" stop="{now}" channel="{CHANNEL_IDS[provider]}">
    <title>{provider} Jadwal Dummy {SUFFIX}</title>
    <desc>EPG dummy dari {url}</desc>
  </programme>
</tv>
"""
    return xml

os.makedirs("epg", exist_ok=True)

for provider, url in PROVIDER_URLS.items():
    xml = generate_dummy_xml(provider, url)
    with open(f"epg/{provider.lower()}.xml", "w", encoding="utf-8") as f:
        f.write(xml)

print("EPG dummy berhasil dibuat.")
