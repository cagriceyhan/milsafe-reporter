OpenVAS XML to Professional Report Generator (with Gemini AI)

Bu araç, OpenVAS (GVM) üzerinden alınan karmaşık XML tarama sonuçlarını, Google Gemini 2.0 Flash modelini kullanarak hem teknik ekiplerin hem de yöneticilerin anlayabileceği profesyonel bir siber güvenlik raporuna dönüştürür.


Özellikler : 

AI Destekli Analiz: Zafiyetleri sadece listelemez, "Nedir?", "Tehlikesi Nedir?" ve "Nasıl Çözülür?" sorularına mantıklı cevaplar üretir.

Dinamik Raporlama: Girdi dosyasının adına göre (örn: deneme.xml -> deneme_report.md) otomatik isimlendirme yapar.

Güvenli Yapı: API anahtarınızı kodun içinde değil, çevresel değişkenlerde (environment variables) saklar.

Hızlı ve Hafif: Sadece Python ve temel kütüphanelerle çalışır.


Kurulum ve Kullanım :

Sisteminizde Python 3.x yüklü olmalıdır. Gerekli kütüphaneyi şu komutla kurabilirsiniz:
pip install requests

API Anahtarını Tanımlama
Bu araç Google Gemini API kullanır. Google AI Studio üzerinden ücretsiz bir API anahtarı aldıktan sonra terminalinize şu komutu girin:
# Linux / MacOS
export GEMINI_API_KEY="BURAYA_API_ANAHTARINIZI_YAZIN"
# Windows (PowerShell)
$env:GEMINI_API_KEY="BURAYA_API_ANAHTARINIZI_YAZIN"

Çalıştırma
Taramadan elde ettiğiniz .xml dosyasını proje klasörüne atın ve şu komutu çalıştırın:
python3 report_gen.py dosya_adiniz.xml
