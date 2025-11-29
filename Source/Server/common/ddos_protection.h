#ifndef __INC_METIN_II_GAME_DDOS_PROTECTION_H__
#define __INC_METIN_II_GAME_DDOS_PROTECTION_H__

#include <map>
#include <string>
#include <time.h>
#include <queue>
#include <algorithm>
#include <cstdio>
#include <cstring>

// Log fonksiyonlarý makro olarak tanýmlý (log.h'de)
// Bu header'ý kullanan dosyalar log.h'i include etmeli
// sys_err ve sys_log makrolarý olduðu için forward declaration yapýlamaz

// ============================================
// PROFESYONEL DDoS KORUMA SÝSTEMÝ
// ============================================

// IP Ban ve Rate Limiting Yapýlarý
struct IPProtectionData
{
	// Unknown Header Tracking
	int unknownHeaderCount;
	time_t unknownHeaderBanTime;
	
	// Rate Limiting
	std::queue<time_t> packetTimestamps;  // Son paket zamanlarý
	int totalPackets;                     // Toplam paket sayýsý
	time_t lastPacketTime;                // Son paket zamaný
	
	// Connection Tracking
	int connectionCount;                  // Ayný IP'den baðlantý sayýsý
	time_t lastConnectionTime;            // Son baðlantý zamaný
	
	// Progressive Ban System
	int banLevel;                         // Ban seviyesi (0-5)
	time_t lastBanTime;                   // Son ban zamaný
	
	// Paket Boyutu Tracking
	int oversizedPacketCount;            // Çok büyük paket sayýsý
	int totalBytesReceived;               // Toplam alýnan byte
	
	// Grace Period
	bool inGracePeriod;                   // Ýlk uyarý döneminde mi?
	time_t gracePeriodStart;              // Grace period baþlangýç zamaný
	
	IPProtectionData() 
		: unknownHeaderCount(0)
		, unknownHeaderBanTime(0)
		, totalPackets(0)
		, lastPacketTime(0)
		, connectionCount(0)
		, lastConnectionTime(0)
		, banLevel(0)
		, lastBanTime(0)
		, oversizedPacketCount(0)
		, totalBytesReceived(0)
		, inGracePeriod(false)
		, gracePeriodStart(0)
	{
	}
};

// Global Protection Maps
static std::map<std::string, IPProtectionData> g_ipProtectionData;
static std::map<std::string, time_t> g_ipBlacklist;  // Manuel blacklist
static std::map<std::string, bool> g_ipWhitelist;    // Manuel whitelist

// ============================================
// KONFIGÜRASYON PARAMETRELERÝ
// ============================================

// Unknown Header Protection
#define ENABLE_UNKNOWN_HEADER_PROTECTION
#define UNKNOWN_HEADER_MAX_COUNT 5
#define UNKNOWN_HEADER_BAN_DURATION_BASE 300  // 5 dakika (base)
#define UNKNOWN_HEADER_BAN_DURATION_MAX 3600  // 1 saat (max)

// Rate Limiting (Paket Hýzý Sýnýrlama)
#define ENABLE_RATE_LIMITING
#define MAX_PACKETS_PER_SECOND 50            // Saniyede maksimum paket
#define MAX_PACKETS_PER_MINUTE 1000          // Dakikada maksimum paket
#define RATE_LIMIT_WINDOW_SECONDS 1          // Rate limit penceresi
#define RATE_LIMIT_WINDOW_MINUTES 60         // Rate limit penceresi (dakika)

// Connection Throttling (Baðlantý Sýnýrlama)
#define ENABLE_CONNECTION_THROTTLING
#define MAX_CONNECTIONS_PER_IP 3             // Ayný IP'den maksimum baðlantý
#define CONNECTION_COOLDOWN_SECONDS 10       // Baðlantý cooldown süresi

// Paket Boyutu Kontrolü
#define ENABLE_PACKET_SIZE_PROTECTION
#define MAX_PACKET_SIZE 65536                // Maksimum paket boyutu (64KB)
#define MAX_OVERSIZED_PACKETS 3              // Maksimum büyük paket sayýsý

// Progressive Ban System (Aþamalý Ban Sistemi)
#define ENABLE_PROGRESSIVE_BAN
#define MAX_BAN_LEVEL 5                      // Maksimum ban seviyesi
#define BAN_LEVEL_MULTIPLIER 2               // Her seviyede ban süresi 2x artar

