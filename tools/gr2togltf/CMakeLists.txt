# ============================================================================
# GR2 to glTF Converter - CMakeLists.txt
# ============================================================================
# Granny2 (.gr2) dosyalarını glTF 2.0 formatına dönüştürür
# ============================================================================

cmake_minimum_required(VERSION 3.16)
project(gr2togltf VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ============================================================================
# Platform
# ============================================================================
if(WIN32)
    set(PLATFORM_DIR "win32")
    add_definitions(-D_WIN32 -DNOMINMAX)
else()
    message(FATAL_ERROR "Bu tool sadece Windows'ta derlenebilir (Granny SDK gerekli)")
endif()

# ============================================================================
# Granny SDK
# ============================================================================
set(GRANNY_SDK_DIR "${CMAKE_SOURCE_DIR}/../../gr2" CACHE PATH "Granny SDK path")

if(NOT EXISTS "${GRANNY_SDK_DIR}/include/granny.h")
    message(FATAL_ERROR "Granny SDK bulunamadı: ${GRANNY_SDK_DIR}/include/granny.h")
endif()

include_directories(${GRANNY_SDK_DIR}/include)
link_directories(${GRANNY_SDK_DIR}/lib/win32)

# ============================================================================
# tinygltf (header-only JSON/glTF library)
# ============================================================================
# tinygltf otomatik indirilecek veya extern'de olmalı
include(FetchContent)
FetchContent_Declare(
    tinygltf
    GIT_REPOSITORY https://github.com/syoyo/tinygltf.git
    GIT_TAG v2.8.21
)
FetchContent_MakeAvailable(tinygltf)
include_directories(${tinygltf_SOURCE_DIR})

# JSON için
add_definitions(-DTINYGLTF_NO_STB_IMAGE_WRITE)
add_definitions(-DTINYGLTF_NO_STB_IMAGE)
add_definitions(-DTINYGLTF_NO_EXTERNAL_IMAGE)

# ============================================================================
# Source Files
# ============================================================================
set(SOURCES
    src/main.cpp
    src/GrannyReader.cpp
    src/GLTFWriter.cpp
    src/Converter.cpp
)

set(HEADERS
    src/GrannyReader.h
    src/GLTFWriter.h
    src/Converter.h
    src/Types.h
)

# ============================================================================
# Executable
# ============================================================================
add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})

# Granny2 library link
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    target_link_libraries(${PROJECT_NAME} granny2_x64)
else()
    target_link_libraries(${PROJECT_NAME} granny2)
endif()

# ============================================================================
# Install
# ============================================================================
install(TARGETS ${PROJECT_NAME} DESTINATION bin)

# ============================================================================
# Test Target
# ============================================================================
add_custom_target(test_convert
    COMMAND ${PROJECT_NAME} 
        --input "${CMAKE_SOURCE_DIR}/../../Tools/binary_unpack/zone/oxevent/ox_01.gr2"
        --output "${CMAKE_BINARY_DIR}/test_output.gltf"
    DEPENDS ${PROJECT_NAME}
    COMMENT "Test: Converting ox_01.gr2 to glTF"
)

message(STATUS "gr2togltf configured successfully")
message(STATUS "Granny SDK: ${GRANNY_SDK_DIR}")
