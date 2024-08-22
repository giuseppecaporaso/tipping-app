@echo off
:: Check for Python Installation
python --version 2>NUL
if errorlevel 1 goto errorNoPython

:: Python installed.
REM pip install --target %%g numpy
REM pip install pandas
REM pip install seaborn
REM pip install itertools
REM pip install pyqt6
REM pip install pyqtdarktheme

pip list
python -m pip install -U matplotlib
pip install openpyxl
pip install seaborn
python3 -m pip install PyQt6
pip install pyqtdarktheme

REM Update path below to python.exe if needed.
FOR /f %%p in ('where python') do SET PYTHONPATH=%%p
ECHO %PYTHONPATH%
%PYTHONPATH% tipping_classes.py %*

:: Exit batch file once done
goto:eof

:errorNoPython
echo.
echo Error^: Python not installed

