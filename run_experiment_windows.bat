@echo off
cd "%~dp0"
cd app_code
setx PYENV "pyenv\pyenv-win\"
setx PYENV_HOME "pyenv\pyenv-win\"
setx PYENV_ROOT "pyenv\pyenv-win\"
setx PATH "pyenv\pyenv-win\bin;pyenv\pyenv-win\shims;%PATH%"
if exist venv (
cmd /k ^
win\RefreshEnv.cmd ^
& pyenv rehash ^
& .\venv\Scripts\activate.bat ^
& python main.py ..\experiment.py
) else (
echo Installing dependencies... (this could take a while!)
cmd /k ^
xcopy "win\pyenv-win" "pyenv\" /s /i /Y ^
& win\RefreshEnv.cmd ^
& pyenv update ^
& pyenv install 3.10.0 ^
& pyenv local 3.10.0 ^
& pyenv rehash ^
& python -m venv venv ^
& .\venv\Scripts\activate.bat ^
& python -m pip install --upgrade pip ^
& python -m pip install wheel ^
& python -m pip install win\h5py-3.6.0-cp310-cp310-win_amd64.whl ^
& python -m pip install win\aggdraw-1.3.12-cp310-cp310-win_amd64.whl ^
& python -m pip install -r requirements.txt ^
& python main.py site_specific_experiment\experiment.py
)
