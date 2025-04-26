#!/bin/bash
cd /home/ubuntu
apt update
apt upgrade
mkdir bin

sudo apt-get install -y libopenblas-dev # OpenBLAS is needed as a backend for when lc0 is executed

git clone https://github.com/AlanYChen/chess-web-server-leela.git
mv chess-web-server-leela/lc0-dir bin/lc0-dir
rmdir chess-web-server-leela

git clone https://github.com/AlanYChen/chess-web-server.git
cd chess-web-server

python3 server.py &