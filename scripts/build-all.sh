#!/bin/bash
# =============================================================================
# ANKA2 Server - Tüm Bileşenleri Derleme Script'i
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SERVER_DIR="$PROJECT_ROOT/Source/Server"

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =============================================================================
# Paralel iş sayısı
# =============================================================================
JOBS="${JOBS:-$(nproc 2>/dev/null || echo 4)}"

# =============================================================================
# Clean build flag
# =============================================================================
CLEAN_BUILD="${CLEAN:-0}"

if [ "$1" == "clean" ] || [ "$1" == "--clean" ]; then
    CLEAN_BUILD=1
fi

# =============================================================================
# Derleme fonksiyonu
# =============================================================================
build_component() {
    local name="$1"
    local path="$2"
    
    log_step "Derleniyor: $name"
    
    cd "$path"
    
    if [ "$CLEAN_BUILD" == "1" ]; then
        make clean 2>/dev/null || true
    fi
    
    if make -j"$JOBS"; then
        log_info "✅ $name başarılı"
    else
        log_error "❌ $name başarısız"
        exit 1
    fi
    
    cd - > /dev/null
}

# =============================================================================
# Ana fonksiyon
# =============================================================================
main() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     ANKA2 Server Build System            ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
    echo ""
    
    log_info "Proje dizini: $PROJECT_ROOT"
    log_info "Paralel iş: $JOBS"
    log_info "Clean build: $CLEAN_BUILD"
    echo ""
    
    # Platform kontrolü
    UNAME_S=$(uname -s)
    log_info "Platform: $UNAME_S"
    
    if [ "$UNAME_S" == "Linux" ]; then
        log_info "Derleyici: clang-14"
    else
        log_info "Derleyici: clang++-devel"
    fi
    echo ""
    
    # ==========================================================================
    # Kütüphaneler
    # ==========================================================================
    echo -e "${YELLOW}=== KÜTÜPHANELER ===${NC}"
    
    build_component "liblua" "$SERVER_DIR/library/liblua"
    build_component "libthecore" "$SERVER_DIR/library/libthecore/src"
    build_component "libsql" "$SERVER_DIR/library/libsql"
    build_component "libpoly" "$SERVER_DIR/library/libpoly"
    build_component "libgame" "$SERVER_DIR/library/libgame/src"
    
    echo ""
    
    # ==========================================================================
    # Ana Binary'ler
    # ==========================================================================
    echo -e "${YELLOW}=== ANA BİNARY'LER ===${NC}"
    
    build_component "db" "$SERVER_DIR/db/src"
    build_component "game" "$SERVER_DIR/game/src"
    
    echo ""
    
    # ==========================================================================
    # Özet
    # ==========================================================================
    echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     ✅ DERLEME TAMAMLANDI               ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
    echo ""
    
    log_info "Binary'ler:"
    echo "  - $SERVER_DIR/game/src/game"
    echo "  - $SERVER_DIR/db/src/db"
    echo ""
    
    # Smoke test öner
    log_info "Test için: ./scripts/smoke-test.sh"
}

# Çalıştır
main "$@"
