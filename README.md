# socialmedia-project
Hola este es un pequeño proyecto de una red social
Para utilizarlo:
Crea un ambiente virtual
python -m venv socialenv

Instala las dependencias/librerias en requirements.txt
pip install -r requirements.txt

Ejecuta las migraciones.
python manage.py makemigrations python manage.py migrate

Crea un superusuario.
python manage.py createsuperuser

Corre el servidor.
python manage.py runserver
