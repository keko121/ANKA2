#!/bin/bash
# =============================================================================
# ANKA2 Projesi - Ubuntu Bağımlılık Kurulum Scripti
# =============================================================================
# Bu script Ubuntu 22.04+ için gerekli paketleri kurar
# Kullanım: sudo ./install-deps-ubuntu.sh
# =============================================================================

set -e

echo "=============================================="
echo "  ANKA2 - Ubuntu Bağımlılık Kurulumu"
echo "=============================================="

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Root kontrolü
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}[HATA]${NC} Bu script root olarak çalıştırılmalı!"
    echo "Kullanım: sudo $0"
    exit 1
fi

echo -e "${YELLOW}[1/5]${NC} Paket listesi güncelleniyor..."
apt-get update -qq

echo -e "${YELLOW}[2/5]${NC} Temel derleme araçları kuruluyor..."
apt-get install -y \
    build-essential \
    ccache \
    clang-14 \
    llvm-14 \
    make \
    cmake \
    git \
    wget \
    curl

echo -e "${YELLOW}[3/5]${NC} 32-bit destek paketleri kuruluyor..."
dpkg --add-architecture i386
apt-get update -qq
apt-get install -y \
    gcc-multilib \
    g++-multilib \
    lib32gcc-s1 \
    lib32stdc++6 \
    libc6-dev-i386

echo -e "${YELLOW}[4/5]${NC} Kütüphaneler kuruluyor..."
apt-get install -y \
    libmysqlclient-dev \
    libssl-dev \
    libcrypto++-dev \
    libdevil-dev \
    liblzo2-dev \
    libboost-all-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev

# 32-bit kütüphaneler
apt-get install -y \
    libssl-dev:i386 \
    zlib1g-dev:i386 \
    || echo -e "${YELLOW}[UYARI]${NC} Bazı 32-bit paketler kurulamadı, devam ediliyor..."

echo -e "${YELLOW}[5/5]${NC} Sembolik linkler oluşturuluyor..."
# clang++ için sembolik link
if [ ! -f /usr/bin/clang++-devel ]; then
    ln -sf /usr/bin/clang++-14 /usr/bin/clang++-devel
    echo "  clang++-devel -> clang++-14"
fi

# Alternatif derleyici ayarı
update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-14 100 || true
update-alternatives --install /usr/bin/clang clang /usr/bin/clang-14 100 || true

echo ""
echo -e "${GREEN}=============================================="
echo "  ✅ Kurulum Tamamlandı!"
echo "==============================================${NC}"
echo ""
echo "Kurulu paketler:"
echo "  - clang++-14 (clang++-devel olarak linkli)"
echo "  - MySQL client library"
echo "  - OpenSSL"
echo "  - Crypto++"
echo "  - DevIL"
echo "  - LZO2"
echo "  - Boost"
echo "  - 32-bit destek"
echo ""
echo "Derleme için: cd Source/Server/game/src && make"
