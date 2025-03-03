
# Nom du Projet Django

## Prérequis

- Python 3.x
- pip
- PostgreSQL

## Installation
### Installer la base de donées
#### Installer PostgreSQL :

Pour installer PostgreSQL et le client psql, utilisez la commande suivante :

```bash
sudo pacman -S postgresql
```
#### Configurer PostgreSQL :

Après l'installation, PostgreSQL est configuré pour démarrer automatiquement en tant que service.
Vous devez également créer un utilisateur et une base de données pour commencer à utiliser PostgreSQL.



Pour démarrer le service PostgreSQL et l'activer au démarrage, exécutez :

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```
**si vous rencontrez un problème cette commande peut vous aider :**
```bash
sudo su - postgres -c "initdb --locale=C.UTF-8 --encoding=UTF8 -D '/var/lib/postgres/data'"
```

### Créer et activer l'environnement virtuel

```bash
python -m venv env
source env/bin/activate  # Sur Windows utilisez `env\Scripts\activate`
```

### Installer les dépendances

```shell
pip install -r requirements.txt
```

## Configuration de la base de données

### PostgreSQL

1. Assurez-vous que PostgreSQL est installé et en cours d'exécution.
2. Créez une base de données et un utilisateur pour votre projet Django :

```bash
sudo -u postgres psql
```
```postgresql
CREATE DATABASE tennisarsacbackenddev;
CREATE USER tennisarsacuser WITH PASSWORD 'tennis_sarsac109ZDFDSLFK!!:QSD';
GRANT ALL PRIVILEGES ON DATABASE tennisarsacbackenddev TO tennisarsacuser;
ALTER DATABASE tennisarsacbackenddev OWNER TO tennisarsacuser;

````

* Reset database
```postgresql
DROP DATABASE tennisarsacbackenddev;
CREATE DATABASE tennisarsacbackenddev;
GRANT ALL PRIVILEGES ON DATABASE tennisarsacbackenddev TO tennisarsacuser;
ALTER DATABASE tennisarsacbackenddev OWNER TO tennisarsacuser;
````


3. Mettez à jour la section `DATABASES` dans `settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tennisarsacbackenddev',
        'USER': 'tennisarsacuser',
        'PASSWORD': 'tennis_sarsac109ZDFDSLFK!!:QSD',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

## Application des migrations

```shell
python manage.py migrate
```

## Création d'un super utilisateur

```shell
python manage.py createsuperuser
```
## Créer l'API key
Se mettre à la racine du dossier (ou il y a le .git).
```bash
export DJANGO_SETTINGS_MODULE=Backend.settings
```
Ouvrir le shell de Django
```bash
python manage.py shell
```
Créer l'api Key
```python
from rest_framework_api_key.models import APIKey
api_key, key = APIKey.objects.create_key(
    name="Api_key"
)
print("Clé générée :", key)
```

## Ajout des données en base
```bash
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/initial_images.json
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/initial_sponsors.json
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/initial_club_value.json
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/initial_pricings.json
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/initial_training.json
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/initial_routes.json
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/initial_renders_navigation_items.json
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/pages/initial_home_pages.json
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/pages/initial_navigation_bars.json
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/pages/initial_pricing_pages.json
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/pages/initial_about_pages.json
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/initial_professors.json
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/initial_team_members.json
python manage.py loaddata BackendTennis/fixtures/init_tennis_db/pages/initial_team_pages.json

```


## Lancer le serveur de développement

* Pour lancer le serveur en HTTPS
  * Créer votre certificat auto-signé
    ```shell
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout dev.key -out dev.crt 
    ```
  * Lancer le serveur avec votre certificat
    ```shell
    python manage.py runserver_plus --cert-file certs/dev.crt --key-file certs/dev.key
    ```
* Sinon 
```shell
python manage.py runserver
```

## Accéder à l'application

Ouvrez votre navigateur et accédez à [http://127.0.0.1:8000](http://127.0.0.1:8000)

## SETUP des TU

```bash
sudo -u postgres psql
```
```postgresql
CREATE DATABASE test_tennisarsacbackenddev;
CREATE USER testuser WITH PASSWORD 'testpassword';
GRANT ALL PRIVILEGES ON DATABASE test_tennisarsacbackenddev TO testuser;
ALTER DATABASE test_tennisarsacbackenddev OWNER TO testuser;
```



## Traductions  
### Génération des traductions
```shell
django-admin makemessages -l fr --ignore 'venv/*'
```

Une fois génerer, il faut remplir les traductions, elles ne sont pas faites automatiquement, vous pouvouz trouver les fichiers dans "locale/"


### Compilation
```shell
django-admin compilemessages --ignore  'venv/*'
```


## Envoie de mail 
### GMAIL
Si le smpt de gmail est utilisé, il est nécessaire que le compte gmail utilisé pour se connecter ait un mot de passe pour l'application:
* Connectez-vous a google avec le compte que vous voulez utiliser
* Allez sur ce lien : https://myaccount.google.com/apppasswords
* Créer un mot de passe pour l'application
* Ajouter le mot de passe dans le .env dans la variable EMAIL_HOST_PASSWORD (sans crochet)