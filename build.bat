@echo off
echo Instalando dependencias...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Gerando YTDown.exe...
pyinstaller ytdown.spec --clean

echo.
echo Pronto! O executavel esta em: dist\YTDown.exe
pause
