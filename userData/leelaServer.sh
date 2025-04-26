#!/bin/bash
cd /home/ubuntu
apt update
apt upgrade

mkdir bin

git clone https://github.com/AlanYChen/chess-web-server-leela.git
mv chess-web-server-leela/lc0-dir bin/lc0-dir

git clone https://github.com/AlanYChen/chess-web-server.git
cd chess-web-server

python3 server.py &