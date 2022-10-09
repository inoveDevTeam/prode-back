ln -sf echo $(dirname -- "$(realpath -- $0;)";)/wololo /etc/nginx/sites-enabled/wololo
sudo systemctl restart nginx.service