# 🎨 Art Informatique - Transformations d'Images et Vidéos Esthétiques ( en dev !!! ne marche pas ) 

Un ensemble de programmes Python créatifs qui transforment vos images et vidéos en œuvres d'art numériques avec des effets visuels avancés.

## ✨ Fonctionnalités

### 🖼️ Transformations d'Images (`start.py`)
Le programme propose 8 effets artistiques différents :

1. **Mosaïque Colorée** - Transforme l'image en mosaïque de carrés colorés avec variations chromatiques
2. **Vagues Chromatiques** - Applique des déformations sinusoïdales avec variations de couleurs
3. **Pixelisation Artistique** - Pixelise l'image avec des formes géométriques (cercles, carrés, triangles)
4. **Décomposition RGB** - Sépare et décale les canaux de couleur rouge, vert et bleu
5. **Effet Kaléidoscope** - Crée un effet de miroir répété en 8 segments
6. **Transformation Sinusoïdale** - Applique des ondulations sinusoïdales à l'image
7. **Effet Fractal** - Transforme l'image avec des algorithmes fractals
8. **Mélange Chromatique** - Mélange créativement les canaux de couleur

### 🎬 Mosaïque Vidéo Photographique (`video_mosaic.py`)
Transforme vos vidéos en mosaïques artistiques en utilisant des photos comme "pixels" :

- **Analyse chromatique** : Chaque région de la vidéo est remplacée par la photo la plus similaire en couleur
- **Photos personnalisées** : Utilisez votre propre collection de photos pour créer des mosaïques uniques
- **Paramètres ajustables** : Taille des "pixels" photos, FPS de sortie, etc.
- **Interface graphique** : Interface conviviale avec `mosaic_interface.py`

## 🚀 Installation

1. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

2. **Lancer les programmes :**

   **Transformations d'images :**
   ```bash
   python start.py
   ```

   **Mosaïque vidéo (ligne de commande) :**
   ```bash
   python video_mosaic.py [chemin_video] --pixel-size 20 --fps 10
   ```

   **Mosaïque vidéo (interface graphique) :**
   ```bash
   python mosaic_interface.py
   ```

## 📖 Utilisation

### 🖼️ Transformations d'Images
1. Lancez `python start.py`
2. Entrez le chemin vers votre image (ou appuyez sur Entrée pour utiliser une image de démonstration)
3. Choisissez un effet artistique (1-9)
4. L'image transformée sera sauvegardée dans le dossier `art_output/`
5. L'image s'ouvrira automatiquement si votre système le permet

### 🎬 Mosaïque Vidéo Photographique
1. **Préparer vos photos** : Placez vos photos dans un dossier (ou utilisez les photos de démonstration générées automatiquement)
2. **Choisir une vidéo** : Sélectionnez la vidéo à transformer
3. **Ajuster les paramètres** : Taille des "pixels" photos, FPS de sortie
4. **Lancer le traitement** : La vidéo mosaïque sera sauvegardée dans `video_mosaic_output/`

**Exemple avec interface graphique :**
```bash
python mosaic_interface.py
```
Puis utilisez l'interface pour sélectionner vos fichiers et paramètres.

## 🎯 Exemples d'effets

- **Mosaïque Colorée** : Parfait pour créer des effets de vitrail
- **Vagues Chromatiques** : Idéal pour des effets psychédéliques
- **Kaléidoscope** : Crée des motifs symétriques répétitifs
- **Décomposition RGB** : Effet de glitch artistique moderne

## 📁 Structure des fichiers

```
procedural-computer-graphics-art/
├── start.py                    # Transformations d'images
├── video_mosaic.py             # Mosaïque vidéo (ligne de commande)
├── mosaic_interface.py         # Interface graphique pour mosaïque vidéo
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
├── art_output/                 # Images transformées (créé automatiquement)
├── video_mosaic_output/        # Vidéos mosaïques (créé automatiquement)
├── photos_mosaique/            # Photos pour mosaïque (créé automatiquement)
├── demo_image.png              # Image de démonstration
└── demo_video.mp4              # Vidéo de démonstration
```

## 🛠️ Dépendances

- **Pillow** : Traitement d'images
- **NumPy** : Calculs mathématiques avancés
- **OpenCV** : Traitement vidéo et analyse d'images
- **Tkinter** : Interface graphique (inclus avec Python)

## 🎨 Personnalisation

Vous pouvez facilement modifier les paramètres des effets en éditant les valeurs dans le code :
- Taille des pixels pour la pixelisation
- Intensité des déformations sinusoïdales
- Nombre de segments du kaléidoscope
- Variations chromatiques

## 📝 Notes techniques

- Les images sont automatiquement redimensionnées à 800x800 pixels maximum pour des performances optimales
- Toutes les images transformées sont sauvegardées en haute qualité (95%)
- Le programme gère automatiquement les erreurs et les interruptions

## 🎭 Inspiration artistique

Ce programme s'inspire de techniques d'art numérique modernes :
- Art génératif
- Glitch art
- Fractals
- Transformations géométriques
- Manipulations chromatiques

Amusez-vous à créer vos propres œuvres d'art numériques ! 🎨✨
