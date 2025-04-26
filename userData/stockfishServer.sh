#!/bin/bash
cd /home/ubuntu
apt update
apt upgrade

mkdir bin

git clone https://github.com/AlanYChen/chess-web-server-stockfish.git
mv chess-web-server-stockfish/stockfish bin/stockfish
rm -rf chess-web-server-stockfish

git clone https://github.com/AlanYChen/chess-web-server.git
cd chess-web-server

python3 server.py &