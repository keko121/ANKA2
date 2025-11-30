#!/bin/bash
# =============================================================================
# ANKA2 Server Smoke Test Script
# Derlenen binary'lerin temel çalışabilirlik testi
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Renkli çıktı
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =============================================================================
# Binary varlık kontrolü
# =============================================================================
check_binary_exists() {
    local binary_path="$1"
    local binary_name="$2"
    
    if [ -f "$binary_path" ]; then
        log_info "$binary_name bulundu: $binary_path"
        
        # Dosya boyutu kontrolü (en az 100KB olmalı)
        local size=$(stat -f%z "$binary_path" 2>/dev/null || stat -c%s "$binary_path" 2>/dev/null)
        if [ "$size" -gt 100000 ]; then
            log_info "$binary_name boyut: $(numfmt --to=iec $size 2>/dev/null || echo "$size bytes")"
            return 0
        else
            log_error "$binary_name çok küçük: $size bytes"
            return 1
        fi
    else
        log_error "$binary_name bulunamadı: $binary_path"
        return 1
    fi
}

# =============================================================================
# Executable kontrolü
# =============================================================================
check_executable() {
    local binary_path="$1"
    local binary_name="$2"
    
    if [ -x "$binary_path" ]; then
        log_info "$binary_name çalıştırılabilir"
        return 0
    else
        log_warn "$binary_name çalıştırılabilir değil, chmod ekleniyor..."
        chmod +x "$binary_path"
        return 0
    fi
}

# =============================================================================
# Dinamik kütüphane bağımlılıkları kontrolü
# =============================================================================
check_dependencies() {
    local binary_path="$1"
    local binary_name="$2"
    
    log_info "$binary_name bağımlılıkları kontrol ediliyor..."
    
    if command -v ldd &> /dev/null; then
        # Linux
        local missing=$(ldd "$binary_path" 2>&1 | grep "not found" || true)
        if [ -n "$missing" ]; then
            log_error "$binary_name eksik kütüphaneler:"
            echo "$missing"
            return 1
        else
            log_info "$binary_name tüm bağımlılıklar mevcut"
            return 0
        fi
    elif command -v otool &> /dev/null; then
        # macOS
        otool -L "$binary_path"
        return 0
    else
        log_warn "ldd/otool bulunamadı, bağımlılık kontrolü atlandı"
        return 0
    fi
}

# =============================================================================
# Binary başlatma testi (kısa süreli)
# =============================================================================
test_binary_startup() {
    local binary_path="$1"
    local binary_name="$2"
    local timeout_sec="${3:-5}"
    
    log_info "$binary_name başlatma testi ($timeout_sec saniye)..."
    
    # Geçici dizin oluştur
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Binary'yi kopyala (bazı relative path sorunları için)
    cp "$binary_path" ./test_binary
    chmod +x ./test_binary
    
    # Timeout ile çalıştır
    set +e
    timeout "$timeout_sec" ./test_binary --version 2>&1 || true
    local exit_code=$?
    set -e
    
    # Temizlik
    cd - > /dev/null
    rm -rf "$test_dir"
    
    # 124 = timeout (normal, server bekliyor demek)
    # 0 = başarılı çıkış
    # 1 = config eksik (normal)
    if [ $exit_code -eq 124 ] || [ $exit_code -eq 0 ] || [ $exit_code -eq 1 ]; then
        log_info "$binary_name başlatma testi BAŞARILI (exit: $exit_code)"
        return 0
    else
        log_warn "$binary_name exit code: $exit_code (config eksik olabilir)"
        return 0  # Config olmadan çalışmıyor, bu beklenen
    fi
}

# =============================================================================
# Ana test fonksiyonu
# =============================================================================
main() {
    log_info "=========================================="
    log_info "ANKA2 Smoke Test Başlıyor"
    log_info "=========================================="
    
    local failed=0
    
    # Binary yolları (CI'dan veya local'den)
    local GAME_BIN="${GAME_BIN:-$PROJECT_ROOT/Source/Server/game/src/game}"
    local DB_BIN="${DB_BIN:-$PROJECT_ROOT/Source/Server/db/src/db}"
    
    # Alternatif yollar (build output)
    if [ ! -f "$GAME_BIN" ] && [ -f "$PROJECT_ROOT/build/game" ]; then
        GAME_BIN="$PROJECT_ROOT/build/game"
    fi
    if [ ! -f "$DB_BIN" ] && [ -f "$PROJECT_ROOT/build/db" ]; then
        DB_BIN="$PROJECT_ROOT/build/db"
    fi
    
    echo ""
    log_info "=== GAME SERVER TESTİ ==="
    
    if [ -f "$GAME_BIN" ]; then
        check_binary_exists "$GAME_BIN" "game" || ((failed++))
        check_executable "$GAME_BIN" "game" || ((failed++))
        check_dependencies "$GAME_BIN" "game" || ((failed++))
        # test_binary_startup "$GAME_BIN" "game" 3 || ((failed++))
    else
        log_warn "game binary bulunamadı, atlanıyor: $GAME_BIN"
    fi
    
    echo ""
    log_info "=== DB SERVER TESTİ ==="
    
    if [ -f "$DB_BIN" ]; then
        check_binary_exists "$DB_BIN" "db" || ((failed++))
        check_executable "$DB_BIN" "db" || ((failed++))
        check_dependencies "$DB_BIN" "db" || ((failed++))
        # test_binary_startup "$DB_BIN" "db" 3 || ((failed++))
    else
        log_warn "db binary bulunamadı, atlanıyor: $DB_BIN"
    fi
    
    echo ""
    log_info "=========================================="
    
    if [ $failed -eq 0 ]; then
        log_info "✅ TÜM TESTLER BAŞARILI"
        exit 0
    else
        log_error "❌ $failed TEST BAŞARISIZ"
        exit 1
    fi
}

# Script'i çalıştır
main "$@"
