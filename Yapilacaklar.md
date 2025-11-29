# 📋 ANKA2 Projesi - Yapılacaklar Listesi

> **Son Güncelleme:** 29 Kasım 2025  
> **Durum:** Planlama Aşaması

---

## 🎯 PROJE ÖZETİ

```
┌─────────────────────────────────────────────────────────────┐
│  SEN: git push                                              │
│         ↓                                                   │
│  GitHub Actions (5 dk):                                     │
│    ✅ Ubuntu'da server derle                                │
│    ✅ Windows'ta client derle                               │
│    ✅ Testler çalıştır                                      │
│    ✅ VPS'e otomatik deploy                                 │
│         ↓                                                   │
│  🎉 Sunucu güncellendi, oyuncular oynuyor!                  │
└─────────────────────────────────────────────────────────────┘
```

### Branch Stratejisi
| Branch | Amaç | Push Sonucu |
|--------|------|-------------|
| `develop` | Geliştirme/test | Sadece build |
| `main` | Production | Build + **Otomatik Deploy** |

---

## 📊 MEVCUT DURUM

| Bileşen | Durum | Platform | Derleme |
|---------|-------|----------|---------|
| Server (game) | ✅ Aktif | FreeBSD 13.1+ | Makefile + clang++ |
| Server (db) | ✅ Aktif | FreeBSD 13.1+ | Makefile + clang++ |
| Client | ✅ Aktif | Windows | VS 2022 (.sln) |
| CI/CD | ❌ Yok | - | - |
| CMake | ❌ Yok | - | - |

---

## 🚀 FAZ 1: ALTYAPI VE CI/CD (0-30 Gün)

### Hafta 1-2: CI/CD Kurulumu

- [x] **1.1** `.github/workflows/build.yml` oluştur ✅ 29.11.2025
  - Ubuntu 22.04 server build
  - Windows client build (MSBuild)
  - Artifact upload

- [x] **1.2** `scripts/install-deps-ubuntu.sh` yaz ✅ 29.11.2025
  - clang-14, libmysqlclient-dev, libssl-dev
  - libcrypto++-dev, libdevil-dev, liblzo2-dev
  - lib32gcc-s1 (32-bit desteği)

- [x] **1.3** Makefile platform algılama ekle ✅ 29.11.2025
  - Linux/FreeBSD otomatik algılama
  - Derleyici ve yol değişkenleri

### Hafta 3-4: Linux Port Temelleri

- [x] **1.4** `fdwatch.c` güncelle ✅ 29.11.2025
  - epoll desteği (Linux)
  - select fallback
  - Mevcut kqueue korunsun (FreeBSD)

- [x] **1.5** Hardcoded yolları konfigüre et ✅ 29.11.2025
  - `/usr/home/share/bin` → değişken
  - Makefile GAMEDIR/DBDIR parametresi

---

## 🔧 FAZ 2: LINUX PORT & STABİLİZASYON (30-90 Gün)

### Hafta 5-8: Server Linux Derlemesi

- [x] **2.1** libthecore güncellemeleri ✅ 29.11.2025
  - fdwatch.c epoll/select
  - Platform makroları

- [x] **2.2** libsql güncellemeleri ✅ 29.11.2025
  - Ubuntu MySQL client yolu
  - Dinamik/statik link seçeneği

- [x] **2.3** game/db Makefile güncellemeleri ✅ 29.11.2025
  - Include/lib yolları
  - Ubuntu paket uyumu

- [ ] **2.4** 32-bit derleme testi
  - multilib paketleri
  - veya 64-bit geçiş planı

### Hafta 9-12: Test ve Stabilizasyon

- [x] **2.5** Smoke test script yaz ✅ 29.11.2025
  - Server başlatma testi
  - Port dinleme kontrolü
  - Graceful shutdown

- [x] **2.6** CI test entegrasyonu ✅ 29.11.2025
  - Build sonrası otomatik test
  - Hata raporlama

- [x] **2.7** cppcheck/linter ekle ✅ 29.11.2025
  - Kod kalitesi kontrolü
  - CI'da zorunlu geçiş

---

## 🎨 FAZ 3: GRANNY → glTF DÖNÜŞÜM (90-180 Gün)

### Hafta 13-16: Converter POC

- [x] **3.1** Granny SDK analizi ✅ 29.11.2025
  - Gerekli fonksiyonlar listele
  - Veri yapıları dokümante et

- [x] **3.2** `tools/gr2togltf/` klasörü oluştur ✅ 29.11.2025
  - CMakeLists.txt
  - main.cpp (CLI tool)
  - GrannyReader.cpp
  - GLTFWriter.cpp

- [ ] **3.3** Tek model dönüştürme
  - Mesh verileri
  - Skeleton/bone
  - 1 animasyon

- [ ] **3.4** Test modeli seç ve dönüştür
  - warrior_m.gr2 önerisi
  - Görsel doğrulama

### Hafta 17-20: Client Loader Entegrasyonu

- [x] **3.5** Assimp kütüphanesi ekle ✅ 29.11.2025
  - extern/include/assimp (README hazır)
  - extern/library/ (.lib dosyaları gerekli)

