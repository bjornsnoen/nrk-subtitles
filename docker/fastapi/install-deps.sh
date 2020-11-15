set -e
apt-get update -y
apt-get install gcc supervisor sqlite3 libnginx-mod-http-lua nginx -y
pip install pipenv
PIPENV_VENV_IN_PROJECT=1 pipenv install
apt-get remove gcc -y
apt-get autoremove -y

mkdir -p /var/cache/nginx/subs