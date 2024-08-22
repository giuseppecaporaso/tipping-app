REM conda create --name py311
:: Check for Python Installation
python --version 2>NUL
if errorlevel 1 goto errorNoPython

REM FOR /F "tokens=*" %%g IN ('where python.exe') do (SET VAR=%%g)

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
FOR /F "tokens=*" %%g IN ('where python') do (SET VAR=%%g)
%%g tipping_classes.py %*

:: Exit batch file once done
goto:eof

:errorNoPython
echo.
echo Error^: Python not installed