- [x] **3.6** Hybrid loader yaz ✅ 29.11.2025
  - .gr2 → mevcut Granny kod
  - .gltf/.glb → Assimp loader

- [x] **3.7** EterGrnLib güncellemeleri ✅ 29.11.2025
  - GLTFModelLoader.cpp/h
  - HybridModelManager.cpp/h

- [ ] **3.8** İlk glTF model testi
  - Dönüştürülen model yükle
  - Render kontrolü
  - Animasyon kontrolü

### Hafta 21-24: PBR Shader (Opsiyonel)

- [ ] **3.9** PBR shader araştırması
  - D3D8 içinde approximation
  - veya D3D11 upgrade planı

- [ ] **3.10** Texture pipeline
  - albedo/normal/metallic/roughness
  - Mevcut texture uyumu

---

## 📦 FAZ 4: BATCH DÖNÜŞÜM & DEPLOY (180+ Gün)

### Toplu Dönüştürme

- [x] **4.1** `tools/batch_convert.py` yaz ✅ 29.11.2025
  - Tüm .gr2 dosyalarını tara
  - Paralel dönüştürme (multiprocessing)
  - Hata raporlama
  - Model önceliklendirme dahil

- [x] **4.2** Model önceliklendirme ✅ 29.11.2025
  - Karakter modelleri önce (priority 4)
  - NPC/mob modelleri sonra (priority 3)
  - Silah/araç (priority 2)
  - Zone/prop en son (priority 1)

- [ ] **4.3** Görsel QA süreci
  - Dönüştürülen modeller kontrol
  - Sorunlu modeller listele

### CI/CD Deploy

- [ ] **4.4** `.github/workflows/deploy.yml`
  - Artifact download
  - VPS'e SCP/rsync
  - Rollback mekanizması

- [ ] **4.5** Monitoring ekle
  - Server health check
  - Otomatik restart

---

## ⚠️ RİSKLER

| Risk | Olasılık | Etki | Mitigasyon |
|------|----------|------|------------|
| Granny SDK erişim sorunu | Orta | Yüksek | SDK header mevcut ✅, .gr2 dosyalar gerekli |
| 32-bit → 64-bit sorunları | Orta | Orta | Önce 32-bit ile devam |
| Animasyon uyumsuzluğu | Yüksek | Yüksek | POC'da erken test |
| DirectX 8 kısıtlamaları | Düşük | Orta | Mevcut renderer ile başla |

---

## ✅ ALINAN KARARLAR

| Karar | Seçim | Tarih |
|-------|-------|-------|
| Deploy Modu | 🟢 Tam Otomatik | 29.11.2025 |
| Sunucu OS | Ubuntu (Linux) | 29.11.2025 |
| Model Formatı | Assimp/glTF | 29.11.2025 |
| Client OS | Windows | 29.11.2025 |

## ❓ BEKLEYEN KARARLAR

1. **VPS Bilgileri** (Deploy için gerekli)
   - [ ] Ubuntu VPS IP adresi
   - [ ] SSH kullanıcı adı
   - [ ] SSH key veya şifre

2. **Granny SDK / .gr2 dosyaları**
   - [ ] Test için hangi modeller kullanılacak?
   - [ ] .gr2 örnek dosyalar mevcut mu?

---

## 📁 OLUŞTURULACAK DOSYALAR

```
Anka2Project-main/
├── .github/
│   └── workflows/
│       ├── build.yml          # CI build workflow
│       ├── test.yml           # CI test workflow
│       └── deploy.yml         # CD deploy workflow
├── scripts/
│   ├── install-deps-ubuntu.sh # Ubuntu bağımlılıkları
│   ├── install-deps-freebsd.sh # FreeBSD bağımlılıkları (mevcut)
│   └── smoke-test.sh          # Basit test script
├── tools/
│   ├── gr2togltf/             # Converter tool
│   │   ├── CMakeLists.txt
│   │   ├── main.cpp
│   │   ├── GrannyReader.cpp
│   │   └── GLTFWriter.cpp
│   └── batch_convert.py       # Toplu dönüştürme
└── docs/
    ├── LINUX_BUILD.md         # Linux derleme rehberi
    └── GLTF_MIGRATION.md      # glTF geçiş dokümantasyonu
```

---

## 📝 NOTLAR

- Tüm değişiklikler PR ile yapılacak
- Her PR için CI must-pass
- Main branch korumalı tutulacak
- Semantic versioning kullanılacak

---

## 🔄 İLERLEME TAKİBİ

| Faz | Başlangıç | Bitiş | Durum |
|-----|-----------|-------|-------|
| Faz 1: CI/CD | 29.11.2025 | - | 🟢 Devam Ediyor |
| Faz 2: Linux Port | 29.11.2025 | - | 🟢 Devam Ediyor |
| Faz 3: Granny→glTF | - | - | ⏳ Beklemede |
| Faz 4: Deploy | - | - | ⏳ Beklemede |

---

*Bu dosya proje ilerledikçe güncellenecektir.*
