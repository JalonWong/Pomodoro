call pyuic5 -x main.ui -o ui_main.py
call pyinstaller main.spec
mkdir dist\i18n
copy i18n\*.qm dist\i18n\ /Y
pause
