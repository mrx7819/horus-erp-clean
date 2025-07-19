@echo off
REM Ruta donde tienes el entorno virtual (reemplaza con la tuya)
set VENV_PATH=C:\Users\frail\Desktop\Capstone\erp_pyme\venv
REM Ruta donde tienes el archivo manage.py de tu proyecto
set PROJECT_PATH=C:\Users\frail\Desktop\Capstone\erp_pyme

REM Activa el entorno virtual
call %VENV_PATH%\Scripts\activate.bat

REM Cambia al directorio del proyecto
cd %PROJECT_PATH%

REM Ejecuta el servidor de Django
python manage.py runserver

REM Mantén la ventana abierta si el servidor se cierra inesperadamente
pause
