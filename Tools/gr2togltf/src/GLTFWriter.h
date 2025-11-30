// ============================================================================
// GLTFWriter.h - glTF 2.0 dosya yazıcı
// ============================================================================
#pragma once

#include "Types.h"
#include <string>
#include <memory>

namespace gr2togltf {

class GLTFWriter {
public:
    GLTFWriter();
    ~GLTFWriter();

    // Model verisini glTF olarak kaydet
    bool Write(const ModelData& model, const std::string& outputPath, const ConvertOptions& options);
    
    // Format seçimi
    bool WriteGLTF(const ModelData& model, const std::string& outputPath);  // .gltf + .bin
    bool WriteGLB(const ModelData& model, const std::string& outputPath);   // tek .glb dosyası

private:
    // tinygltf model oluşturma
    void BuildScene(const ModelData& model);
    void BuildMeshes(const ModelData& model);
    void BuildMaterials(const ModelData& model);
    void BuildSkeleton(const ModelData& model);
    void BuildAnimations(const ModelData& model);
    
    // Buffer yönetimi
    void CreateBuffers();
    int AddBuffer(const void* data, size_t size, int target);
    int AddAccessor(int bufferView, int componentType, int count, const std::string& type);
    
    // İç veri
    struct Impl;
    std::unique_ptr<Impl> m_impl;
};

} // namespace gr2togltf