// Grace Period (Ýlk Uyarý Sistemi)
#define ENABLE_GRACE_PERIOD
#define GRACE_PERIOD_DURATION 30             // 30 saniye grace period
#define GRACE_PERIOD_WARNINGS 2              // Grace period'da maksimum uyarý

// Otomatik Temizleme
#define ENABLE_AUTO_CLEANUP
#define CLEANUP_INTERVAL_SECONDS 300         // 5 dakikada bir temizleme
static time_t g_lastCleanupTime = 0;

// ============================================
// FONKSÝYONLAR
// ============================================

// IP'nin whitelist'te olup olmadýðýný kontrol et
inline bool IsIPWhitelisted(const std::string& ip)
{
	// Localhost ve loopback IP'leri otomatik whitelist'te
	if (ip == "127.0.0.1" || ip == "::1" || ip == "localhost" || ip.find("127.") == 0)
		return true;
	
	return g_ipWhitelist.count(ip) && g_ipWhitelist[ip];
}

// IP'nin blacklist'te olup olmadýðýný kontrol et
inline bool IsIPBlacklisted(const std::string& ip)
{
	time_t now = time(0);
	if (g_ipBlacklist.count(ip))
	{
		// Süresiz ban (0 = süresiz)
		if (g_ipBlacklist[ip] == 0)
			return true;
		// Süreli ban
		if (g_ipBlacklist[ip] > now)
			return true;
		// Süre dolmuþ, temizle
		g_ipBlacklist.erase(ip);
	}
	return false;
}

// IP'yi whitelist'e ekle
inline void AddToWhitelist(const std::string& ip)
{
	g_ipWhitelist[ip] = true;
}

// IP'yi blacklist'e ekle (süreli veya süresiz)
inline void AddToBlacklist(const std::string& ip, time_t banDuration = 0)
{
	if (banDuration == 0)
		g_ipBlacklist[ip] = 0;  // Süresiz ban
	else
		g_ipBlacklist[ip] = time(0) + banDuration;
}

// IP'yi blacklist'ten çýkar
inline void RemoveFromBlacklist(const std::string& ip)
{
	g_ipBlacklist.erase(ip);
}

// IP'nin banlý olup olmadýðýný kontrol et
inline bool IsIPBanned(const std::string& ip)
{
	// Whitelist kontrolü
	if (IsIPWhitelisted(ip))
		return false;
	
	// Blacklist kontrolü
	if (IsIPBlacklisted(ip))
		return true;
	
	// Protection data kontrolü
	if (g_ipProtectionData.count(ip))
	{
		IPProtectionData& data = g_ipProtectionData[ip];
		time_t now = time(0);
		
		// Unknown header ban kontrolü
		if (data.unknownHeaderBanTime > now)
			return true;
	}
	
	return false;
}

// Rate limiting kontrolü
inline bool CheckRateLimit(const std::string& ip, int packetSize = 0)
{
#ifdef ENABLE_RATE_LIMITING
	if (IsIPWhitelisted(ip))
		return true;
	
	time_t now = time(0);
	IPProtectionData& data = g_ipProtectionData[ip];
	
	// Eski paket zamanlarýný temizle (1 saniyelik pencere)
	while (!data.packetTimestamps.empty() && 
		   (now - data.packetTimestamps.front()) > RATE_LIMIT_WINDOW_SECONDS)
	{
		data.packetTimestamps.pop();
	}
	
	// Saniyede maksimum paket kontrolü
	if (data.packetTimestamps.size() >= MAX_PACKETS_PER_SECOND)
	{
		sys_err("[DDoS Protection] Rate limit exceeded for IP %s (%d packets/sec)", 
				ip.c_str(), (int)data.packetTimestamps.size());
		return false;
	}
	
	// Paket zamanýný ekle
	data.packetTimestamps.push(now);
	data.totalPackets++;
	data.lastPacketTime = now;
	
	// Dakikalýk toplam paket kontrolü
	if (data.totalPackets > MAX_PACKETS_PER_MINUTE)
	{
		// Son 1 dakikadaki paket sayýsýný kontrol et
		time_t oneMinuteAgo = now - RATE_LIMIT_WINDOW_MINUTES;
		if (data.lastPacketTime > oneMinuteAgo)
		{
			sys_err("[DDoS Protection] Minute rate limit exceeded for IP %s (%d total packets)", 
					ip.c_str(), data.totalPackets);
			return false;
		}
		// 1 dakika geçti, sýfýrla
		data.totalPackets = 0;
	}
	
	// Paket boyutu kontrolü
#ifdef ENABLE_PACKET_SIZE_PROTECTION
	if (packetSize > MAX_PACKET_SIZE)
	{
		data.oversizedPacketCount++;
		if (data.oversizedPacketCount >= MAX_OVERSIZED_PACKETS)
		{
			sys_err("[DDoS Protection] Oversized packet limit exceeded for IP %s (size: %d)", 
					ip.c_str(), packetSize);
			return false;
		}
	}
	data.totalBytesReceived += packetSize;
#endif
#endif
	
	return true;
}

