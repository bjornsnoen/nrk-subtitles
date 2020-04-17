apt-get update -y
apt-get install gcc supervisor -y
pip install -r requirements.txt
apt-get install nginx -y
apt-get remove gcc -y
apt-get autoremove -y

mkdir -p /var/cache/nginx/subs