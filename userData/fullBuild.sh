#!/bin/bash

echo "Starting"
# This userdata version compiles engines from scratch

cd /home/ubuntu
mkdir bin

apt update
apt upgrade

# Leela
git clone https://github.com/AlanYChen/lc0-linux-build
cd lc0-linux-build/0.28

snap install docker # Using the version of docker-compose installed from apt didn't deem to work for some reason
docker-compose up --build # Results in lc0-0.28.tar.gz in this directory
tar -xvzf lc0-0.28.tar.gz -C . # Extract the tarball into lc0-0.28
mv lc0-0.28 ../../bin/lc0

sudo apt-get install -y libopenblas-dev # Needed when lc0 is executed

cd ../..

# Stockfish
git clone https://github.com/official-stockfish/Stockfish
cd Stockfish/src
apt install -y make
apt install -y g++
make build ARCH=x86-64 # after make build, executable file is just named 'stockfish'

cd ../..
mv Stockfish/src/stockfish bin/stockfish

# Final phase!
git clone https://github.com/AlanYChen/chess-web-server.git
cd chess-web-server
echo "About to run server.py"
python3 server.py &