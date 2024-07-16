
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

```sh
pip install -r requirement.txt
```

## Configuration de la base de données

### PostgreSQL

1. Assurez-vous que PostgreSQL est installé et en cours d'exécution.
2. Créez une base de données et un utilisateur pour votre projet Django :

```bash
sudo -u postgres psql
CREATE DATABASE tennisarsacbackenddev;
CREATE USER tennisarsacuser WITH PASSWORD 'tennis_sarsac109ZDFDSLFK!!:QSD';
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

```sh
python manage.py migrate
```

## Création d'un super utilisateur

```sh
python manage.py createsuperuser
```

## Lancer le serveur de développement

```sh
python manage.py runserver
```

## Accéder à l'application

Ouvrez votre navigateur et accédez à [http://127.0.0.1:8000](http://127.0.0.1:8000)