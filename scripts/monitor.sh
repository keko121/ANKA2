#!/bin/bash
# ============================================================================
# ANKA2 Server Monitor Script
# ============================================================================
# Sunucu durumunu izler ve gerektiğinde yeniden başlatır
# Cron ile her 5 dakikada bir çalıştırılabilir:
#   */5 * * * * /home/mt2/scripts/monitor.sh >> /home/mt2/logs/monitor.log 2>&1
# ============================================================================

set -e

# ==========================================================================
# Konfigürasyon
# ==========================================================================
GAME_DIR="${GAME_DIR:-/home/mt2/game}"
LOG_DIR="${LOG_DIR:-/home/mt2/logs}"
SLACK_WEBHOOK="${SLACK_WEBHOOK:-}"
DISCORD_WEBHOOK="${DISCORD_WEBHOOK:-}"

# Beklenen portlar
GAME_PORTS=(13000 13001 13002 13003)
DB_PORT=13099
AUTH_PORT=11000

# Retry ayarları
MAX_RETRIES=3
RETRY_DELAY=10

# ==========================================================================
# Log Fonksiyonları
# ==========================================================================
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >&2
}

log_warn() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARN: $1"
}

log_success() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ $1"
}

# ==========================================================================
# Bildirim Fonksiyonları
# ==========================================================================
send_notification() {
    local message="$1"
    local severity="${2:-info}"  # info, warning, error
    
    log "Sending notification: $message"
    
    # Discord
    if [ -n "$DISCORD_WEBHOOK" ]; then
        local color=3447003  # blue
        case "$severity" in
            warning) color=15105570 ;;  # orange
            error)   color=15158332 ;;  # red
            success) color=3066993 ;;   # green
        esac
        
        curl -s -X POST -H "Content-Type: application/json" \
            -d "{\"embeds\":[{\"title\":\"ANKA2 Monitor\",\"description\":\"$message\",\"color\":$color}]}" \
            "$DISCORD_WEBHOOK" > /dev/null 2>&1 || true
    fi
    
    # Slack
    if [ -n "$SLACK_WEBHOOK" ]; then
        local emoji=":information_source:"
        case "$severity" in
            warning) emoji=":warning:" ;;
            error)   emoji=":x:" ;;
            success) emoji=":white_check_mark:" ;;
        esac
        
        curl -s -X POST -H "Content-Type: application/json" \
            -d "{\"text\":\"$emoji $message\"}" \
            "$SLACK_WEBHOOK" > /dev/null 2>&1 || true
    fi
}

# ==========================================================================
# Durum Kontrol Fonksiyonları
# ==========================================================================
check_process() {
    local process_name="$1"
    pgrep -f "$process_name" > /dev/null 2>&1
}

check_port() {
    local port="$1"
    netstat -tuln 2>/dev/null | grep -q ":${port}" || \
    ss -tuln 2>/dev/null | grep -q ":${port}"
}

get_memory_usage() {
    local process_name="$1"
    local pid=$(pgrep -f "$process_name" | head -1)
    if [ -n "$pid" ]; then
        ps -o rss= -p "$pid" 2>/dev/null | awk '{print int($1/1024)}'
    else
        echo "0"
    fi
}

get_cpu_usage() {
    local process_name="$1"
    local pid=$(pgrep -f "$process_name" | head -1)
    if [ -n "$pid" ]; then
        ps -o %cpu= -p "$pid" 2>/dev/null | awk '{print int($1)}'
    else
        echo "0"
    fi
}

# ==========================================================================
# Sunucu Yönetim Fonksiyonları
# ==========================================================================
start_game_server() {
    log "Starting game server..."
    cd "$GAME_DIR"
    
    if [ -f "./start.sh" ]; then
        ./start.sh
    else
        # Manuel başlatma
        ./game &
    fi
    
    sleep 5
}

start_db_server() {
    log "Starting DB server..."
    cd "$GAME_DIR"
    
    if [ -f "./db" ]; then
        ./db &
    fi
    
    sleep 3
}

stop_all_servers() {
    log "Stopping all servers..."
    
    if [ -f "$GAME_DIR/stop.sh" ]; then
        cd "$GAME_DIR" && ./stop.sh
    else
        pkill -f "game" || true
        pkill -f "db" || true
    fi
    
    sleep 5
}

restart_server() {
    local server_type="$1"
    log_warn "Restarting $server_type server..."
    
    send_notification "🔄 $server_type sunucusu yeniden başlatılıyor..." "warning"
    
    case "$server_type" in
        game)
            pkill -f "game" || true
            sleep 3
            start_game_server
            ;;
        db)
            pkill -f "db" || true
            sleep 3
            start_db_server
            ;;
        all)
            stop_all_servers
            start_db_server
            start_game_server
            ;;
    esac
}

