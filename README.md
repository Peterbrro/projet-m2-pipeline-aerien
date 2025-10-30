#  Projet M2 Data — Pipeline ETL Distribué (Données Aériennes)

##  Auteurs
- **Peter**  
- **Matéo**  
   *Master Big Data et Intelligence Artificielle*

---

##  Objectif du projet

Ce projet a pour but de construire un **pipeline ETL distribué** permettant de collecter, traiter et visualiser en quasi temps réel des **données aériennes** issues d’API publiques.

Nous avons mis en œuvre une architecture complète, conteneurisée avec Docker, intégrant plusieurs outils Big Data afin d’assurer un flux continu depuis la source de données jusqu’à la visualisation finale.

---

##  Architecture globale

**Flux de données :**


Chaque composant a un rôle bien défini :
- **NiFi** → ingestion et transformation des données API  
- **Kafka** → gestion du flux de messages distribué  
- **Spark** → traitement et agrégation en streaming  
- **PostgreSQL** → stockage structuré des résultats  
- **Power BI** → visualisation des indicateurs en temps quasi réel  

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
- Publication des données JSON dans le topic Kafka `flights_positions`

### 2️ Streaming — *Apache Kafka*
- Centralisation du flux d’événements NiFi
- Communication fiable et distribuée entre NiFi et Spark

### 3️ Traitement — *Apache Spark*
- Lecture continue depuis Kafka (Structured Streaming)
- Nettoyage et transformation des données
- Calculs d’agrégations (ex : nombre de vols actifs, vitesse moyenne par pays, altitudes incohérentes)
- Écriture des résultats dans PostgreSQL

### 4️ Stockage — *PostgreSQL*
```sql
CREATE TABLE flights_agg (
    timestamp TIMESTAMP,
    icao24 VARCHAR,
    country VARCHAR,
    altitude FLOAT,
    speed FLOAT,
    lat FLOAT,
    lon FLOAT
);
