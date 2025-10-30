#  Projet M2 Data — Pipeline ETL Distribué (Données Aériennes)

##  Auteurs
- **Peter Broussaud**  
- **Matéo Guillard**  
   *Master Big Data et Intelligence Artificielle*

---

##  Objectif du projet

Ce projet a pour but de construire un **pipeline de données distribuées** permettant de collecter, traiter et visualiser en quasi temps réel des **données aériennes** issues d’API publiques.

Nous avons mis en œuvre une architecture, conteneurisée avec Docker, intégrant plusieurs outils Big Data afin d’assurer un flux depuis la source de données jusqu’à la visualisation finale.

---

##  Architecture globale

**Flux de données :**

- **NiFi** → ingestion et transformation des données API  
- **Kafka** → gestion du flux de messages distribué  
- **Spark** → traitement et agrégation des données  
- **PostgreSQL** → stockage structuré des résultats  
- **Power BI** → visualisation des indicateurs
*(Un schéma d’architecture est fourni dans le dossier `/schema`.)*

---

##  Environnement & Technologies

| Composant | Rôle principal | Port (Docker) |
|------------|----------------|---------------|
| Apache NiFi | Ingestion des données (API → Kafka) | 8080 |
| Apache Kafka | Message broker distribué | 9092 |
| Apache Spark | Traitement distribué des flux | 4040 |
| PostgreSQL | Base de données relationnelle | 5432 |
| Power BI | Outil de visualisation | — |

Tous les services sont déployés et orchestrés via **Docker Compose**.

---

##  Pipeline de traitement

### 1 Ingestion — *Apache NiFi*
- Appel des API
- Extraction et nettoyage des champs utiles (timestamp, icao24, lat, lon, altitude, vitesse, pays…)
- Publication des données JSON dans le topic Kafka `quickstart`

### 2️ Streaming — *Apache Kafka*
- Centralisation du flux d’événements NiFi
- Communication distribuée entre NiFi et Spark

### 3️ Traitement — *Apache Spark*
- Lecture continue depuis Kafka (Structured Streaming)
- Nettoyage et transformation des données
- Calculs d’agrégations 
- Écriture des résultats dans PostgreSQL

### 4️ Stockage — *PostgreSQL*
```sql
CREATE TABLE aeroport ( airport_id,name,type,country,longitude,latitude,elevation_value
    airport_id VARCHAR,
    name VARCHAR,
    type FLOAT,
    country VARCHAR,
    longitude FLOAT,
    latitude FLOAT,
    elevation_value FLOAT
);