# ==========================================================================
# Sağlık Kontrolü
# ==========================================================================
health_check() {
    local status=0
    local issues=()
    
    log "Running health check..."
    
    # Game process kontrolü
    if ! check_process "game"; then
        log_error "Game process not running!"
        issues+=("Game process down")
        status=1
    fi
    
    # DB process kontrolü
    if ! check_process "db"; then
        log_error "DB process not running!"
        issues+=("DB process down")
        status=1
    fi
    
    # Game port kontrolleri
    for port in "${GAME_PORTS[@]}"; do
        if ! check_port "$port"; then
            log_warn "Game port $port not listening"
            issues+=("Port $port closed")
            status=1
        fi
    done
    
    # DB port kontrolü
    if ! check_port "$DB_PORT"; then
        log_error "DB port $DB_PORT not listening!"
        issues+=("DB port $DB_PORT closed")
        status=1
    fi
    
    # Bellek kullanımı kontrolü (MB)
    local game_mem=$(get_memory_usage "game")
    local db_mem=$(get_memory_usage "db")
    
    if [ "$game_mem" -gt 4096 ]; then
        log_warn "Game memory usage high: ${game_mem}MB"
        issues+=("High memory: ${game_mem}MB")
    fi
    
    # CPU kullanımı kontrolü
    local game_cpu=$(get_cpu_usage "game")
    if [ "$game_cpu" -gt 90 ]; then
        log_warn "Game CPU usage high: ${game_cpu}%"
        issues+=("High CPU: ${game_cpu}%")
    fi
    
    # Disk alanı kontrolü
    local disk_usage=$(df "$GAME_DIR" | tail -1 | awk '{print int($5)}')
    if [ "$disk_usage" -gt 90 ]; then
        log_warn "Disk usage high: ${disk_usage}%"
        issues+=("Disk ${disk_usage}% full")
    fi
    
    # Sonuç
    if [ $status -eq 0 ]; then
        log_success "Health check passed"
    else
        log_error "Health check failed: ${issues[*]}"
    fi
    
    return $status
}

# ==========================================================================
# Auto-Recovery
# ==========================================================================
auto_recover() {
    local retry_count=0
    
    while [ $retry_count -lt $MAX_RETRIES ]; do
        log "Auto-recovery attempt $((retry_count + 1))/$MAX_RETRIES"
        
        # Game process kontrolü ve yeniden başlatma
        if ! check_process "game"; then
            start_game_server
        fi
        
        # DB process kontrolü ve yeniden başlatma
        if ! check_process "db"; then
            start_db_server
        fi
        
        sleep $RETRY_DELAY
        
        # Tekrar kontrol
        if health_check; then
            send_notification "✅ Sunucu otomatik olarak düzeltildi!" "success"
            return 0
        fi
        
        retry_count=$((retry_count + 1))
    done
    
    # Başarısız
    send_notification "❌ Sunucu otomatik kurtarılamadı! Manuel müdahale gerekli." "error"
    return 1
}

# ==========================================================================
# Rapor Oluşturma
# ==========================================================================
generate_report() {
    echo "======================================"
    echo "ANKA2 Server Status Report"
    echo "Generated: $(date)"
    echo "======================================"
    echo ""
    
    echo "PROCESSES:"
    echo "----------"
    if check_process "game"; then
        echo "  Game: ✅ Running (PID: $(pgrep -f game | head -1))"
        echo "    Memory: $(get_memory_usage game)MB"
        echo "    CPU: $(get_cpu_usage game)%"
    else
        echo "  Game: ❌ Not Running"
    fi
    
    if check_process "db"; then
        echo "  DB: ✅ Running (PID: $(pgrep -f db | head -1))"
        echo "    Memory: $(get_memory_usage db)MB"
        echo "    CPU: $(get_cpu_usage db)%"
    else
        echo "  DB: ❌ Not Running"
    fi
    
    echo ""
    echo "PORTS:"
    echo "------"
    for port in "${GAME_PORTS[@]}"; do
        if check_port "$port"; then
            echo "  $port: ✅ Listening"
        else
            echo "  $port: ❌ Closed"
        fi
    done
    
    echo ""
    echo "SYSTEM:"
    echo "-------"
    echo "  Disk: $(df -h "$GAME_DIR" | tail -1 | awk '{print $5}') used"
    echo "  Load: $(uptime | awk -F'load average:' '{print $2}')"
    echo "  Uptime: $(uptime -p)"
    echo ""
}

# ==========================================================================
# Ana Program
# ==========================================================================
main() {
    local command="${1:-check}"
    
    mkdir -p "$LOG_DIR"
    
    case "$command" in
        check)
            if ! health_check; then
                auto_recover
            fi
            ;;
        status|report)
            generate_report
            ;;
        restart)
            restart_server "${2:-all}"
            ;;
        start)
            start_db_server
            start_game_server
            ;;
        stop)
            stop_all_servers
            ;;
        *)
            echo "Usage: $0 {check|status|report|restart|start|stop}"
            echo ""
            echo "Commands:"
            echo "  check   - Health check and auto-recover (default)"
            echo "  status  - Show server status report"
            echo "  restart - Restart servers [game|db|all]"
            echo "  start   - Start all servers"
            echo "  stop    - Stop all servers"
            exit 1
            ;;
    esac
}

main "$@"
