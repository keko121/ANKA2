// ============================================================================
// GrannyReader.cpp - Granny SDK Dosya Okuyucu (Simplified)
// ============================================================================
// GrannyCopyMeshVertices kullanarak vertex okuma
// ============================================================================

#include "GrannyReader.h"
#include <granny.h>
#include <algorithm>
#include <cstring>

namespace gr2togltf {

// ============================================================================
// Standart Vertex Yapıları (Granny formatına uyumlu)
// ============================================================================
#pragma pack(push, 1)
struct GrannyPNT332 {
    float position[3];
    float normal[3];
    float texCoord[2];
};

struct GrannyPWNT3132 {
    float position[3];
    granny_uint8 boneWeights[4];
    granny_uint8 boneIndices[4];
    float normal[3];
    float texCoord[2];
};
#pragma pack(pop)

// ============================================================================
// Constructor / Destructor
// ============================================================================
GrannyReader::GrannyReader() : m_file(nullptr), m_fileInfo(nullptr) {}

GrannyReader::~GrannyReader() {
    Close();
}

// ============================================================================
// Dosya Açma / Kapama
// ============================================================================
bool GrannyReader::Open(const std::string& filePath) {
    Close();
    
    m_filePath = filePath;
    m_file = GrannyReadEntireFile(filePath.c_str());
    
    if (!m_file) {
        m_lastError = "Dosya açılamadı: " + filePath;
        return false;
    }
    
    m_fileInfo = GrannyGetFileInfo(m_file);
    if (!m_fileInfo) {
        m_lastError = "FileInfo alınamadı";
        Close();
        return false;
    }
    
    return true;
}

void GrannyReader::Close() {
    if (m_file) {
        GrannyFreeFile(m_file);
        m_file = nullptr;
    }
    m_fileInfo = nullptr;
    m_meshes.clear();
    m_bones.clear();
    m_animations.clear();
}

// ============================================================================
// Model Verilerini Oku
// ============================================================================
bool GrannyReader::ReadModel() {
    if (!m_fileInfo) return false;
    
    // Skeleton oku
    ReadSkeleton();
    
    // Mesh'leri oku
    ReadMeshes();
    
    // Animasyonları oku
    ReadAnimations();
    
    return !m_meshes.empty();
}

// ============================================================================
// Skeleton Okuma
// ============================================================================
void GrannyReader::ReadSkeleton() {
    m_bones.clear();
    
    if (!m_fileInfo || m_fileInfo->SkeletonCount == 0) return;
    
    granny_skeleton* skeleton = m_fileInfo->Skeletons[0];
    if (!skeleton) return;
    
    m_bones.reserve(skeleton->BoneCount);
    
    for (int i = 0; i < skeleton->BoneCount; ++i) {
        granny_bone& srcBone = skeleton->Bones[i];
        
        Bone bone;
        bone.name = srcBone.Name ? srcBone.Name : "";
        bone.parentIndex = srcBone.ParentIndex;
        
        // Local transform
        memcpy(bone.localPosition, srcBone.LocalTransform.Position, sizeof(float) * 3);
        memcpy(bone.localRotation, srcBone.LocalTransform.Orientation, sizeof(float) * 4);
        memcpy(bone.localScale, srcBone.LocalTransform.ScaleShear, sizeof(float) * 3);
        
        // Inverse bind matrix
        if (srcBone.InverseWorld4x4) {
            memcpy(bone.inverseBindMatrix, srcBone.InverseWorld4x4, sizeof(float) * 16);
        } else {
            // Identity matrix
            memset(bone.inverseBindMatrix, 0, sizeof(bone.inverseBindMatrix));
            bone.inverseBindMatrix[0] = bone.inverseBindMatrix[5] = 
            bone.inverseBindMatrix[10] = bone.inverseBindMatrix[15] = 1.0f;
        }
        
        m_bones.push_back(bone);
    }
}

// ============================================================================
// Mesh Okuma
// ============================================================================
void GrannyReader::ReadMeshes() {
    m_meshes.clear();
    
    if (!m_fileInfo) return;
    
    // Model'lerdeki mesh'leri oku
    for (int m = 0; m < m_fileInfo->ModelCount; ++m) {
        granny_model* model = m_fileInfo->Models[m];
        if (!model) continue;
        
        for (int i = 0; i < model->MeshBindingCount; ++i) {
            granny_mesh* srcMesh = model->MeshBindings[i].Mesh;
            if (!srcMesh) continue;
            
            ReadSingleMesh(srcMesh);
        }
    }
    
    // Eğer model yoksa direkt mesh'leri oku
    if (m_meshes.empty()) {
        for (int i = 0; i < m_fileInfo->MeshCount; ++i) {
            granny_mesh* srcMesh = m_fileInfo->Meshes[i];
            if (srcMesh) {
                ReadSingleMesh(srcMesh);
            }
        }
    }
}

void GrannyReader::ReadSingleMesh(granny_mesh* srcMesh) {
    if (!srcMesh) return;
    
    Mesh mesh;
    mesh.name = srcMesh->Name ? srcMesh->Name : "mesh";
    
    int vertexCount = GrannyGetMeshVertexCount(srcMesh);
    int indexCount = GrannyGetMeshIndexCount(srcMesh);
    
    if (vertexCount <= 0 || indexCount <= 0) return;
    
    // Vertex'leri oku - GrannyCopyMeshVertices kullan
    mesh.vertices.resize(vertexCount);
    
    // Skinned mi kontrol et
    bool isSkinned = !GrannyMeshIsRigid(srcMesh);
    
    if (isSkinned && m_bones.size() > 0) {
        // Skinned mesh - bone weight'leri ile
        std::vector<GrannyPWNT3132> grannyVerts(vertexCount);
        GrannyCopyMeshVertices(srcMesh, GrannyPWNT3132VertexType, grannyVerts.data());
        
        mesh.boneWeights.resize(vertexCount);
        mesh.boneIndices.resize(vertexCount);
        
        for (int v = 0; v < vertexCount; ++v) {
            mesh.vertices[v].position.x = grannyVerts[v].position[0];
            mesh.vertices[v].position.y = grannyVerts[v].position[1];
            mesh.vertices[v].position.z = grannyVerts[v].position[2];
            
            mesh.vertices[v].normal.x = grannyVerts[v].normal[0];
            mesh.vertices[v].normal.y = grannyVerts[v].normal[1];
            mesh.vertices[v].normal.z = grannyVerts[v].normal[2];
            
            mesh.vertices[v].texCoord.u = grannyVerts[v].texCoord[0];
            mesh.vertices[v].texCoord.v = grannyVerts[v].texCoord[1];
            
            // Bone weights (0-255 -> 0-1)
            for (int j = 0; j < 4; ++j) {
                mesh.boneWeights[v][j] = grannyVerts[v].boneWeights[j] / 255.0f;
                mesh.boneIndices[v][j] = grannyVerts[v].boneIndices[j];
            }
        }
    } else {
        // Static mesh - sadece PNT
        std::vector<GrannyPNT332> grannyVerts(vertexCount);
        GrannyCopyMeshVertices(srcMesh, GrannyPNT332VertexType, grannyVerts.data());
        
        for (int v = 0; v < vertexCount; ++v) {
            mesh.vertices[v].position.x = grannyVerts[v].position[0];
            mesh.vertices[v].position.y = grannyVerts[v].position[1];
            mesh.vertices[v].position.z = grannyVerts[v].position[2];
            
            mesh.vertices[v].normal.x = grannyVerts[v].normal[0];
            mesh.vertices[v].normal.y = grannyVerts[v].normal[1];
            mesh.vertices[v].normal.z = grannyVerts[v].normal[2];
            
            mesh.vertices[v].texCoord.u = grannyVerts[v].texCoord[0];
            mesh.vertices[v].texCoord.v = grannyVerts[v].texCoord[1];
        }
    }
    
    // Index'leri oku
    mesh.indices.resize(indexCount);
    int bytesPerIndex = GrannyGetMeshBytesPerIndex(srcMesh);
    
    if (bytesPerIndex == 2) {
        GrannyCopyMeshIndices(srcMesh, 2, mesh.indices.data());
    } else {
        // 32-bit index -> 16-bit'e dönüştür
        std::vector<uint32_t> indices32(indexCount);
        GrannyCopyMeshIndices(srcMesh, 4, indices32.data());
        for (int i = 0; i < indexCount; ++i) {
            mesh.indices[i] = static_cast<uint16_t>(indices32[i]);
        }
    }
    
    // Material
    if (srcMesh->MaterialBindingCount > 0 && srcMesh->MaterialBindings) {
        granny_material* mat = srcMesh->MaterialBindings[0].Material;
        if (mat && mat->Name) {
            mesh.materialName = mat->Name;
        }
    }
    
    m_meshes.push_back(std::move(mesh));
}

// ============================================================================
// Animasyon Okuma
// ============================================================================
void GrannyReader::ReadAnimations() {
    m_animations.clear();
    
    if (!m_fileInfo) return;
    
    for (int a = 0; a < m_fileInfo->AnimationCount; ++a) {
        granny_animation* srcAnim = m_fileInfo->Animations[a];
        if (!srcAnim) continue;
        
        Animation anim;
        anim.name = srcAnim->Name ? srcAnim->Name : "animation";
        anim.duration = srcAnim->Duration;
        anim.timeStep = srcAnim->TimeStep > 0 ? srcAnim->TimeStep : (1.0f / 30.0f);
        
        // Track gruplarını oku
        for (int tg = 0; tg < srcAnim->TrackGroupCount; ++tg) {
            granny_track_group* trackGroup = srcAnim->TrackGroups[tg];
            if (!trackGroup) continue;
            
            for (int t = 0; t < trackGroup->TransformTrackCount; ++t) {
                granny_transform_track& srcTrack = trackGroup->TransformTracks[t];
                
                AnimationTrackSimple track;
                track.boneName = srcTrack.Name ? srcTrack.Name : "";
                
                // Bone index bul
                track.boneIndex = -1;
                for (size_t b = 0; b < m_bones.size(); ++b) {
                    if (m_bones[b].name == track.boneName) {
                        track.boneIndex = static_cast<int>(b);
                        break;
                    }
                }
                
                // Keyframe'leri al (basitleştirilmiş - sample et)
                int keyCount = static_cast<int>(anim.duration / anim.timeStep) + 1;
                track.positionKeys.resize(keyCount);
                track.rotationKeys.resize(keyCount);
                track.scaleKeys.resize(keyCount);
                
                for (int k = 0; k < keyCount; ++k) {
                    float time = k * anim.timeStep;
                    track.positionKeys[k] = time;
                    track.rotationKeys[k] = time;
                    track.scaleKeys[k] = time;
                }
                
                // TODO: GrannySampleTrackGroup ile gerçek değerleri al
                // Şimdilik keyframe zamanlarını kaydediyoruz
                
                anim.tracks.push_back(std::move(track));
            }
        }
        
        m_animations.push_back(std::move(anim));
    }
}

} // namespace gr2togltf
