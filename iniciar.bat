@echo off
:: Cambia al directorio del entorno virtual
cd venv
cd Scripts

:: Activa el entorno virtual
call .\activate

:: Regresa a la carpeta del proyecto
cd ..
cd ..

:: Ejecuta el servidor de Django
py manage.py runserver

:: Mantén la ventana abierta en caso de que haya errores
pause
