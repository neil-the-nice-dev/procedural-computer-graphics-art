#!/usr/bin/env python3
"""
Interface Utilisateur pour Mosaïque Vidéo Photographique
Interface conviviale pour transformer des vidéos en mosaïques
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from video_mosaic import VideoMosaic
import cv2
from PIL import Image, ImageTk

class MosaicInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Mosaïque Vidéo Photographique")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.video_path = tk.StringVar()
        self.photos_path = tk.StringVar(value="photos_mosaique")
        self.pixel_size = tk.IntVar(value=20)
        self.fps_output = tk.IntVar(value=10)
        self.progress = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Prêt à traiter une vidéo")
        
        # Instance de mosaïque
        self.mosaic = None
        self.processing = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#ecf0f1')
        style.configure('Info.TLabel', font=('Arial', 10), foreground='#bdc3c7')
        style.configure('Custom.TButton', font=('Arial', 10, 'bold'))
        
        # Titre principal
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(pady=20)
        
        title_label = ttk.Label(title_frame, text="🎨 MOSAÏQUE VIDÉO PHOTOGRAPHIQUE", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Transformez vos vidéos en œuvres d'art avec des photos", style='Info.TLabel')
        subtitle_label.pack()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=2)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Section vidéo
        video_frame = tk.LabelFrame(main_frame, text="📹 Vidéo à traiter", bg='#34495e', fg='#ecf0f1', font=('Arial', 12, 'bold'))
        video_frame.pack(padx=10, pady=10, fill='x')
        
        tk.Label(video_frame, text="Chemin de la vidéo:", bg='#34495e', fg='#ecf0f1').pack(anchor='w', padx=10, pady=5)
        
        video_path_frame = tk.Frame(video_frame, bg='#34495e')
        video_path_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Entry(video_path_frame, textvariable=self.video_path, width=50, bg='#2c3e50', fg='#ecf0f1').pack(side='left', fill='x', expand=True)
        tk.Button(video_path_frame, text="Parcourir", command=self.browse_video, bg='#3498db', fg='white', font=('Arial', 10)).pack(side='right', padx=(10, 0))
        
        # Section photos
        photos_frame = tk.LabelFrame(main_frame, text="🖼️ Photos pour la mosaïque", bg='#34495e', fg='#ecf0f1', font=('Arial', 12, 'bold'))
        photos_frame.pack(padx=10, pady=10, fill='x')
        
        tk.Label(photos_frame, text="Dossier des photos:", bg='#34495e', fg='#ecf0f1').pack(anchor='w', padx=10, pady=5)
        
        photos_path_frame = tk.Frame(photos_frame, bg='#34495e')
        photos_path_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Entry(photos_path_frame, textvariable=self.photos_path, width=50, bg='#2c3e50', fg='#ecf0f1').pack(side='left', fill='x', expand=True)
        tk.Button(photos_path_frame, text="Parcourir", command=self.browse_photos, bg='#3498db', fg='white', font=('Arial', 10)).pack(side='right', padx=(10, 0))
        
        # Section paramètres
        params_frame = tk.LabelFrame(main_frame, text="⚙️ Paramètres", bg='#34495e', fg='#ecf0f1', font=('Arial', 12, 'bold'))
        params_frame.pack(padx=10, pady=10, fill='x')
        
        # Taille des pixels
        pixel_frame = tk.Frame(params_frame, bg='#34495e')
        pixel_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(pixel_frame, text="Taille des 'pixels' photos:", bg='#34495e', fg='#ecf0f1').pack(side='left')
        tk.Scale(pixel_frame, from_=10, to=50, orient='horizontal', variable=self.pixel_size, bg='#34495e', fg='#ecf0f1', highlightbackground='#34495e').pack(side='right', fill='x', expand=True)
        
        # FPS de sortie
        fps_frame = tk.Frame(params_frame, bg='#34495e')
        fps_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(fps_frame, text="FPS de sortie:", bg='#34495e', fg='#ecf0f1').pack(side='left')
        tk.Scale(fps_frame, from_=5, to=30, orient='horizontal', variable=self.fps_output, bg='#34495e', fg='#ecf0f1', highlightbackground='#34495e').pack(side='right', fill='x', expand=True)
        
        # Section traitement
        process_frame = tk.LabelFrame(main_frame, text="🎬 Traitement", bg='#34495e', fg='#ecf0f1', font=('Arial', 12, 'bold'))
        process_frame.pack(padx=10, pady=10, fill='x')
        
        # Boutons
        buttons_frame = tk.Frame(process_frame, bg='#34495e')
        buttons_frame.pack(pady=10)
        
        self.process_button = tk.Button(buttons_frame, text="🚀 Démarrer le traitement", command=self.start_processing, 
                                       bg='#27ae60', fg='white', font=('Arial', 12, 'bold'), width=20, height=2)
        self.process_button.pack(side='left', padx=5)
        
        self.demo_button = tk.Button(buttons_frame, text="🎬 Créer vidéo demo", command=self.create_demo, 
                                    bg='#f39c12', fg='white', font=('Arial', 12, 'bold'), width=15, height=2)
        self.demo_button.pack(side='left', padx=5)
        
        # Barre de progression
        progress_frame = tk.Frame(process_frame, bg='#34495e')
        progress_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(progress_frame, text="Progression:", bg='#34495e', fg='#ecf0f1').pack(anchor='w')
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress, maximum=100)
        self.progress_bar.pack(fill='x', pady=5)
        
        # Status
        status_frame = tk.Frame(process_frame, bg='#34495e')
        status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = tk.Label(status_frame, textvariable=self.status_text, bg='#34495e', fg='#ecf0f1', font=('Arial', 10))
        self.status_label.pack(anchor='w')
    
    def browse_video(self):
        """Ouvrir le dialogue pour choisir une vidéo"""
        filename = filedialog.askopenfilename(
            title="Choisir une vidéo",
            filetypes=[
                ("Vidéos", "*.mp4 *.avi *.mov *.mkv *.wmv"),
                ("Tous les fichiers", "*.*")
            ]
        )
        if filename:
            self.video_path.set(filename)
    
    def browse_photos(self):
        """Ouvrir le dialogue pour choisir un dossier de photos"""
        folder = filedialog.askdirectory(title="Choisir le dossier des photos")
        if folder:
            self.photos_path.set(folder)
    
    def create_demo(self):
        """Créer une vidéo de démonstration"""
        self.status_text.set("Création de la vidéo de démonstration...")
        self.root.update()
        
        try:
            if not self.mosaic:
                self.mosaic = VideoMosaic(self.photos_path.get())
            
            demo_path = self.mosaic.creer_video_demo()
            self.video_path.set(demo_path)
            self.status_text.set(f"Vidéo de démonstration créée: {demo_path}")
            messagebox.showinfo("Succès", f"Vidéo de démonstration créée:\n{demo_path}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création de la vidéo demo:\n{str(e)}")
            self.status_text.set("Erreur lors de la création de la vidéo demo")
    
    def start_processing(self):
        """Démarrer le traitement de la vidéo"""
        if self.processing:
            return
        
        if not self.video_path.get():
            messagebox.showwarning("Attention", "Veuillez sélectionner une vidéo à traiter")
            return
        
        # Démarrer le traitement dans un thread séparé
        self.processing = True
        self.process_button.config(state='disabled', text="⏳ Traitement en cours...")
        self.demo_button.config(state='disabled')
        
        thread = threading.Thread(target=self.process_video)
        thread.daemon = True
        thread.start()
    
    def process_video(self):
        """Traiter la vidéo dans un thread séparé"""
        try:
            # Initialiser la mosaïque
            self.status_text.set("Initialisation de la mosaïque...")
            self.root.update()
            
            self.mosaic = VideoMosaic(self.photos_path.get())
            
            # Traiter la vidéo
            self.status_text.set("Traitement de la vidéo en cours...")
            self.root.update()
            
            resultat = self.mosaic.traiter_video(
                self.video_path.get(),
                self.pixel_size.get(),
                self.fps_output.get()
            )
            
            # Succès
            self.root.after(0, lambda: self.processing_complete(resultat))
            
        except Exception as e:
            # Erreur
            self.root.after(0, lambda: self.processing_error(str(e)))
    
    def processing_complete(self, resultat):
        """Appelé quand le traitement est terminé avec succès"""
        self.processing = False
        self.process_button.config(state='normal', text="🚀 Démarrer le traitement")
        self.demo_button.config(state='normal')
        self.progress.set(100)
        self.status_text.set(f"Traitement terminé! Vidéo sauvegardée: {resultat}")
        
        messagebox.showinfo("Succès", f"Vidéo mosaïque créée avec succès!\n\nSauvegardée dans:\n{resultat}")
    
    def processing_error(self, error_msg):
        """Appelé quand le traitement échoue"""
        self.processing = False
        self.process_button.config(state='normal', text="🚀 Démarrer le traitement")
        self.demo_button.config(state='normal')
        self.status_text.set(f"Erreur: {error_msg}")
        
        messagebox.showerror("Erreur", f"Erreur lors du traitement:\n{error_msg}")

def main():
    """Fonction principale"""
    root = tk.Tk()
    app = MosaicInterface(root)
    
    # Centrer la fenêtre
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
