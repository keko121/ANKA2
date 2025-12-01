# Anka2 Game Server & Client Projesi

> Last updated: December 1, 2025

## 📋 Proje Hakkında

Bu proje, Anka2 MMORPG oyunu için geliştirilmiş sunucu ve istemci kaynak kodlarını içermektedir. Proje, modern C++ standartları kullanılarak geliştirilmiş ve optimize edilmiştir.

### ⚠️ Önemli Notlar

- **FoxFS Formatı**: FoxFS'nin düzgün çalışması için `.rar` dosyasındaki formatı takip edin. Dosya yapısını ve dizin organizasyonunu değiştirmeyin.
- **Kod Temizliği**: Proje kodları %75 oranında temizlenmiştir. Ölü kodlar ve yorum satırları tamamen kaldırılmıştır.
- **Client Temizliği**: Client tarafında tekrarlanan eşyalar, moblar, yorum satırları ve kullanılmayan kodlar temizlenmiştir.
- **Lokalizasyon**: Mob sohbetleri, OX Quiz ve locale_string artık client'tan `locale/[lang]` dizininden yüklenmektedir. Görev çevirileri hala `[lang]/translate.lua` dosyasından yüklenmektedir. Yakında görev çevirileri de client tarafına taşınacaktır.

---

## 🏗️ Altyapı Bilgileri

- **Altyapı**: Mainline
- **İşletim Sistemi**: FreeBSD 13.1 ve üzeri
- **Veritabanı**: MySQL 5.6 (libmysqlclient.a)
- **Server Derleyici**: ccache clang++-devel (C++2a/C++20 standardı)
- **Client Derleyici**: Visual Studio 2022 (v143 toolset)
- **Server C++ Standardı**: C++2a (C++20)
- **Client C++ Standardı**: C++17 (Debug), C++20 (Release)
- **Server Mimari**: 32-bit (x32)
- **Client Mimari**: 32-bit (Win32)
- **Build Sistemi**: Makefile (Server), Visual Studio Solution (Client)
- **Önbellek**: ccache (Server derleme hızlandırma)

---

## 📁 Proje Yapısı

### Client (Binary)

```
Source/Binary/
├── source/                    # Kaynak kodlar
│   ├── UserInterface/        # Ana kullanıcı arayüzü modülü (182 dosya)
│   ├── GameLib/              # Oyun mantığı kütüphanesi (98 dosya)
│   ├── EterLib/              # Eter altyapı kütüphanesi (157 dosya)
│   ├── EterBase/             # Temel yardımcı sınıflar
│   ├── EterGrnLib/           # Granny model sistemi
│   ├── EterImageLib/         # Görüntü işleme kütüphanesi
│   ├── EterLocale/           # Lokalizasyon desteği
│   ├── EterPack/             # Paket dosyası yönetimi
│   ├── EterPythonLib/        # Python 2.7 entegrasyonu
│   ├── EffectLib/            # Parçacık efektleri
│   ├── ScriptLib/            # Script yönetimi
│   ├── SpeedTreeLib/         # SpeedTree entegrasyonu
│   ├── SphereLib/            # Fizik motoru
│   ├── MilesLib/             # Ses sistemi
│   ├── Discord/              # Discord RPC entegrasyonu
│   └── CWebBrowser/          # Web tarayıcı entegrasyonu
├── extern/                    # Harici kütüphaneler
│   ├── include/              # Header dosyaları
│   │   ├── boost/            # Boost C++ kütüphaneleri
│   │   ├── cryptopp/         # Crypto++ şifreleme
│   │   ├── Python-2.7/       # Python 2.7 headers
│   │   ├── d3d8/             # DirectX 8 headers
│   │   ├── FoxFS.h           # FoxFS dosya sistemi
│   │   └── ...
│   └── library/              # Derlenmiş kütüphaneler (.lib)
├── vs_files/                 # Visual Studio proje dosyaları
└── client.sln                # Visual Studio solution dosyası
```

