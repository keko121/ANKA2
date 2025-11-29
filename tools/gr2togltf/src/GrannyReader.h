// ============================================================================
// GrannyReader.h - Granny2 SDK ile .gr2 dosya okuyucu (Simplified)
// ============================================================================
#pragma once

#include "Types.h"
#include <string>
#include <vector>

// Granny SDK forward declarations
struct granny_file;
struct granny_file_info;
struct granny_mesh;

namespace gr2togltf {

class GrannyReader {
public:
    GrannyReader();
    ~GrannyReader();

    // .gr2 dosyasını aç
    bool Open(const std::string& filePath);
    void Close();
    
    // Model verilerini oku
    bool ReadModel();
    
    // Okunan verilere erişim
    const std::vector<Mesh>& GetMeshes() const { return m_meshes; }
    const std::vector<Bone>& GetBones() const { return m_bones; }
    const std::vector<Animation>& GetAnimations() const { return m_animations; }
    
    // Durum
    bool IsOpen() const { return m_file != nullptr; }
    const std::string& GetLastError() const { return m_lastError; }
    const std::string& GetFilePath() const { return m_filePath; }

private:
    void ReadSkeleton();
    void ReadMeshes();
    void ReadSingleMesh(granny_mesh* srcMesh);
    void ReadAnimations();

    granny_file* m_file;
    granny_file_info* m_fileInfo;
    
    std::string m_filePath;
    std::string m_lastError;
    
    std::vector<Mesh> m_meshes;
    std::vector<Bone> m_bones;
    std::vector<Animation> m_animations;
};

} // namespace gr2togltf
