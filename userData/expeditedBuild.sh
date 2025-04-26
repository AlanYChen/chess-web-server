# This userdata version doesn't compile engines from scratch;
# just downloads the engine binaries from the github

apt update; apt upgrade
cd /home/ubuntu

sudo apt-get install -y libopenblas-dev # OpenBLAS is needed as a backend for when lc0 is executed

git clone https://github.com/AlanYChen/chess-web-server.git
cd chess-web-server
cd bin
chmod 100 lc0 # By default, these binaries have the permission of rw-r--r-- (644)
chmod 100 stockfish

python3 server.py &