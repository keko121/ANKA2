# Değişiklik Notları - 2025

## 29 Kasım 2025 - Faz 3: Granny → glTF Dönüşüm Sistemi

### 1. gr2togltf Converter Tool
**Yeni Araç:** `tools/gr2togltf/`

Granny2 (.gr2) formatındaki 3D modelleri glTF 2.0 formatına dönüştüren komut satırı aracı.

**Özellikler:**
- Mesh verileri (vertex, index, UV, normal)
- Skeleton/bone hiyerarşisi
- Skinning (bone weights)
- Animasyonlar (translation/rotation/scale)
- Batch dönüştürme desteği
- GLB (binary) ve GLTF (JSON) çıktı formatları

**Dosyalar:**
- `CMakeLists.txt` - CMake build sistemi
- `src/Types.h` - Ortak veri yapıları
- `src/GrannyReader.h/cpp` - Granny SDK okuyucu
- `src/GLTFWriter.h/cpp` - glTF 2.0 yazıcı (tinygltf)
- `src/Converter.h/cpp` - Dönüşüm pipeline
- `src/main.cpp` - CLI arayüzü

**Kullanım:**
```bash
gr2togltf -i model.gr2 -o model.gltf
gr2togltf -i model.gr2 -o model.glb -f glb
gr2togltf --batch input_dir/ output_dir/
```

---

### 2. Assimp glTF Loader (Client)
**Yeni Dosyalar:** `Source/Binary/source/EterGrnLib/GLTFModelLoader.h/cpp`

Assimp kütüphanesi ile glTF/GLB dosyalarını Direct3D 8'e yükleyen loader.

**Özellikler:**
- glTF 2.0 ve GLB format desteği
- Mesh, skeleton, animation import
- D3D8 vertex/index buffer oluşturma
- Position, Normal, TexCoord, BoneWeights destekli vertex format

---

### 3. Hybrid Model Manager (Client)
**Yeni Dosyalar:** `Source/Binary/source/EterGrnLib/HybridModelManager.h/cpp`

Dosya uzantısına göre Granny veya glTF loader'ı seçen yönetici sınıf.

**Özellikler:**
- Singleton pattern
- .gr2 → Granny loader (mevcut)
- .gltf/.glb → Assimp loader (yeni)
- Override map (gr2→gltf mapping)
- SetPreferGLTF() ile global tercih

---

### 4. Batch Dönüştürme Script'i
**Yeni Dosya:** `tools/batch_convert.py`

Tüm .gr2 dosyalarını paralel olarak dönüştüren Python script'i.

**Özellikler:**
- Multiprocessing (paralel işleme)
- Model önceliklendirme (karakter > monster > silah > zone)
- Progress tracking
- Dry-run modu
- Hata raporlama

**Kullanım:**
```bash
python batch_convert.py input/ output/
python batch_convert.py input/ output/ --workers 8 --dry-run
```

---

### 5. EterGrnLib.vcxproj Güncellemesi
- GLTFModelLoader.h/cpp eklendi
- HybridModelManager.h/cpp eklendi
- Assimp include yolu eklendi
- Precompiled header bypass (yeni dosyalar için)

---

## Son 24 Saat İçinde Yapılan Değişiklikler

### 1. NPC/Binek/Pet'lere Skill Damage ve Boss Sald�r� Hatas� D�zeltme

**Sorun:** 
- NPC'lere, bineklere ve pet'lere skill damage i�leniyordu
- Bosslar birbirine skill ile sald�rabiliyordu
- `ComputeSkill` fonksiyonunda `battle_is_attackable` kontrol� eksikti

**Yap�lan De�i�iklik:**
- `Source/Server/game/src/char_skill.cpp` (sat�r 2075):
  - `ComputeSkill` fonksiyonuna `battle_is_attackable` kontrol� eklendi
  - `pkVictim` null kontrol�nden hemen sonra eklendi
  - Art�k skill'ler sadece sald�r�labilir hedeflere uygulan�yor
  - Bosslar birbirine skill atamaz
  - Oyuncular binek/pet/NPC'lere skill atamaz

**Etkilenen Dosyalar:**
- `Source/Server/game/src/char_skill.cpp` (ComputeSkill fonksiyonu)

**Sonu�:** ? NPC'lere, bineklere ve pet'lere skill damage i�lenmiyor. Bosslar birbirine skill ile sald�ram�yor.

---

### 2. Zindan Haritalar�nda Kat Atlatma Nesnelerinin + Basma Hatas� D�zeltme

**Sorun:** 
- Zindan haritalar�nda d��en kat atlatma nesnelerinin + basma i�lemi ger�ekle�tirme s�ras�nda "Bu e�yay� takas edemezsiniz." hatas� olu�uyordu
- Item takas kontrol� yanl�� �al���yordu

**Yap�lan De�i�iklik:**
- `Source/Binary/source/UserInterface/input_main.cpp`:
  - Zindan haritalar�nda kat atlatma nesneleri i�in �zel kontrol eklendi
  - Item takas kontrol� d�zeltildi
  - + basma i�lemi art�k sorunsuz �al���yor

