# prode-back

### Activar el entorno virtual
En windows:
```sh
.\dev\Scripts\activate
```
En linux:
```sh
source dev/bin/activate
```

### Crear DB sino existe o no tiene datos
Ingresar a la carpeta donde se encuentre "manage.py" y ejecutar:
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```

### Lanzar Django
Ingresar a la carpeta donde se encuentre "manage.py" y ejecutar:
```sh
python manage.py runserver 0.0.0.0:8000
```

### Configurar NGINX
Lanzar:
```sh
./nginx/enable.sh <entorno>
```