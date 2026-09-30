# Data Center Monitoring — Guide de passation

Ce document explique comment reprendre en main le projet, obtenir un accès administrateur, et relancer l'ensemble des services.

## 1. Prérequis

- Docker et Docker Compose installés
- Accès au dépôt/dossier du projet (`~/datacenter-monitoring/`)
- Un fichier `.env` à la racine du projet (voir section 4) — **à demander séparément, ne jamais le transmettre par email ou chat en clair**

## 2. Lancer le projet

Depuis la racine du projet :

```bash
cd ~/datacenter-monitoring
docker compose up -d
```

Vérifier que tout tourne :

```bash
docker compose ps
```

Tous les services doivent être à l'état `Up` :
`postgres`, `cleaning`, `collector`, `web`, `simulator`, `snmp-sim`, `modbus-sim`, `grafana`.

## 3. Accès aux interfaces

| Service | URL | Notes |
|---|---|---|
| Site web (login, dashboard, admin) | http://localhost:5002 | Page de connexion : `/login` |
| Grafana | http://localhost:3000 | Identifiants dans `.env` (`GRAFANA_ADMIN_PASSWORD`) |

## 4. Se créer un compte administrateur

**Important : ne jamais partager un mot de passe admin existant.** Chaque personne doit avoir son propre compte, créé via la procédure ci-dessous — le mot de passe n'est ainsi jamais connu par quelqu'un d'autre que la personne elle-même.

Depuis la machine où tourne le projet (ou en SSH dessus) :

```bash
cd ~/datacenter-monitoring/web
python3 create_admin.py
```

Le script demande interactivement :
- Un nom d'utilisateur
- Un email
- Un mot de passe (min. 8 caractères)

La personne qui prend la main doit exécuter ce script **elle-même**, ou le faire pendant un appel/partage d'écran, pour choisir son propre mot de passe sans le communiquer à qui que ce soit.

### Alternative si `create_admin.py` n'est pas accessible directement

Si le projet tourne sur un serveur distant, il est possible d'exécuter le script à l'intérieur du conteneur `web` :

```bash
docker exec -it web python3 create_admin.py
```

(à condition que le script soit copié dans l'image du conteneur — vérifier avant utilisation)

## 5. Une fois connecté en tant qu'admin

Aller sur :
```
http://localhost:5002/admin/users
```

Cette page permet de :
- Créer des comptes employés (nom + email professionnel)
- Le système génère un mot de passe temporaire, envoyé automatiquement par email à l'employé
- L'employé doit changer ce mot de passe à sa première connexion

## 6. Secrets à transmettre séparément (jamais dans ce document ni en clair)

À communiquer via un canal sécurisé (gestionnaire de mots de passe partagé, appel vocal, etc.) :

- Contenu du fichier `.env` (racine du projet) : mots de passe DB, clé secrète Flask, identifiants SMTP
- Mot de passe admin PostgreSQL si accès direct à la base est nécessaire

## 7. Structure du projet (aperçu rapide)

```
datacenter-monitoring/
├── web/          → Site Flask (auth, dashboard, admin)
├── collector/    → Collecte des données SNMP/Modbus
├── cleaning/     → Nettoyage, validation, détection d'anomalies
├── simulator/    → Génère des données d'équipements simulées
├── snmp-sim/     → Simulateur SNMP
├── modbus-sim/   → Simulateur Modbus
├── grafana/      → Config Grafana (dashboards à exporter en JSON)
├── kubernetes/   → Manifests K8s (en cours de développement)
└── docker-compose.yml
```

## 8. Contact / questions

En cas de blocage sur le déploiement Docker, vérifier en priorité :
- L'espace disque disponible (`df -h`) — Grafana et les autres services peuvent échouer silencieusement si le disque est plein
- Que tous les ports nécessaires (5000, 5002, 3000, 5433, 5020, 11611) sont libres sur la machine hôte
