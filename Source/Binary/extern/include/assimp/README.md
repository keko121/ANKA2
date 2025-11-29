# Assimp Kütüphanesi Kurulumu

Bu klasör Assimp (Open Asset Import Library) header dosyalarını içerir.

## Kurulum

### Seçenek 1: vcpkg ile (Önerilen)

```powershell
# vcpkg kurulu değilse:
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat

# Assimp'i kur (32-bit)
.\vcpkg install assimp:x86-windows

# Header ve lib'leri kopyala
copy .\installed\x86-windows\include\assimp\* ..\Source\Binary\extern\include\assimp\
copy .\installed\x86-windows\lib\assimp*.lib ..\Source\Binary\extern\library\
copy .\installed\x86-windows\bin\assimp*.dll ..\Client\
```

### Seçenek 2: GitHub Release

1. https://github.com/assimp/assimp/releases adresinden son sürümü indir
2. `include/assimp/` klasöründeki header'ları buraya kopyala
3. `lib/` klasöründen `.lib` dosyalarını `extern/library/` klasörüne kopyala
4. `bin/` klasöründen `.dll` dosyalarını `Client/` klasörüne kopyala

### Seçenek 3: CMake ile derle

```powershell
git clone https://github.com/assimp/assimp.git
cd assimp
mkdir build && cd build
cmake .. -G "Visual Studio 17 2022" -A Win32 -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release

# Dosyaları kopyala
```

## Gerekli Dosyalar

### Headers (bu klasöre):
- anim.h
- camera.h
- cimport.h
- color4.h
- config.h
- defs.h
- Exporter.hpp
- Importer.hpp
- light.h
- material.h
- matrix3x3.h
- matrix4x4.h
- mesh.h
- metadata.h
- postprocess.h
- quaternion.h
- scene.h
- texture.h
- types.h
- vector2.h
- vector3.h
- version.h
- ...

### Libraries (extern/library/):
- assimp-vc143-mt.lib (Release)
- assimp-vc143-mtd.lib (Debug)

### DLLs (Client/):
- assimp-vc143-mt.dll (Release)
- assimp-vc143-mtd.dll (Debug)

## Proje Ayarları

Visual Studio'da şu ayarları yapın:

1. **Include Directories**: `$(SolutionDir)extern\include`
2. **Library Directories**: `$(SolutionDir)extern\library`
3. **Additional Dependencies**: `assimp-vc143-mt.lib` (Release) veya `assimp-vc143-mtd.lib` (Debug)
4. **Preprocessor**: `ASSIMP_DLL` tanımlayın (DLL kullanıyorsanız)

## Kullanım

```cpp
#include <assimp/Importer.hpp>
#include <assimp/scene.h>
#include <assimp/postprocess.h>

// Model yükle
Assimp::Importer importer;
const aiScene* scene = importer.ReadFile("model.gltf",
    aiProcess_Triangulate |
    aiProcess_GenNormals |
    aiProcess_FlipUVs);

if (!scene || scene->mFlags & AI_SCENE_FLAGS_INCOMPLETE) {
    // Hata
}

// Mesh'leri işle
for (unsigned int i = 0; i < scene->mNumMeshes; i++) {
    aiMesh* mesh = scene->mMeshes[i];
    // ...
}
```
