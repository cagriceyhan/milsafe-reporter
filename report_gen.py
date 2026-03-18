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
    for result in root.findall(".//result"):
        severity_node = result.find("severity")
        severity = float(severity_node.text) if severity_node is not None and severity_node.text else 0
        if severity >= 4.0:
            vulns.append({
                "ip": result.find(".//host").text if result.find(".//host") is not None else "N/A",
                "port": result.find(".//port").text if result.find(".//port") is not None else "N/A",
                "name": result.find("name").text if result.find("name") is not None else "N/A",
                "cvss": severity,
                "detail": result.find("description").text[:500] if result.find("description") is not None else "N/A",
                "solution": result.find("solution").text if result.find("solution") is not None else "N/A"
            })
    return vulns

try:
    if not API_KEY:
        print("HATA: GEMINI_API_KEY bulunamadı!")
        sys.exit(1)

    xml_filename = sys.argv[1] if len(sys.argv) > 1 else 'deneme.xml'
    base_name = os.path.splitext(xml_filename)[0] 
    output_filename = f"{base_name}_report.md" 

    with open(xml_filename, 'r', encoding="utf-8") as f:
        xml_content = f.read()
    
    data = get_vulnerabilities(xml_content)
    print(f"--- Rapor Hazırlanıyor... ---")
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"""
                Sen kıdemli bir Siber Güvenlik Danışmanı ve Analistisin. 
                Aşağıdaki OpenVAS tarama verilerini kullanarak, hem teknik ekibin hem de teknik bilgisi olmayan bir yöneticinin anlayabileceği, akademik ve profesyonel bir 'Zafiyet Analiz ve İyileştirme Raporu' oluştur.

                Raporun yapısı tam olarak şu şekilde olmalı:
                1. **Yönetici Özeti:** Sistemin genel güvenlik durumunu 2-3 cümleyle özetle.
                2. **Risk ve Öncelik Tablosu:** Zafiyetleri; Adı, Kritiklik Seviyesi, Port ve Varsa CVE Numarası şeklinde bir Markdown tablosunda göster.
                3. **Detaylı Analiz ve Aksiyon Planı:** Her bir zafiyet için 'Nedir?', 'Tehlikesi Nedir?' ve 'Nasıl Çözülür?' kısımlarını açıkla.
                4. **Acil Müdahale Çağrısı:** En kritik zafiyeti vurgula.

                DİL: Tamamen Türkçe.
                VERİLER:
                {data}
                """
            }]
        }]
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
    result = response.json()

    if response.status_code == 200:
        report_text = result['candidates'][0]['content']['parts'][0]['text']
        print("\n" + report_text)

        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(report_text)
        print(f"\n--- İşlem Tamam! {output_filename} kaydedildi. ---")
    else:
        print(f"Hata Kodu: {response.status_code}")
        print(f"Mesaj: {response.text}")

except Exception as e:
    print(f"Bir hata oluştu: {e}")
