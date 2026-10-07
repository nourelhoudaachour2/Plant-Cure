<h1 align="center">Plant Cure</h1>

<p align="center"><b>Application web de diagnostic des maladies des plantes par Deep Learning, avec recommandations de traitement par IA</b></p>

<p align="center">
  <img src="https://img.shields.io/badge/TensorFlow-Modele%20CNN-FF6F00?logo=tensorflow&logoColor=white" alt="TensorFlow">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/OpenAI-Recommandations-412991?logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/Docker-Conteneurs-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes&logoColor=white" alt="Kubernetes">
  <img src="https://img.shields.io/badge/Google%20Cloud-Deploiement-4285F4?logo=googlecloud&logoColor=white" alt="Google Cloud">
</p>

---

## À propos

**Plant Cure** est une application full stack qui permet à un utilisateur de **téléverser la photo d'une feuille de plante** et d'obtenir instantanément la maladie détectée, accompagnée de **conseils de traitement et de prévention** générés par l'IA.

Les maladies des plantes causent d'importantes pertes agricoles et leur identification demande souvent un expert. Plant Cure rend ce diagnostic accessible à tous, en quelques secondes.

Le projet est composé de trois applications indépendantes, chacune dans son propre conteneur Docker :

| Application | Rôle | Technologies |
|---|---|---|
| `frontend` | Interface utilisateur : envoi de l'image, affichage du diagnostic et de l'historique | HTML, CSS, JavaScript, Nginx |
| `backend` | API : orchestration, historique des diagnostics, recommandations | FastAPI, Python, OpenAI API |
| `model_service` | Prédiction de la maladie à partir de l'image | TensorFlow, Keras |

---

## Fonctionnalités

- Téléversement d'une photo de feuille depuis l'interface web
- Détection de la maladie (38 classes, y compris plante saine)
- Recommandations de traitement et de prévention générées par OpenAI
- Historique des diagnostics
- Trois environnements séparés : `dev`, `test`, `prod`

---

## Architecture

```
Utilisateur --> Frontend (Nginx) --> Backend (FastAPI) --> Model Service (TensorFlow)
                                           |
                                           +--> OpenAI API (recommandations)
```

1. L'utilisateur envoie une image via le frontend.
2. Le backend transmet l'image au service de modèle.
3. Le CNN renvoie la classe de maladie prédite.
4. Le backend interroge OpenAI pour obtenir les recommandations.
5. Le résultat est affiché à l'utilisateur et enregistré dans l'historique.

---

## Modèle de Deep Learning

| Élément | Détail |
|---|---|
| Dataset | PlantVillage (images en couleur) |
| Classes | 38 |
| Architecture | 4 blocs Conv2D + MaxPooling, Dense(512) + Dropout(0.5), Dense(38) + Softmax |
| Précision | environ 84 à 89 % en validation |
| Framework | TensorFlow / Keras |
| Fichier | `model/plant_disease_prediction_model.keras` (stocké avec Git LFS) |

---

## Structure du dépôt

```
Plant-Cure/
├── frontend/              # Interface web (Nginx + static)
├── model_service/         # Service de prédiction TensorFlow
├── services/              # Service de recommandation (OpenAI)
├── model/                 # Modèle CNN entraîné (Git LFS)
├── data/                  # Historique des diagnostics par environnement
├── k8s/                   # Manifests Kubernetes (dev / test / prod)
├── main.py                # API backend FastAPI
├── utils.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Installation et lancement

### Prérequis

- Docker et Docker Compose
- Git LFS
- Une clé API OpenAI

### 1. Cloner le dépôt

```bash
git lfs install
git clone https://github.com/nourelhoudaachour2/Plant-Cure.git
cd Plant-Cure
```

### 2. Configurer les variables d'environnement

Créer un fichier `.env` à la racine (non versionné pour des raisons de sécurité) :

```env
OPENAI_API_KEY=votre_cle_openai
```

### 3. Lancer l'application

```bash
docker-compose up --build
```

---

## Déploiement

| Outil | Utilisation |
|---|---|
| Docker | Une image par service |
| Kubernetes | Manifests par environnement dans `k8s/dev`, `k8s/test` et `k8s/prod` (namespace, deployment, service, configmap, ingress) |
| Google Cloud | Hébergement de l'application |

---

## Technologies utilisées

`Python` · `TensorFlow` · `Keras` · `FastAPI` · `OpenAI API` · `Docker` · `Kubernetes` · `Nginx` · `Google Cloud` · `JavaScript`

---

## Auteure

**Nour El Houda Achour**
Cycle Ingénieur Génie Logiciel et Applications, IT Business School (ITBS)

GitHub : [@nourelhoudaachour2](https://github.com/nourelhoudaachour2)
