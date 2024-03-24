import os
import shutil
import subprocess

# Répertoire source de votre projet Flask
source_directory = os.path.join(os.path.dirname(__file__), 'api_videoDownloader')

# Répertoire de destination pour le déploiement Elastic Beanstalk
destination_directory = os.path.join(os.path.dirname(__file__), 'build')

# Fichier ZIP de destination
zip_filename = f'{destination_directory}.zip'

# Supprimer le fichier ZIP de destination s'il existe déjà
if os.path.exists(zip_filename):
    os.remove(zip_filename)
    print(f'Fichier {zip_filename} supprimé.')

# Supprimer le dossier de destination s'il existe déjà
if os.path.exists(destination_directory):
    shutil.rmtree(destination_directory)
    print(f'Dossier {destination_directory} supprimé.')

# Exécuter la commande "pip freeze > requirements.txt" dans le répertoire source
subprocess.run(['pip3', 'freeze'], stdout=open(f'{source_directory}/requirements.txt', 'w'))

# Copier les fichiers du projet Flask dans le répertoire de destination
shutil.copytree(source_directory, destination_directory)


# Créer un fichier ZIP à partir du répertoire de destination
shutil.make_archive(destination_directory, 'zip', destination_directory)

print('Dossier de déploiement pour Elastic Beanstalk créé avec succès.')
