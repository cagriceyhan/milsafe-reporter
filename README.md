MILSAFE - AI Powered Vulnerability Reporting Engine
MILSAFE, siber güvenlik tarama araçlarından (Nmap, Nessus, OpenVAS, Acunetix) elde edilen XML tabanlı teknik verileri analiz ederek, Google Gemini yapay zeka desteği ile ISO 27001 ve NIST standartlarında profesyonel denetim raporları üreten bir otomasyon sistemidir.

Teknik Özellikler
Otomatik Araç Tespiti: Girdi olarak verilen XML dosyasının yapısına göre tarama aracını (Nmap, Nessus, OpenVAS veya Acunetix) otomatik olarak tanımlar.

Yapay Zeka Analizi: Google Gemini 1.5 Flash modelini kullanarak teknik zafiyetleri yönetici özeti, risk matrisi ve stratejik yol haritası gibi bölümlere dönüştürür.

Rapor Formatı: Çıktıları Markdown (.md) formatında üretir ve otomatik olarak isimlendirir.

Modüler Yapı: Bağımsız fonksiyonlar sayesinde yeni tarama araçlarının entegrasyonuna açıktır.

Kurulum ve Konfigürasyon
Sistemin kurulumu için Python 3.x yüklü olmalıdır. Bağımlılık çakışmalarını önlemek amacıyla sanal ortam (venv) kullanılması zorunludur.

1. Deponun Yerel Ortama Aktarılması
Bash
git clone https://github.com/cagriceyhan/milsafe-reporter.git
cd milsafe-reporter
2. Sanal Ortamın Hazırlanması
Bash
# Sanal ortam oluşturma
python3 -m venv venv

# Sanal ortamın aktif edilmesi (Linux/MacOS)
source venv/bin/activate

# Sanal ortamın aktif edilmesi (Windows PowerShell)
.\venv\Scripts\Activate.ps1
3. Bağımlılıkların Yüklenmesi
Bash
pip install -r requirements.txt
4. Çevresel Değişkenlerin Tanımlanması
Güvenlik protokolleri gereği API anahtarı kod içerisine yazılmamalıdır. Bunun yerine terminal üzerinden çevresel değişken (environment variable) olarak tanımlanmalıdır:

Bash
# Linux / MacOS
export GEMINI_API_KEY="AIzaSy..."

# Windows (PowerShell)
$env:GEMINI_API_KEY="AIzaSy..."
Kullanım Rehberi
Analiz işlemini başlatmak için tarama sonucunu içeren XML dosyasını proje dizinine ekledikten sonra şu komutu çalıştırınız:

Bash
python3 report_gen.py tarama_sonucu.xml
Komut çalıştırıldığında sistem şu aşamaları izler:

XML verisindeki kritik bulguları ayrıştırır.

Teknik verileri Gemini API üzerinden analiz eder.

Çıktı olarak tarama_sonucu_report.md dosyasını oluşturur.

Dosya Yapısı
report_gen.py: Çekirdek motor ve API entegrasyon katmanı.

requirements.txt: Projenin ihtiyaç duyduğu kütüphane listesi.

.gitignore: Depoya dahil edilmemesi gereken sistem dosyalarının yapılandırması.

Geliştirici Bilgileri
Çağrı Ceyhan