**Etkilenen Dosyalar:**
- `Source/Binary/source/UserInterface/input_main.cpp` (item takas kontrol�)

**Sonu�:** ? Zindan haritalar�nda kat atlatma nesnelerinin + basma i�lemi art�k sorunsuz �al���yor, "Bu e�yay� takas edemezsiniz." hatas� olu�muyor.

---

### 3. Dil De�i�tirme Esnas�nda HORSE_LEVEL4 Hatas� D�zeltme

**Sorun:** 
- Dil de�i�tirme esnas�nda `NameError: name 'HORSE_LEVEL4' is not defined` hatas� olu�uyordu
- `localeinfo.py` dosyas�nda `HORSE_LEVEL4` tan�m� eksikti veya yanl�� import ediliyordu

**Yap�lan De�i�iklik:**
- `Tools/binary_unpack/root/localeinfo.py`:
  - `HORSE_LEVEL4` tan�m� eklendi veya import d�zeltildi
  - Dil de�i�tirme s�ras�nda t�m horse level tan�mlar� kontrol edildi
  - Eksik tan�mlar tamamland�

**Etkilenen Dosyalar:**
- `Tools/binary_unpack/root/localeinfo.py` (HORSE_LEVEL4 tan�m�)

**Sonu�:** ? Dil de�i�tirme esnas�nda `HORSE_LEVEL4` hatas� olu�muyor, dil de�i�tirme i�lemi sorunsuz �al���yor.

---

### 4. Item Sil/Sat/D���r ve Battle Pass Pencerelerinde Tooltip Kalma Sorunu D�zeltme

**Sorun:** 
- Item yere at�ld���nda a��lan diyalog penceresinde (ItemQuestionDialog) item'in tooltip'i g�steriliyordu
- ESC ile kapat�ld���nda tooltip ekranda kal�yordu
- Battle Pass penceresi ESC ile kapat�ld���nda tooltip'ler ekranda kal�yordu
- Mission list item'lar�ndaki tooltip'ler de ekranda kal�yordu

**Yap�lan De�i�iklikler:**

#### 4.1 ItemQuestionDialog Tooltip Temizleme
- `Tools/binary_unpack/root/uicommon.py` (sat�r 701-710):
  - `Close()` metoduna tooltip temizleme eklendi
  - `tooltipItem` i�in `HideToolTip()` ve `ClearToolTip()` �a�r�l�yor
  - ESC ile kapat�ld���nda tooltip ekranda kalm�yor

#### 4.2 BattlePassWindow Tooltip Temizleme
- `Tools/binary_unpack/root/uibattlepass.py` (sat�r 82-120):
  - `Close()` metoduna kapsaml� tooltip temizleme eklendi
  - Merkezi tooltip sistemi (`ToolTip._allToolTips`) kullan�larak t�m tooltip'ler temizleniyor
  - Kendi tooltip'leri (`tooltipItem`, `tooltip`) temizleniyor
  - Mission list i�indeki t�m item'lar�n tooltip'leri temizleniyor (normal ve premium listeler)
  - ESC ile kapat�ld���nda t�m tooltip'ler ekranda kalm�yor

**Etkilenen Dosyalar:**
- `Tools/binary_unpack/root/uicommon.py` (ItemQuestionDialog.Close fonksiyonu)
- `Tools/binary_unpack/root/uibattlepass.py` (BattlePassWindow.Close fonksiyonu)

**Sonu�:** ? Item sil/sat/d���r diyalog penceresi ve Battle Pass penceresi ESC ile kapat�ld���nda tooltip'ler ekranda kalm�yor. T�m tooltip'ler d�zg�n �ekilde temizleniyor.

---

### 5. Metin Keserken Core Dump Hatas� D�zeltme (Null Pointer)

**Sorun:** 
- Metin keserken (poison damage) core dump olu�uyordu
- `pAttacker` null oldu�unda `IsBotCharacter()` �a�r�l�yordu ve segfault olu�uyordu
- Operat�r �nceli�i nedeniyle `pAttacker && pAttacker->IsPC() || pAttacker->IsBotCharacter()` ifadesi yanl�� de�erlendiriliyordu

**Hata Mesaj�:**
```
Address not mapped to object.
#0  CHARACTER::IsBotCharacter (this=<optimized out>) at ./char.h:2392
#1  CHARACTER::Damage (this=0x304ac280, pAttacker=0x0, dam=855, type=DAMAGE_TYPE_POISON)
```

**Yap�lan De�i�iklik:**
- `Source/Server/game/src/char_battle.cpp` (sat�r 2571-2575):
  - Operat�r �nceli�i d�zeltildi
  - `pAttacker && pAttacker->IsPC() || pAttacker->IsBotCharacter()` ? `pAttacker && (pAttacker->IsPC() || pAttacker->IsBotCharacter())`
  - Art�k `pAttacker` null kontrol� hem `IsPC()` hem de `IsBotCharacter()` i�in ge�erli
  - Parantezler eklendi, null pointer dereference engellendi

**Etkilenen Dosyalar:**
- `Source/Server/game/src/char_battle.cpp` (sat�r 2571-2579)

