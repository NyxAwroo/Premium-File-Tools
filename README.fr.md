# Outils Fichiers Premium

![Windows](https://img.shields.io/badge/Windows-10%20%2F%2011-0078D4?style=for-the-badge&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/UI-Tkinter%20%2F%20ttk-2B579A?style=for-the-badge)
![Langues](https://img.shields.io/badge/Langues-Français%20%2F%20English-22A06B?style=for-the-badge)
![Statut](https://img.shields.io/badge/Statut-Actif-brightgreen?style=for-the-badge)

**Outils Fichiers Premium ajoute à l'Explorateur Windows les fonctions rapides d'organisation et de renommage qui lui manquent.**

Windows permet de parcourir ses fichiers efficacement, mais il reste très limité dès qu'il faut organiser, renommer, regrouper, extraire, nettoyer ou préparer des dossiers rapidement. Outils Fichiers Premium comble ce manque en ajoutant des actions pratiques directement dans le menu contextuel du clic droit.

Au lieu d'ouvrir un gestionnaire lourd, d'écrire des scripts ou de déplacer des fichiers manuellement pendant de longues minutes, tu fais clic droit, tu choisis une action, tu prévisualises si nécessaire, et l'outil s'occupe du travail répétitif de manière sûre.

> Documentation anglaise : [README.md](README.md)

## Captures d'écran

Remplace les images ci-dessous par tes propres captures avant publication.

| Interface principale | Dossier personnalisé rapide |
|---|---|
| ![Main organizer screenshot](https://github.com/NyxAwroo/Premium-File-Tools/blob/5b4806349630f3d094f29209d76ea81bbc005aa9/screenshots/interface%20(2).png) | ![Quick custom folder screenshot](https://github.com/NyxAwroo/Premium-File-Tools/blob/5b4806349630f3d094f29209d76ea81bbc005aa9/screenshots/2.png) |

| Extraction sélective | Menu contextuel Windows |
|---|---|
| ![Selective extraction screenshot](https://github.com/NyxAwroo/Premium-File-Tools/blob/5b4806349630f3d094f29209d76ea81bbc005aa9/screenshots/3.png) | ![Context menu screenshot](https://github.com/NyxAwroo/Premium-File-Tools/blob/5b4806349630f3d094f29209d76ea81bbc005aa9/screenshots/1.png)) |

## Pourquoi Cet Outil Existe

L'Explorateur Windows ne propose pas de workflow natif en un clic pour des tâches pourtant très fréquentes :

- regrouper des fichiers par type, taille, mois, préfixe ou extension ;
- renommer beaucoup de fichiers avec nettoyage et casse cohérente ;
- prévisualiser les futurs emplacements avant de déplacer ;
- extraire le contenu de dossiers imbriqués sans tout faire à la main ;
- copier des noms de dossiers comme modèles vides ;
- nettoyer les fichiers parasites et dossiers vides.

Outils Fichiers Premium transforme ces manques en actions rapides accessibles au clic droit.

## Bénéfices

- **Gain de temps immédiat** : trie des dizaines ou centaines de fichiers en quelques secondes.
- **Moins d'erreurs manuelles** : prévisualise les destinations avant validation.
- **Reste dans l'Explorateur Windows** : pas besoin de changer d'environnement.
- **Gère les grosses sélections** : l'accumulateur évite les fenêtres multiples et les courses entre processus.
- **Évite les écrasements accidentels** : tous les déplacements passent par une gestion de conflit.
- **Annule le dernier rangement** si nécessaire.
- **Disponible en français et en anglais** avec détection automatique et réglage manuel.

## Fonctions Du Menu Contextuel

### Menu Sur Les Fichiers Sélectionnés

| Fonction | Utilité |
|---|---|
| **Organiser (Interface Graphique)** | Ouvre l'interface complète avec tri, renommage, gestion des conflits et aperçu en temps réel. |
| **Rapide : Dossier personnalisé** | Demande un nom de dossier et y déplace les fichiers sélectionnés. |
| **Rapide : 1 Fichier = 1 Dossier** | Crée un dossier par fichier, basé sur le nom du fichier. |
| **Rapide : Catégories Intelligentes** | Trie automatiquement dans Images, Vidéos, Musiques, Documents, Archives et Programmes. |
| **Rapide : Grouper par Extension** | Regroupe les fichiers dans des dossiers JPG, PDF, MP4, etc. |
| **Rapide : Grouper par Mois** | Regroupe par mois, par exemple `2026-06`. |
| **Rapide : Grouper par Taille** | Classe les fichiers par tranches de taille. |
| **Rapide : Tranche Alphabétique** | Regroupe dans A-E, F-J, K-O, etc. |
| **Rapide : Grouper par Préfixe Commun** | Regroupe les fichiers qui partagent le même début de nom. |

### Menu Sur Les Dossiers Sélectionnés

| Fonction | Utilité |
|---|---|
| **Extraire à la racine du dossier** | Ouvre l'extraction sélective pour les dossiers sélectionnés. |
| **Rapide : Extraire 1 niveau** | Remonte les éléments directs d'un dossier sans ouvrir chaque sous-dossier. |
| **Copier pour coller vide ailleurs** | Mémorise les noms des dossiers sélectionnés pour recréer ailleurs la même structure vide. |
| **Deep Clean du dossier** | Supprime les fichiers parasites et les sous-dossiers vides. |

### Menu Dans Le Fond D'Un Dossier

| Fonction | Utilité |
|---|---|
| **Extraire vers la racine (Sélectif)** | Extrait le contenu des sous-dossiers vers le dossier courant avec filtres. |
| **Rapide : Extraire 1 niveau uniquement** | Aplatit les sous-dossiers directs dans l'emplacement courant. |
| **Deep Clean** | Nettoie l'arborescence du dossier courant. |
| **Coller les dossiers vides copiés ici** | Recrée ici les dossiers vides copiés précédemment. |
| **Annuler le dernier rangement** | Restaure les fichiers déplacés lors de la dernière opération. |

## Fonctionnalités Principales

### Organisation Intelligente

- Dossier personnalisé.
- Un dossier par fichier.
- Tri par catégories intelligentes.
- Groupement par extension.
- Groupement par date ou mois.
- Groupement par taille.
- Tranches alphabétiques.
- Préfixe commun.

### Renommage

- Minuscules, majuscules, titre, snake_case et kebab-case.
- Suppression des tags entre crochets et parenthèses.
- Suppression des URLs et noms de domaine.
- Numérotation séquentielle.
- Horodatage en préfixe ou suffixe.

### Extraction Et Nettoyage

- Extraction sélective par catégorie ou extension.
- Extraction rapide sur un niveau.
- Deep Clean des fichiers parasites et dossiers vides.
- Copie/collage de structures de dossiers vides.

### Sécurité

- Déplacement sécurisé pour chaque fichier.
- Gestion des conflits : renommer, écraser ou ignorer.
- Journal d'annulation pour la dernière organisation.
- Accumulateur multi-processus pour les grosses sélections Explorer.

## Installation

Prérequis :

- Windows 10 ou Windows 11.
- Python 3 installé.

Installation recommandée :

1. Télécharge ou clone ce dépôt.
2. Double-clique sur `Install.bat`.
3. Accepte la demande administrateur/UAC.
4. Fais clic droit sur des fichiers ou dossiers dans l'Explorateur et ouvre **Outils Fichiers Premium**.

Installation manuelle possible : double-cliquer directement sur `Outils_Fichiers.py`.

## Langue

Outils Fichiers Premium prend en charge le français et l'anglais.

- Sur un Windows français, le français est sélectionné automatiquement.
- Sur les autres systèmes, l'anglais est sélectionné automatiquement.
- La langue peut être changée dans les paramètres.

Pour mettre à jour la langue du menu contextuel Windows après modification :

1. Ouvre l'interface complète.
2. Va dans **Paramètres**.
3. Sélectionne **Français** ou **English**.
4. Ferme l'application.
5. Relance `Install.bat`.

## Structure Du Projet

```text
Outils_Fichiers.py   Application principale en un seul fichier
Install.bat         Installateur simple avec élévation UAC
README.md           Documentation anglaise
README.fr.md        Documentation française
.gitignore          Règles Git
```

## Notes Techniques

- Application Python en un seul fichier.
- Interface construite avec `tkinter` et `ttk`.
- Intégration au menu contextuel via `winreg`.
- Paramètres stockés dans `%APPDATA%\OutilsFichiersPremium\config.json`.
- Journal d'annulation dans `%APPDATA%\OutilsFichiersPremium\undo_log.json`.
- Fichiers temporaires d'accumulation dans `%TEMP%\OF_Premium`.

## Avertissement

L'outil modifie des entrées du registre Windows pendant l'installation afin d'ajouter le menu contextuel. Lis le code avant un déploiement large.
