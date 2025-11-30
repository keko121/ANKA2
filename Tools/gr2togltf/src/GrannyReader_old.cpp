// ============================================================================
// GrannyReader.cpp - Granny2 SDK ile .gr2 dosya okuyucu implementasyonu
// ============================================================================

#include "GrannyReader.h"
#include <granny.h>
#include <iostream>
#include <cstring>

namespace gr2togltf {

// ============================================================================
// Constructor / Destructor
// ============================================================================
GrannyReader::GrannyReader() = default;

GrannyReader::~GrannyReader() {
    if (m_file) {
        GrannyFreeFile(m_file);
        m_file = nullptr;
        m_fileInfo = nullptr;
    }
}

// ============================================================================
// Dosya Yükleme
// ============================================================================
bool GrannyReader::Load(const std::string& filePath) {
    // Önceki dosyayı temizle
    if (m_file) {
        GrannyFreeFile(m_file);
        m_file = nullptr;
        m_fileInfo = nullptr;
    }
    
    m_filePath = filePath;
    
    // Granny dosyasını oku
    m_file = GrannyReadEntireFile(filePath.c_str());
    if (!m_file) {
        std::cerr << "HATA: Dosya okunamadi: " << filePath << std::endl;
        return false;
    }
    
    // File info al
    m_fileInfo = GrannyGetFileInfo(m_file);
    if (!m_fileInfo) {
        std::cerr << "HATA: FileInfo alinamadi: " << filePath << std::endl;
        GrannyFreeFile(m_file);
        m_file = nullptr;
        return false;
    }
    
    std::cout << "Dosya yuklendi: " << filePath << std::endl;
    std::cout << "  Mesh sayisi: " << GetMeshCount() << std::endl;
    std::cout << "  Model sayisi: " << GetModelCount() << std::endl;
    std::cout << "  Skeleton sayisi: " << GetSkeletonCount() << std::endl;
    std::cout << "  Animasyon sayisi: " << GetAnimationCount() << std::endl;
    std::cout << "  Material sayisi: " << GetMaterialCount() << std::endl;
    
    return true;
}

// ============================================================================
// Sayılar
// ============================================================================
int GrannyReader::GetMeshCount() const {
    return m_fileInfo ? m_fileInfo->MeshCount : 0;
}

int GrannyReader::GetModelCount() const {
    return m_fileInfo ? m_fileInfo->ModelCount : 0;
}

int GrannyReader::GetSkeletonCount() const {
    return m_fileInfo ? m_fileInfo->SkeletonCount : 0;
}

int GrannyReader::GetAnimationCount() const {
    return m_fileInfo ? m_fileInfo->AnimationCount : 0;
}

int GrannyReader::GetMaterialCount() const {
    return m_fileInfo ? m_fileInfo->MaterialCount : 0;
}

int GrannyReader::GetTextureCount() const {
    return m_fileInfo ? m_fileInfo->TextureCount : 0;
}

// ============================================================================
// Model Verisi Çıkart
// ============================================================================
bool GrannyReader::ExtractModelData(ModelData& outData, const ConvertOptions& options) {
    if (!m_fileInfo) return false;
    
    outData.sourceFile = m_filePath;
    
    // İsim belirle
    if (m_fileInfo->FromFileName) {
        outData.name = m_fileInfo->FromFileName;
    } else {
        // Dosya adından al
        size_t lastSlash = m_filePath.find_last_of("/\\");
        size_t lastDot = m_filePath.find_last_of('.');
        if (lastSlash != std::string::npos) {
            outData.name = m_filePath.substr(lastSlash + 1, lastDot - lastSlash - 1);
        } else {
            outData.name = m_filePath.substr(0, lastDot);
        }
    }
    
    // =========================================================================
    // Materials
    // =========================================================================
    if (options.exportMaterials) {
        for (int i = 0; i < m_fileInfo->MaterialCount; ++i) {
            MaterialData matData;
            if (ExtractMaterial(m_fileInfo->Materials[i], matData)) {
                outData.materials.push_back(std::move(matData));
            }
        }
    }
    
    // =========================================================================
    // Skeleton (ilk skeleton'u kullan)
    // =========================================================================
    if (m_fileInfo->SkeletonCount > 0) {
        if (ExtractSkeleton(m_fileInfo->Skeletons[0], outData.skeleton)) {
            outData.isRigid = false;
        }
    }
    
    // =========================================================================
    // Meshes
    // =========================================================================
    for (int i = 0; i < m_fileInfo->MeshCount; ++i) {
        MeshData meshData;
        if (ExtractMesh(m_fileInfo->Meshes[i], meshData, options)) {
            outData.totalVertexCount += static_cast<int>(meshData.vertices.size());
            outData.totalIndexCount += static_cast<int>(meshData.indices.size());
            outData.meshes.push_back(std::move(meshData));
        }
    }
    
    // =========================================================================
    // Animations
    // =========================================================================
    if (options.exportAnimations) {
        for (int i = 0; i < m_fileInfo->AnimationCount; ++i) {
            AnimationData animData;
            if (ExtractAnimation(m_fileInfo->Animations[i], animData, outData.skeleton)) {
                outData.animations.push_back(std::move(animData));
            }
        }
    }
    
    std::cout << "Model verisi cikarildi:" << std::endl;
    std::cout << "  Ad: " << outData.name << std::endl;
    std::cout << "  Mesh: " << outData.meshes.size() << std::endl;
    std::cout << "  Material: " << outData.materials.size() << std::endl;
    std::cout << "  Bone: " << outData.skeleton.bones.size() << std::endl;
    std::cout << "  Animasyon: " << outData.animations.size() << std::endl;
    
    return !outData.meshes.empty();
}

// ============================================================================
// Mesh Çıkart
// ============================================================================
bool GrannyReader::ExtractMesh(granny_mesh* grnMesh, MeshData& outMesh, const ConvertOptions& options) {
    if (!grnMesh) return false;
    
    // İsim
    outMesh.name = grnMesh->Name ? grnMesh->Name : "unnamed_mesh";
    
    // Vertex sayısı
    int vertexCount = GrannyGetMeshVertexCount(grnMesh);
    if (vertexCount <= 0) return false;
    
    outMesh.vertices.resize(vertexCount);
    
    // =========================================================================
    // Vertex Verilerini Oku
    // =========================================================================
    ReadVertexPositions(grnMesh, outMesh.vertices);
    ReadVertexNormals(grnMesh, outMesh.vertices);
    ReadVertexTexCoords(grnMesh, outMesh.vertices, 0);
    ReadVertexTexCoords(grnMesh, outMesh.vertices, 1);
    
    // Skinning verileri
    if (!GrannyMeshIsRigid(grnMesh)) {
        ReadVertexWeights(grnMesh, outMesh.vertices);
        outMesh.hasSkinning = true;
    }
    
    // =========================================================================
    // Scale faktörü uygula
    // =========================================================================
    if (options.scaleFactor != 1.0f) {
        for (auto& v : outMesh.vertices) {
            v.position.x *= options.scaleFactor;
            v.position.y *= options.scaleFactor;
            v.position.z *= options.scaleFactor;
        }
    }
    
    // =========================================================================
    // UV flip
    // =========================================================================
    if (options.flipUV) {
        for (auto& v : outMesh.vertices) {
            v.texCoord0.y = 1.0f - v.texCoord0.y;
            v.texCoord1.y = 1.0f - v.texCoord1.y;
        }
    }
    
    // =========================================================================
    // Index Verilerini Oku
    // =========================================================================
    int indexCount = GrannyGetMeshIndexCount(grnMesh);
    if (indexCount > 0) {
        outMesh.indices.resize(indexCount);
        GrannyCopyMeshIndices(grnMesh, sizeof(uint32_t), outMesh.indices.data());
        
        // Winding order flip
        if (options.flipWindingOrder) {
            for (size_t i = 0; i + 2 < outMesh.indices.size(); i += 3) {
                std::swap(outMesh.indices[i + 1], outMesh.indices[i + 2]);
            }
        }
    }
    
    // =========================================================================
    // Material binding
    // =========================================================================
    if (grnMesh->MaterialBindingCount > 0 && grnMesh->MaterialBindings) {
        // İlk material'ı kullan (basitlik için)
        // TODO: Multi-material desteği
        granny_material* mat = grnMesh->MaterialBindings[0].Material;
        if (mat && m_fileInfo) {
            for (int i = 0; i < m_fileInfo->MaterialCount; ++i) {
                if (m_fileInfo->Materials[i] == mat) {
                    outMesh.materialIndex = i;
                    break;
                }
            }
        }
    }
    
    std::cout << "  Mesh: " << outMesh.name 
              << " (vtx:" << outMesh.vertices.size() 
              << ", idx:" << outMesh.indices.size() 
              << ", skinned:" << (outMesh.hasSkinning ? "yes" : "no") << ")" << std::endl;
    
    return true;
}

// ============================================================================
// Vertex Position Oku
// ============================================================================
void GrannyReader::ReadVertexPositions(granny_mesh* mesh, std::vector<Vertex>& vertices) {
    granny_data_type_definition* vertexType = GrannyGetMeshVertexType(mesh);
    void* vertexData = GrannyGetMeshVertices(mesh);
    int vertexCount = static_cast<int>(vertices.size());
    
    // Position offset bul
    int posOffset = GrannyGetMemberOffset(vertexType, GrannyVertexPositionName);
    if (posOffset < 0) return;
    
    int vertexSize = GrannyGetTotalObjectSize(vertexType);
    uint8_t* data = static_cast<uint8_t*>(vertexData);
    
    for (int i = 0; i < vertexCount; ++i) {
        float* pos = reinterpret_cast<float*>(data + i * vertexSize + posOffset);
        vertices[i].position.x = pos[0];
        vertices[i].position.y = pos[1];
        vertices[i].position.z = pos[2];
    }
}

// ============================================================================
// Vertex Normal Oku
// ============================================================================
void GrannyReader::ReadVertexNormals(granny_mesh* mesh, std::vector<Vertex>& vertices) {
    granny_data_type_definition* vertexType = GrannyGetMeshVertexType(mesh);
    void* vertexData = GrannyGetMeshVertices(mesh);
    int vertexCount = static_cast<int>(vertices.size());
    
    int normOffset = GrannyGetMemberOffset(vertexType, GrannyVertexNormalName);
    if (normOffset < 0) return;
    
    int vertexSize = GrannyGetTotalObjectSize(vertexType);
    uint8_t* data = static_cast<uint8_t*>(vertexData);
    
    for (int i = 0; i < vertexCount; ++i) {
        float* norm = reinterpret_cast<float*>(data + i * vertexSize + normOffset);
        vertices[i].normal.x = norm[0];
        vertices[i].normal.y = norm[1];
        vertices[i].normal.z = norm[2];
    }
}

// ============================================================================
// Vertex TexCoord Oku
// ============================================================================
void GrannyReader::ReadVertexTexCoords(granny_mesh* mesh, std::vector<Vertex>& vertices, int channel) {
    granny_data_type_definition* vertexType = GrannyGetMeshVertexType(mesh);
    void* vertexData = GrannyGetMeshVertices(mesh);
    int vertexCount = static_cast<int>(vertices.size());
    
    // TextureCoordinates0, TextureCoordinates1 etc.
    char tcName[64];
    snprintf(tcName, sizeof(tcName), "%s%d", GrannyVertexTextureCoordinatesName, channel);
    
    int tcOffset = GrannyGetMemberOffset(vertexType, tcName);
    if (tcOffset < 0) return;
    
    int vertexSize = GrannyGetTotalObjectSize(vertexType);
    uint8_t* data = static_cast<uint8_t*>(vertexData);
    
    for (int i = 0; i < vertexCount; ++i) {
        float* tc = reinterpret_cast<float*>(data + i * vertexSize + tcOffset);
        if (channel == 0) {
            vertices[i].texCoord0.x = tc[0];
            vertices[i].texCoord0.y = tc[1];
        } else {
            vertices[i].texCoord1.x = tc[0];
            vertices[i].texCoord1.y = tc[1];
        }
    }
}

// ============================================================================
// Vertex Weights Oku (Skinning)
// ============================================================================
void GrannyReader::ReadVertexWeights(granny_mesh* mesh, std::vector<Vertex>& vertices) {
    granny_data_type_definition* vertexType = GrannyGetMeshVertexType(mesh);
    void* vertexData = GrannyGetMeshVertices(mesh);
    int vertexCount = static_cast<int>(vertices.size());
    
    // BoneWeights ve BoneIndices offset'leri
    int weightOffset = GrannyGetMemberOffset(vertexType, GrannyVertexBoneWeightsName);
    int indexOffset = GrannyGetMemberOffset(vertexType, GrannyVertexBoneIndicesName);
    
    if (weightOffset < 0 || indexOffset < 0) return;
    
    int vertexSize = GrannyGetTotalObjectSize(vertexType);
    uint8_t* data = static_cast<uint8_t*>(vertexData);
    
    for (int i = 0; i < vertexCount; ++i) {
        // Weights (genellikle 4 tane, uint8 normalized veya float)
        uint8_t* weights = data + i * vertexSize + weightOffset;
        uint8_t* indices = data + i * vertexSize + indexOffset;
        
        // Granny genellikle uint8 kullanır, normalize edelim
        for (int j = 0; j < 4; ++j) {
            vertices[i].weights[j] = weights[j] / 255.0f;
            vertices[i].joints[j] = indices[j];
        }
    }
}

// ============================================================================
// Skeleton Çıkart
// ============================================================================
bool GrannyReader::ExtractSkeleton(granny_skeleton* grnSkeleton, SkeletonData& outSkeleton) {
    if (!grnSkeleton || grnSkeleton->BoneCount <= 0) return false;
    
    outSkeleton.name = grnSkeleton->Name ? grnSkeleton->Name : "skeleton";
    outSkeleton.bones.resize(grnSkeleton->BoneCount);
    
    for (int i = 0; i < grnSkeleton->BoneCount; ++i) {
        granny_bone* bone = &grnSkeleton->Bones[i];
        BoneData& outBone = outSkeleton.bones[i];
        
        outBone.name = bone->Name ? bone->Name : ("bone_" + std::to_string(i));
        outBone.parentIndex = bone->ParentIndex;
        
        // Transform
        granny_transform& lt = bone->LocalTransform;
        
        // Position
        outBone.position.x = lt.Position[0];
        outBone.position.y = lt.Position[1];
        outBone.position.z = lt.Position[2];
        
        // Rotation (Granny quaternion: x,y,z,w)
        outBone.rotation.x = lt.Orientation[0];
        outBone.rotation.y = lt.Orientation[1];
        outBone.rotation.z = lt.Orientation[2];
        outBone.rotation.w = lt.Orientation[3];
        
        // Scale
        outBone.scale.x = lt.ScaleShear[0][0];
        outBone.scale.y = lt.ScaleShear[1][1];
        outBone.scale.z = lt.ScaleShear[2][2];
        
        // Inverse Bind Matrix
        for (int r = 0; r < 4; ++r) {
            for (int c = 0; c < 4; ++c) {
                outBone.inverseBindMatrix.m[r * 4 + c] = bone->InverseWorld4x4[r][c];
            }
        }
    }
    
    std::cout << "  Skeleton: " << outSkeleton.name 
              << " (" << outSkeleton.bones.size() << " bones)" << std::endl;
    
    return true;
}

// ============================================================================
// Animation Çıkart
// ============================================================================
bool GrannyReader::ExtractAnimation(granny_animation* grnAnim, AnimationData& outAnim, const SkeletonData& skeleton) {
    if (!grnAnim) return false;
    
    outAnim.name = grnAnim->Name ? grnAnim->Name : "animation";
    outAnim.duration = grnAnim->Duration;
    
    // Track groups'u işle
    for (int tg = 0; tg < grnAnim->TrackGroupCount; ++tg) {
        granny_track_group* trackGroup = grnAnim->TrackGroups[tg];
        if (!trackGroup) continue;
        
        for (int t = 0; t < trackGroup->TransformTrackCount; ++t) {
            granny_transform_track* track = &trackGroup->TransformTracks[t];
            if (!track || !track->Name) continue;
            
            AnimationTrack animTrack;
            animTrack.boneName = track->Name;
            
            // Bone index bul
            for (size_t b = 0; b < skeleton.bones.size(); ++b) {
                if (skeleton.bones[b].name == animTrack.boneName) {
                    animTrack.boneIndex = static_cast<int>(b);
                    break;
                }
            }
            
            // Keyframe'leri sample et
            // Granny curve sistemini kullanarak keyframe'leri çıkart
            int sampleCount = static_cast<int>(outAnim.duration * 30.0f); // 30 FPS
            if (sampleCount < 2) sampleCount = 2;
            
            for (int s = 0; s < sampleCount; ++s) {
                float time = (outAnim.duration * s) / (sampleCount - 1);
                
                granny_transform result;
                GrannySampleTrackGroup(
                    trackGroup,
                    0,      // track index
                    time,
                    &result,
                    nullptr  // model instance
                );
                
                // Position key
                KeyframeVec3 posKey;
                posKey.time = time;
                posKey.value.x = result.Position[0];
                posKey.value.y = result.Position[1];
                posKey.value.z = result.Position[2];
                animTrack.positionKeys.push_back(posKey);
                
                // Rotation key
                KeyframeQuat rotKey;
                rotKey.time = time;
                rotKey.value.x = result.Orientation[0];
                rotKey.value.y = result.Orientation[1];
                rotKey.value.z = result.Orientation[2];
                rotKey.value.w = result.Orientation[3];
                animTrack.rotationKeys.push_back(rotKey);
                
                // Scale key
                KeyframeVec3 scaleKey;
                scaleKey.time = time;
                scaleKey.value.x = result.ScaleShear[0][0];
                scaleKey.value.y = result.ScaleShear[1][1];
                scaleKey.value.z = result.ScaleShear[2][2];
                animTrack.scaleKeys.push_back(scaleKey);
            }
            
            if (!animTrack.positionKeys.empty()) {
                outAnim.tracks.push_back(std::move(animTrack));
            }
        }
    }
    
    std::cout << "  Animation: " << outAnim.name 
              << " (dur:" << outAnim.duration << "s, tracks:" << outAnim.tracks.size() << ")" << std::endl;
    
    return !outAnim.tracks.empty();
}

// ============================================================================
// Material Çıkart
// ============================================================================
bool GrannyReader::ExtractMaterial(granny_material* grnMaterial, MaterialData& outMaterial) {
    if (!grnMaterial) return false;
    
    outMaterial.name = grnMaterial->Name ? grnMaterial->Name : "material";
    
    // Texture bul (Maps array'inden)
    if (grnMaterial->MapCount > 0 && grnMaterial->Maps) {
        granny_material_map* map = &grnMaterial->Maps[0];
        if (map->Material && map->Material->Texture) {
            granny_texture* tex = map->Material->Texture;
            if (tex->FromFileName) {
                outMaterial.diffuseTexture = tex->FromFileName;
            }
        }
    }
    
    // Extended data'dan renk al (varsa)
    // Granny extended data sistemi karmaşık, basit tutuyoruz
    outMaterial.baseColor = Vec4(1, 1, 1, 1);
    outMaterial.metallic = 0.0f;
    outMaterial.roughness = 0.8f;
    
    std::cout << "  Material: " << outMaterial.name;
    if (!outMaterial.diffuseTexture.empty()) {
        std::cout << " (tex: " << outMaterial.diffuseTexture << ")";
    }
    std::cout << std::endl;
    
    return true;
}

} // namespace gr2togltf
