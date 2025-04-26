#!/bin/bash

echo "Starting"
# This userdata version doesn't compile engines from scratch;
# just downloads the engine binaries from the github

cd /home/ubuntu
apt update
apt upgrade

sudo apt-get install -y libopenblas-dev # OpenBLAS is needed as a backend for when lc0 is executed

git clone https://github.com/AlanYChen/chess-web-server.git
cd chess-web-server

echo "About to run server.py"
python3 server.py &
echo "End"