#!/usr/bin/env python3
"""
Mosaïque Vidéo Photographique - Art Informatique
Transforme une vidéo en utilisant des photos comme "pixels"
"""

import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
import math
from pathlib import Path
import argparse
from collections import defaultdict

class VideoMosaic:
    def __init__(self, dossier_photos="photos_mosaique"):
        self.dossier_photos = dossier_photos
        self.photos_cache = {}
        self.photos_moyennes = {}
        self.charger_photos_mosaique()
    
    def charger_photos_mosaique(self):
        """Charge toutes les photos du dossier de mosaïque"""
        print("🖼️  Chargement des photos pour la mosaïque...")
        
        if not os.path.exists(self.dossier_photos):
            print(f"⚠️  Dossier '{self.dossier_photos}' non trouvé. Création d'un dossier avec des photos de démonstration...")
            self.creer_photos_demo()
        
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        photos = []
        
        for fichier in os.listdir(self.dossier_photos):
            if any(fichier.lower().endswith(ext) for ext in extensions):
                chemin = os.path.join(self.dossier_photos, fichier)
                photos.append(chemin)
        
        if not photos:
            print("❌ Aucune photo trouvée dans le dossier. Création de photos de démonstration...")
            self.creer_photos_demo()
            photos = [os.path.join(self.dossier_photos, f) for f in os.listdir(self.dossier_photos) 
                     if any(f.lower().endswith(ext) for ext in extensions)]
        
        print(f"📸 {len(photos)} photos chargées pour la mosaïque")
        
        # Calculer la couleur moyenne de chaque photo
        for i, chemin_photo in enumerate(photos):
            try:
                img = cv2.imread(chemin_photo)
                if img is not None:
                    # Redimensionner pour un calcul plus rapide
                    img_petite = cv2.resize(img, (10, 10))
                    moyenne = cv2.mean(img_petite)[:3]  # BGR
                    self.photos_moyennes[chemin_photo] = moyenne
                    
                    if i % 10 == 0:
                        print(f"   Traitement: {i+1}/{len(photos)}")
            except Exception as e:
                print(f"⚠️  Erreur avec {chemin_photo}: {e}")
        
        print("✅ Photos chargées et analysées!")
    
    def creer_photos_demo(self):
        """Crée des photos de démonstration colorées"""
        Path(self.dossier_photos).mkdir(exist_ok=True)
        
        print("🎨 Création de photos de démonstration...")
        
        # Créer 100 photos colorées différentes
        for i in range(100):
            # Créer une image avec une couleur dominante
            img = Image.new('RGB', (50, 50))
            draw = ImageDraw.Draw(img)
            
            # Couleur de base
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            
            # Dessiner des formes géométriques
            for _ in range(random.randint(3, 8)):
                x1 = random.randint(0, 50)
                y1 = random.randint(0, 50)
                x2 = random.randint(0, 50)
                y2 = random.randint(0, 50)
                
                couleur = (
                    min(255, max(0, r + random.randint(-50, 50))),
                    min(255, max(0, g + random.randint(-50, 50))),
                    min(255, max(0, b + random.randint(-50, 50)))
                )
                
                forme = random.choice(['rectangle', 'cercle', 'ligne'])
                if forme == 'rectangle':
                    draw.rectangle([x1, y1, x2, y2], fill=couleur)
                elif forme == 'cercle':
                    rayon = random.randint(5, 15)
                    draw.ellipse([x1-rayon, y1-rayon, x1+rayon, y1+rayon], fill=couleur)
                else:
                    draw.line([x1, y1, x2, y2], fill=couleur, width=random.randint(1, 3))
            
            # Sauvegarder
            chemin = os.path.join(self.dossier_photos, f"demo_{i:03d}.png")
            img.save(chemin)
    
    def trouver_photo_similaire(self, couleur_cible, taille_pixel):
        """Trouve la photo la plus similaire à la couleur cible"""
        couleur_cible = np.array(couleur_cible)
        meilleure_photo = None
        meilleure_distance = float('inf')
        
        for chemin_photo, moyenne in self.photos_moyennes.items():
            distance = np.linalg.norm(couleur_cible - moyenne)
            if distance < meilleure_distance:
                meilleure_distance = distance
                meilleure_photo = chemin_photo
        
        return meilleure_photo
    
    def creer_mosaique_frame(self, frame, taille_pixel=20):
        """Crée une mosaïque pour une frame de la vidéo"""
        hauteur, largeur = frame.shape[:2]
        resultat = np.zeros((hauteur, largeur, 3), dtype=np.uint8)
        
        # Parcourir la frame par blocs
        for y in range(0, hauteur, taille_pixel):
            for x in range(0, largeur, taille_pixel):
                # Extraire la région
                y_end = min(y + taille_pixel, hauteur)
                x_end = min(x + taille_pixel, largeur)
                region = frame[y:y_end, x:x_end]
                
                # Calculer la couleur moyenne de la région
                moyenne = cv2.mean(region)[:3]  # BGR
                
                # Trouver la photo la plus similaire
                photo_similaire = self.trouver_photo_similaire(moyenne, taille_pixel)
                
                if photo_similaire:
                    # Charger et redimensionner la photo
                    if photo_similaire not in self.photos_cache:
                        img_photo = cv2.imread(photo_similaire)
                        if img_photo is not None:
                            self.photos_cache[photo_similaire] = img_photo
                    
                    if photo_similaire in self.photos_cache:
                        img_photo = self.photos_cache[photo_similaire]
                        img_redimensionnee = cv2.resize(img_photo, (x_end - x, y_end - y))
                        resultat[y:y_end, x:x_end] = img_redimensionnee
        
        return resultat
    
    def traiter_video(self, chemin_video, taille_pixel=20, fps_output=10):
        """Traite une vidéo complète en mosaïque photographique"""
        print(f"🎬 Traitement de la vidéo: {chemin_video}")
        
        # Ouvrir la vidéo
        cap = cv2.VideoCapture(chemin_video)
        if not cap.isOpened():
            print(f"❌ Impossible d'ouvrir la vidéo: {chemin_video}")
            return
        
        # Obtenir les propriétés de la vidéo
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        largeur = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        hauteur = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"📊 Propriétés vidéo: {largeur}x{hauteur}, {fps} FPS, {total_frames} frames")
        
        # Créer le dossier de sortie
        dossier_sortie = "video_mosaic_output"
        Path(dossier_sortie).mkdir(exist_ok=True)
        
        # Préparer le writer vidéo
        nom_sortie = os.path.join(dossier_sortie, f"mosaic_{os.path.basename(chemin_video)}")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(nom_sortie, fourcc, fps_output, (largeur, hauteur))
        
        frame_count = 0
        frames_traitees = 0
        
        print("🎨 Début du traitement des frames...")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Traiter seulement une frame sur plusieurs pour accélérer
            if frame_count % max(1, fps // fps_output) == 0:
                print(f"   Frame {frame_count}/{total_frames} ({frame_count/total_frames*100:.1f}%)")
                
                # Créer la mosaïque
                frame_mosaique = self.creer_mosaique_frame(frame, taille_pixel)
                
                # Écrire la frame
                out.write(frame_mosaique)
                frames_traitees += 1
        
        # Nettoyer
        cap.release()
        out.release()
        
        print(f"✅ Vidéo traitée! {frames_traitees} frames créées")
        print(f"📁 Sauvegardée: {nom_sortie}")
        
        return nom_sortie
    
    def creer_video_demo(self):
        """Crée une vidéo de démonstration si aucune vidéo n'est fournie"""
        print("🎬 Création d'une vidéo de démonstration...")
        
        # Créer une vidéo simple avec des formes animées
        largeur, hauteur = 640, 480
        fps = 30
        duree = 5  # secondes
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('demo_video.mp4', fourcc, fps, (largeur, hauteur))
        
        for frame_num in range(fps * duree):
            # Créer une frame avec des formes animées
            frame = np.zeros((hauteur, largeur, 3), dtype=np.uint8)
            
            # Cercle qui bouge
            centre_x = int(largeur/2 + 100 * math.sin(frame_num * 0.1))
            centre_y = int(hauteur/2 + 50 * math.cos(frame_num * 0.15))
            cv2.circle(frame, (centre_x, centre_y), 50, (0, 255, 0), -1)
            
            # Rectangle qui tourne
            angle = frame_num * 5
            points = np.array([
                [largeur//4, hauteur//4],
                [largeur//4 + 100, hauteur//4],
                [largeur//4 + 100, hauteur//4 + 100],
                [largeur//4, hauteur//4 + 100]
            ], dtype=np.int32)
            
            # Matrice de rotation
            M = cv2.getRotationMatrix2D((largeur//4 + 50, hauteur//4 + 50), angle, 1)
            points_rotates = cv2.transform(points.reshape(-1, 1, 2), M).reshape(-1, 2)
            cv2.fillPoly(frame, [points_rotates], (255, 0, 0))
            
            # Ligne qui bouge
            y1 = int(hauteur * 0.7 + 30 * math.sin(frame_num * 0.2))
            y2 = int(hauteur * 0.7 + 30 * math.sin(frame_num * 0.2 + math.pi))
            cv2.line(frame, (0, y1), (largeur, y2), (0, 0, 255), 5)
            
            out.write(frame)
        
        out.release()
        print("✅ Vidéo de démonstration créée: demo_video.mp4")
        return "demo_video.mp4"

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Mosaïque Vidéo Photographique")
    parser.add_argument("video", nargs="?", help="Chemin vers la vidéo à traiter")
    parser.add_argument("--photos", default="photos_mosaique", help="Dossier contenant les photos pour la mosaïque")
    parser.add_argument("--pixel-size", type=int, default=20, help="Taille des 'pixels' photos (défaut: 20)")
    parser.add_argument("--fps", type=int, default=10, help="FPS de la vidéo de sortie (défaut: 10)")
    
    args = parser.parse_args()
    
    print("🎨 MOSAÏQUE VIDÉO PHOTOGRAPHIQUE 🎨")
    print("=" * 50)
    
    # Créer l'instance
    mosaic = VideoMosaic(args.photos)
    
    # Déterminer la vidéo à traiter
    if args.video:
        chemin_video = args.video
    else:
        print("📹 Aucune vidéo spécifiée. Création d'une vidéo de démonstration...")
        chemin_video = mosaic.creer_video_demo()
    
    # Traiter la vidéo
    try:
        resultat = mosaic.traiter_video(chemin_video, args.pixel_size, args.fps)
        print(f"\n🎉 Traitement terminé avec succès!")
        print(f"📁 Vidéo mosaïque: {resultat}")
        print(f"🔧 Paramètres utilisés:")
        print(f"   - Taille des pixels: {args.pixel_size}")
        print(f"   - FPS de sortie: {args.fps}")
        print(f"   - Photos utilisées: {len(mosaic.photos_moyennes)}")
        
    except Exception as e:
        print(f"❌ Erreur lors du traitement: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
