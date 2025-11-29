// ============================================================================
// HybridModelManager.cpp - Granny2 + glTF Hybrid Yükleme Yöneticisi
// ============================================================================

#include "HybridModelManager.h"
#include "GLTFModelLoader.h"

#include <algorithm>
#include <filesystem>

namespace fs = std::filesystem;

// ============================================================================
// Singleton Instance
// ============================================================================
CHybridModelManager& CHybridModelManager::Instance()
{
    static CHybridModelManager instance;
    return instance;
}

// ============================================================================
// Constructor / Destructor
// ============================================================================
CHybridModelManager::CHybridModelManager()
    : m_preferGLTF(true)  // Varsayılan: glTF varsa onu tercih et
{
}

CHybridModelManager::~CHybridModelManager()
{
    ClearCache();
}

// ============================================================================
// Format Tespiti
// ============================================================================
EModelFormat CHybridModelManager::DetectFormat(const std::string& filePath)
{
    // Uzantıyı al
    size_t dotPos = filePath.rfind('.');
    if (dotPos == std::string::npos)
        return EModelFormat::Unknown;
    
    std::string ext = filePath.substr(dotPos + 1);
    return DetectFormatFromExtension(ext);
}

EModelFormat CHybridModelManager::DetectFormatFromExtension(const std::string& extension)
{
    std::string ext = extension;
    std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
    
    if (ext == "gr2")  return EModelFormat::Granny2;
    if (ext == "gltf") return EModelFormat::GLTF;
    if (ext == "glb")  return EModelFormat::GLB;
    if (ext == "fbx")  return EModelFormat::FBX;
    if (ext == "obj")  return EModelFormat::OBJ;
    
    return EModelFormat::Unknown;
}

// ============================================================================
// glTF Desteği Kontrolü
// ============================================================================
bool CHybridModelManager::IsGLTFSupported()
{
#ifdef USE_ASSIMP
    return true;
#else
    return false;
#endif
}

// ============================================================================
// gr2 -> gltf Yol Dönüşümü
// ============================================================================
std::string CHybridModelManager::GetGLTFPath(const std::string& gr2Path)
{
    // .gr2 uzantısını .gltf ile değiştir
    std::string gltfPath = gr2Path;
    
    size_t dotPos = gltfPath.rfind('.');
    if (dotPos != std::string::npos)
    {
        gltfPath = gltfPath.substr(0, dotPos) + ".gltf";
    }
    else
    {
        gltfPath += ".gltf";
    }
    
    return gltfPath;
}

// ============================================================================
// Model Yolu Çözümleme
// ============================================================================
std::string CHybridModelManager::ResolveModelPath(const std::string& originalPath)
{
    // glTF tercih edilmiyorsa veya desteklenmiyorsa, orijinali döndür
    if (!m_preferGLTF || !IsGLTFSupported())
        return originalPath;
    
    // Format kontrol
    EModelFormat format = DetectFormat(originalPath);
    
    // Zaten glTF ise, doğrudan döndür
    if (format == EModelFormat::GLTF || format == EModelFormat::GLB)
        return originalPath;
    
    // Granny ise, glTF versiyonunu kontrol et
    if (format == EModelFormat::Granny2)
    {
        std::string gltfPath = GetGLTFPath(originalPath);
        
        // glTF dosyası var mı?
        // NOT: Dosya sistemi kontrolü yerine pack sistemi kullanılmalı
        // Şimdilik basit bir dosya kontrolü yapıyoruz
        if (fs::exists(gltfPath))
        {
            return gltfPath;
        }
        
        // GLB versiyonunu da kontrol et
        std::string glbPath = originalPath;
        size_t dotPos = glbPath.rfind('.');
        if (dotPos != std::string::npos)
        {
            glbPath = glbPath.substr(0, dotPos) + ".glb";
            if (fs::exists(glbPath))
            {
                return glbPath;
            }
        }
    }
    
    // glTF bulunamadı, orijinali döndür
    return originalPath;
}

// ============================================================================
// Model Yükleme
// ============================================================================
bool CHybridModelManager::LoadModel(const std::string& filePath)
{
    EModelFormat format = DetectFormat(filePath);
    
    switch (format)
    {
        case EModelFormat::Granny2:
            // Mevcut Granny loader'ı kullanılacak
            // Bu fonksiyon sadece glTF için gerekli
            return true;
            
        case EModelFormat::GLTF:
        case EModelFormat::GLB:
        case EModelFormat::FBX:
        case EModelFormat::OBJ:
        {
#ifdef USE_ASSIMP
            // Cache kontrol
            auto it = m_gltfCache.find(filePath);
            if (it != m_gltfCache.end())
            {
                // Zaten yüklenmiş
                return true;
            }
            
            // Yeni yükle
            auto loader = std::make_unique<GLTF::GLTFModelLoader>();
            if (!loader->Load(filePath))
            {
                // Hata
                return false;
            }
            
            // Cache'e ekle
            auto modelData = std::make_shared<GLTF::ModelData>(loader->GetModelData());
            m_gltfCache[filePath] = modelData;
            
            return true;
#else
            // Assimp desteği yok
            return false;
#endif
        }
            
        default:
            return false;
    }
}

// ============================================================================
// Cache Yönetimi
// ============================================================================
void CHybridModelManager::ClearCache()
{
    m_gltfCache.clear();
}

bool CHybridModelManager::IsCached(const std::string& filePath) const
{
    return m_gltfCache.find(filePath) != m_gltfCache.end();
}

