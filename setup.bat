@echo off
echo ================================
echo   CONFIGURANDO PROYECTO
echo ================================

echo.
echo [1/2] Actualizando pip...
python -m pip install --upgrade pip

echo.
echo [2/2] Instalando dependencias...

pip install flask
pip install requests
pip install PyPDF2
pip install pdfplumber
pip install sentence-transformers
pip install faiss-cpu
pip install numpy
pip install pymysql

echo.
echo ================================
echo   TODO LISTO PARA EL PROYECTO
echo ================================
echo.

pause