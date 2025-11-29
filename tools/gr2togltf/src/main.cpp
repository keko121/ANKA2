// ============================================================================
// main.cpp - gr2togltf CLI arayüzü
// ============================================================================
// Kullanım:
//   gr2togltf --input file.gr2 --output file.gltf
//   gr2togltf --input ./models/ --output ./output/ --batch
//   gr2togltf --help
// ============================================================================

#include "Converter.h"
#include <iostream>
#include <string>
#include <cstring>

using namespace gr2togltf;

// ============================================================================
// Yardım Metni
// ============================================================================
void PrintHelp(const char* programName) {
    std::cout << R"(
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         gr2togltf - Granny2 to glTF Converter                ║
║                              ANKA2 Project Tool                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

KULLANIM:
  )" << programName << R"( [seçenekler]

SEÇENEKLER:
  -i, --input <dosya/dizin>   Girdi .gr2 dosyası veya dizin
  -o, --output <dosya/dizin>  Çıktı dosyası veya dizin
  
  -b, --batch                 Dizin modu (tüm .gr2 dosyalarını dönüştür)
  -f, --format <gltf|glb>     Çıktı formatı (varsayılan: gltf)
  
  --no-animations             Animasyonları dışla
  --no-materials              Materyalleri dışla
  --flip-uv                   UV V koordinatını çevir
  --flip-winding              Triangle winding order'ı çevir
  --scale <değer>             Ölçek faktörü (varsayılan: 1.0)
  
  -h, --help                  Bu yardım mesajını göster
  -v, --version               Versiyon bilgisini göster

ÖRNEKLER:
  # Tek dosya dönüştürme
  )" << programName << R"( -i warrior.gr2 -o warrior.gltf
  
  # GLB formatında
  )" << programName << R"( -i warrior.gr2 -o warrior.glb -f glb
  
  # Tüm dizini dönüştür
  )" << programName << R"( -i ./models/ -o ./output/ --batch
  
  # Animasyonsuz, UV çevirili
  )" << programName << R"( -i model.gr2 -o model.gltf --no-animations --flip-uv

)" << std::endl;
}

void PrintVersion() {
    std::cout << "gr2togltf v1.0.0" << std::endl;
    std::cout << "ANKA2 Project - Granny2 to glTF Converter" << std::endl;
    std::cout << "Build: " << __DATE__ << " " << __TIME__ << std::endl;
}

// ============================================================================
// Argüman Ayrıştırma
// ============================================================================
struct Arguments {
    std::string input;
    std::string output;
    bool batch = false;
    ConvertOptions options;
    bool showHelp = false;
    bool showVersion = false;
};

bool ParseArguments(int argc, char* argv[], Arguments& args) {
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        
        if (arg == "-h" || arg == "--help") {
            args.showHelp = true;
            return true;
        }
        else if (arg == "-v" || arg == "--version") {
            args.showVersion = true;
            return true;
        }
        else if (arg == "-i" || arg == "--input") {
            if (i + 1 < argc) {
                args.input = argv[++i];
            } else {
                std::cerr << "HATA: --input için değer gerekli" << std::endl;
                return false;
            }
        }
        else if (arg == "-o" || arg == "--output") {
            if (i + 1 < argc) {
                args.output = argv[++i];
            } else {
                std::cerr << "HATA: --output için değer gerekli" << std::endl;
                return false;
            }
        }
        else if (arg == "-b" || arg == "--batch") {
            args.batch = true;
        }
        else if (arg == "-f" || arg == "--format") {
            if (i + 1 < argc) {
                args.options.outputFormat = argv[++i];
                if (args.options.outputFormat != "gltf" && args.options.outputFormat != "glb") {
                    std::cerr << "HATA: Geçersiz format. 'gltf' veya 'glb' kullanın." << std::endl;
                    return false;
                }
            }
        }
        else if (arg == "--no-animations") {
            args.options.exportAnimations = false;
        }
        else if (arg == "--no-materials") {
            args.options.exportMaterials = false;
        }
        else if (arg == "--flip-uv") {
            args.options.flipUV = true;
        }
        else if (arg == "--flip-winding") {
            args.options.flipWindingOrder = true;
        }
        else if (arg == "--scale") {
            if (i + 1 < argc) {
                args.options.scaleFactor = std::stof(argv[++i]);
            }
        }
        else {
            std::cerr << "UYARI: Bilinmeyen argüman: " << arg << std::endl;
        }
    }
    
    return true;
}

// ============================================================================
// Main
// ============================================================================
int main(int argc, char* argv[]) {
    Arguments args;
    
    if (!ParseArguments(argc, argv, args)) {
        return 1;
    }
    
    if (args.showHelp) {
        PrintHelp(argv[0]);
        return 0;
    }
    
    if (args.showVersion) {
        PrintVersion();
        return 0;
    }
    
    // Input kontrolü
    if (args.input.empty()) {
        std::cerr << "HATA: Girdi dosyası belirtilmedi. -h ile yardım alın." << std::endl;
        return 1;
    }
    
    // Dönüştürme
    Converter converter;
    
    if (args.batch) {
        // Batch mod
        if (args.output.empty()) {
            args.output = "./output";
        }
        int count = converter.ConvertDirectory(args.input, args.output, args.options);
        return (count > 0) ? 0 : 1;
    } else {
        // Tek dosya
        bool success = converter.Convert(args.input, args.output, args.options);
        return success ? 0 : 1;
    }
}
