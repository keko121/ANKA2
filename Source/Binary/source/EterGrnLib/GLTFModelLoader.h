// ============================================================================
// GLTFModelLoader.h - glTF 2.0 model yükleyici
// ============================================================================
// Assimp kullanarak glTF/GLB dosyalarını yükler ve CGrannyModel uyumlu
// veri yapılarına dönüştürür.
// ============================================================================
// 
// KULLANIM:
// 1. Assimp kütüphanesini kurun (vcpkg veya manuel)
// 2. USE_ASSIMP_LOADER makrosunu tanımlayın
// 3. assimp-vc143-mt.lib ile link edin
// 
// vcpkg ile kurulum:
//   vcpkg install assimp:x86-windows
// 
// BUILD OLMADAN TEST:
//   USE_ASSIMP_LOADER tanımlamayın, stub kod kullanılır
// ============================================================================
#pragma once

// Assimp aktifleştirme makrosu - kurulum sonrası açın
// #define USE_ASSIMP_LOADER

#include <string>
#include <vector>
#include <memory>

#ifdef USE_ASSIMP_LOADER
// Forward declarations for Assimp types
struct aiScene;
struct aiNode;
struct aiMesh;
struct aiMaterial;
struct aiBone;
struct aiAnimation;
#endif

class CGrannyModel;
class CGrannyMesh;

namespace GLTF {

// ============================================================================
// Vertex yapısı (PNT formatı ile uyumlu)
// ============================================================================
struct Vertex {
    float position[3];
    float normal[3];
    float texCoord[2];
};

// ============================================================================
// Skinned Vertex yapısı
// ============================================================================
struct SkinnedVertex {
    float position[3];
    float normal[3];
    float texCoord[2];
    unsigned char boneIndices[4];
    float boneWeights[4];
};

// ============================================================================
// Mesh verisi
// ============================================================================
struct MeshData {
    std::string name;
    std::vector<Vertex> vertices;
    std::vector<unsigned short> indices;
    int materialIndex;
    bool isSkinned;
    
    // Skinning için
    std::vector<SkinnedVertex> skinnedVertices;
};

// ============================================================================
// Bone verisi
// ============================================================================
struct BoneData {
    std::string name;
    int parentIndex;
    float localTransform[16];
    float inverseBindMatrix[16];
};

// ============================================================================
// Animation keyframe
// ============================================================================
struct PositionKey {
    float time;
    float value[3];
};

struct RotationKey {
    float time;
    float value[4]; // quaternion
};

struct ScaleKey {
    float time;
    float value[3];
};

// ============================================================================
// Animation track
// ============================================================================
struct AnimationTrack {
    std::string boneName;
    int boneIndex;
    std::vector<PositionKey> positionKeys;
    std::vector<RotationKey> rotationKeys;
    std::vector<ScaleKey> scaleKeys;
};

// ============================================================================
// Animation verisi
// ============================================================================
struct AnimationData {
    std::string name;
    float duration;
    float ticksPerSecond;
    std::vector<AnimationTrack> tracks;
};

// ============================================================================
// Material verisi
// ============================================================================
struct MaterialData {
    std::string name;
    std::string diffuseTexture;
    float baseColor[4];
    float metallic;
    float roughness;
};

// ============================================================================
// Model verisi (tüm yüklenen veri)
// ============================================================================
struct ModelData {
    std::string name;
    std::vector<MeshData> meshes;
    std::vector<BoneData> bones;
    std::vector<AnimationData> animations;
    std::vector<MaterialData> materials;
    
    int totalVertexCount;
    int totalIndexCount;
    bool hasSkeleton;
};

// ============================================================================
// GLTFModelLoader sınıfı
// ============================================================================
class GLTFModelLoader {
public:
    GLTFModelLoader();
    ~GLTFModelLoader();
    
    // Model yükle
    bool Load(const std::string& filePath);
    bool LoadFromMemory(const void* data, size_t size, const std::string& hint = "gltf");
    
    // Yüklenmiş veriyi al
    const ModelData& GetModelData() const { return m_modelData; }
    
    // Hata mesajı
    const std::string& GetLastError() const { return m_lastError; }
    
    // Yükleme seçenekleri
    void SetFlipUV(bool flip) { m_flipUV = flip; }
    void SetScale(float scale) { m_scale = scale; }
    void SetGenerateNormals(bool gen) { m_generateNormals = gen; }
    
    // Desteklenen formatları kontrol
    static bool IsSupported(const std::string& extension);
    
private:
    // İç fonksiyonlar
    bool ProcessScene(const aiScene* scene);
    void ProcessNode(const aiNode* node, const aiScene* scene, int parentBoneIndex = -1);
    bool ProcessMesh(const aiMesh* mesh, const aiScene* scene);
    bool ProcessMaterial(const aiMaterial* material, int index);
    bool ProcessSkeleton(const aiScene* scene);
    bool ProcessAnimations(const aiScene* scene);
    
    // Yardımcı
    int FindBoneIndex(const std::string& name) const;
    void ExtractBoneWeights(const aiMesh* mesh, MeshData& outMesh);
    
private:
    ModelData m_modelData;
    std::string m_lastError;
    std::string m_basePath;
    
    // Seçenekler
    bool m_flipUV;
    float m_scale;
    bool m_generateNormals;
};

// ============================================================================
// Yardımcı fonksiyonlar
// ============================================================================

// Dosya uzantısına göre format tespiti
bool IsGLTFFile(const std::string& filePath);
bool IsGLBFile(const std::string& filePath);

// glTF mi yoksa Granny mi yüklenecek?
enum class ModelFormat {
    Unknown,
    Granny2,    // .gr2
    GLTF,       // .gltf
    GLB         // .glb
};

ModelFormat DetectModelFormat(const std::string& filePath);

} // namespace GLTF
