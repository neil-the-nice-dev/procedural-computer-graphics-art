#!/usr/bin/env python3
"""
Démonstration Complète - Art Informatique
Script qui démontre toutes les fonctionnalités du projet
"""

import os
import sys
import time
from pathlib import Path

def print_banner():
    """Affiche la bannière du projet"""
    print("=" * 60)
    print("🎨 ART INFORMATIQUE - DÉMONSTRATION COMPLÈTE 🎨")
    print("=" * 60)
    print("Transformations d'images et mosaïques vidéo photographiques")
    print("=" * 60)

def demo_image_transformations():
    """Démonstration des transformations d'images"""
    print("\n🖼️  DÉMONSTRATION DES TRANSFORMATIONS D'IMAGES")
    print("-" * 50)
    
    print("1. Création d'une image de démonstration...")
    os.system("python start.py")
    
    print("\n✅ Transformations d'images terminées!")
    print("📁 Vérifiez le dossier 'art_output/' pour voir les résultats")

def demo_video_mosaic():
    """Démonstration de la mosaïque vidéo"""
    print("\n🎬 DÉMONSTRATION DE LA MOSAÏQUE VIDÉO")
    print("-" * 50)
    
    print("1. Création de photos de démonstration...")
    print("2. Création d'une vidéo de démonstration...")
    print("3. Traitement de la vidéo en mosaïque...")
    
    os.system("python video_mosaic.py")
    
    print("\n✅ Mosaïque vidéo terminée!")
    print("📁 Vérifiez le dossier 'video_mosaic_output/' pour voir le résultat")

def show_file_structure():
    """Affiche la structure des fichiers créés"""
    print("\n📁 STRUCTURE DES FICHIERS CRÉÉS")
    print("-" * 50)
    
    def list_files(directory, prefix=""):
        if os.path.exists(directory):
            print(f"{prefix}📂 {directory}/")
            try:
                for item in os.listdir(directory):
                    item_path = os.path.join(directory, item)
                    if os.path.isfile(item_path):
                        size = os.path.getsize(item_path)
                        print(f"{prefix}  📄 {item} ({size} bytes)")
                    elif os.path.isdir(item_path):
                        list_files(item_path, prefix + "  ")
            except PermissionError:
                print(f"{prefix}  🔒 Accès refusé")
        else:
            print(f"{prefix}❌ {directory}/ (n'existe pas)")
    
    directories = [
        "art_output",
        "video_mosaic_output", 
        "photos_mosaique"
    ]
    
    for directory in directories:
        list_files(directory)

def show_usage_instructions():
    """Affiche les instructions d'utilisation"""
    print("\n📖 INSTRUCTIONS D'UTILISATION")
    print("-" * 50)
    
    print("🎨 Transformations d'images:")
    print("   python start.py")
    print()
    
    print("🎬 Mosaïque vidéo (ligne de commande):")
    print("   python video_mosaic.py [chemin_video] --pixel-size 20 --fps 10")
    print()
    
    print("🎬 Mosaïque vidéo (interface graphique):")
    print("   python mosaic_interface.py")
    print()
    
    print("📚 Pour plus d'informations, consultez le README.md")

def main():
    """Fonction principale de démonstration"""
    print_banner()
    
    try:
        # Vérifier que les dépendances sont installées
        print("🔍 Vérification des dépendances...")
        try:
            import PIL
            import cv2
            import numpy
            print("✅ Toutes les dépendances sont installées")
        except ImportError as e:
            print(f"❌ Dépendance manquante: {e}")
            print("💡 Installez les dépendances avec: pip install -r requirements.txt")
            return
        
        # Créer les dossiers nécessaires
        print("\n📁 Création des dossiers de sortie...")
        Path("art_output").mkdir(exist_ok=True)
        Path("video_mosaic_output").mkdir(exist_ok=True)
        print("✅ Dossiers créés")
        
        # Demander à l'utilisateur ce qu'il veut voir
        print("\n🎯 Que souhaitez-vous démontrer?")
        print("1. Transformations d'images seulement")
        print("2. Mosaïque vidéo seulement")
        print("3. Tout (recommandé)")
        print("4. Voir la structure des fichiers")
        print("5. Instructions d'utilisation")
        print("0. Quitter")
        
        while True:
            choix = input("\nVotre choix (0-5): ").strip()
            
            if choix == "0":
                print("👋 Au revoir!")
                break
            elif choix == "1":
                demo_image_transformations()
                break
            elif choix == "2":
                demo_video_mosaic()
                break
            elif choix == "3":
                demo_image_transformations()
                demo_video_mosaic()
                break
            elif choix == "4":
                show_file_structure()
                break
            elif choix == "5":
                show_usage_instructions()
                break
            else:
                print("❌ Choix invalide. Veuillez choisir un nombre entre 0 et 5.")
        
        # Afficher la structure finale
        if choix in ["1", "2", "3"]:
            show_file_structure()
        
        print("\n🎉 Démonstration terminée!")
        print("📚 Consultez le README.md pour plus d'informations")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Démonstration interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")

if __name__ == "__main__":
    main()
