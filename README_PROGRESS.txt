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

------
--------------------------------------------------
Gelişim Özeti (19 Şubat 2026) - Karar Mekanizması ve Stabilizasyon

1. Mantık Katmanı (Logic Layer) Gelişimi:
* State Machine entegre edilerek sistemin IDLE, BUSY ve ALERT durumları tanımlandı[cite: 11, 20].
* Priority Manager mantığı ile düşük pil durumuna işlemci yükünden daha yüksek öncelik verildi[cite: 19].

2. Dinamik Yapılandırma (Config System):
* Tüm eşik değerleri (CPU sınırı, pil uyarısı) ve ekran renkleri dış bir 'config.json' dosyasına taşındı.
* Kodun içine müdahale etmeden sistemin çalışma parametrelerini değiştirme imkanı sağlandı.

3. Akıllı Loglama ve Filtreleme:
* Olay tabanlı (Event-driven) loglama sistemi kuruldu; sadece durum değişiklikleri kaydedilerek veri kirliliği önlendi[cite: 11, 32].
* Anlık CPU sıçramalarını (jitter) engellemek için zaman tabanlı filtreleme eklendi.

4. Görsel Motor Geliştirmeleri:
* Delta Time prensibi kullanılarak, donanım hızından bağımsız pürüzsüz animasyon altyapısı oluşturuldu[cite: 12, 30].
* Durumlara göre dinamik arka plan rengi değişimi aktif edildi[cite: 34].

----
--------------------------------------------------
Progress Summary (February 19, 2026) - Power Management & UI Finalization

1. Power Management (Deep Sleep):
* Implemented a simulated 'Deep Sleep' mode triggered by PC signal loss. 
* Added a professional fade-out animation using alpha blending in Pygame. [cite: 12, 31]
* Logic Layer now prioritizes connection status over system metrics during sleep transitions. 

2. Visual Refinement:
* Integrated dynamic progress bars for CPU and Battery with Lerp (Linear Interpolation) for smoothness. [cite: 12, 30]
* Re-organized UI layout to include real-time timestamps, system state, and metric bars. 
* Verified Delta Time implementation ensures consistent animation speed regardless of hardware performance. [cite: 12, 30]

3. System Integrity:
* Completed M1 (Python Core) milestone including config-driven thresholds and event-based logging. [cite: 32, 36]