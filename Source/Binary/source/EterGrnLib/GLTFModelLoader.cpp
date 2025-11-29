// ============================================================================
// GLTFModelLoader.cpp - glTF 2.0 model yükleyici implementasyonu
// ============================================================================
// 
// BUILD REQUIREMENTS:
// - USE_ASSIMP_LOADER makrosu tanımlanmalı
// - assimp-vc143-mt.lib ile link edilmeli
// - Assimp DLL runtime'da bulunmalı
// 
// Assimp olmadan bu dosya stub implementasyon kullanır.
// ============================================================================

#include "GLTFModelLoader.h"

#ifdef USE_ASSIMP_LOADER
// Assimp headers (sadece USE_ASSIMP_LOADER tanımlıysa)
#include <assimp/Importer.hpp>
#include <assimp/scene.h>
#include <assimp/postprocess.h>
#include <assimp/GltfMaterial.h>
#endif

#include <algorithm>
#include <filesystem>

namespace GLTF {

// ============================================================================
// Constructor / Destructor
// ============================================================================
GLTFModelLoader::GLTFModelLoader()
    : m_flipUV(true)
    , m_scale(1.0f)
    , m_generateNormals(true)
{
}

GLTFModelLoader::~GLTFModelLoader() = default;

// ============================================================================
// Format Tespiti
// ============================================================================
bool IsGLTFFile(const std::string& filePath) {
    std::string ext = filePath.substr(filePath.find_last_of('.') + 1);
    std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
    return ext == "gltf";
}

bool IsGLBFile(const std::string& filePath) {
    std::string ext = filePath.substr(filePath.find_last_of('.') + 1);
    std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
    return ext == "glb";
}

ModelFormat DetectModelFormat(const std::string& filePath) {
    std::string ext = filePath.substr(filePath.find_last_of('.') + 1);
    std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
    
    if (ext == "gr2") return ModelFormat::Granny2;
    if (ext == "gltf") return ModelFormat::GLTF;
    if (ext == "glb") return ModelFormat::GLB;
    
    return ModelFormat::Unknown;
}

bool GLTFModelLoader::IsSupported(const std::string& extension) {
    std::string ext = extension;
    std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
    
    // Desteklenen formatlar
    return ext == "gltf" || ext == "glb" || 
           ext == "fbx" || ext == "obj" ||
           ext == "dae" || ext == "3ds";
}

// ============================================================================
// Model Yükleme
// ============================================================================
bool GLTFModelLoader::Load(const std::string& filePath) {
#ifndef USE_ASSIMP_LOADER
    m_lastError = "Assimp desteği etkin değil. USE_ASSIMP_LOADER tanımlayın.";
    return false;
#else
    m_lastError.clear();
    m_modelData = ModelData();
    
    // Base path al (texture'lar için)
    std::filesystem::path p(filePath);
    m_basePath = p.parent_path().string();
    if (!m_basePath.empty() && m_basePath.back() != '/' && m_basePath.back() != '\\') {
        m_basePath += '/';
    }
    
    // Model adı
    m_modelData.name = p.stem().string();
    
    // Assimp importer
    Assimp::Importer importer;
    
    // Post-process flags
    unsigned int flags = 
        aiProcess_Triangulate |           // Tüm primitive'leri üçgene çevir
        aiProcess_JoinIdenticalVertices | // Aynı vertex'leri birleştir
        aiProcess_SortByPType |           // Primitive type'a göre sırala
        aiProcess_LimitBoneWeights |      // Max 4 bone per vertex
        aiProcess_ValidateDataStructure;  // Veri yapısını doğrula
    
    if (m_generateNormals) {
        flags |= aiProcess_GenSmoothNormals;
    }
    
    if (m_flipUV) {
        flags |= aiProcess_FlipUVs;
    }
    
    // Dosyayı yükle
    const aiScene* scene = importer.ReadFile(filePath, flags);
    
    if (!scene || (scene->mFlags & AI_SCENE_FLAGS_INCOMPLETE) || !scene->mRootNode) {
        m_lastError = "Assimp hatası: " + std::string(importer.GetErrorString());
        return false;
    }
    
    // Scene'i işle
    return ProcessScene(scene);
#endif
}

bool GLTFModelLoader::LoadFromMemory(const void* data, size_t size, const std::string& hint) {
#ifndef USE_ASSIMP_LOADER
    m_lastError = "Assimp desteği etkin değil. USE_ASSIMP_LOADER tanımlayın.";
    return false;
#else
    m_lastError.clear();
    m_modelData = ModelData();
    
    Assimp::Importer importer;
    
    unsigned int flags = 
        aiProcess_Triangulate |
        aiProcess_JoinIdenticalVertices |
        aiProcess_LimitBoneWeights;
    
    if (m_generateNormals) {
        flags |= aiProcess_GenSmoothNormals;
    }
    
    if (m_flipUV) {
        flags |= aiProcess_FlipUVs;
    }
    
    const aiScene* scene = importer.ReadFileFromMemory(
        data, size, flags, hint.c_str()
    );
    
    if (!scene || !scene->mRootNode) {
        m_lastError = "Assimp hatası: " + std::string(importer.GetErrorString());
        return false;
    }
    
    return ProcessScene(scene);
#endif
}

// ============================================================================
// Scene İşleme
// ============================================================================
#ifdef USE_ASSIMP_LOADER
bool GLTFModelLoader::ProcessScene(const aiScene* scene) {
    // Materials
    for (unsigned int i = 0; i < scene->mNumMaterials; ++i) {
        ProcessMaterial(scene->mMaterials[i], i);
    }
    
    // Skeleton (bones)
    ProcessSkeleton(scene);
    
    // Node ağacını işle (mesh'leri topla)
    ProcessNode(scene->mRootNode, scene);
    
    // Animations
    ProcessAnimations(scene);
    
    // Toplam sayıları hesapla
    m_modelData.totalVertexCount = 0;
    m_modelData.totalIndexCount = 0;
    for (const auto& mesh : m_modelData.meshes) {
        m_modelData.totalVertexCount += static_cast<int>(mesh.vertices.size());
        m_modelData.totalIndexCount += static_cast<int>(mesh.indices.size());
    }
    
    m_modelData.hasSkeleton = !m_modelData.bones.empty();
    
    return !m_modelData.meshes.empty();
}

void GLTFModelLoader::ProcessNode(const aiNode* node, const aiScene* scene, int parentBoneIndex) {
    // Node'un mesh'lerini işle
    for (unsigned int i = 0; i < node->mNumMeshes; ++i) {
        aiMesh* mesh = scene->mMeshes[node->mMeshes[i]];
        ProcessMesh(mesh, scene);
    }
    
    // Alt node'ları işle
    for (unsigned int i = 0; i < node->mNumChildren; ++i) {
        ProcessNode(node->mChildren[i], scene, parentBoneIndex);
    }
}

bool GLTFModelLoader::ProcessMesh(const aiMesh* mesh, const aiScene* scene) {
    MeshData meshData;
    meshData.name = mesh->mName.C_Str();
    meshData.materialIndex = mesh->mMaterialIndex;
    meshData.isSkinned = mesh->HasBones();
    
    // Vertex'leri oku
    meshData.vertices.reserve(mesh->mNumVertices);
    
    for (unsigned int i = 0; i < mesh->mNumVertices; ++i) {
        Vertex v;
        
        // Position
        v.position[0] = mesh->mVertices[i].x * m_scale;
        v.position[1] = mesh->mVertices[i].y * m_scale;
        v.position[2] = mesh->mVertices[i].z * m_scale;
        
        // Normal
        if (mesh->HasNormals()) {
            v.normal[0] = mesh->mNormals[i].x;
            v.normal[1] = mesh->mNormals[i].y;
            v.normal[2] = mesh->mNormals[i].z;
        } else {
            v.normal[0] = 0.0f;
            v.normal[1] = 1.0f;
            v.normal[2] = 0.0f;
        }
        
        // TexCoord
        if (mesh->HasTextureCoords(0)) {
            v.texCoord[0] = mesh->mTextureCoords[0][i].x;
            v.texCoord[1] = mesh->mTextureCoords[0][i].y;
        } else {
            v.texCoord[0] = 0.0f;
            v.texCoord[1] = 0.0f;
        }
        
        meshData.vertices.push_back(v);
    }
    
    // Index'leri oku
    for (unsigned int i = 0; i < mesh->mNumFaces; ++i) {
        const aiFace& face = mesh->mFaces[i];
        
        // Sadece triangles
        if (face.mNumIndices == 3) {
            for (unsigned int j = 0; j < 3; ++j) {
                if (face.mIndices[j] < 65536) {
                    meshData.indices.push_back(static_cast<unsigned short>(face.mIndices[j]));
                }
            }
        }
    }
    
    // Bone weights (skinning için)
    if (meshData.isSkinned) {
        ExtractBoneWeights(mesh, meshData);
    }
    
    m_modelData.meshes.push_back(std::move(meshData));
    return true;
}

bool GLTFModelLoader::ProcessMaterial(const aiMaterial* material, int index) {
    MaterialData matData;
    
    // İsim
    aiString name;
    if (material->Get(AI_MATKEY_NAME, name) == AI_SUCCESS) {
        matData.name = name.C_Str();
    } else {
        matData.name = "material_" + std::to_string(index);
    }
    
    // Diffuse texture
    if (material->GetTextureCount(aiTextureType_DIFFUSE) > 0) {
        aiString texPath;
        if (material->GetTexture(aiTextureType_DIFFUSE, 0, &texPath) == AI_SUCCESS) {
            matData.diffuseTexture = m_basePath + texPath.C_Str();
        }
    }
    
    // Base Color Texture (PBR)
    if (matData.diffuseTexture.empty() && material->GetTextureCount(aiTextureType_BASE_COLOR) > 0) {
        aiString texPath;
        if (material->GetTexture(aiTextureType_BASE_COLOR, 0, &texPath) == AI_SUCCESS) {
            matData.diffuseTexture = m_basePath + texPath.C_Str();
        }
    }
    
    // Base color
    aiColor4D color;
    if (material->Get(AI_MATKEY_COLOR_DIFFUSE, color) == AI_SUCCESS) {
        matData.baseColor[0] = color.r;
        matData.baseColor[1] = color.g;
        matData.baseColor[2] = color.b;
        matData.baseColor[3] = color.a;
    } else {
        matData.baseColor[0] = 1.0f;
        matData.baseColor[1] = 1.0f;
        matData.baseColor[2] = 1.0f;
        matData.baseColor[3] = 1.0f;
    }
    
    // PBR properties
    float metallic = 0.0f;
    float roughness = 0.8f;
    material->Get(AI_MATKEY_METALLIC_FACTOR, metallic);
    material->Get(AI_MATKEY_ROUGHNESS_FACTOR, roughness);
    matData.metallic = metallic;
    matData.roughness = roughness;
    
    m_modelData.materials.push_back(std::move(matData));
    return true;
}

bool GLTFModelLoader::ProcessSkeleton(const aiScene* scene) {
    // Tüm mesh'lerdeki bone'ları topla
    std::set<std::string> boneNames;
    
    for (unsigned int m = 0; m < scene->mNumMeshes; ++m) {
        aiMesh* mesh = scene->mMeshes[m];
        for (unsigned int b = 0; b < mesh->mNumBones; ++b) {
            boneNames.insert(mesh->mBones[b]->mName.C_Str());
        }
    }
    
    if (boneNames.empty()) {
        return true; // Skeleton yok
    }
    
    // Bone'ları oluştur
    for (const auto& boneName : boneNames) {
        BoneData bone;
        bone.name = boneName;
        bone.parentIndex = -1;
        
        // Identity matrix
        for (int i = 0; i < 16; ++i) {
            bone.localTransform[i] = (i % 5 == 0) ? 1.0f : 0.0f;
            bone.inverseBindMatrix[i] = (i % 5 == 0) ? 1.0f : 0.0f;
        }
        
        // Inverse bind matrix'i bul
        for (unsigned int m = 0; m < scene->mNumMeshes; ++m) {
            aiMesh* mesh = scene->mMeshes[m];
            for (unsigned int b = 0; b < mesh->mNumBones; ++b) {
                if (mesh->mBones[b]->mName.C_Str() == boneName) {
                    const aiMatrix4x4& mat = mesh->mBones[b]->mOffsetMatrix;
                    bone.inverseBindMatrix[0] = mat.a1; bone.inverseBindMatrix[1] = mat.b1;
                    bone.inverseBindMatrix[2] = mat.c1; bone.inverseBindMatrix[3] = mat.d1;
                    bone.inverseBindMatrix[4] = mat.a2; bone.inverseBindMatrix[5] = mat.b2;
                    bone.inverseBindMatrix[6] = mat.c2; bone.inverseBindMatrix[7] = mat.d2;
                    bone.inverseBindMatrix[8] = mat.a3; bone.inverseBindMatrix[9] = mat.b3;
                    bone.inverseBindMatrix[10] = mat.c3; bone.inverseBindMatrix[11] = mat.d3;
                    bone.inverseBindMatrix[12] = mat.a4; bone.inverseBindMatrix[13] = mat.b4;
                    bone.inverseBindMatrix[14] = mat.c4; bone.inverseBindMatrix[15] = mat.d4;
                    break;
                }
            }
        }
        
        m_modelData.bones.push_back(std::move(bone));
    }
    
    // Parent index'leri bul (node hiyerarşisinden)
    // TODO: Node ağacından parent-child ilişkilerini çıkart
    
    return true;
}

bool GLTFModelLoader::ProcessAnimations(const aiScene* scene) {
    for (unsigned int a = 0; a < scene->mNumAnimations; ++a) {
        const aiAnimation* anim = scene->mAnimations[a];
        
        AnimationData animData;
        animData.name = anim->mName.C_Str();
        animData.ticksPerSecond = (anim->mTicksPerSecond > 0) ? 
                                   static_cast<float>(anim->mTicksPerSecond) : 30.0f;
        animData.duration = static_cast<float>(anim->mDuration / animData.ticksPerSecond);
        
        // Her channel bir bone'un animasyonu
        for (unsigned int c = 0; c < anim->mNumChannels; ++c) {
            const aiNodeAnim* channel = anim->mChannels[c];
            
            AnimationTrack track;
            track.boneName = channel->mNodeName.C_Str();
            track.boneIndex = FindBoneIndex(track.boneName);
            
            // Position keys
            for (unsigned int k = 0; k < channel->mNumPositionKeys; ++k) {
                PositionKey key;
                key.time = static_cast<float>(channel->mPositionKeys[k].mTime / animData.ticksPerSecond);
                key.value[0] = channel->mPositionKeys[k].mValue.x;
                key.value[1] = channel->mPositionKeys[k].mValue.y;
                key.value[2] = channel->mPositionKeys[k].mValue.z;
                track.positionKeys.push_back(key);
            }
            
            // Rotation keys
            for (unsigned int k = 0; k < channel->mNumRotationKeys; ++k) {
                RotationKey key;
                key.time = static_cast<float>(channel->mRotationKeys[k].mTime / animData.ticksPerSecond);
                key.value[0] = channel->mRotationKeys[k].mValue.x;
                key.value[1] = channel->mRotationKeys[k].mValue.y;
                key.value[2] = channel->mRotationKeys[k].mValue.z;
                key.value[3] = channel->mRotationKeys[k].mValue.w;
                track.rotationKeys.push_back(key);
            }
            
            // Scale keys
            for (unsigned int k = 0; k < channel->mNumScalingKeys; ++k) {
                ScaleKey key;
                key.time = static_cast<float>(channel->mScalingKeys[k].mTime / animData.ticksPerSecond);
                key.value[0] = channel->mScalingKeys[k].mValue.x;
                key.value[1] = channel->mScalingKeys[k].mValue.y;
                key.value[2] = channel->mScalingKeys[k].mValue.z;
                track.scaleKeys.push_back(key);
            }
            
            animData.tracks.push_back(std::move(track));
        }
        
        m_modelData.animations.push_back(std::move(animData));
    }
    
    return true;
}

void GLTFModelLoader::ExtractBoneWeights(const aiMesh* mesh, MeshData& outMesh) {
    // Her vertex için bone weights
    outMesh.skinnedVertices.resize(mesh->mNumVertices);
    
    // Başlangıç değerleri
    for (auto& sv : outMesh.skinnedVertices) {
        for (int i = 0; i < 4; ++i) {
            sv.boneIndices[i] = 0;
            sv.boneWeights[i] = 0.0f;
        }
    }
    
    // Her bone'u işle
    for (unsigned int b = 0; b < mesh->mNumBones; ++b) {
        aiBone* bone = mesh->mBones[b];
        int boneIndex = FindBoneIndex(bone->mName.C_Str());
        
        if (boneIndex < 0) continue;
        
        // Bu bone'un etkilediği vertex'leri işle
        for (unsigned int w = 0; w < bone->mNumWeights; ++w) {
            unsigned int vertexId = bone->mWeights[w].mVertexId;
            float weight = bone->mWeights[w].mWeight;
            
            if (vertexId >= outMesh.skinnedVertices.size()) continue;
            
            SkinnedVertex& sv = outMesh.skinnedVertices[vertexId];
            
            // Vertex bilgilerini kopyala
            sv.position[0] = outMesh.vertices[vertexId].position[0];
            sv.position[1] = outMesh.vertices[vertexId].position[1];
            sv.position[2] = outMesh.vertices[vertexId].position[2];
            sv.normal[0] = outMesh.vertices[vertexId].normal[0];
            sv.normal[1] = outMesh.vertices[vertexId].normal[1];
            sv.normal[2] = outMesh.vertices[vertexId].normal[2];
            sv.texCoord[0] = outMesh.vertices[vertexId].texCoord[0];
            sv.texCoord[1] = outMesh.vertices[vertexId].texCoord[1];
            
            // En düşük weight'i bul ve değiştir
            int minIdx = 0;
            float minWeight = sv.boneWeights[0];
            for (int i = 1; i < 4; ++i) {
                if (sv.boneWeights[i] < minWeight) {
                    minWeight = sv.boneWeights[i];
                    minIdx = i;
                }
            }
            
            if (weight > minWeight) {
                sv.boneIndices[minIdx] = static_cast<unsigned char>(boneIndex);
                sv.boneWeights[minIdx] = weight;
            }
        }
    }
    
    // Weights'leri normalize et
    for (auto& sv : outMesh.skinnedVertices) {
        float total = sv.boneWeights[0] + sv.boneWeights[1] + 
                      sv.boneWeights[2] + sv.boneWeights[3];
        if (total > 0.0f) {
            for (int i = 0; i < 4; ++i) {
                sv.boneWeights[i] /= total;
            }
        } else {
            sv.boneWeights[0] = 1.0f;
        }
    }
}

int GLTFModelLoader::FindBoneIndex(const std::string& name) const {
    for (size_t i = 0; i < m_modelData.bones.size(); ++i) {
        if (m_modelData.bones[i].name == name) {
            return static_cast<int>(i);
        }
    }
    return -1;
}
#endif // USE_ASSIMP_LOADER

} // namespace GLTF
