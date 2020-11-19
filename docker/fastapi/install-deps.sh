set -e
apt-get update -y
apt-get install gcc supervisor sqlite3 libnginx-mod-http-lua nginx curl -y
curl -sL https://deb.nodesource.com/setup_14.x | bash -
apt-get install -y nodejs

pip install pipenv
npm install -g yarn

apt-get autoremove -y