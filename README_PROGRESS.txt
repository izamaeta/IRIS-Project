IRIS Project - Gelişim Özeti (18 Şubat 2026)
1. Proje Altyapısı ve Hazırlık:

Sanal Ortam: Proje, bağımlılıkların izole edilmesi amacıyla .venv (virtual environment) üzerine kuruldu.

Teknoloji Yığını: Python 3.13 tabanlı; psutil (sistem izleme), pygame (sanal ekran simülasyonu) ve pyserial (donanım iletişimi) kütüphaneleri entegre edildi.

Sürüm Kontrolü: Git reposu oluşturuldu ve .gitignore dosyası ile gereksiz dosyalar (pycache, .venv vb.) kapsam dışı bırakıldı.

2. Modüler Mimari (Refactoring):
Master Plan'da belirtilen "3 Katmanlı Yapı" kod seviyesinde ayrıştırıldı:


Sensör Katmanı (agents/): SystemMonitor sınıfı ile CPU, pil ve zaman verilerini toplayan yapı kuruldu.


İletişim/Görsel Katman (core/): Donanım (ESP32-S3) henüz mevcut olmadığı için DisplayManager sınıfı üzerinden Pygame ile sanal bir ekran (480x320) oluşturuldu.
+1

Orkestrasyon (main.py): Ana döngü, veriyi toplayıp ekrana basan bir "şef" görevi görecek şekilde optimize edildi.

3. Uygulanan Kritik Özellikler:


Polling Interval: Sistem kaynaklarını korumak amacıyla veri toplama işlemi saniyede 1 kez olacak şekilde sınırlandırıldı.

Sanal Simülasyon: Donanım erişimi sağlanana kadar tüm animasyon ve veri akışı testleri Pygame penceresi üzerinden takip edilebilir hale getirildi.