**Client Modülleri:**
- **UserInterface**: Ana oyun arayüzü, ağ yönetimi, oyuncu yönetimi, envanter sistemi
- **GameLib**: Oyun nesneleri, aktörler, çarpışma tespiti, hareket sistemi
- **EterLib**: Grafik motoru, DirectX 8 wrapper, render sistemi
- **EterPythonLib**: Python script entegrasyonu, UI modülleri
- **EffectLib**: Parçacık efektleri, ışık efektleri, görsel efektler

### Server

```
Source/Server/
├── game/                     # Oyun sunucusu
│   └── src/                  # Kaynak kodlar (316 dosya)
│       ├── char.cpp          # Karakter yönetimi
│       ├── item.cpp          # Eşya sistemi
│       ├── questmanager.cpp  # Görev yönetimi
│       ├── mob_manager.cpp   # Mob yönetimi
│       ├── guild.cpp         # Lonca sistemi
│       ├── party.cpp         # Parti sistemi
│       ├── shop.cpp          # Dükkan sistemi
│       ├── dungeon.cpp       # Zindan sistemi
│       └── ...
├── db/                       # Veritabanı sunucusu
│   └── src/                  # Kaynak kodlar
│       ├── DBManager.cpp     # Veritabanı yönetimi
│       ├── ClientManager.cpp # İstemci yönetimi
│       └── ...
├── common/                   # Ortak header dosyaları
│   ├── service.h             # Servis tanımlamaları
│   ├── singleton.h           # Singleton pattern
│   └── ...
└── library/                  # Sunucu kütüphaneleri
    ├── libthecore/           # Çekirdek kütüphane
    ├── liblua/               # Lua script motoru
    ├── libsql/               # SQL wrapper
    ├── libgame/              # Oyun yardımcıları
    └── ...
```

**Server Modülleri:**
- **game/src**: Ana oyun sunucusu, karakter yönetimi, savaş sistemi, görev sistemi
- **db/src**: Veritabanı sunucusu, SQL sorguları, veri yönetimi
- **library**: Paylaşılan kütüphaneler (Lua, SQL, çekirdek)

---

## 🔧 Derleme Gereksinimleri

### Server (FreeBSD)

**Gerekli Paketler:**
```bash
pkg install boost-all cryptopp ccache llvm-devel gmake devil lzo2 \
             mysql56-server mysql56-client python27 openssl \
             makedepend subversion binutils
```

**Build Komutları:**
```bash
cd Source/Server/game/src
make clean
make
```

**Özellikler:**
- FreeBSD 13.1+ gereklidir
- ccache clang++-devel derleyici kullanılır
- C++20 (C++2a) standardı
- 32-bit (x32) mimari
- Makefile tabanlı build sistemi
- ccache ile hızlandırılmış derleme
- MySQL 5.6 client library (libmysqlclient.a)

### Client (Windows)

**Gereksinimler:**
- Visual Studio 2022 (v143 toolset)
- Windows SDK 10.0
- Python 2.7 (development headers)

**Build Komutları:**
```batch
cd Source\Binary
# Visual Studio'da client.sln dosyasını açın
# Release x32 konfigürasyonunu seçin
# Build > Rebuild Solution
```

**Özellikler:**
- Visual Studio 2022 solution
- C++17 (Debug) / C++20 (Release)
- Precompiled headers kullanımı
- Multi-processor compilation
- 16 adet statik kütüphane projesi

---

## 🛠️ Kullanılan Teknolojiler

### Client Tarafı

- **Programlama Dili**: C++17/C++20
- **Grafik API**: DirectX 8
- **Script Dili**: Python 2.7
- **Kütüphaneler**:
  - Boost C++ Libraries
  - Crypto++ (şifreleme)
  - FoxFS (dosya sistemi)
  - Granny2 (3D model formatı)
  - DevIL (görüntü işleme)
  - LZ4/LZO (sıkıştırma)
  - RapidJSON (JSON işleme)
  - Discord RPC (Discord entegrasyonu)

### Server Tarafı

