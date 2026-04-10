import os
import requests
import json
import xml.etree.ElementTree as ET
import sys

API_KEY = os.getenv("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

def get_vulnerabilities(xml_text):
    root = ET.fromstring(xml_text)
    vulns = []
    scan_method = "Bilinmeyen Tarama"

    if root.tag == 'nmaprun':
        scan_method = "Nmap (Script/Port Taraması)" if root.find(".//script") is not None else "Nmap (Hızlı Port Taraması)"
    elif root.find(".//result") is not None:
        scan_method = "OpenVAS / GVM (Kapsamlı Kurumsal Zafiyet Taraması)"
    elif root.tag == 'NessusClientData_v2':
        scan_method = "Nessus (Profesyonel Zafiyet Taraması)"
    elif root.tag == 'Scan' and 'Acunetix' in xml_text[:500]:
        scan_method = "Acunetix (Web Uygulama Güvenlik Taraması)"
    else:
        scan_method = "Genel XML / Bilinmeyen Araç (Otomatik Analiz)"

    for result in root.findall(".//result"):
        severity_node = result.find("severity")
        severity = float(severity_node.text) if severity_node is not None and severity_node.text else 0
        if severity >= 4.0:
            vulns.append({
                "source": "OpenVAS",
                "ip": result.find(".//host").text if result.find(".//host") is not None else "N/A",
                "port": result.find(".//port").text if result.find(".//port") is not None else "N/A",
                "name": result.find("name").text if result.find("name") is not None else "N/A",
                "cvss": severity,
                "detail": result.find("description").text[:500] if result.find("description") is not None else "N/A"
            })

    for host in root.findall(".//host"):
        ip = host.find(".//address").get("addr") if host.find(".//address") is not None else "N/A"
        for port_node in host.findall(".//port"):
            port_id = port_node.get("portid")
            for script in port_node.findall(".//script"):
                vulns.append({
                    "source": "Nmap Script",
                    "ip": ip,
                    "port": port_id,
                    "name": script.get("id"),
                    "cvss": "Nmap/Vuln Data",
                    "detail": script.get("output")[:500] if script.get("output") else "Detay yok"
                })
            if not port_node.findall(".//script") and port_node.find("state").get("state") == "open":
                vulns.append({
                    "source": "Nmap Port",
                    "ip": ip,
                    "port": port_id,
                    "name": port_node.find("service").get("name") if port_node.find("service") is not None else "Unknown",
                    "cvss": "Açık Port",
                    "detail": "Servis aktif, potansiyel zayıflık analizi gerekli."
                })

    for item in root.findall(".//ReportItem"):
        severity_val = item.get("severity")
        if severity_val and int(severity_val) >= 2: 
            vulns.append({
                "source": "Nessus",
                "ip": item.find("../").get("name") if item.find("../") is not None else "N/A",
                "port": item.get("port"),
                "name": item.get("pluginName"),
                "cvss": item.find("cvss_base_score").text if item.find("cvss_base_score") is not None else severity_val,
                "detail": item.find("description").text[:500] if item.find("description") is not None else "N/A"
            })

    for alert in root.findall(".//Vulnerability"):
        vulns.append({
            "source": "Acunetix",
            "ip": "Web Target",
            "port": "80/443",
            "name": alert.find("Name").text if alert.find("Name") is not None else "N/A",
            "cvss": alert.find("Severity").text if alert.find("Severity") is not None else "N/A",
            "detail": alert.find("Description").text[:500] if alert.find("Description") is not None else "N/A"
        })

    if not vulns:
        for node in root.iter():
            if any(key in node.tag.lower() for key in ["vuln", "alert", "issue", "finding"]):
                vulns.append({
                    "source": "Otomatik Keşif (Genel)",
                    "ip": "Bilinmiyor",
                    "port": "N/A",
                    "name": node.tag,
                    "cvss": "Analiz Ediliyor",
                    "detail": node.text[:300] if node.text else "Veri çekilemedi"
                })

    return {"method": scan_method, "data": vulns}

try:
    if not API_KEY:
        print("HATA: GEMINI_API_KEY bulunamadı!")
        sys.exit(1)

    xml_filename = sys.argv[1] if len(sys.argv) > 1 else 'deneme.xml'
    base_name = os.path.splitext(xml_filename)[0] 
    output_filename = f"{base_name}_report.md" 

    with open(xml_filename, 'r', encoding="utf-8") as f:
        xml_content = f.read()
    
    extraction = get_vulnerabilities(xml_content)
    scan_method = extraction["method"]
    vuln_data = extraction["data"]

    if not vuln_data:
        print("UYARI: XML içinde analiz edilecek bulgu bulunamadı.")
        sys.exit(0)

    print(f"--- Metodoloji: {scan_method} ---")
    print(f"--- {len(vuln_data)} adet bulgu analiz ediliyor... ---")
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"""
                Sen; CISSP, OSCP ve CISA sertifikalı kıdemli bir Siber Güvenlik Denetçisisin. 
                Sana iletilen teknik verileri kullanarak ISO 27001 standartlarında bir rapor hazırla.

                **KRİTİK BİLGİ - TARAMA METODOLOJİSİ:** {scan_method}
                Bu metodolojiye göre raporun başında 'Tarama Metodolojisi ve Kapsam' bölümü oluştur. 
                Eğer sadece port taramasıysa risklerin teorik olduğunu, script/openvas taramasıysa bulguların doğrulandığını belirt.

                TEKNİK VERİLER:
                {vuln_data}

                RAPOR YAPISI:
                1. Tarama Metodolojisi ve Kapsam
                2. Yönetici Özeti (Executive Summary)
                3. Risk ve Öncelik Matrisi (Tablo)
                4. Derinlemesine Teknik Analiz (İstismar Senaryosu ve Çözüm dahil)
                5. 24s / 7g / 30g Stratejik Yol Haritası

                DİL: Tamamen Türkçe ve profesyonel/akademik.
                """
            }]
        }]
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
    result = response.json()

    if response.status_code == 200:
        report_text = result['candidates'][0]['content']['parts'][0]['text']
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(report_text)
        print(f"\n--- İşlem Tamam! {output_filename} kaydedildi. ---")
    else:
        print(f"Hata: {response.text}")

except Exception as e:
    print(f"Bir hata oluştu: {e}")