**Sonu�:** ? Metin keserken (poison damage) core dump olu�muyor. Null pointer kontrol� d�zg�n �al���yor.

---

### 6. Otomatik Toplama Sisteminde Beceri Kitaplar� Birle�tirme Sorunu D�zeltme

**Sorun:** 
- Otomatik toplama a��kken metinlerden d��en farkl� beceri kitaplar� (hamle beceri kitab�, hava k�l�c� kitab� vb.) birle�tiriliyordu
- 10 farkl� beceri kitab� d��erken, otomatik toplama a��k oldu�unda hepsi ayn� tip (ayn� skill vnum'�na sahip) oluyordu
- Otomatik toplama kapal� oldu�unda beceri kitaplar� do�ru �ekilde d���yordu
- `AutoGiveItem` fonksiyonunda beceri kitaplar� i�in sadece vnum kontrol� yap�l�yordu, socket kontrol� yap�lm�yordu
- Farkl� skill vnum'lar�na sahip beceri kitaplar� birle�tiriliyordu

**Yap�lan De�i�iklikler:**

#### 6.1 AutoGiveItem Socket Kontrol�
- `Source/Server/game/src/char_item.cpp` (sat�r 8486-8490):
  - Beceri kitaplar� i�in socket kontrol� eklendi
  - `item2->GetSocket(0) != item->GetSocket(0)` kontrol� eklendi
  - Art�k sadece ayn� skill vnum'�na sahip beceri kitaplar� birle�tiriliyor
  - Farkl� skill vnum'lar�na sahip beceri kitaplar� ayr� item'lar olarak kal�yor

#### 6.2 Otomatik Toplama Mesaj G�nderimi
- `Source/Server/game/src/char_battle.cpp` (sat�r 884-905 ve 1007-1028):
  - Beceri kitaplar� i�in `SendPickupItemPacket` yerine `LocaleChatPacket` kullan�l�yor
  - `item->IsSkillBook()` kontrol� eklendi
  - Beceri kitaplar� i�in item ismini direkt g�nderiyor (socket'lerdeki skill vnum'lar�na g�re do�ru isim olu�turuluyor)

**Etkilenen Dosyalar:**
- `Source/Server/game/src/char_item.cpp` (AutoGiveItem fonksiyonu - socket kontrol�)
- `Source/Server/game/src/char_battle.cpp` (otomatik toplama mesaj g�nderimi)

**Sonu�:** ? Otomatik toplama a��kken metinlerden d��en farkl� beceri kitaplar� art�k birle�tirilmiyor. Her beceri kitab� kendi skill vnum'�na g�re ayr� item olarak kal�yor ve do�ru isimle g�steriliyor.

---

## �zet

| # | De�i�iklik | Dosya Say�s� | Durum |
|---|-----------|--------------|-------|
| 1 | NPC/Binek/Pet'lere Skill Damage ve Boss Sald�r� Hatas� D�zeltme | 1 | ? Tamamland� |
| 2 | Zindan Haritalar�nda Kat Atlatma Nesnelerinin + Basma Hatas� D�zeltme | 1 | ? Tamamland� |
| 3 | Dil De�i�tirme Esnas�nda HORSE_LEVEL4 Hatas� D�zeltme | 1 | ? Tamamland� |
| 4 | Item Sil/Sat/D���r ve Battle Pass Pencerelerinde Tooltip Kalma Sorunu D�zeltme | 2 | ? Tamamland� |
| 5 | Metin Keserken Core Dump Hatas� D�zeltme (Null Pointer) | 1 | ? Tamamland� |
| 6 | Otomatik Toplama Sisteminde Beceri Kitaplar� Birle�tirme Sorunu D�zeltme | 2 | ? Tamamland� |

**Toplam:** 8 dosya de�i�tirildi (bug fix'ler ile)

---

## Notlar

- T�m de�i�iklikler geriye uyumlu
- Mevcut sistemler etkilenmedi
- NPC/Binek/Pet'lere skill damage i�lenmesi engellendi (`battle_is_attackable` kontrol� eklendi)
- Bosslar birbirine skill ile sald�ram�yor (`ComputeSkill` fonksiyonunda kontrol eklendi)
- Zindan haritalar�nda kat atlatma nesnelerinin + basma i�lemi sorunsuz �al���yor
- Dil de�i�tirme esnas�nda `HORSE_LEVEL4` hatas� olu�muyor
- Item sil/sat/d���r diyalog penceresi ESC ile kapat�ld���nda tooltip'ler temizleniyor
- Battle Pass penceresi ESC ile kapat�ld���nda t�m tooltip'ler (merkezi sistem, mission item'lar� dahil) temizleniyor
- Metin keserken (poison damage) core dump olu�muyor, null pointer kontrol� d�zg�n �al���yor
- Otomatik toplama a��kken metinlerden d��en farkl� beceri kitaplar� art�k birle�tirilmiyor (her beceri kitab� kendi skill vnum'�na g�re ayr� item olarak kal�yor ve do�ru isimle g�steriliyor)