- **Programlama Dili**: C++20 (C++2a)
- **Script Dili**: Lua 5.x
- **Veritabanı**: MySQL 5.6 (libmysqlclient.a)
- **Kütüphaneler**:
  - Boost C++ Libraries
  - Crypto++ (şifreleme)
  - Lua (script motoru)
  - Custom SQL wrapper
  - Custom core library (libthecore)

---

## 📝 Kod Yapısı Örnekleri

### Client - Python Entegrasyonu

```cpp
// UserInterface/PythonNetworkStream.cpp
// Python script'lerinden ağ işlemlerine erişim

class CPythonNetworkStream {
    void SetLanguage(BYTE bLanguage);
    void SendChangeLanguagePacket(BYTE bLanguage);
    // ...
};
```

### Server - Karakter Yönetimi

```cpp
// game/src/char.cpp
// Karakter oluşturma, güncelleme, kaydetme

class CHARACTER {
    bool Create(const char* name, DWORD vid, bool isPC);
    void Update();
    void Save();
    // ...
};
```

### Server - Görev Sistemi

```cpp
// game/src/questmanager.cpp
// Lua tabanlı görev sistemi

class CQuestManager {
    bool RunState(const char* quest_name, const char* state_name);
    void ExecuteQuestScript(const char* quest_name);
    // ...
};
```

---

## 📄 Önemli Dosyalar

### Client

- `UserInterface/PythonNetworkStream.cpp`: Ağ iletişimi ve paket yönetimi
- `UserInterface/Locale.cpp`: Lokalizasyon yönetimi
- `GameLib/ActorInstance.cpp`: Oyun karakterleri ve NPC'ler
- `EterLib/GrpDevice.cpp`: DirectX 8 grafik cihazı yönetimi

### Server

- `game/src/char.cpp`: Karakter sistemi (162+ dosya içinde en önemlisi)
- `game/src/questmanager.cpp`: Görev yönetim sistemi
- `game/src/item.cpp`: Eşya sistemi
- `game/src/mob_manager.cpp`: Mob yönetimi
- `db/src/DBManager.cpp`: Veritabanı yönetimi
- `common/service.h`: Tüm özellik flag'leri ve yapılandırma

---

## ✨ Özellikler

Proje, `common/service.h` dosyasında tanımlanan 100+ özellik flag'i ile genişletilebilir bir yapıya sahiptir:

- 🐾 Pet Sistemi
- 🐴 Binek Sistemi
- 📜 Görev Sistemi (Lua tabanlı)
- 🏰 Lonca Sistemi (Guild System)
  - Temel lonca yönetimi
  - Lonca seviye sistemi (20 seviye, ENABLE_EXTENDED_GUILD_LEVEL ile 40 seviyeye çıkarılabilir)
  - Lonca bankası (para yatırma/çekme)
  - Lonca üye yönetimi
  - Lonca yetki sistemi
  - Lonca savaşı
- 👥 Parti Sistemi
- 🛒 Çevrimdışı Pazar
- 👗 Kostüm Sistemi
- 🌍 Çoklu Dil Desteği
- 💎 Premium Sistemi
- 🏛️ Zindan Sistemi
- 🎣 Avcılık Sistemi
- 🐉 Büyüme Pet Sistemi
- Ve daha fazlası...

### 🏰 Lonca Sistemi (Guild System) Detayları

Lonca sistemi `Source/Server/game/src/guild.cpp` dosyasında implemente edilmiştir. Sistem aşağıdaki özelliklere sahiptir:

**Temel Özellikler:**
- Lonca oluşturma ve yönetimi
- Üye ekleme/çıkarma
- Lonca seviye sistemi (GUILD_MAX_LEVEL = 20, ENABLE_EXTENDED_GUILD_LEVEL ile 40)
- Lonca bankası (para yatırma/çekme)
- Lonca yetki sistemi (15 seviye)
- Lonca yorum sistemi

**Güvenlik Özellikleri:**
- SQL injection koruması (EscapeString kullanımı)
- Null pointer kontrolleri
- Integer overflow kontrolleri
- Buffer overflow koruması
- Memory leak önleme

