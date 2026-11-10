from pathlib import Path
import base64,zipfile
from PIL import Image
P=Path('/mnt/data/meatloaf_case'); im=Path('/mnt/data/grafik(20261022-145918).png')
b64=base64.b64encode(im.read_bytes()).decode()
# SVG 1:1, full front visualization and printable cut panel, coordinates x from left, z from top
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="150mm" height="40mm" viewBox="0 0 150 40">
<title>Meatloaf Frontgestaltung V0.1 - Maßstab 1:1</title>
<rect x="0.2" y="0.2" width="149.6" height="39.6" rx="2" fill="#c9bda7" stroke="#333" stroke-width="0.4"/>
<rect x="6" y="1.5" width="138" height="8" rx="1" fill="#383431"/>
<text x="9" y="7.4" font-size="5.1" font-family="Arial,sans-serif" font-weight="bold" fill="#f3f3f3">commodore</text>
<image x="111" y="2.1" width="31" height="6.7" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,{b64}"/>
<rect x="6" y="11" width="138" height="26" rx="0.5" fill="#39332f" stroke="#111" stroke-width="0.2"/>
<rect x="13" y="16" width="42" height="16" rx="0.4" fill="#03090d" stroke="#70c8d8" stroke-width="0.3"/>
<text x="15" y="21" font-size="2.9" fill="#56d6e8" font-family="monospace">MEATLOAF</text><text x="15" y="25" font-size="2.5" fill="#56d6e8" font-family="monospace">WLAN VERBUNDEN</text><text x="15" y="29" font-size="2.5" fill="#56d6e8" font-family="monospace">192.168.178.42</text>
'''
for x,col,t in [(75,'#62d13f','POWER'),(88,'#edc838','WLAN'),(101,'#ed5142','IEC'),(114,'#ed5142','DATA')]:
 svg+=f'<circle cx="{x}" cy="24" r="2.55" fill="{col}" stroke="#111" stroke-width="0.35"/><text x="{x}" y="30.5" font-size="2.7" text-anchor="middle" fill="white" font-family="Arial">{t}</text>\n'
svg+='''<rect x="123.5" y="22.4" width="17" height="3.2" fill="#080808" stroke="#ddd" stroke-width="0.25"/><text x="132" y="20.8" font-size="2.8" fill="white" text-anchor="middle">microSD</text>
<circle cx="7" cy="24" r="1.55" fill="none" stroke="#ddd" stroke-width="0.3"/><circle cx="143" cy="24" r="1.55" fill="none" stroke="#ddd" stroke-width="0.3"/>
</svg>'''
(P/'Meatloaf_Frontgestaltung_1zu1_v0.1.svg').write_text(svg)
# cutting SVG with coordinates exactly 138x26
cut='''<svg xmlns="http://www.w3.org/2000/svg" width="138mm" height="26mm" viewBox="0 0 138 26"><title>Frontplatte Schnittkontur 1:1 V0.1</title><g fill="none" stroke="#ff0000" stroke-width="0.15"><rect x="0.2" y="0.2" width="137.6" height="25.6"/><rect x="7" y="5" width="42" height="16"/><rect x="119.5" y="11.4" width="17" height="3.2"/>'''
for x in [69,82,95,108]:cut+=f'<circle cx="{x}" cy="13" r="2.55"/>'
for x in [1,137]:cut+=f'<circle cx="{x}" cy="13" r="1.55"/>'
cut+='</g></svg>'
(P/'Meatloaf_Frontplatte_Schnittvorlage_1zu1_v0.1.svg').write_text(cut)
readme='''MEATLOAF GEHÄUSE V0.1 - KONZEPT / PROTOTYP\n\nAußenmaß 150 x 110 x 40 mm. Drei STL: Boden, Deckel, Frontplatte.\nKoordinaten: Front = negative Y-Richtung. Druckempfehlung: PLA/PETG, 0,2 mm Schichthöhe, 3 Perimeter, 20 % Infill; Ausrichtung im Slicer prüfen.\nFrontplatte 138 x 26 x 2 mm, OLED-Ausschnitt 42 x 16 mm, 4 LED-Bohrungen 5,1 mm, microSD-Schlitz 17 x 3,2 mm.\nRückseite: IEC-Bohrung 18 mm, USB-C 10 x 4 mm, Reset 4 mm.\nDeckel mit Lüftungsschlitzen und vier Schraubpositionen. Pilotbohrungen 2,5 mm, Deckel 3,3 mm.\nWICHTIG: Nicht produktionsreif. Abmessungen für Buchsen, Displays, SD-Modul und Board sind Annahmen; insbesondere IEC-Buchse mit Flansch, OLED-Platine, microSD-Modul und USB-C-Positionen mechanisch abgleichen.\nDie Gehäuseform ist keine exakte Rekonstruktion eines Commodore-Geräts. Markenlogos nur für persönliche Visualisierung; Rechte vor öffentlicher Verwertung klären.\nDie SVG Frontgestaltung enthält die vom Nutzer bereitgestellte Meatloaf-Originalgrafik als eingebettete PNG. SVG auf 100 % (ohne Seitenanpassung) drucken.\nCAD-Quelldatei: build.py (CadQuery).\n'''
(P/'README.txt').write_text(readme)
with zipfile.ZipFile('/mnt/data/Meatloaf_Gehaeuse_v0.1.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in P.iterdir():
  if f.is_file():z.write(f,f.name)
print([(p.name,p.stat().st_size) for p in P.iterdir()])
