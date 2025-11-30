// ============================================================================
// Types.h - Ortak veri tipleri
// ============================================================================
#pragma once

#include <vector>
#include <string>
#include <array>
#include <cstdint>

namespace gr2togltf {

// ============================================================================
// Temel Matematik Tipleri
// ============================================================================
struct Vec2 {
    float x, y;
    Vec2() : x(0), y(0) {}
    Vec2(float x_, float y_) : x(x_), y(y_) {}
};

struct Vec3 {
    float x, y, z;
    Vec3() : x(0), y(0), z(0) {}
    Vec3(float x_, float y_, float z_) : x(x_), y(y_), z(z_) {}
};

struct Vec4 {
    float x, y, z, w;
    Vec4() : x(0), y(0), z(0), w(1) {}
    Vec4(float x_, float y_, float z_, float w_) : x(x_), y(y_), z(z_), w(w_) {}
};

struct Quat {
    float x, y, z, w;
    Quat() : x(0), y(0), z(0), w(1) {}
    Quat(float x_, float y_, float z_, float w_) : x(x_), y(y_), z(z_), w(w_) {}
};

struct Mat4x4 {
    float m[16];
    Mat4x4() { 
        for (int i = 0; i < 16; ++i) m[i] = (i % 5 == 0) ? 1.0f : 0.0f;
    }
};

// ============================================================================
// Vertex Tipleri
// ============================================================================
struct TexCoord {
    float u, v;
    TexCoord() : u(0), v(0) {}
    TexCoord(float u_, float v_) : u(u_), v(v_) {}
};

struct Vertex {
    Vec3 position;
    Vec3 normal;
    TexCoord texCoord;
    Vec2 texCoord0;  // Alias for GLTFWriter compatibility
    Vec2 texCoord1;
    
    // Skinning için
    std::array<int, 4> joints = {0, 0, 0, 0};
    std::array<float, 4> weights = {0.0f, 0.0f, 0.0f, 0.0f};
};

// ============================================================================
// Simplified Structures (for GrannyReader)
// ============================================================================
struct Bone {
    std::string name;
    int parentIndex = -1;
    float localPosition[3] = {0, 0, 0};
    float localRotation[4] = {0, 0, 0, 1};  // quaternion
    float localScale[3] = {1, 1, 1};
    float inverseBindMatrix[16];
};

struct Mesh {
    std::string name;
    std::string materialName;
    std::vector<Vertex> vertices;
    std::vector<uint16_t> indices;
    std::vector<std::array<float, 4>> boneWeights;
    std::vector<std::array<uint8_t, 4>> boneIndices;
};

struct AnimationTrackSimple {
    std::string boneName;
    int boneIndex = -1;
    std::vector<float> positionKeys;
    std::vector<float> rotationKeys;
    std::vector<float> scaleKeys;
};

struct Animation {
    std::string name;
    float duration = 0.0f;
    float timeStep = 1.0f / 30.0f;
    std::vector<AnimationTrackSimple> tracks;
};

// ============================================================================
// Mesh Verileri
// ============================================================================
struct MeshData {
    std::string name;
    std::vector<Vertex> vertices;
    std::vector<uint32_t> indices;
    int materialIndex = -1;
    bool hasSkinning = false;
};

// ============================================================================
// Material Verileri
// ============================================================================
struct MaterialData {
    std::string name;
    std::string diffuseTexture;
    Vec4 baseColor = Vec4(1, 1, 1, 1);
    float metallic = 0.0f;
    float roughness = 0.8f;
};

// ============================================================================
// Bone/Joint Verileri
// ============================================================================
struct BoneData {
    std::string name;
    int parentIndex = -1;
    Vec3 position;
    Quat rotation;
    Vec3 scale = Vec3(1, 1, 1);
    Mat4x4 inverseBindMatrix;
};

// ============================================================================
// Animation Keyframe
// ============================================================================
struct KeyframeVec3 {
    float time;
    Vec3 value;
};

struct KeyframeQuat {
    float time;
    Quat value;
};

// ============================================================================
// Animation Track
// ============================================================================
struct AnimationTrack {
    std::string boneName;
    int boneIndex = -1;
    std::vector<KeyframeVec3> positionKeys;
    std::vector<KeyframeQuat> rotationKeys;
    std::vector<KeyframeVec3> scaleKeys;
};

// ============================================================================
// Animation Data
// ============================================================================
struct AnimationData {
    std::string name;
    float duration = 0.0f;
    std::vector<AnimationTrack> tracks;
};

// ============================================================================
// Skeleton Data
// ============================================================================
struct SkeletonData {
    std::string name;
    std::vector<BoneData> bones;
};

// ============================================================================
// Model Data (tüm veriler)
// ============================================================================
struct ModelData {
    std::string name;
    std::string sourceFile;
    
    std::vector<MeshData> meshes;
    std::vector<MaterialData> materials;
    SkeletonData skeleton;
    std::vector<AnimationData> animations;
    
    // Metadata
    bool isRigid = true;  // Skeleton yoksa true
    int totalVertexCount = 0;
    int totalIndexCount = 0;
};

// ============================================================================
// Converter Options
// ============================================================================
struct ConvertOptions {
    bool exportAnimations = true;
    bool exportMaterials = true;
    bool embedTextures = false;
    bool flipUV = false;           // V koordinatını çevir
    bool flipWindingOrder = false; // Triangle yönünü çevir
    float scaleFactor = 1.0f;
    std::string outputFormat = "gltf"; // "gltf" veya "glb"
};

} // namespace gr2togltf
