# Arkalia Luna System

Je construis des projets Python (et un peu de Flutter) autour de la robotique,
du jeu et de la santé. Ce n'est pas un produit unique : plusieurs dépôts,
dont trois que je maintiens vraiment.

## En bref

- **Sujets** : robotique (Reachy Mini), jeu narratif web, assistant santé mobile, Azure en préparation.
- **Périmètre** : 13 projets suivis (repositories GitHub), archives comprises.
- **Mise à jour** : `update-profile.py` et `auto-update-readme.py`.

## Parcours cloud

Je prépare l'administration Azure. **Je n'ai pas encore le badge AZ-104.**

- **AZ-900** : Microsoft Learn + tests blancs (ce n'est pas un badge Credly affiché ici).
- **AZ-104** : en préparation · examen prévu le **09/10/2026** (OnVUE).
- **Labs** : parcours Microsoft Learn et labs (réseau, stockage, calcul, backup, monitor) sur un abonnement réel.
- **Notes publiques** : [az104-portfolio](https://github.com/arkalia-luna-system/az104-portfolio) (règles, schémas, pas de dumps d'examen).

Le dépôt de révision perso reste privé. Après le badge Credly, cette section sera mise à jour (date + lien), pas avant.

## Activité récente

Les dates viennent de GitHub (`pushed_at`), fuseau Europe/Paris.

<!-- AUTO-UPDATE:status -->
| Dépôt | Rôle | Statut | Dernier commit (Europe/Paris) | Branche |
|:------|:-----|:------:|:------------------------------|:--------|
| **[bbia-sim](https://github.com/arkalia-luna-system/bbia-sim)** | Robotique | Actif | 20/07/2026 11:10 CEST | `main` |
| **[arkalia-quest](https://github.com/arkalia-luna-system/arkalia-quest)** | Jeu | Actif | 21/07/2026 02:33 CEST | `main` |
| **[arkalia-cia](https://github.com/arkalia-luna-system/arkalia-cia)** | Santé / Mobile | Bêta | 14/08/2026 16:43 CEST | `main` |
| **[arkalia-luna-pro](https://github.com/arkalia-luna-system/arkalia-luna-pro)** | R&D | Actif | 14/08/2026 16:44 CEST | `develop` |
| **[arkalia-luna-system](https://github.com/arkalia-luna-system/arkalia-luna-system)** | Profil | Actif | 14/08/2026 16:41 CEST | `develop` |
## Comment c'est organisé

<!-- AUTO-UPDATE:vision -->
### Organisation

Les dépôts se regroupent à peu près comme ça :

#### Projets principaux
Les dépôts applicatifs, pas tous au même rythme :
- **arkalia-luna-pro** : Orchestrateur IA expérimental, Python et Docker.
- **arkalia-cia** : Assistant santé mobile Flutter, hors ligne. En bêta.
- **arkalia-quest** : Jeu narratif web (Flask) pour ados, autour d'une...
- **bbia-sim** : Simulation et moteur cognitif Python pour Reachy Mini.

#### Design
Outils visuels, plutôt perso :
- **Arkalia-luna-logo** : Générateur de logos SVG, usage perso, peu actif.

#### Outillage
Scripts, templates, notes, ce profil :
- **az104-portfolio** : Notes publiques de préparation AZ-104. Pas encore...
- **arkalia-luna-system** : Ce profil GitHub.
- **arkalia-metrics-collector** : CLI de collecte de métriques pour projets Python.
- **ia-pipeline** : Projet en pause (maintenance minimale).
- **base_template** : Squelette Python/FastAPI, peu mis à jour.

#### Archives
Dépôts figés, gardés pour l'historique :
- **nours_interface** : Ancien POC web Flask, conservé en archive.
- **Arkalia-aria** : Dépôt archivé. Le suivi santé a été fusionné dans CIA.
- **bbia_branding** : Dépôt archivé. Les assets sont dans bbia-sim.

## Trois projets à ouvrir

<!-- AUTO-UPDATE:featured -->
Ceux que je maintiens vraiment, dans cet ordre :

- **[bbia-sim](https://github.com/arkalia-luna-system/bbia-sim)** — Simulation et moteur cognitif Python pour Reachy Mini.
- **[arkalia-quest](https://github.com/arkalia-luna-system/arkalia-quest)** — Jeu narratif web (Flask) pour ados, autour d'une IA appelée LUNA.
- **[arkalia-cia](https://github.com/arkalia-luna-system/arkalia-cia)** — Assistant santé mobile Flutter, hors ligne. En bêta.
## Tous les dépôts

Tableau généré depuis `config/projects-data.json`.

<!-- AUTO-UPDATE:projects -->
| Projet | Description | Stack | Rôle | Statut |
|:------:|:-----------:|:-----:|:----:|:-----:|
| **[arkalia-luna-pro](https://github.com/arkalia-luna-system/arkalia-luna-pro)** | Orchestrateur IA expérimental, Python et Docker. | Python + Docker | R&D | Actif |
| **[arkalia-cia](https://github.com/arkalia-luna-system/arkalia-cia)** | Assistant santé mobile Flutter, hors ligne. En bêta. | Flutter | Santé | Bêta |
| **[az104-portfolio](https://github.com/arkalia-luna-system/az104-portfolio)** | Notes publiques de préparation AZ-104. Pas encore certifiée. | Markdown | Notes | Actif |
| **[arkalia-luna-system](https://github.com/arkalia-luna-system/arkalia-luna-system)** | Ce profil GitHub. | Python | Profil | Actif |
| **[Arkalia-luna-logo](https://github.com/arkalia-luna-system/Arkalia-luna-logo)** | Générateur de logos SVG, usage perso, peu actif. | Design | Design | Peu actif |
| **[nours_interface](https://github.com/arkalia-luna-system/nours_interface)** | Ancien POC web Flask, conservé en archive. | Python + Flask | Archive | Archivé |
| **[arkalia-quest](https://github.com/arkalia-luna-system/arkalia-quest)** | Jeu narratif web (Flask) pour ados, autour d'une IA appelée LUNA. | Python + Flask | Jeu | Actif |
| **[arkalia-metrics-collector](https://github.com/arkalia-luna-system/arkalia-metrics-collector)** | CLI de collecte de métriques pour projets Python. | Python + CLI | Outillage | Actif |
| **[bbia-sim](https://github.com/arkalia-luna-system/bbia-sim)** | Simulation et moteur cognitif Python pour Reachy Mini. | Python + MuJoCo | Robotique | Actif |
| **[bbia_branding](https://github.com/arkalia-luna-system/bbia_branding)** | Dépôt archivé. Les assets sont dans bbia-sim. | Design | Archive | Archivé |
| **[ia-pipeline](https://github.com/arkalia-luna-system/ia-pipeline)** | Projet en pause (maintenance minimale). | Python + IA | Outillage | En pause |
| **[base_template](https://github.com/arkalia-luna-system/base_template)** | Squelette Python/FastAPI, peu mis à jour. | Python + FastAPI | Outillage | Template |
## Langages vus dans les dépôts

<!-- AUTO-UPDATE:stats -->
### Statistiques

- **Projets** : 13 au total
- **Langages** : Python (12), Markdown (11), JSON (9), Shell (9), YAML (7), Makefile (6), HTML (6), Dockerfile (4), JavaScript (2), Dart (1), CSS (1)

<sub>*Dernière mise à jour : 14 août 2026*</sub>
<!-- AUTO-UPDATE:languages -->

## Stack

Ce que j'utilise vraiment, selon les dépôts :

- **Langages** : Python, Dart, JavaScript, Shell.
- **Web / API** : Flask, FastAPI.
- **Mobile** : Flutter.
- **Robotique** : MuJoCo, SDK Reachy Mini.
- **Infra** : Docker, GitHub Actions.
- **Cloud** : Azure (portail + CLI, labs) — AZ-104 en préparation, pas un rôle cloud en prod.

## Contact

- GitHub : [@arkalia-luna-system](https://github.com/arkalia-luna-system)
- Email : [arkalia.luna.system@gmail.com](mailto:arkalia.luna.system@gmail.com)
