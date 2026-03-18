import xml.etree.ElementTree as ET

def get_vulnerabilities(xml_input):
    root = ET.fromstring(xml_input)
    vulns = []

    for result in root.findall(".//result"):
        severity = float(result.find("severity").text or 0)
        if severity >= 4.0:
            vulns.append({
                "ip": result.find(".//host").text,
                "port": result.find(".//port").text,
                "name": result.find("name").text,
                "cvss": severity,
                "description": result.find("description").text[:500],
                "solution": result.find("solution").text if result.find("solution") is not None else "N/A"
            })
    return vulns
