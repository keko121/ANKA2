// ============================================================================
// GLTFWriter.cpp - glTF 2.0 dosya yazıcı implementasyonu
// ============================================================================

#define TINYGLTF_IMPLEMENTATION
#define TINYGLTF_NO_STB_IMAGE_WRITE
#define TINYGLTF_NO_STB_IMAGE
#define TINYGLTF_NO_EXTERNAL_IMAGE
#include "tiny_gltf.h"

#include "GLTFWriter.h"
#include <iostream>
#include <fstream>
#include <algorithm>
#include <limits>

namespace gr2togltf {

// ============================================================================
// Implementation struct (PIMPL)
// ============================================================================
struct GLTFWriter::Impl {
    tinygltf::Model model;
    tinygltf::TinyGLTF gltf;
    std::vector<unsigned char> bufferData;
    
    // Accessor min/max hesaplama
    Vec3 posMin, posMax;
};

// ============================================================================
// Constructor / Destructor
// ============================================================================
GLTFWriter::GLTFWriter() : m_impl(std::make_unique<Impl>()) {}
GLTFWriter::~GLTFWriter() = default;

// ============================================================================
// Ana Yazma Fonksiyonu
// ============================================================================
bool GLTFWriter::Write(const ModelData& model, const std::string& outputPath, const ConvertOptions& options) {
    if (model.meshes.empty()) {
        std::cerr << "HATA: Yazilacak mesh yok!" << std::endl;
        return false;
    }
    
    // Model'i oluştur
    BuildScene(model);
    BuildMaterials(model);
    BuildMeshes(model);
    
    if (!model.skeleton.bones.empty()) {
        BuildSkeleton(model);
    }
    
    if (!model.animations.empty()) {
        BuildAnimations(model);
    }
    
    CreateBuffers();
    
    // Format'a göre yaz
    if (options.outputFormat == "glb") {
        return WriteGLB(model, outputPath);
    } else {
        return WriteGLTF(model, outputPath);
    }
}

// ============================================================================
// glTF Yazma (.gltf + .bin)
// ============================================================================
bool GLTFWriter::WriteGLTF(const ModelData& model, const std::string& outputPath) {
    std::string err, warn;
    
    bool success = m_impl->gltf.WriteGltfSceneToFile(
        &m_impl->model,
        outputPath,
        true,   // embed images
        true,   // embed buffers
        true,   // pretty print
        false   // binary
    );
    
    if (!success) {
        std::cerr << "HATA: glTF yazma basarisiz!" << std::endl;
        return false;
    }
    
    std::cout << "glTF yazildi: " << outputPath << std::endl;
    return true;
}

// ============================================================================
// GLB Yazma (tek dosya)
// ============================================================================
bool GLTFWriter::WriteGLB(const ModelData& model, const std::string& outputPath) {
    std::string err, warn;
    
    bool success = m_impl->gltf.WriteGltfSceneToFile(
        &m_impl->model,
        outputPath,
        true,   // embed images
        true,   // embed buffers
        false,  // pretty print (GLB için false)
        true    // binary
    );
    
    if (!success) {
        std::cerr << "HATA: GLB yazma basarisiz!" << std::endl;
        return false;
    }
    
    std::cout << "GLB yazildi: " << outputPath << std::endl;
    return true;
}

// ============================================================================
// Scene Oluştur
// ============================================================================
void GLTFWriter::BuildScene(const ModelData& model) {
    m_impl->model.asset.version = "2.0";
    m_impl->model.asset.generator = "gr2togltf (ANKA2 Project)";
    
    // Scene oluştur
    tinygltf::Scene scene;
    scene.name = model.name;
    scene.nodes.push_back(0);  // root node
    m_impl->model.scenes.push_back(scene);
    m_impl->model.defaultScene = 0;
    
    // Root node
    tinygltf::Node rootNode;
    rootNode.name = model.name;
    // Mesh node'larını ekleyeceğiz
    m_impl->model.nodes.push_back(rootNode);
}

// ============================================================================
// Materials Oluştur
// ============================================================================
void GLTFWriter::BuildMaterials(const ModelData& model) {
    for (const auto& mat : model.materials) {
        tinygltf::Material gltfMat;
        gltfMat.name = mat.name;
        
        // PBR Metallic Roughness
        gltfMat.pbrMetallicRoughness.baseColorFactor = {
            mat.baseColor.x, mat.baseColor.y, mat.baseColor.z, mat.baseColor.w
        };
        gltfMat.pbrMetallicRoughness.metallicFactor = mat.metallic;
        gltfMat.pbrMetallicRoughness.roughnessFactor = mat.roughness;
        
        // Texture (TODO: texture loading)
        if (!mat.diffuseTexture.empty()) {
            // Texture URI olarak kaydet
            // gltfMat.pbrMetallicRoughness.baseColorTexture.index = ...
        }
        
        m_impl->model.materials.push_back(gltfMat);
    }
    
    // Default material yoksa ekle
    if (m_impl->model.materials.empty()) {
        tinygltf::Material defaultMat;
        defaultMat.name = "default";
        defaultMat.pbrMetallicRoughness.baseColorFactor = {0.8, 0.8, 0.8, 1.0};
        defaultMat.pbrMetallicRoughness.metallicFactor = 0.0;
        defaultMat.pbrMetallicRoughness.roughnessFactor = 0.8;
        m_impl->model.materials.push_back(defaultMat);
    }
}

// ============================================================================
// Meshes Oluştur
// ============================================================================
void GLTFWriter::BuildMeshes(const ModelData& model) {
    // Min/max başlangıç
    m_impl->posMin = Vec3(std::numeric_limits<float>::max(),
                          std::numeric_limits<float>::max(),
                          std::numeric_limits<float>::max());
    m_impl->posMax = Vec3(std::numeric_limits<float>::lowest(),
                          std::numeric_limits<float>::lowest(),
                          std::numeric_limits<float>::lowest());
    
    int nodeIndex = 1; // 0 = root
    
    for (size_t meshIdx = 0; meshIdx < model.meshes.size(); ++meshIdx) {
        const MeshData& meshData = model.meshes[meshIdx];
        
        // =====================================================================
        // Vertex verileri hazırla
        // =====================================================================
        std::vector<float> positions;
        std::vector<float> normals;
        std::vector<float> texcoords;
        
        positions.reserve(meshData.vertices.size() * 3);
        normals.reserve(meshData.vertices.size() * 3);
        texcoords.reserve(meshData.vertices.size() * 2);
        
        for (const auto& v : meshData.vertices) {
            positions.push_back(v.position.x);
            positions.push_back(v.position.y);
            positions.push_back(v.position.z);
            
            normals.push_back(v.normal.x);
            normals.push_back(v.normal.y);
            normals.push_back(v.normal.z);
            
            texcoords.push_back(v.texCoord0.x);
            texcoords.push_back(v.texCoord0.y);
            
            // Min/max güncelle
            m_impl->posMin.x = std::min(m_impl->posMin.x, v.position.x);
            m_impl->posMin.y = std::min(m_impl->posMin.y, v.position.y);
            m_impl->posMin.z = std::min(m_impl->posMin.z, v.position.z);
            m_impl->posMax.x = std::max(m_impl->posMax.x, v.position.x);
            m_impl->posMax.y = std::max(m_impl->posMax.y, v.position.y);
            m_impl->posMax.z = std::max(m_impl->posMax.z, v.position.z);
        }
        
        // =====================================================================
        // Buffer'a ekle
        // =====================================================================
        size_t posOffset = m_impl->bufferData.size();
        size_t posSize = positions.size() * sizeof(float);
        m_impl->bufferData.resize(posOffset + posSize);
        memcpy(m_impl->bufferData.data() + posOffset, positions.data(), posSize);
        
        size_t normOffset = m_impl->bufferData.size();
        size_t normSize = normals.size() * sizeof(float);
        m_impl->bufferData.resize(normOffset + normSize);
        memcpy(m_impl->bufferData.data() + normOffset, normals.data(), normSize);
        
        size_t tcOffset = m_impl->bufferData.size();
        size_t tcSize = texcoords.size() * sizeof(float);
        m_impl->bufferData.resize(tcOffset + tcSize);
        memcpy(m_impl->bufferData.data() + tcOffset, texcoords.data(), tcSize);
        
        // =====================================================================
        // Index buffer
        // =====================================================================
        // uint16 veya uint32 seç
        bool use32bit = meshData.vertices.size() > 65535;
        size_t idxOffset = m_impl->bufferData.size();
        size_t idxSize;
        
        if (use32bit) {
            idxSize = meshData.indices.size() * sizeof(uint32_t);
            m_impl->bufferData.resize(idxOffset + idxSize);
            memcpy(m_impl->bufferData.data() + idxOffset, meshData.indices.data(), idxSize);
        } else {
            std::vector<uint16_t> indices16(meshData.indices.begin(), meshData.indices.end());
            idxSize = indices16.size() * sizeof(uint16_t);
            m_impl->bufferData.resize(idxOffset + idxSize);
            memcpy(m_impl->bufferData.data() + idxOffset, indices16.data(), idxSize);
        }
        
        // =====================================================================
        // BufferViews
        // =====================================================================
        int posViewIdx = static_cast<int>(m_impl->model.bufferViews.size());
        {
            tinygltf::BufferView view;
            view.buffer = 0;
            view.byteOffset = posOffset;
            view.byteLength = posSize;
            view.target = TINYGLTF_TARGET_ARRAY_BUFFER;
            m_impl->model.bufferViews.push_back(view);
        }
        
        int normViewIdx = static_cast<int>(m_impl->model.bufferViews.size());
        {
            tinygltf::BufferView view;
            view.buffer = 0;
            view.byteOffset = normOffset;
            view.byteLength = normSize;
            view.target = TINYGLTF_TARGET_ARRAY_BUFFER;
            m_impl->model.bufferViews.push_back(view);
        }
        
        int tcViewIdx = static_cast<int>(m_impl->model.bufferViews.size());
        {
            tinygltf::BufferView view;
            view.buffer = 0;
            view.byteOffset = tcOffset;
            view.byteLength = tcSize;
            view.target = TINYGLTF_TARGET_ARRAY_BUFFER;
            m_impl->model.bufferViews.push_back(view);
        }
        
        int idxViewIdx = static_cast<int>(m_impl->model.bufferViews.size());
        {
            tinygltf::BufferView view;
            view.buffer = 0;
            view.byteOffset = idxOffset;
            view.byteLength = idxSize;
            view.target = TINYGLTF_TARGET_ELEMENT_ARRAY_BUFFER;
            m_impl->model.bufferViews.push_back(view);
        }
        
        // =====================================================================
        // Accessors
        // =====================================================================
        int posAccIdx = static_cast<int>(m_impl->model.accessors.size());
        {
            tinygltf::Accessor acc;
            acc.bufferView = posViewIdx;
            acc.byteOffset = 0;
            acc.componentType = TINYGLTF_COMPONENT_TYPE_FLOAT;
            acc.count = meshData.vertices.size();
            acc.type = TINYGLTF_TYPE_VEC3;
            acc.minValues = {m_impl->posMin.x, m_impl->posMin.y, m_impl->posMin.z};
            acc.maxValues = {m_impl->posMax.x, m_impl->posMax.y, m_impl->posMax.z};
            m_impl->model.accessors.push_back(acc);
        }
        
        int normAccIdx = static_cast<int>(m_impl->model.accessors.size());
        {
            tinygltf::Accessor acc;
            acc.bufferView = normViewIdx;
            acc.byteOffset = 0;
            acc.componentType = TINYGLTF_COMPONENT_TYPE_FLOAT;
            acc.count = meshData.vertices.size();
            acc.type = TINYGLTF_TYPE_VEC3;
            m_impl->model.accessors.push_back(acc);
        }
        
        int tcAccIdx = static_cast<int>(m_impl->model.accessors.size());
        {
            tinygltf::Accessor acc;
            acc.bufferView = tcViewIdx;
            acc.byteOffset = 0;
            acc.componentType = TINYGLTF_COMPONENT_TYPE_FLOAT;
            acc.count = meshData.vertices.size();
            acc.type = TINYGLTF_TYPE_VEC2;
            m_impl->model.accessors.push_back(acc);
        }
        
        int idxAccIdx = static_cast<int>(m_impl->model.accessors.size());
        {
            tinygltf::Accessor acc;
            acc.bufferView = idxViewIdx;
            acc.byteOffset = 0;
            acc.componentType = use32bit ? TINYGLTF_COMPONENT_TYPE_UNSIGNED_INT 
                                         : TINYGLTF_COMPONENT_TYPE_UNSIGNED_SHORT;
            acc.count = meshData.indices.size();
            acc.type = TINYGLTF_TYPE_SCALAR;
            m_impl->model.accessors.push_back(acc);
        }
        
        // =====================================================================
        // Mesh Primitive
        // =====================================================================
        tinygltf::Primitive prim;
        prim.attributes["POSITION"] = posAccIdx;
        prim.attributes["NORMAL"] = normAccIdx;
        prim.attributes["TEXCOORD_0"] = tcAccIdx;
        prim.indices = idxAccIdx;
        prim.mode = TINYGLTF_MODE_TRIANGLES;
        prim.material = (meshData.materialIndex >= 0) ? meshData.materialIndex : 0;
        
        tinygltf::Mesh mesh;
        mesh.name = meshData.name;
        mesh.primitives.push_back(prim);
        
        int meshIndex = static_cast<int>(m_impl->model.meshes.size());
        m_impl->model.meshes.push_back(mesh);
        
        // =====================================================================
        // Node for mesh
        // =====================================================================
        tinygltf::Node meshNode;
        meshNode.name = meshData.name;
        meshNode.mesh = meshIndex;
        
        m_impl->model.nodes.push_back(meshNode);
        m_impl->model.nodes[0].children.push_back(nodeIndex);
        nodeIndex++;
    }
}

// ============================================================================
// Skeleton Oluştur
// ============================================================================
void GLTFWriter::BuildSkeleton(const ModelData& model) {
    if (model.skeleton.bones.empty()) return;
    
    // Skin oluştur
    tinygltf::Skin skin;
    skin.name = model.skeleton.name;
    
    int boneNodeStart = static_cast<int>(m_impl->model.nodes.size());
    
    // Her bone için node oluştur
    for (size_t i = 0; i < model.skeleton.bones.size(); ++i) {
        const BoneData& bone = model.skeleton.bones[i];
        
        tinygltf::Node node;
        node.name = bone.name;
        
        // Transform
        node.translation = {bone.position.x, bone.position.y, bone.position.z};
        node.rotation = {bone.rotation.x, bone.rotation.y, bone.rotation.z, bone.rotation.w};
        node.scale = {bone.scale.x, bone.scale.y, bone.scale.z};
        
        // Children (parent-child ilişkisi)
        for (size_t j = 0; j < model.skeleton.bones.size(); ++j) {
            if (model.skeleton.bones[j].parentIndex == static_cast<int>(i)) {
                node.children.push_back(boneNodeStart + static_cast<int>(j));
            }
        }
        
        m_impl->model.nodes.push_back(node);
        skin.joints.push_back(boneNodeStart + static_cast<int>(i));
    }
    
    // Root bone'u bul ve skeleton root olarak ayarla
    for (size_t i = 0; i < model.skeleton.bones.size(); ++i) {
        if (model.skeleton.bones[i].parentIndex < 0) {
            skin.skeleton = boneNodeStart + static_cast<int>(i);
            m_impl->model.nodes[0].children.push_back(boneNodeStart + static_cast<int>(i));
            break;
        }
    }
    
    // Inverse bind matrices buffer'a ekle
    size_t ibmOffset = m_impl->bufferData.size();
    size_t ibmSize = model.skeleton.bones.size() * 16 * sizeof(float);
    m_impl->bufferData.resize(ibmOffset + ibmSize);
    
    float* ibmData = reinterpret_cast<float*>(m_impl->bufferData.data() + ibmOffset);
    for (size_t i = 0; i < model.skeleton.bones.size(); ++i) {
        memcpy(ibmData + i * 16, model.skeleton.bones[i].inverseBindMatrix.m, 16 * sizeof(float));
    }
    
    // BufferView
    int ibmViewIdx = static_cast<int>(m_impl->model.bufferViews.size());
    {
        tinygltf::BufferView view;
        view.buffer = 0;
        view.byteOffset = ibmOffset;
        view.byteLength = ibmSize;
        m_impl->model.bufferViews.push_back(view);
    }
    
    // Accessor
    int ibmAccIdx = static_cast<int>(m_impl->model.accessors.size());
    {
        tinygltf::Accessor acc;
        acc.bufferView = ibmViewIdx;
        acc.byteOffset = 0;
        acc.componentType = TINYGLTF_COMPONENT_TYPE_FLOAT;
        acc.count = model.skeleton.bones.size();
        acc.type = TINYGLTF_TYPE_MAT4;
        m_impl->model.accessors.push_back(acc);
    }
    
    skin.inverseBindMatrices = ibmAccIdx;
    m_impl->model.skins.push_back(skin);
    
    // Mesh node'larına skin ata
    for (auto& node : m_impl->model.nodes) {
        if (node.mesh >= 0) {
            node.skin = 0;
        }
    }
}

// ============================================================================
// Animations Oluştur
// ============================================================================
void GLTFWriter::BuildAnimations(const ModelData& model) {
    if (model.skeleton.bones.empty()) return;
    
    int boneNodeStart = static_cast<int>(m_impl->model.nodes.size()) - static_cast<int>(model.skeleton.bones.size());
    
    for (const auto& animData : model.animations) {
        tinygltf::Animation anim;
        anim.name = animData.name;
        
        for (const auto& track : animData.tracks) {
            if (track.boneIndex < 0) continue;
            
            int targetNode = boneNodeStart + track.boneIndex;
            
            // =================================================================
            // Position
            // =================================================================
            if (!track.positionKeys.empty()) {
                // Time buffer
                size_t timeOffset = m_impl->bufferData.size();
                size_t timeSize = track.positionKeys.size() * sizeof(float);
                m_impl->bufferData.resize(timeOffset + timeSize);
                for (size_t i = 0; i < track.positionKeys.size(); ++i) {
                    float* ptr = reinterpret_cast<float*>(m_impl->bufferData.data() + timeOffset);
                    ptr[i] = track.positionKeys[i].time;
                }
                
                // Value buffer
                size_t valueOffset = m_impl->bufferData.size();
                size_t valueSize = track.positionKeys.size() * 3 * sizeof(float);
                m_impl->bufferData.resize(valueOffset + valueSize);
                for (size_t i = 0; i < track.positionKeys.size(); ++i) {
                    float* ptr = reinterpret_cast<float*>(m_impl->bufferData.data() + valueOffset) + i * 3;
                    ptr[0] = track.positionKeys[i].value.x;
                    ptr[1] = track.positionKeys[i].value.y;
                    ptr[2] = track.positionKeys[i].value.z;
                }
                
                // BufferViews & Accessors
                int timeViewIdx = static_cast<int>(m_impl->model.bufferViews.size());
                {
                    tinygltf::BufferView v; v.buffer = 0; v.byteOffset = timeOffset; v.byteLength = timeSize;
                    m_impl->model.bufferViews.push_back(v);
                }
                int valueViewIdx = static_cast<int>(m_impl->model.bufferViews.size());
                {
                    tinygltf::BufferView v; v.buffer = 0; v.byteOffset = valueOffset; v.byteLength = valueSize;
                    m_impl->model.bufferViews.push_back(v);
                }
                
                int timeAccIdx = static_cast<int>(m_impl->model.accessors.size());
                {
                    tinygltf::Accessor a;
                    a.bufferView = timeViewIdx;
                    a.componentType = TINYGLTF_COMPONENT_TYPE_FLOAT;
                    a.count = track.positionKeys.size();
                    a.type = TINYGLTF_TYPE_SCALAR;
                    a.minValues = {track.positionKeys.front().time};
                    a.maxValues = {track.positionKeys.back().time};
                    m_impl->model.accessors.push_back(a);
                }
                int valueAccIdx = static_cast<int>(m_impl->model.accessors.size());
                {
                    tinygltf::Accessor a;
                    a.bufferView = valueViewIdx;
                    a.componentType = TINYGLTF_COMPONENT_TYPE_FLOAT;
                    a.count = track.positionKeys.size();
                    a.type = TINYGLTF_TYPE_VEC3;
                    m_impl->model.accessors.push_back(a);
                }
                
                // Sampler
                int samplerIdx = static_cast<int>(anim.samplers.size());
                tinygltf::AnimationSampler sampler;
                sampler.input = timeAccIdx;
                sampler.output = valueAccIdx;
                sampler.interpolation = "LINEAR";
                anim.samplers.push_back(sampler);
                
                // Channel
                tinygltf::AnimationChannel channel;
                channel.sampler = samplerIdx;
                channel.target_node = targetNode;
                channel.target_path = "translation";
                anim.channels.push_back(channel);
            }
            
            // =================================================================
            // Rotation (benzer şekilde)
            // =================================================================
            if (!track.rotationKeys.empty()) {
                size_t timeOffset = m_impl->bufferData.size();
                size_t timeSize = track.rotationKeys.size() * sizeof(float);
                m_impl->bufferData.resize(timeOffset + timeSize);
                for (size_t i = 0; i < track.rotationKeys.size(); ++i) {
                    float* ptr = reinterpret_cast<float*>(m_impl->bufferData.data() + timeOffset);
                    ptr[i] = track.rotationKeys[i].time;
                }
                
                size_t valueOffset = m_impl->bufferData.size();
                size_t valueSize = track.rotationKeys.size() * 4 * sizeof(float);
                m_impl->bufferData.resize(valueOffset + valueSize);
                for (size_t i = 0; i < track.rotationKeys.size(); ++i) {
                    float* ptr = reinterpret_cast<float*>(m_impl->bufferData.data() + valueOffset) + i * 4;
                    ptr[0] = track.rotationKeys[i].value.x;
                    ptr[1] = track.rotationKeys[i].value.y;
                    ptr[2] = track.rotationKeys[i].value.z;
                    ptr[3] = track.rotationKeys[i].value.w;
                }
                
                int timeViewIdx = static_cast<int>(m_impl->model.bufferViews.size());
                { tinygltf::BufferView v; v.buffer=0; v.byteOffset=timeOffset; v.byteLength=timeSize; m_impl->model.bufferViews.push_back(v); }
                int valueViewIdx = static_cast<int>(m_impl->model.bufferViews.size());
                { tinygltf::BufferView v; v.buffer=0; v.byteOffset=valueOffset; v.byteLength=valueSize; m_impl->model.bufferViews.push_back(v); }
                
                int timeAccIdx = static_cast<int>(m_impl->model.accessors.size());
                { tinygltf::Accessor a; a.bufferView=timeViewIdx; a.componentType=TINYGLTF_COMPONENT_TYPE_FLOAT; a.count=track.rotationKeys.size(); a.type=TINYGLTF_TYPE_SCALAR; m_impl->model.accessors.push_back(a); }
                int valueAccIdx = static_cast<int>(m_impl->model.accessors.size());
                { tinygltf::Accessor a; a.bufferView=valueViewIdx; a.componentType=TINYGLTF_COMPONENT_TYPE_FLOAT; a.count=track.rotationKeys.size(); a.type=TINYGLTF_TYPE_VEC4; m_impl->model.accessors.push_back(a); }
                
                int samplerIdx = static_cast<int>(anim.samplers.size());
                tinygltf::AnimationSampler sampler; sampler.input=timeAccIdx; sampler.output=valueAccIdx; sampler.interpolation="LINEAR";
                anim.samplers.push_back(sampler);
                
                tinygltf::AnimationChannel channel; channel.sampler=samplerIdx; channel.target_node=targetNode; channel.target_path="rotation";
                anim.channels.push_back(channel);
            }
        }
        
        if (!anim.channels.empty()) {
            m_impl->model.animations.push_back(anim);
        }
    }
}

// ============================================================================
// Buffer Finalize
// ============================================================================
void GLTFWriter::CreateBuffers() {
    tinygltf::Buffer buffer;
    buffer.data = m_impl->bufferData;
    m_impl->model.buffers.push_back(buffer);
}

} // namespace gr2togltf
