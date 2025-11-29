// ============================================================================
// Converter.cpp - GrannyReader + GLTFWriter birleştirici (Simplified)
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

// ModelData'yı GrannyReader'dan doldur
static void FillModelData(const GrannyReader& reader, ModelData& modelData) {
    const auto& meshes = reader.GetMeshes();
    const auto& bones = reader.GetBones();
    const auto& anims = reader.GetAnimations();
    
    // Meshes
    for (const auto& src : meshes) {
        MeshData mesh;
        mesh.name = src.name;
        mesh.hasSkinning = !src.boneWeights.empty();
        
        // Vertices
        mesh.vertices.reserve(src.vertices.size());
        for (size_t i = 0; i < src.vertices.size(); ++i) {
            Vertex v;
            v.position = src.vertices[i].position;
            v.normal = src.vertices[i].normal;
            v.texCoord0 = Vec2(src.vertices[i].texCoord.u, src.vertices[i].texCoord.v);
            
            if (mesh.hasSkinning && i < src.boneWeights.size()) {
                for (int j = 0; j < 4; ++j) {
                    v.joints[j] = src.boneIndices[i][j];
                    v.weights[j] = src.boneWeights[i][j];
                }
            }
            mesh.vertices.push_back(v);
        }
        
        // Indices
        mesh.indices.reserve(src.indices.size());
        for (uint16_t idx : src.indices) {
            mesh.indices.push_back(static_cast<uint32_t>(idx));
        }
        
        modelData.meshes.push_back(std::move(mesh));
    }
    
    // Skeleton
    for (const auto& src : bones) {
        BoneData bone;
        bone.name = src.name;
        bone.parentIndex = src.parentIndex;
        bone.position = Vec3(src.localPosition[0], src.localPosition[1], src.localPosition[2]);
        bone.rotation = Quat(src.localRotation[0], src.localRotation[1], src.localRotation[2], src.localRotation[3]);
        bone.scale = Vec3(src.localScale[0], src.localScale[1], src.localScale[2]);
        
        for (int i = 0; i < 16; ++i) {
            bone.inverseBindMatrix.m[i] = src.inverseBindMatrix[i];
        }
        
        modelData.skeleton.bones.push_back(std::move(bone));
    }
    
    // Animations
    for (const auto& src : anims) {
        AnimationData anim;
        anim.name = src.name;
        anim.duration = src.duration;
        
        for (const auto& srcTrack : src.tracks) {
            gr2togltf::AnimationTrack track;  // Use full namespace
            track.boneName = srcTrack.boneName;
            track.boneIndex = srcTrack.boneIndex;
            // TODO: Keyframe data
            anim.tracks.push_back(std::move(track));
        }
        
        modelData.animations.push_back(std::move(anim));
    }
    
    modelData.isRigid = bones.empty();
}

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
    if (!reader.Open(inputPath)) {
        m_lastError = "GR2 dosyasi acilamadi: " + reader.GetLastError();
        m_failCount++;
        return false;
    }
    
    if (!reader.ReadModel()) {
        m_lastError = "Model okunamadi: " + reader.GetLastError();
        m_failCount++;
        return false;
    }
    
    // 2. ModelData'ya dönüştür
    ModelData modelData;
    modelData.sourceFile = inputPath;
    FillModelData(reader, modelData);
    
    if (modelData.meshes.empty()) {
        m_lastError = "Mesh bulunamadi: " + inputPath;
        m_failCount++;
        return false;
    }
    
    // 3. Çıktı yolunu hazırla
    std::string finalOutput = outputPath;
    if (finalOutput.empty()) {
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
    
    std::cout << "Donusum basarili: " << finalOutput << std::endl;
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
    
    int convertedCount = 0;
    for (const auto& entry : fs::recursive_directory_iterator(inputDir)) {
        if (!entry.is_regular_file()) continue;
        std::string ext = entry.path().extension().string();
        std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
        if (ext != ".gr2") continue;
            fs::path outPath = entry.path();
            outPath.replace_extension(options.outputFormat == "glb" ? ".glb" : ".gltf");
            if (Convert(entry.path().string(), outPath.string(), options)) {
                convertedCount++;
            }
    }
    return convertedCount;
}

} // namespace gr2togltf