// Connection throttling kontrolü
inline bool CheckConnectionLimit(const std::string& ip)
{
#ifdef ENABLE_CONNECTION_THROTTLING
	if (IsIPWhitelisted(ip))
		return true;
	
	time_t now = time(0);
	IPProtectionData& data = g_ipProtectionData[ip];
	
	// Cooldown kontrolü
	if (data.lastConnectionTime > 0 && 
		(now - data.lastConnectionTime) < CONNECTION_COOLDOWN_SECONDS)
	{
		data.connectionCount++;
		if (data.connectionCount >= MAX_CONNECTIONS_PER_IP)
		{
			sys_err("[DDoS Protection] Connection limit exceeded for IP %s (%d connections)", 
					ip.c_str(), data.connectionCount);
			return false;
		}
	}
	else
	{
		// Cooldown geçti, sýfýrla
		data.connectionCount = 1;
	}
	
	data.lastConnectionTime = now;
#endif
	
	return true;
}

// Unknown header tespiti ve ban
inline void HandleUnknownHeader(const std::string& ip)
{
#ifdef ENABLE_UNKNOWN_HEADER_PROTECTION
	if (IsIPWhitelisted(ip))
		return;
	
	time_t now = time(0);
	IPProtectionData& data = g_ipProtectionData[ip];
	
	data.unknownHeaderCount++;
	
	// Grace period kontrolü
#ifdef ENABLE_GRACE_PERIOD
	if (!data.inGracePeriod)
	{
		data.inGracePeriod = true;
		data.gracePeriodStart = now;
		sys_log(0, "[DDoS Protection] Grace period started for IP %s", ip.c_str());
	}
	
	// Grace period içindeyse sadece uyarý ver
	if (data.inGracePeriod && 
		(now - data.gracePeriodStart) < GRACE_PERIOD_DURATION)
	{
		if (data.unknownHeaderCount <= GRACE_PERIOD_WARNINGS)
		{
			sys_log(0, "[DDoS Protection] Warning %d/%d for IP %s (grace period)", 
					data.unknownHeaderCount, GRACE_PERIOD_WARNINGS, ip.c_str());
			return;
		}
	}
	
	// Grace period bitti veya limit aþýldý
	data.inGracePeriod = false;
#endif
	
	// Progressive ban sistemi
#ifdef ENABLE_PROGRESSIVE_BAN
	// Ban seviyesini artýr
	if (data.unknownHeaderCount >= UNKNOWN_HEADER_MAX_COUNT)
	{
		if (data.banLevel < MAX_BAN_LEVEL)
		{
			// Son ban'dan bu yana geçen süre kontrolü
			if (data.lastBanTime > 0 && (now - data.lastBanTime) < 3600)  // 1 saat içinde
			{
				data.banLevel++;
			}
			else
			{
				// 1 saat geçti, ban seviyesini sýfýrla
				data.banLevel = 1;
			}
		}
		
		// Ban süresini hesapla
		time_t banDuration = UNKNOWN_HEADER_BAN_DURATION_BASE;
		for (int i = 0; i < data.banLevel && i < MAX_BAN_LEVEL; i++)
		{
			banDuration *= BAN_LEVEL_MULTIPLIER;
		}
		
		// Maksimum ban süresini aþma
		if (banDuration > UNKNOWN_HEADER_BAN_DURATION_MAX)
			banDuration = UNKNOWN_HEADER_BAN_DURATION_MAX;
		
		data.unknownHeaderBanTime = now + banDuration;
		data.lastBanTime = now;
		data.unknownHeaderCount = 0;  // Sayaç sýfýrla
		
		sys_err("[DDoS Protection] IP %s banned for %d seconds (ban level: %d)", 
				ip.c_str(), (int)banDuration, data.banLevel);
	}
#else
	// Basit ban sistemi
	if (data.unknownHeaderCount >= UNKNOWN_HEADER_MAX_COUNT)
	{
		data.unknownHeaderBanTime = now + UNKNOWN_HEADER_BAN_DURATION_BASE;
		data.unknownHeaderCount = 0;
		sys_err("[DDoS Protection] IP %s banned for %d seconds", 
				ip.c_str(), UNKNOWN_HEADER_BAN_DURATION_BASE);
	}
#endif
#endif
}

