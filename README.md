# AYDAKAR – Otonom Hedef Tespit ve Takip Sistemi

> TEKNOFEST 2026 **Savaşan İHA** yarışması AYDAKAR takımı için geliştirdiğim otonom hedef tespit, takip ve kilitlenme yazılımından seçilmiş parçalar.

⚠️ **Not:** Bu depo bir **vitrin (showcase)** deposudur. Sistemin tamamı takıma ait olduğu için paylaşılmamıştır. Burada yalnızca mimariyi göstermek için seçilen birkaç bağımsız modül bulunur. Dosyalar tek başına çalıştırılmak için değil, kod yapısını göstermek için eklenmiştir (`core.config` gibi bağımlılıklar depoda yoktur).

## 🎥 Demo

_Çalışma videosu yakında eklenecek._ <!-- media/ klasörüne eklenecek -->

## Sistem Hakkında

Sistem, İHA kamerasından gelen görüntüde rakip İHA'ları tespit eder, takip eder, hedef seçer ve yarışma kurallarına uygun şekilde kilitlenme sağlar. Windows'ta test edilip Linux/WSL ve NVIDIA Jetson Orin NX üzerinde çalışacak şekilde modüler tasarlandı.

**Ana modüller (tam sistemde):**

| Katman | Görev |
|---|---|
| `core/` | Konfigürasyon, merkezi state, thread-safe event bus, zamanlama, loglama |
| `vision/` | Görüntü kaynağı, YOLO tabanlı nesne tespiti, QR tespiti, pinhole kamera modeli |
| `tracking/` | Kalman / **IMM (Interacting Multiple Model)** tabanlı çoklu hedef takibi, tehdit yönetimi |
| `decision/` | OODA döngüsü, enerji yönetimi, hedef seçici, kilitlenme motoru |
| `control/` | Mesafeye bağlı dinamik PID kontrol |
| `mission/`, `communication/` | Görev yönetimi, telemetri haberleşmesi |
| `bridge/`, `ui/` | Flask/HTTP köprüsü (Yer Kontrol İstasyonu bağlantısı), HUD |

## Bu Depodaki Örnek Modüller

- **`src/control/pid_controller.py`**: Hedefe olan mesafe azaldıkça P ve D kazançlarını dinamik olarak artıran 3 eksenli PID kontrolcü. *Anti-windup* ve *derivative on measurement* (derivative kick önleme) içerir.
- **`src/vision/camera_model.py`**: Pinhole kamera modeli. Bounding box'tan hedefin metrik 3D konumunu tahmin eder ve tersini hesaplar.
- **`src/core/event_bus.py`**: Modüller arası gevşek bağlı iletişim için thread-safe, singleton event bus.
- **`src/core/types.py`**: Sistem genelinde kullanılan veri tipleri (`Vector3`, `BBox`, `TrackedEntity`, `FlightState`).

## Teknolojiler

Python · OpenCV · Ultralytics YOLO · PyTorch · FilterPy (Kalman/IMM) · NumPy · Flask · Cython · NVIDIA Jetson

---
*AYDAKAR İHA Takımı – Isparta Uygulamalı Bilimler Üniversitesi.*
