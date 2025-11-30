# 🐧 ANKA2 Linux (Ubuntu) Derleme Rehberi

Bu dokümantasyon, ANKA2 sunucusunun Ubuntu Linux üzerinde derlenmesini açıklar.

## 📋 Gereksinimler

### İşletim Sistemi
- **Ubuntu 22.04 LTS** (önerilen)
- Ubuntu 20.04 LTS (desteklenir)

### Donanım
- **RAM:** Minimum 2GB (derleme için 4GB önerilir)
- **Disk:** Minimum 10GB boş alan
- **CPU:** x86_64 (32-bit binary üretilir)

## 🔧 Bağımlılıklar

### Otomatik Kurulum

```bash
# Proje dizinine git
cd /path/to/Anka2Project-main

# Bağımlılıkları kur
chmod +x scripts/install-deps-ubuntu.sh
sudo ./scripts/install-deps-ubuntu.sh
```

### Manuel Kurulum

```bash
# Temel araçlar
sudo apt update
sudo apt install -y build-essential git wget curl

# Derleyici
sudo apt install -y clang-14

# 32-bit destek
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install -y gcc-multilib g++-multilib lib32gcc-s1 lib32stdc++6

# Kütüphaneler
sudo apt install -y \
    libmysqlclient-dev \
    libssl-dev \
    libcrypto++-dev \
    libdevil-dev \
    liblzo2-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev

# 32-bit kütüphaneler
sudo apt install -y \
    libmysqlclient-dev:i386 \
    libssl-dev:i386 \
    zlib1g-dev:i386
```

## 🏗️ Derleme

### Tüm Projeyi Derleme

```bash
# Proje dizinine git
cd /path/to/Anka2Project-main/Source/Server

# Tüm kütüphaneleri derle
cd library/libthecore/src && make clean && make && cd ../../..
cd library/libsql && make clean && make && cd ../..
cd library/libpoly && make clean && make && cd ../..
cd library/libgame/src && make clean && make && cd ../../..
cd library/liblua && make clean && make && cd ../..

# Ana binary'leri derle
cd game/src && make clean && make && cd ../..
cd db/src && make clean && make && cd ../..
```

### Tek Komutla Derleme

```bash
# scripts/build-all.sh kullanabilirsiniz (oluşturulacak)
./scripts/build-all.sh
```

### Sadece Belirli Binary

```bash
# Sadece game server
cd Source/Server/game/src
make clean && make

# Sadece db server  
cd Source/Server/db/src
make clean && make
```

## 🧪 Test

```bash
# Smoke test çalıştır
./scripts/smoke-test.sh

# Binary kontrolü
file Source/Server/game/src/game
# Çıktı: ELF 32-bit LSB executable...

# Bağımlılık kontrolü
ldd Source/Server/game/src/game
```

## ❓ Sık Karşılaşılan Sorunlar

### 1. "clang-14: command not found"

```bash
# Alternatif clang sürümü kullan
sudo apt install clang
sudo ln -s /usr/bin/clang /usr/bin/clang-14
```

### 2. "cannot find -lmysqlclient"

```bash
# 32-bit MySQL client kur
sudo apt install libmysqlclient-dev:i386

# veya symlink oluştur
sudo ln -s /usr/lib/x86_64-linux-gnu/libmysqlclient.so /usr/lib/i386-linux-gnu/
```

### 3. "bits/c++config.h: No such file"

```bash
# 32-bit C++ headers kur
sudo apt install g++-multilib
```

### 4. "epoll.h: No such file"

Bu dosya Linux'ta standart olarak bulunur. Eğer hata alıyorsanız:
```bash
sudo apt install linux-libc-dev
```

## 📁 Çıktı Dosyaları

Başarılı derlemeden sonra:

```
Source/Server/
├── game/src/game          # Game server binary
├── db/src/db              # DB server binary
└── library/
    ├── libthecore/src/libthecore.a
    ├── libsql/libsql.a
    ├── libpoly/libpoly.a
    ├── libgame/src/libgame.a
    └── liblua/lib/liblua.a
```

## 🚀 Çalıştırma

> ⚠️ **Not:** Sunucuyu çalıştırmak için ek konfigürasyon dosyaları gereklidir.

```bash
# Game server
cd /path/to/server/game
./game

# DB server (ayrı terminal)
cd /path/to/server/db
./db
```

## 🔄 CI/CD ile Otomatik Derleme

GitHub Actions ile her push'ta otomatik derleme yapılır:

1. `develop` branch → Sadece build
2. `main` branch → Build + Deploy

Detaylar için `.github/workflows/build.yml` dosyasına bakın.

---

## 📚 Ek Kaynaklar

- [FreeBSD'den Linux'a Port Notları](./MIGRATION_NOTES.md)
- [Yapılacaklar Listesi](../Yapilacaklar.md)
- [GitHub Actions Workflow](../.github/workflows/build.yml)
