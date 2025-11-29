// ============================================================================
// HybridModelManager.h - Granny2 + glTF Hybrid Yükleme Yöneticisi
// ============================================================================
// Bu sınıf, model dosyasının formatına göre uygun loader'ı seçer:
// - .gr2 dosyaları → Mevcut Granny SDK ile yüklenir
// - .gltf/.glb dosyaları → Assimp ile yüklenir
// ============================================================================
#pragma once

#include <string>
#include <memory>
#include <unordered_map>

// Forward declarations
class CGraphicThing;

namespace GLTF {
    class GLTFModelLoader;
    struct ModelData;
}

// ============================================================================
// Model Format Enum
// ============================================================================
enum class EModelFormat
{
    Unknown,
    Granny2,    // .gr2
    GLTF,       // .gltf
    GLB,        // .glb
    FBX,        // .fbx (Assimp ile)
    OBJ         // .obj (Assimp ile)
};

// ============================================================================
// Hybrid Model Manager
// ============================================================================
class CHybridModelManager
{
public:
    // Singleton erişimi
    static CHybridModelManager& Instance();
    
    // Format tespiti
    static EModelFormat DetectFormat(const std::string& filePath);
    static EModelFormat DetectFormatFromExtension(const std::string& extension);
    
    // Yükleme fonksiyonları
    // Granny veya glTF formatına göre otomatik yükleme
    bool LoadModel(const std::string& filePath);
    
    // Cache yönetimi
    void ClearCache();
    bool IsCached(const std::string& filePath) const;
    
    // glTF desteği etkin mi?
    static bool IsGLTFSupported();
    
    // Ayarlar
    void SetPreferGLTF(bool prefer) { m_preferGLTF = prefer; }
    bool GetPreferGLTF() const { return m_preferGLTF; }
    
    // .gr2 -> .gltf dosya adı dönüşümü
    // Örnek: "warrior.gr2" -> "warrior.gltf"
    static std::string GetGLTFPath(const std::string& gr2Path);
    
    // glTF dosyası varsa onu, yoksa gr2'yi yükle
    std::string ResolveModelPath(const std::string& originalPath);

private:
    CHybridModelManager();
    ~CHybridModelManager();
    
    // Singleton için kopyalama engeli
    CHybridModelManager(const CHybridModelManager&) = delete;
    CHybridModelManager& operator=(const CHybridModelManager&) = delete;
    
private:
    bool m_preferGLTF;  // glTF varsa onu tercih et
    
    // Model cache (glTF için)
    std::unordered_map<std::string, std::shared_ptr<GLTF::ModelData>> m_gltfCache;
};

// ============================================================================
// Yardımcı Makrolar
// ============================================================================

// glTF desteği için preprocessor tanımı
// Projeye USE_ASSIMP tanımı eklendiğinde aktif olur
#ifdef USE_ASSIMP
    #define GLTF_SUPPORT_ENABLED 1
#else
    #define GLTF_SUPPORT_ENABLED 0
#endif

// Model yüklerken format kontrolü
#define HYBRID_LOAD_MODEL(path) \
    CHybridModelManager::Instance().LoadModel(path)

// Format kontrolü
#define IS_GLTF_FILE(path) \
    (CHybridModelManager::DetectFormat(path) == EModelFormat::GLTF || \
     CHybridModelManager::DetectFormat(path) == EModelFormat::GLB)

#define IS_GRANNY_FILE(path) \
    (CHybridModelManager::DetectFormat(path) == EModelFormat::Granny2)

