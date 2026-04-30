REM Guarda las variables de entorno para AWS
REM Comprueba que estás en la carpeta correcta
REM Crea data/ si no existe
REM Crea la base de datos automáticamente
REM Instala dependencias si faltan
REM Verifica que Ollama está instalado
REM Arranca Ollama en otra ventana
REM Descarga el modelo phi si no lo tienes
REM Arranca Flask
REM Abre el navegador automáticamente

@echo off
title PIA - Lanzador completo
color 0A

REM ---------------------------------
REM Variables de entorno AWS RDS
REM ---------------------------------
echo Configurando variables de entorno...

set DB_HOST=pia-db-aws.caqi1nngjk8d.us-east-1.rds.amazonaws.com
set DB_USER=admin
set DB_PASSWORD=admin-pia-db-aws
set DB_NAME=pia_db

REM Guardarlas permanentemente para futuras ejecuciones
setx DB_HOST "pia-db-aws.caqi1nngjk8d.us-east-1.rds.amazonaws.com" >nul
setx DB_USER "admin" >nul
setx DB_PASSWORD "admin-pia-db-aws" >nul
setx DB_NAME "pia_db" >nul

echo Variables configuradas correctamente
echo.

echo ===============================
echo     INICIANDO APLICACION PIA
echo ===============================
echo.

REM ---------------------------------
REM 1. Comprobar que estamos en la ruta correcta
REM ---------------------------------
if not exist backend (
    echo ERROR: No se encuentra la carpeta backend
    echo Ejecuta este archivo desde la raiz del proyecto
    pause
    exit /b
)

REM ---------------------------------
REM 2. Inicializar base de datos en AWS RDS
REM ---------------------------------
echo [1/5] Comprobando base de datos en AWS RDS...

cd backend
python Iniciar_BBDD.py
cd ..

echo Base de datos inicializada (o ya existente en RDS)
echo.

REM ---------------------------------
REM 3. Comprobar dependencias
REM ---------------------------------
echo [2/5] Comprobando dependencias...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
) else (
    echo Dependencias OK
)

echo.

REM ---------------------------------
REM 4. Iniciar Ollama
REM ---------------------------------
echo [3/5] Iniciando Ollama...

where ollama >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama no esta instalado
    echo Descargalo de: https://ollama.com/download
    pause
    exit /b
)

start cmd /k "ollama serve"

echo Esperando a que Ollama arranque...
timeout /t 5 >nul

REM ---------------------------------
REM 5. Descargar modelo si no existe
REM ---------------------------------
echo [4/5] Comprobando modelo 'phi'...

ollama list | findstr phi >nul
if errorlevel 1 (
    echo Modelo no encontrado. Descargando...
    ollama pull phi
) else (
    echo Modelo phi ya disponible
)

REM ---------------------------------
REM Extra: Descargar modelo deepseek-r1:8b si no existe
REM ---------------------------------
echo Comprobando modelo 'deepseek-r1:8b'...
ollama list | findstr "deepseek-r1:8b" >nul
if errorlevel 1 (
    echo Modelo no encontrado. Descargando...
    ollama pull deepseek-r1:8b
) else (
    echo Modelo deepseek-r1:8b ya disponible
)

echo.

REM ---------------------------------
REM 6. Iniciar Flask
REM ---------------------------------
echo [5/5] Iniciando servidor Flask...
cd backend
start http://127.0.0.1:5000
python app.py

echo.
echo Pulsa una tecla para cerrar TODO...
pause > nul

echo Cerrando procesos...

taskkill /f /im python.exe
taskkill /f /im ollama.exe

echo Todo cerrado.
pause