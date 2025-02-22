Voici une documentation pour utiliser vos microservices Flask :

# Documentation des Microservices de Gestion de Requêtes

## 1. Aperçu
Le système comprend deux microservices :
- **Service 1** (Port 5000) : Service principal avec base de données SQLite
- **Service 2** (Port 5001) : Service secondaire avec base de données PostgreSQL

Les deux services fournissent des endpoints RESTful pour :
- Créer des requêtes
- Lister toutes les requêtes

## 2. Documentation Swagger
Chaque service dispose d'une interface Swagger intégrée :
- Service 1: http://localhost:5000/docs
- Service 2: http://localhost:5001/docs

L'interface Swagger permet de :
- Voir tous les endpoints disponibles
- Tester les API directement depuis le navigateur
- Consulter les modèles de requêtes/réponses

## 3. Endpoints Principaux

### 3.1 Création de Requête
**Service 1**:
```
POST http://localhost:5000/query
```
**Service 2** (appelé automatiquement par Service 1):
```
POST http://localhost:5001/query
```

### 3.2 Liste des Requêtes
**Service 1**:
```
GET http://localhost:5000/queries
```

**Service 2**:
```
GET http://localhost:5001/queries
```

Exemple de réponse :
```json
[
  {"id": 1, "content": "Première requête"},
  {"id": 2, "content": "Deuxième requête"}
]
```

### 3.3 Suppression de Requête
**Service 1**:
```
DELETE http://localhost:5000/query/1
```

**Service 2** (appelé automatiquement par Service 1):
```
DELETE http://localhost:5001/query/1
```

## 4. Configuration et Démarrage

### Prérequis
- Python 3.11
- Packages requis :
  ```bash
  pip install -r requirements.txt
  ```

### Lancement des services
1. Service 2 (PostgreSQL):
   ```bash
   python service2.py
   ```

2. Service 1 (SQLite):
   ```bash
   python service1.py
   ```

## 5. Workflow d'Utilisation

1. Création d'une requête :
   - Envoyer POST à Service 1
   - La requête est automatiquement répliquée dans Service 2

2. Consultation :
   - Les GET peuvent être faits sur les deux services indépendamment

3. Suppression :
   - Envoyer DELETE à Service 1
   - La suppression est propagée à Service 2


## 4. Architecture des Données
**Structure de la table Query**:
- id (Integer, clé primaire)
- content (String(200))

Cette documentation couvre les principales fonctionnalités des microservices. Pour plus de détails techniques, consulter la documentation Swagger intégrée de chaque service.
