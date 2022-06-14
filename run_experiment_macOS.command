#!/usr/bin/env bash

set -e #errors will cause script to exit immediately

#change directory to location of this bash script
cd "`dirname -- "$0"`"

#make sure the logs dir exists
mkdir -p logs

#redirect output to log file (from: https://serverfault.com/a/103569/72634)
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>logs/console_`date +"%Y_%m_%d_%H_%M_%S"`.log 2>&1

cd app_code
BREW_HOME=~/.homebrew
export PATH=$BREW_HOME/bin:$PATH
export PYENV_ROOT=~/.pyenv
export PATH=$PYENV_ROOT/bin:$PATH
echo $PATH

echo "">&3
echo "">&3

#check if the venv folder already exists
if [[ -d "venv" ]];
then
	echo '[CAST] Folder "venv" found, starting app...' >&3
	#if it does, activate & run
	eval "$(pyenv init --path)"
	pyenv rehash
	if [ "$(uname)" == "Darwin" ]
	then
		export PATH="$(brew --prefix)/opt/gnu-sed/libexec/gnubin:$PATH"
	fi
	sed -i '43s/.*/VIRTUAL_ENV="$(cd "$(dirname "$(dirname "${BASH_SOURCE[0]}" )")" \&\& pwd)"/' venv/bin/activate
	sed -i '1s/.*/#!\/usr\/bin\/env python/' venv/bin/pip*
	source venv/bin/activate
	python3.10 main.py site_specific_experiment/experiment.py
	echo "[CAST] App terminated. You may now close this window." >&3
	read -p "" x && exit
fi

echo '[CAST] Folder "venv" not found, checking dependencies...' >&3

if [ "$(uname)" == "Darwin" ]
then
	if ! command -v xcode-select &> /dev/null
	then #xcode is absent
		echo '[CAST] Installing Xcode...' >&3
		XCODE_MESSAGE="$(osascript -e 'tell app "System Events" to display dialog "Please click \"install\" when Command Line Developer Tools appears"')"
		if [ "$XCODE_MESSAGE" = "button returned:OK" ]; then
			xcode-select --install
			until ["$(xcode-select -p)"]; do
				echo -n "." >&3
				sleep 1
			done
			echo '[CAST] Xcode installed.' >&3
		else
			echo "[CAST] You have cancelled the installation, please rerun the installer." >&3
			exit
		fi
	else
		echo '[CAST] Found Xcode.' >&3
	fi
else
	#we're on linux, so install dependencies
	#python (from https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
	sudo apt-get update
	sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
	libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
	libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
	#app
	sudo apt install -y libhdf5-dev libsdl2-2.0-0 libsdl2-gfx-1.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0 libportaudio2 libsndfile1
fi


if [ "$(which brew)" ]
then
	echo "[CAST] Found brew." >&3
else
	#install brew "locally" to ~/.homebrew (avoids needing admin rights)
	echo '[CAST] Installing brew...' >&3
	mkdir $BREW_HOME
	curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C $BREW_HOME
	eval "$($BREW_HOME/bin/brew shellenv)"
	brew update --force --quiet
	chmod -R go-w "$(brew --prefix)/share/zsh"
	echo '[CAST] Brew installed.' >&3
fi

echo '[CAST] Installing pyenv dependencies via brew...' >&3
#install python-building dependencies on mac
if [ "$(uname)" == "Darwin" ]
then
	brew install openssl readline sqlite3 xz zlib gnu-sed
	export PATH="$(brew --prefix)/opt/gnu-sed/libexec/gnubin:$PATH"
else
	#on linux, need gcc (even though we installed it already)
	brew install gcc 
fi
echo '[CAST] Pyenv dependencies installed.' >&3

echo '[CAST] Installing pyenv...' >&3
brew install pyenv 
eval "$(pyenv init --path)"
echo '[CAST] Pyenv installed.' >&3

echo '[CAST] Installing Python 3.10 ... ' >&3

if [ "$(uname)" == "Darwin" ]
then
	pyenv install -s --verbose 3.10.0
else
	CC="$(brew --prefix gcc)/bin/gcc-11" \
	CFLAGS="$(pkg-config --cflags libffi)" \
	LDFLAGS="$(pkg-config --libs libffi)" \
	pyenv install -s --verbose 3.10.0
fi

pyenv rehash
echo '[CAST] Python 3.10 Installed.' >&3

echo "[CAST] Creating venv..." >&3
python3.10 -m venv --copies venv
#hack from: https://aarongorka.com/blog/portable-virtualenv/
sed -i '43s/.*/VIRTUAL_ENV="$(cd "$(dirname "$(dirname "${BASH_SOURCE[0]}" )")" \&\& pwd)"/' venv/bin/activate
sed -i '1s/.*/#!\/usr\/bin\/env python/' venv/bin/pip*
source venv/bin/activate
echo "[CAST] Installing python packages..." >&3
python3.10 -m pip install --upgrade setuptools
python3.10 -m pip install --upgrade pip
python3.10 -m pip install wheel
python3.10 -m pip install -r requirements.txt
echo "[CAST] Starting app..." >&3
sudo python3.10 main.py site_specific_experiment/experiment.py
echo "[CAST] App terminated. You may now close this window." >&3
read -p "" x && exit
