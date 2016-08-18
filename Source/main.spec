# -*- mode: python -*-

block_cipher = None
added_files = [
         ( 'main.ui', '.' ),
         ( 'i18n/*.qm','i18n' )
     ]

a = Analysis(['main.py'],
             pathex=['D:\\work\\Projects\\Python\\Pomodoro\\Source'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Pomodoro',
          icon='Resource/tomato.ico',
          debug=False,
          strip=False,
          upx=True,
          console=True )