// Otomatik temizleme (eski verileri sil)
inline void CleanupOldData()
{
#ifdef ENABLE_AUTO_CLEANUP
	time_t now = time(0);
	
	// Cleanup interval kontrolü
	if (g_lastCleanupTime > 0 && (now - g_lastCleanupTime) < CLEANUP_INTERVAL_SECONDS)
		return;
	
	g_lastCleanupTime = now;
	
	// Eski protection data'larý temizle (1 saatten eski ve banlý deðilse)
	auto it = g_ipProtectionData.begin();
	while (it != g_ipProtectionData.end())
	{
		IPProtectionData& data = it->second;
		
		// Ban süresi dolmuþ mu?
		if (data.unknownHeaderBanTime > 0 && data.unknownHeaderBanTime <= now)
		{
			// Ban süresi dolmuþ, veriyi temizle
			it = g_ipProtectionData.erase(it);
			continue;
		}
		
		// Son paket zamaný 1 saatten eski mi?
		if (data.lastPacketTime > 0 && (now - data.lastPacketTime) > 3600)
		{
			// Banlý deðilse temizle
			if (data.unknownHeaderBanTime <= now)
			{
				it = g_ipProtectionData.erase(it);
				continue;
			}
		}
		
		++it;
	}
	
	// Eski blacklist kayýtlarýný temizle (süreli banlar için)
	auto bit = g_ipBlacklist.begin();
	while (bit != g_ipBlacklist.end())
	{
		// Süresiz ban deðilse ve süre dolmuþsa temizle
		if (bit->second > 0 && bit->second <= now)
		{
			bit = g_ipBlacklist.erase(bit);
			continue;
		}
		++bit;
	}
#endif
}

// IP koruma verilerini sýfýrla (admin komutu için)
inline void ResetIPProtection(const std::string& ip)
{
	g_ipProtectionData.erase(ip);
	sys_log(0, "[DDoS Protection] Protection data reset for IP %s", ip.c_str());
}

// Tüm koruma verilerini sýfýrla (admin komutu için)
inline void ResetAllProtection()
{
	g_ipProtectionData.clear();
	sys_log(0, "[DDoS Protection] All protection data cleared");
}

// IP koruma istatistiklerini al (admin komutu için)
inline void GetIPProtectionStats(const std::string& ip, std::string& stats)
{
	if (!g_ipProtectionData.count(ip))
	{
		stats = "No protection data for IP: " + ip;
		return;
	}
	
	IPProtectionData& data = g_ipProtectionData[ip];
	char buf[512];
	
	snprintf(buf, sizeof(buf), 
		"IP: %s\n"
		"Unknown Headers: %d\n"
		"Ban Time: %ld\n"
		"Ban Level: %d\n"
		"Total Packets: %d\n"
		"Connections: %d\n"
		"Oversized Packets: %d\n"
		"Total Bytes: %d\n"
		"In Grace Period: %s",
		ip.c_str(),
		data.unknownHeaderCount,
		(long)data.unknownHeaderBanTime,
		data.banLevel,
		data.totalPackets,
		data.connectionCount,
		data.oversizedPacketCount,
		data.totalBytesReceived,
		data.inGracePeriod ? "Yes" : "No"
	);
	
	stats = buf;
}

#endif // __INC_METIN_II_GAME_DDOS_PROTECTION_H__

