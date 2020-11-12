apt-get update -y
apt-get install gcc supervisor sqlite3 -y
pip install pipenv
PIPENV_VENV_IN_PROJECT=1 pipenv install
PIPENV_VENV_IN_PROJECT=1 pipenv install uwsgi
apt-get install nginx -y
apt-get remove gcc -y
apt-get autoremove -y

mkdir -p /var/cache/nginx/subs