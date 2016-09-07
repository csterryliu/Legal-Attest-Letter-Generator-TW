@echo off

src\tw-lal-generator.py --help

echo %cd%

if errorlevel == 1 (
echo 設定 PYTHONPATH....
setx PYTHONPATH "%cd%/dep/PyPDF2;%cd%/dep/reportlab/src"
)

echo 環境變數設置成功!
pause