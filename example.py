# import os 

# platforms = []

# file = open('data.csv', 'r')
# content = file.readlines()
# for line in content:
#     row = line.split(',')
#     for tile in row:
#         tile = (int)(row[0])
#         if tile != -1:
#             print("Yes")
#         else:
#             print("No")



for i in range(0,64):
    print(i*32)

'''

pyinstaller --onefile --windowed --add-data "Assets/tilesets/Archer-Purple.png:." --add-data "Assets/tilesets/Mage-Red.png:." --add-data "Assets/sounds/gamemusic3.mp3:." --add-data "Assets/font2.TTF:." --add-data "Assets/tilesets/tileset.png:." --add-data "Assets/gameover.png:." --add-data "Assets/level1Larger.png:." --add-data "Assets/level2Larger.png:." --add-data "Assets/level3Larger.png:." --add-data "Assets/level4Larger.png:." --add-data "Assets/level5Larger.png:." --add-data "Assets/startMenu.png:." --add-data "Assets/startUnchecked.png:." --add-data "Assets/startChecked.png:." --add-data "Assets/story1.png:." --add-data "Assets/story2.png:." --add-data "Assets/help1.png:." --add-data "Assets/help2.png:." --add-data "Assets/helpBG.png:." --add-data "Assets/tilesets/chest.png:." --add-data "Assets/tilesets/item3.png:." --add-data "Assets/newProgressBar2.png:." --add-data "Assets/arrow.png:."  main.py



import glob

# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = ('')

a = Analysis(
    ['Scripts/main.py'],
    pathex=[],
    binaries=[],
    
    datas=[('Assets/tilesets/Archer-Purple.png', '.'), ('Assets/tilesets/Mage-Red.png', '.'), ('Assets/sounds/gamemusic3.mp3', '.'), ('Assets/font2.TTF', '.'), ('Assets/tilesets/tileset.png', '.'), ('Assets/gameover.png', '.'), ('Assets/level1Larger.png', '.'), ('Assets/level2Larger.png', '.'), ('Assets/level3Larger.png', '.'), ('Assets/level4Larger.png', '.'), ('Assets/level5Larger.png', '.'), ('Assets/startMenu.png', '.'), ('Assets/startUnchecked.png', '.'), ('Assets/startChecked.png', '.'), ('Assets/story1.png', '.'), ('Assets/story2.png', '.'), ('Assets/help1.png', '.'), ('Assets/help2.png', '.'), ('Assets/helpBG.png', '.'), ('Assets/tilesets/chest.png', '.'), ('Assets/tilesets/item3.png', '.'), ('Assets/newProgressBar2.png', '.'), ('Assets/arrow.png', '.')],
    datas=[('Assets/tilesets/*.png', 'Assets/tilesets'), ('Assets/sounds/*.mp3', 'Assets/sounds'), ('Assets/*.TTF', 'Assets'), ('Assets/tilesets/tileset.png', '.'), ('Assets/gameover.png', '.'), ('Assets/level1Larger.png', '.'), ('Assets/level2Larger.png', '.'), ('Assets/level3Larger.png', '.'), ('Assets/level4Larger.png', '.'), ('Assets/level5Larger.png', '.'), ('Assets/startMenu.png', '.'), ('Assets/startUnchecked.png', '.'), ('Assets/startChecked.png', '.'), ('Assets/story1.png', '.'), ('Assets/story2.png', '.'), ('Assets/help1.png', '.'), ('Assets/help2.png', '.'), ('Assets/helpBG.png', '.'), ('Assets/tilesets/chest.png', '.'), ('Assets/tilesets/item3.png', '.'), ('Assets/newProgressBar2.png', '.'), ('Assets/arrow.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)



'''