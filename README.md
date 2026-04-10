MILSAFE - AI Powered Vulnerability Reporting Engine
MILSAFE, siber güvenlik tarama araçlarından (Nmap, Nessus, OpenVAS, Acunetix) elde edilen karmaşık XML verilerini analiz eden ve yapay zeka desteğiyle ISO 27001 standartlarında profesyonel denetim raporları sunan bir otomasyon aracıdır.

Öne Çıkan Özellikler
Çoklu Araç Desteği: Nmap, Nessus, OpenVAS ve Acunetix çıktılarını otomatik olarak tanır ve ayrıştırır.

Yapay Zeka Entegrasyonu: Google Gemini AI kullanarak teknik bulguları yönetici özetleri ve çözüm önerilerine dönüştürür.

ISO 27001 Uyumluluğu: Bulguları doğrudan Bilgi Güvenliği Yönetim Sistemi kontrolleriyle eşleştirir.

Dinamik Raporlama: Girdi dosyasına göre otomatik isimlendirme yaparak Markdown (.md) formatında profesyonel raporlar üretir.

Hızlı Kurulum: Bağımlılıkları optimize edilmiş, taşınabilir yapı.

Teknik Gereksinimler ve Kurulum
Proje, bağımlılık çakışmalarını önlemek için Python sanal ortamı (venv) üzerinde çalışacak şekilde tasarlanmıştır.

Depoyu Klonlayın:

Bash
git clone https://github.com/cagriceyhan/milsafe-reporter.git
cd milsafe-reporter
Sanal Ortamı Kurun ve Aktif Edin:

Bash
# Linux / MacOS
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
Bağımlılıkları Yükleyin:

Bash
pip install -r requirements.txt
Kullanım
Uygulamayı çalıştırmadan önce Google AI Studio üzerinden aldığınız API anahtarını sisteme tanıtmanız gerekmektedir.

1. API Anahtarını Tanımlama
Bash
# Linux / MacOS
export GEMINI_API_KEY="BURAYA_API_ANAHTARINIZI_YAZIN"

# Windows (PowerShell)
$env:GEMINI_API_KEY="BURAYA_API_ANAHTARINIZI_YAZIN"
2. Analizi Başlatma
Taramadan elde ettiğiniz XML dosyasını proje dizinine kopyalayın ve aşağıdaki komutu çalıştırın:

Bash
python3 report_gen.py hedef_dosya.xml
Proje Yapısı
report_gen.py: Ana motor ve API entegrasyonu.

requirements.txt: Gerekli Python kütüphanelerinin listesi.

.gitignore: Gereksiz dosyaların (venv, pycache) depoya yüklenmesini engelleyen yapılandırma.

README.md: Proje dokümantasyonu.

Geliştirici
Çağrı Ceyhan (0xCC)
