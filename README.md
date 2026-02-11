# Smart Error Tracker (Mini)

Smart Error Tracker, bir uygulama log dosyasını analiz ederek INFO / WARNING / ERROR seviyelerini sayan, en sık görülen hataları bulan ve basit öneriler üreten mini bir Python aracıdır.

Bu proje, gerçek dünyada backend sistemlerinde sıkça kullanılan log analizi mantığını göstermek için hazırlanmıştır.

---

## Özellikler

- `app.log` dosyasını okur
- INFO / WARNING / ERROR satırlarını sayar
- En sık görülen ilk 3 hata mesajını çıkarır
- Hata türlerine göre basit çözüm önerileri üretir
- Analiz sonucunu hem terminal çıktısı olarak gösterir hem de `report.json` dosyasına kaydeder

---

## Dosyalar

- `tracker.py` → analiz aracı
- `app.log` → örnek log dosyası
- `report.json` → örnek rapor çıktısı

---

## Örnek Çıktı (Terminal)

