# Traitement d'images :mountain:

*Par Gautier Jaulin, Baptiste Plaut-Aubry, Pablo Berecoechea*

![Photo montagne dossier data](Data/2007041608_cam01p.jpg)

> ***Livrable : 1/3***

## SOMMAIRE

1. [**Objectif du projet**](#objectif-du-projet)
2. [**Organisation du dossier**](#organisation-du-dossier)
3. [**Prérequis**](#prérequis)
4. [**Prérequis**](#installation)
    1. [Git](#git)
    2. [Préparation de l'environnement virtuel](#préparation-de-lenvironnement-virtuel)
        1. [*Sur un environnement Linux*](#sur-un-environnement-linux)
        2. [*Sur un environnement Windows*](#sur-un-environnement-windows)
    3. [Installation des dépendences](#installation-des-dépendences)
        1. [*Sur un environnement Linux*](#sur-un-environnement-linux-1)
        2. [*Sur un environnement Windows*](#sur-un-environnement-windows-1)
5. [**Exécution**](#exécution)
    1. [Exécution dans un environnement virtuel](#exécution-dans-un-environnement-virtuel)
        1. [*Sur un environnement Linux*](#sur-un-environnement-linux-2)
        2. [*Sur un environnement Windows*](#sur-un-environnement-windows-2)
6. [**Résultats**](#résultats)


## Objectif du projet

> à remplir

## Organisation du dossier

```
ti-compressed-sensing/
├─ src/
│  ├─ constants.py
│  ├─ image_processing.py
│  ├─ __init__.py
├─ Data/
│  ├─ 2007041608_cam01p.jpg
|  ├─ ...
├─ .gitignore
├─ main.py
├─ README.md
├─ requirements.txt

```

## Prérequis

* Avoir installé Python 3.10 (+).
* (Optionel) Avoir installé git. 

## Installation

### Git 

Si le dossier du projet n'est pas déjà installé, vous pouvez le cloner depuis le dépôt [`🗃️ Github`](https://github.com/pberecoechea/ti-compressed-sensing.git). Pour cela, ouvrez un terminal, déplacez vous dans le dossier où vous souhaitez placer le projet et exécutez :

```bash
git clone https://github.com/pberecoechea/ti-compressed-sensing.git
```

### Préparation de l'environnement virtuel

Pour commencer à préparer l'environnement virtuel, il faut se déplacer dans le dossier racine `📁 ti-compressed-sensing` et exécuter :

```bash
python -m venv venv
```

Une fois l'environnement virtuel installé, il faudra l'activer grâce à la commande suivante :

#### Sur un environnement Linux

```bash
source venv/bin/activate
```

#### Sur un environnement Windows

```shell
venv/Scripts/activate
```

Par la suite et pour l'exécution du projet, il faudra toujours activer l'environnement virtuel au préalable.

### Installation des dépendences

Le nouvel environnement virtuel ne possède pas encore les dépendences du projets. Il faudra donc les installer. Pour cela, exécutez les commandes suivantes :

#### Sur un environnement Linux
```bash
venv/bin/pip install -r requirements.txt
```

#### Sur un environnement Windows

```shell
venv/Scripts/pip install -r requirements.txt
```

## Exécution

Pour exécuter le programme, lancez un terminal dans le fichier racine du projet. Ouvrez un terminal, lancez l'environnement virtuel et exécutez :

### Exécution dans un environnement virtuel
 
#### Sur un environnement Linux

```bash
venv/bin/python main.py
```

#### Sur un environnement Windows

```shell
venv/Scripts/python main.py
```

## Résultats

Pour le premier rendu, le résultat sera l'image initiale recréée après être transformée en vecteur puis de nouveau en image. Ce résultat sera dans le dossier `📁 results`, dossier créé après exécution du programme.