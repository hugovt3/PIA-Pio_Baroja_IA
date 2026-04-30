REM Guarda las variables de entorno para AWS
REM Comprueba que estás en la carpeta correcta
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
REM 2. Iniciar Ollama
REM ---------------------------------
echo Iniciando Ollama...

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
REM 3. Iniciar Flask
REM ---------------------------------
echo Iniciando servidor Flask...
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