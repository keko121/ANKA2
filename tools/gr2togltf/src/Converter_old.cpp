// ============================================================================
// Converter.cpp - GrannyReader + GLTFWriter birleştirici implementasyonu
// ============================================================================

#include "Converter.h"
#include "GrannyReader.h"
#include "GLTFWriter.h"

#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

namespace gr2togltf {

Converter::Converter() = default;
Converter::~Converter() = default;

// ============================================================================
// Tek Dosya Dönüştürme
// ============================================================================
bool Converter::Convert(const std::string& inputPath, const std::string& outputPath, const ConvertOptions& options) {
    m_lastError.clear();
    
    // Input kontrolü
    if (!fs::exists(inputPath)) {
        m_lastError = "Girdi dosyasi bulunamadi: " + inputPath;
        std::cerr << "HATA: " << m_lastError << std::endl;
        m_failCount++;
        return false;
    }
    
    std::cout << "========================================" << std::endl;
    std::cout << "Donusturuluyor: " << inputPath << std::endl;
    std::cout << "========================================" << std::endl;
    
    // 1. GR2 dosyasını oku
    GrannyReader reader;
    if (!reader.Load(inputPath)) {
        m_lastError = "GR2 dosyasi okunamadi: " + inputPath;
        m_failCount++;
        return false;
    }
    
    // 2. Model verisini çıkart
    ModelData modelData;
    if (!reader.ExtractModelData(modelData, options)) {
        m_lastError = "Model verisi cikarilamadi: " + inputPath;
        m_failCount++;
        return false;
    }
    
    // 3. Çıktı yolunu hazırla
    std::string finalOutput = outputPath;
    if (finalOutput.empty()) {
        // Input dosya adından oluştur
        fs::path p(inputPath);
        p.replace_extension(options.outputFormat == "glb" ? ".glb" : ".gltf");
        finalOutput = p.string();
    }
    
    // Çıktı dizinini oluştur
    fs::path outDir = fs::path(finalOutput).parent_path();
    if (!outDir.empty() && !fs::exists(outDir)) {
        fs::create_directories(outDir);
    }
    
    // 4. glTF olarak yaz
    GLTFWriter writer;
    if (!writer.Write(modelData, finalOutput, options)) {
        m_lastError = "glTF yazma basarisiz: " + finalOutput;
        m_failCount++;
        return false;
    }
    
    std::cout << "✅ Donusum basarili: " << finalOutput << std::endl;
    std::cout << std::endl;
    
    m_successCount++;
    return true;
}

// ============================================================================
// Dizin Dönüştürme (Batch)
// ============================================================================
int Converter::ConvertDirectory(const std::string& inputDir, const std::string& outputDir, const ConvertOptions& options) {
    if (!fs::exists(inputDir) || !fs::is_directory(inputDir)) {
        m_lastError = "Gecersiz girdi dizini: " + inputDir;
        std::cerr << "HATA: " << m_lastError << std::endl;
        return 0;
    }
    
    // Çıktı dizinini oluştur
    if (!fs::exists(outputDir)) {
        fs::create_directories(outputDir);
    }
    
    int convertedCount = 0;
    
    // .gr2 dosyalarını bul
    for (const auto& entry : fs::recursive_directory_iterator(inputDir)) {
        if (entry.is_regular_file()) {
            std::string ext = entry.path().extension().string();
            // Büyük/küçük harf duyarsız karşılaştırma
            std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
            
            if (ext == ".gr2") {
                // Çıktı yolunu hesapla (dizin yapısını koru)
                fs::path relativePath = fs::relative(entry.path(), inputDir);
                fs::path outputPath = fs::path(outputDir) / relativePath;
                outputPath.replace_extension(options.outputFormat == "glb" ? ".glb" : ".gltf");
                
                if (Convert(entry.path().string(), outputPath.string(), options)) {
                    convertedCount++;
                }
            }
        }
    }
    
    std::cout << "========================================" << std::endl;
    std::cout << "Batch donusum tamamlandi!" << std::endl;
    std::cout << "Basarili: " << m_successCount << std::endl;
    std::cout << "Basarisiz: " << m_failCount << std::endl;
    std::cout << "========================================" << std::endl;
    
    return convertedCount;
}

} // namespace gr2togltf
