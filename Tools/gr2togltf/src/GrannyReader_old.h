// ============================================================================
// GrannyReader.h - Granny2 SDK ile .gr2 dosya okuyucu
// ============================================================================
#pragma once

#include "Types.h"
#include <string>
#include <memory>

// Granny SDK forward declarations
struct granny_file;
struct granny_file_info;
struct granny_model;
struct granny_mesh;
struct granny_skeleton;
struct granny_animation;
struct granny_material;

namespace gr2togltf {

class GrannyReader {
public:
    GrannyReader();
    ~GrannyReader();

    // .gr2 dosyasını yükle
    bool Load(const std::string& filePath);
    
    // Yüklenmiş verileri al
    bool ExtractModelData(ModelData& outData, const ConvertOptions& options);
    
    // Dosya bilgisi
    const std::string& GetFilePath() const { return m_filePath; }
    bool IsLoaded() const { return m_file != nullptr; }
    
    // Sayılar
    int GetMeshCount() const;
    int GetModelCount() const;
    int GetSkeletonCount() const;
    int GetAnimationCount() const;
    int GetMaterialCount() const;
    int GetTextureCount() const;

private:
    // İç yardımcı fonksiyonlar
    bool ExtractMesh(granny_mesh* grnMesh, MeshData& outMesh, const ConvertOptions& options);
    bool ExtractSkeleton(granny_skeleton* grnSkeleton, SkeletonData& outSkeleton);
    bool ExtractAnimation(granny_animation* grnAnim, AnimationData& outAnim, const SkeletonData& skeleton);
    bool ExtractMaterial(granny_material* grnMaterial, MaterialData& outMaterial);
    
    // Vertex okuma
    void ReadVertexPositions(granny_mesh* mesh, std::vector<Vertex>& vertices);
    void ReadVertexNormals(granny_mesh* mesh, std::vector<Vertex>& vertices);
    void ReadVertexTexCoords(granny_mesh* mesh, std::vector<Vertex>& vertices, int channel);
    void ReadVertexWeights(granny_mesh* mesh, std::vector<Vertex>& vertices);
    
    // Granny handles
    granny_file* m_file = nullptr;
    granny_file_info* m_fileInfo = nullptr;
    std::string m_filePath;
};

} // namespace gr2togltf
