if [[ $# -ne 1 ]]; then
    echo "Ingrese el entorno a habilitar"
    exit 2
fi

ln -sf $(dirname -- "$(realpath -- $0;)";)/$1 /etc/nginx/sites-enabled/$1
sudo systemctl restart nginx.service