**Yapılandırılabilir Özellikler (service.h):**
- `ENABLE_GUILDRENEWAL_SYSTEM`: Gelişmiş lonca altyapısı
- `ENABLE_EXTENDED_GUILD_LEVEL`: Lonca seviye kapasitesinin 40'a çıkarılması
- `ENABLE_NEW_WAR_OPTIONS`: Tur, puan ve süre bazlı modern lonca savaşı seçenekleri
- `ENABLE_GUILD_DONATE_ATTENDANCE`: Günlük lonca bağışı ve katılım takip sistemi
- `ENABLE_GUILD_WAR_SCORE`: Lonca savaş istatistiklerinin detaylı skor ekranı
- `ENABLE_GUILD_LAND_INFO`: Lonca arazilerine ait detaylı bilgi arayüzü
- `ENABLE_GUILDBANK_LOG`: Lonca banka ve işlem kayıtlarının günlük sistemi
- `ENABLE_GUILDBANK_EXTENDED_LOGS`: Genişletilmiş günlükler için Log.cpp bağlantısı
- `ENABLE_EXTENDED_RENEWAL_FEATURES`: Lonca lideri devri ve arazi silme yönetimi
- `ENABLE_COLEADER_WAR_PRIVILEGES`: Lider çevrimdışı olduğunda, Yardımcı Lider lider ile aynı yetkilere sahip olur
- `ENABLE_GUILDWAR_BUTTON`: Arayüzde Lonca Savaşı erişim düğmesini aktif eder

**Güvenlik Düzeltmeleri:**
- SQL sorgu sonuçları için null pointer kontrolleri eklendi
- Kullanıcı girdileri EscapeString ile sanitize ediliyor
- Integer overflow kontrolleri eklendi (GOLD_MAX kontrolü)
- Buffer overflow koruması (strlcpy, snprintf kullanımı)
- Memory leak önleme (unique_ptr kullanımı)

---

## 🔒 Güvenlik ve Performans

### Güvenlik Önlemleri

Proje, aşağıdaki güvenlik önlemlerini içermektedir:

1. **SQL Injection Koruması**
   - Tüm kullanıcı girdileri `DBManager::EscapeString()` ile sanitize edilir
   - Parametreli sorgular kullanılır

2. **Buffer Overflow Koruması**
   - `strlcpy`, `snprintf` gibi güvenli fonksiyonlar kullanılır
   - Buffer boyut kontrolleri yapılır

3. **Null Pointer Kontrolleri**
   - SQL sorgu sonuçları kontrol edilir
   - Pointer kullanımlarından önce null kontrolü yapılır

4. **Integer Overflow Kontrolleri**
   - GOLD_MAX gibi maksimum değer kontrolleri
   - Aritmetik işlemlerde overflow kontrolü

5. **Memory Leak Önleme**
   - `std::unique_ptr` kullanımı
   - RAII prensiplerine uyum

### Performans Optimizasyonları

- SQL sorguları optimize edilmiştir
- Gereksiz sorgu tekrarları önlenmiştir
- Buffer yönetimi optimize edilmiştir

---

## 📜 Lisans ve Kullanım

Bu proje eğitim ve araştırma amaçlıdır. Ticari kullanım için gerekli lisansları kontrol edin.

---

## 👥 Katkıda Bulunanlar

- **Altyapı**: Mainline
- **Kod Temizleme**: %75 ölü kod temizliği yapılmıştır
- **Güvenlik Düzeltmeleri**: SQL injection, buffer overflow, null pointer kontrolleri eklendi
- **Performans Optimizasyonları**: SQL sorgu optimizasyonları ve memory leak önlemleri

---

## 💬 Destek

Sorularınız için proje issue'larını kullanabilirsiniz.

---

**Not**: Bu dokümantasyon proje yapısına göre oluşturulmuştur. Gerçek kod yapısı ve özellikler kaynak kodları inceleyerek doğrulanmalıdır.

---

## 📅 Son Güncellemeler

Detaylı değişiklik notları için `CHANGELOG_2025.md` dosyasına bakın.