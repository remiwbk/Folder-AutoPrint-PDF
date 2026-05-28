@echo off
:: =============================================
:: Lanceur universel pour pdf-print.py
:: Utilise des chemins relatifs au .bat
:: Fonctionne pour n'importe quel utilisateur
:: =============================================

:: Chemin vers python.exe (utilise %LOCALAPPDATA% pour trouver Python)
set PYTHON="%LOCALAPPDATA%\Python\pythoncore-3.14-64\pythonw.exe"

:: Vérifie si Python existe dans %LOCALAPPDATA%
if not exist "%PYTHON%" (
    :: Si non trouvé, essaie avec le chemin par défaut de Python
    set PYTHON="C:\Python314\pythonw.exe"
)

:: Vérifie que pythonw.exe existe
if not exist "%PYTHON%" (
    echo =============================================
    echo ERREUR: pythonw.exe introuvable.
    echo =============================================
    echo Installez Python 3.14+ depuis:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Chemin vers le script Python (même dossier que le .bat)
set SCRIPT_PATH="%~dp0pdf-print.py"

:: Vérifie que le script existe
if not exist "%SCRIPT_PATH%" (
    echo =============================================
    echo ERREUR: pdf-print.py introuvable dans %~dp0
    echo =============================================
    pause
    exit /b 1
)

:: Lance le script SANS afficher de fenêtre CMD
start "" "%PYTHON%" "%SCRIPT_PATH%"