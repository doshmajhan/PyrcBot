# -*- mode: python -*-
a = Analysis(['adobe.py'],
             pathex=['C:\\Users\\MC\\Documents\\GitHub\\pythonbot'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='adobe.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
