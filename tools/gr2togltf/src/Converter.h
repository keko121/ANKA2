// ============================================================================
// Converter.h - GrannyReader + GLTFWriter birleştirici
// ============================================================================
#pragma once

#include "Types.h"
#include <string>

namespace gr2togltf {

class Converter {
public:
    Converter();
    ~Converter();
    
    // Ana dönüştürme fonksiyonu
    bool Convert(const std::string& inputPath, const std::string& outputPath, const ConvertOptions& options = ConvertOptions());
    
    // Batch dönüştürme
    int ConvertDirectory(const std::string& inputDir, const std::string& outputDir, const ConvertOptions& options = ConvertOptions());
    
    // Son hata mesajı
    const std::string& GetLastError() const { return m_lastError; }
    
    // İstatistikler
    int GetSuccessCount() const { return m_successCount; }
    int GetFailCount() const { return m_failCount; }

private:
    std::string m_lastError;
    int m_successCount = 0;
    int m_failCount = 0;
};

} // namespace gr2togltf
