# -*- coding: utf-8 -*-

# Imports

import tkinter as tk
import tkinter.scrolledtext as sc
from tkinter import ttk
from tkinter import messagebox
from Modele import Virus
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from pathlib import Path


# Classes

class Monde(tk.Tk):
    
    def __init__(self, Controleur, l_canvas, h_canvas, h_menu, rayon):
        """
        Initialise la fenêtre principale.
        
        Args : 
            Controleur (Controleur) : Controleur du jeu 
            l_canvas (int) : largeur du canvas
            h_canvas (int) : hauteur du canvas 
            h_menu (int) : hauteur du menu
            rayon (int) : rayon nécessaire pour dessiner les villes
        """
        super().__init__()
        self.title("Fenêtre principale")
        self.geometry(f"{l_canvas}x{h_canvas+h_menu}")
        
        self.l_canvas = l_canvas
        self.h_canvas = h_canvas
        self.rayon = rayon
        
        self.Controleur = Controleur
        self.texte = ""
        self.Controleur.lier_monde(self)
        
        self.id_villes = {}
        
        self.nb_jours_passes = 5
        
        self.carte = tk.Canvas(width = l_canvas, height = h_canvas, bg='lightblue')
        self.tooltip = tk.Label(self.carte, text="", bg="white")
        
        # Chargement de la carte en fond
        img = Image.open(Path(__file__).resolve().parent / "carte_monde.png").resize((l_canvas, h_canvas), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(img)

        # self.wm_attributes('-transparentcolor','black')
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        s.configure("black.Horizontal.TProgressbar", foreground='black', background='black')

        self.carte.create_image(0, 0, anchor="nw", image=self.bg_img)
        self.tracer_widgets()
    
    
    def tracer_widgets(self):
        """
        Trace tous les widgets de la fenêtre princiapale.
        """
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_rowconfigure(9, weight=1)
        
        self.grid_columnconfigure(0, weight=1, uniform="same_group")
        self.grid_columnconfigure(1, weight=1, uniform="same_group")
        self.grid_columnconfigure(2, weight=1, uniform="same_group")
        self.grid_columnconfigure(3, weight=1, uniform="same_group")
        self.grid_columnconfigure(4, weight=1, uniform="same_group")
        self.grid_columnconfigure(5, weight=1, uniform="same_group")
        self.grid_columnconfigure(6, weight=1, uniform="same_group")
        self.grid_columnconfigure(7, weight=1, uniform="same_group")
        self.grid_columnconfigure(8, weight=1, uniform="same_group")
        self.grid_columnconfigure(9, weight=1, uniform="same_group")
        self.grid_columnconfigure(10, weight=1, uniform="same_group")
        self.grid_columnconfigure(11, weight=1, uniform="same_group")
        
        self.carte.grid(row=1, column=0, rowspan=8, columnspan=12)
        
        bouton_cdb = tk.Button(self, text='Carnet de bord', command=self.ouvrir_cdb).grid(row=9, column=10, columnspan=2, sticky="nswe")
        bouton_fdt = tk.Button(self, text='Finir le tour', command=self.ouvrir_fdt).grid(row=9, column=8, columnspan=2, sticky="nswe")
        bouton_vaccin = tk.Button(self, text="Recherche d'un vaccin", command=self.ouvrir_recherche_vaccin).grid(row=9, column=6, columnspan=2, sticky="nswe")


        self.affichage_jours = tk.Label(self, text=f"Nombre de jours : {self.Controleur.jour}")
        self.affichage_jours.grid(row=9, column=0, columnspan=2, sticky="nswe")
        
        label_pop = tk.Label(self, text="Popularité :")
        label_pop.grid(row=0, column=0, sticky="nswe")
        self.jauge_pop = ttk.Progressbar(self, style="blue.Horizontal.TProgressbar", length=150, maximum=1, value=self.Controleur.Popularite.popularite)
        self.jauge_pop.grid(row=0, column=1, sticky="nswe")
    
        label_monnaie_t = tk.Label(self, text="Monnaie :").grid(row=0, column=2, sticky="nswe")
        self.label_monnaie = tk.Label(self, text=f"{formatage(self.Controleur.Monnaie.valeur)}")
        self.label_monnaie.grid(row=0, column=3, sticky="nswe")
        
        pop_i = self.Controleur.Propagation.pop_infectee / self.Controleur.Reseau.pop_mondiale_ref
        label_pop_i = tk.Label(self, text="Pop infectée :")
        label_pop_i.grid(row=0, column=7, sticky="nswe")
        self.jauge_pop_i = ttk.Progressbar(self, style="red.Horizontal.TProgressbar", length=150, maximum=0.75, value=pop_i)
        self.jauge_pop_i.grid(row=0, column=8, sticky="nswe")
    
        pop_d = self.Controleur.Propagation.pop_decedee / self.Controleur.Reseau.pop_mondiale_ref
        label_pop_d = tk.Label(self, text="Pop décédée :")
        label_pop_d.grid(row=0, column=9, sticky="nswe")
        self.jauge_pop_d = ttk.Progressbar(self, style="black.Horizontal.TProgressbar", length=150, maximum=0.25, value=pop_d)
        self.jauge_pop_d.grid(row=0, column=10, sticky="nswe")
    
    
    def afficher_ville(self, nom, x, y):
        """
        Crée l'affichage de la ville sur la fenêtre principale
        
        Args : 
            nom (str) : nom de la ville 
            x, y (float) : coordonnées carthésiennes de la ville dans Monde
        """
        ville = self.Controleur.Reseau.villes[nom]
        rayon = ville.pop**(1/6) + ville.poids/5
        if ville in self.Controleur.Propagation.villes_infectees:
            couleur = "red"
        else:
            couleur = "black"
        ville.id = self.carte.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, fill="white", outline=couleur)
        
        rayon2 = rayon*ville.sir["d"]
        rayon3 = rayon2 + rayon*ville.sir["i"]
        self.carte.create_oval(x-rayon3, y-rayon3, x+rayon3, y+rayon3, fill="red", state='disabled') if rayon3 != 0 else None
        self.carte.create_oval(x-rayon2, y-rayon2, x+rayon2, y+rayon2, fill="black", state='disabled') if rayon2 != 0 else None
        
        
        ville.id_cercle = self.carte.create_oval(x-self.rayon, y-self.rayon, x+self.rayon, y+self.rayon, outline="black", state="hidden", tag='Cercle')
        self.id_villes[ville.id] = ville
        self.carte.tag_bind(ville.id, '<Button-1>', self.ouvrir_info_v)
        self.carte.tag_bind(ville.id, '<Enter>', self.survol_ville)
        self.carte.tag_bind(ville.id, '<Leave>', self.fin_survol)
    
    
    def survol_ville(self, event):
        """
        Gère le survol de la souris sur une ville et affiche le nom de la ville, sa population et son PUB. 
        
        Args :
            event (tkinter.Event) : événement de déplacement de la souris contenant les coordonnées du curseur sur le canvas.
        """
        ident = self.carte.find_withtag("current")[0]
        ville = self.id_villes[ident]
        texte = f"{ville.nom}\nPopulation : {formatage(ville.pop, monnaie=False)}\nPUB : {formatage(ville.get_pub_effectif())}"
        self.tooltip.config(text=texte)
        x = event.x - 100 if event.x > self.l_canvas - 120 else event.x + 10
        y = event.y - 60 if event.y > self.h_canvas - 80 else event.y + 10
        self.tooltip.place(x=x, y=y)
        self.carte.itemconfig(ville.id_cercle, state='disabled')
        
    
    def fin_survol(self, event):
        """
        Gère la fin du survol de la souris sur une ville en cachant les informations qui ont été affichées lors du survol
        
        Args :
            event (tkinter.Event) : événement déclenché lorsque le curseur quitte l'élément survolé.
        """
        self.tooltip.place_forget()
        self.carte.itemconfig("Cercle", state='hidden')
        
    
    def ouvrir_cdb(self):
        """
        Ouvre la fenêtre secondaire "Carnet de bord"
        """
        carnet_de_bord = Carnet_de_bord(self, 650, 420, self.texte)
        carnet_de_bord.mainloop()


    def ouvrir_info_v(self, event):
        """
        Ouvre la fenêtre secondaire "Info_ville"
        """
        ident = self.carte.find_withtag("current")[0]
        info_ville = Info_ville(self, self.id_villes[ident])
        info_ville.mainloop()
    
    
    def ouvrir_fdt(self):
        """
        Ouvre la fenêtre secondaire "fin de tour"
        """
        fin_de_tour = Fin_de_tour(self, 650, 420)
        fin_de_tour.mainloop()
        
    
    def ouvrir_fdp(self, resultat):
        """
        Ouvre la fenêtre secondaire "fin de jeu"
        
        Args : 
            resultat (str) : chaîne de caratères indiquant si le joueur a gagné ou a perdu 
        """
        fin_de_partie = Fin_de_partie(self, 650, 430, resultat)
        fin_de_partie.mainloop()
        
    
    def maj_affichage_jours(self):
        """
        Affiche le nombre de jours passés
        """
        self.affichage_jours.config(text=f"Nombre de jours : {self.Controleur.jour}")
    
    
    def maj_aff_popularite(self, montant):
        """
        Met à jour la valeur et l'affichage de popularité
        """
        pop = self.jauge_pop.cget("value")
        if montant > 0:
            for i in range(int(montant*100)):
                self.jauge_pop.config(value=pop+(i+1)/100)
        else:
            for i in range(0, int(montant*100), -1):
                self.jauge_pop.config(value=pop+(i-1)/100)
    
    
    def maj_aff_jauges(self):
        """
        Met à jour l'affichage des jauges en fonction des valeurs de populations infectée et décédée
        """
        pop_i = self.Controleur.Propagation.pop_infectee / self.Controleur.Reseau.pop_mondiale_ref
        pop_d = self.Controleur.Propagation.pop_decedee / self.Controleur.Reseau.pop_mondiale_ref
        self.jauge_pop_i.config(value=pop_i)
        self.jauge_pop_d.config(value=pop_d)
        
    def ouvrir_recherche_vaccin(self):
        """
        Ouvre la fenêtre secondaire liée à la mesure "Recherche d'un vaccin"
        """
        recherche_vaccin = Info_vaccin(self)
        recherche_vaccin.mainloop()
        
        

class Info_vaccin(tk.Toplevel) :
    
    def __init__(self, Monde):
        """
        Initialise la fenêtre secondaire liée à la mesure "Recherche d'un vaccin"
        
        Args :
            Monde (Monde) : fenêtre principale
        """
        super().__init__()
        self.title("Information sur la recherche d'un vaccin")
        self.geometry(f"{800}x{200}")
        
        self.Monde = Monde
        self.Controleur = Monde.Controleur
        self.dico_mesures = list(self.Controleur.Reseau.villes.values())[0].dico_mesures
        
        cle = "Recherche d'un vaccin"
        # 1. Affichage des infos sur recherche d'un vaccin (Haut de la fenêtre)
        info_str = f"Étape : {self.dico_mesures[cle].etape}"
        tk.Label(self, text=info_str, justify=tk.CENTER, font=("Arial", 11, "bold")).pack(pady=10)
        
        info_vaccin = f"Cout pour passer à l'étape {self.dico_mesures[cle].etape + 1} : {formatage((self.dico_mesures[cle].etape + 1)*abs(self.dico_mesures[cle].cout))} "
        tk.Label(self, text=info_vaccin, justify=tk.CENTER, font=("Arial", 11, "bold")).pack(pady=20)

        #  Affichage du bouton d'activation si la mesure n'est pas déjà en cours d'activation
        if self.dico_mesures[cle].active == 0:
            btn_confirmer = tk.Button(self, text="Confirmer l'activation", bg="green", fg="white", font=("Arial", 10, "bold"),
                                      command=lambda: self.lancer_recherche_vaccin())
            btn_confirmer.pack(pady=10)
        elif self.dico_mesures[cle].active == 1:
            tk.Label(self, text="⏳ Cette mesure est déjà en cours d'activation.", fg="orange", font=("Arial", 10, "italic")).pack(pady=10)

        
    def lancer_recherche_vaccin(self):
        """
        Vérifie que le joueur a assez d'argent pour activer "Recherche d'un vaccin" et lance son amélioration (passage à une étape supérieure).
        """
        cle = "Recherche d'un vaccin"
        
        if not self.Controleur.Monnaie.modif_valeur((self.dico_mesures[cle].etape + 1) * self.dico_mesures["Recherche d'un vaccin"].cout):
            messagebox.showinfo("Action impossible", "Fonds insuffisants !") #affichage d'une notification du message d'erreur
            
        else:
            self.dico_mesures["Recherche d'un vaccin"].activation()
            self.Monde.texte += f"La mesure Recheche d'un vaccin a été appliquée, elle passera à l'étape {self.dico_mesures[cle].etape + 1}\n\n"
            if self.dico_mesures["Recherche d'un vaccin"].impact_politique != 0:
                self.Monde.maj_aff_popularite(self.dico_mesures["Recherche d'un vaccin"].impact_politique)
                self.Controleur.Popularite.popularite += self.dico_mesures["Recherche d'un vaccin"].impact_politique
                self.Monde.texte += f"Votre popularité est maintenant de {round(100*self.Monde.Controleur.Popularite.popularite, 2)}%.\n\n"
        self.destroy()
        


class Info_ville(tk.Toplevel):
    
    def __init__(self, Monde, ville):
        """
        Initialise la fenêtre secondaire liée aux informations de la ville sur laquelle le joueur a cliquer.
        
        Args : 
            Monde (Monde) : fenêtre principale
            ville (ville) : ville dont on souhaite connaître des informations
        """
        super().__init__()
        self.title(f"Information {ville.nom}")
        self.geometry(f"{700}x{600}")
        
        self.Monde = Monde
        self.controleur = Monde.Controleur
        self.ville = ville
        
        # 1. Affichage des infos statiques de la ville (Haut de la fenêtre)
        info_str = f"Ville : {ville.nom}  |  Pays : {ville.pays.nom} | Population  initiale : {formatage(ville.pop, monnaie=False)} hab \n \
        Population : infectée - {formatage(int(ville.sir['i']*ville.pop), monnaie=False)} hab ({round(ville.sir['i']*100, 4)} %) | décédée : {formatage(int(ville.sir['d']*ville.pop), monnaie=False)} hab ({round(ville.sir['d']*100, 4)} %) \n \
        PUB : {formatage(ville.get_pub_effectif())}  |  Statut : {ville.statut}  |  Coord : ({ville.lat}, {ville.long})"
        
        tk.Label(self, text=info_str, justify=tk.CENTER, font=("Arial", 11, "bold")).pack(pady=10)
        
        # 2. Création des trois grands cadres (Frames) pour classer les mesures
        # Cadre pour l'état 1
        self.frame_dispo = tk.LabelFrame(self, text="💡 Mesures disponibles (État 1)", fg="blue")
        self.frame_dispo.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Cadre pour l'état 2
        self.frame_cours = tk.LabelFrame(self, text="⏳ Mesures en cours d'activation (État 2)", fg="orange")
        self.frame_cours.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Cadre pour l'état 3
        self.frame_actives = tk.LabelFrame(self, text="✅ Mesures actives (État 3)", fg="green")
        self.frame_actives.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # On appelle la méthode qui va remplir ces cadres avec des boutons
        self.afficher_boutons_mesures()
        
        btn_prop = tk.Button(self, text="📊 Consulter la matrice de propagation", 
                             command=self.ouvrir_info_propagation,
                             font=("Arial", 10, "bold"), bg="#34495e", fg="white").pack(pady=5)
        
        btn_graph = tk.Button(self, text="📈 Afficher le graphique de propagation", 
                              command=self.ouvrir_graphique_propagation,
                              font=("Arial", 10, "bold"), bg="#8e44ad", fg="white")
        btn_graph.pack(pady=5)


    def afficher_boutons_mesures(self):
        """
        Vide les cadres puis les remplit avec les mesures selon leur état dans la ville.
        """
        # On vide les frames (utile quand la fenêtre s'actualise après un achat)
        for widget in self.frame_dispo.winfo_children(): widget.destroy()
        for widget in self.frame_cours.winfo_children(): widget.destroy()
        for widget in self.frame_actives.winfo_children(): widget.destroy()
        
        # On parcourt le dictionnaire des mesures de la ville
        for nom_mesure, donnees in self.ville.dico_mesures_ville.items():
            etat = donnees["etat"]
            mesure = donnees["mesure"]
            
            # --- ÉTAT 1 : DISPONIBLE ---
            if etat == 1:
                # Texte affiché sur le bouton
                texte = f"{nom_mesure} (Coût : {formatage(abs(mesure.cout))}, Pol : {mesure.impact_politique}, Délai : {mesure.delai}j)"
                # lambda permet de "sauvegarder" les variables pour quand le joueur cliquera
                cmd = lambda m=mesure, n=nom_mesure, e=etat: self.ouvrir_fenetre_mesure(m, n, e)
                tk.Button(self.frame_dispo, text=texte, command=cmd).pack(anchor="w", padx=10, pady=2)
                
            # --- ÉTAT 2 : EN COURS ---
            elif etat == 2:
                # Si l'attribut delai_restant n'existe pas encore sur l'objet, on le crée temporairement par sécurité
                if not hasattr(mesure, "delai_restant"): 
                    mesure.delai_restant = mesure.delai
                    
                texte = f"{nom_mesure} (En cours... Délai restant : {mesure.delai_restant}j)"
                cmd = lambda m=mesure, n=nom_mesure, e=etat: self.ouvrir_fenetre_mesure(m, n, e)
                tk.Button(self.frame_cours, text=texte, command=cmd).pack(anchor="w", padx=10, pady=2)
                
            # --- ÉTAT 3 : ACTIF ---
            elif etat == 3:
                texte = f"{nom_mesure} (Active pour {mesure.duree_activation} jours)"
                cmd = lambda m=mesure, n=nom_mesure, e=etat: self.ouvrir_fenetre_mesure(m, n, e)
                tk.Button(self.frame_actives, text=texte, command=cmd).pack(anchor="w", padx=10, pady=2)


    def ouvrir_fenetre_mesure(self, mesure, nom_mesure, etat):
        """
        Ouvre une sous-fenêtre avec le détail de la mesure et le bouton d'achat si elle est dispo.
        """
        fen = tk.Toplevel(self) # Sous-fenêtre
        fen.title(f"Détail : {nom_mesure}")
        fen.geometry("450x300")
        
        # On crée une échelle pour choisir la durée pour laquelle la mesure sera active
        self.duree_mesure = tk.IntVar(value=5)
        scale = tk.Scale(fen, variable = self.duree_mesure, orient='horizontal', from_= 1, to = 10, resolution=1, length=400, label='Choix de la durée de la mesure').pack(pady=10)
        
        # On va chercher une brève description (définie plus bas)
        desc = self.get_description_mesure(nom_mesure)
        
        # Affichage des informations
        texte_info = f"--- {nom_mesure.upper()} ---\n\n"
        texte_info += f"💰 Coût économique : {formatage(abs(mesure.cout))} / jour\n"
        texte_info += f"📉 Impact politique : {mesure.impact_politique}\n"
        texte_info += f"⏱️ Délai d'activation : {mesure.delai} jours\n\n"
        texte_info += f"Effets : {desc}"
        
        tk.Label(fen, text=texte_info, justify=tk.LEFT, wraplength=400).pack(pady=15)
        
        # Affichage conditionnel des boutons selon l'état
        if etat == 1:
            btn_confirmer = tk.Button(fen, text="Confirmer l'activation", bg="green", fg="white", font=("Arial", 10, "bold"),
                                      command=lambda: self.lancer_activation(nom_mesure, mesure, fen))
            btn_confirmer.pack(pady=10)
        elif etat == 2:
            tk.Label(fen, text="⏳ Cette mesure est déjà en cours d'activation.", fg="orange", font=("Arial", 10, "italic")).pack(pady=10)
        elif etat == 3:
            tk.Label(fen, text="✅ Cette mesure est actuellement active et protège la ville.", fg="green", font=("Arial", 10, "italic")).pack(pady=10)


    def lancer_activation(self, nom_mesure, mesure, fen_popup):
        """
        Fonction appelée lors du clic sur 'Confirmer l'activation'.
        
        Args : 
            nom_mesure (str) : nom de la mesure à activer
            mesure (Mesure) : objet mesure à activer
            fen_popup (tk.Toplevel) : sous fenêtre de l'affichage permettant de lancer la mesure
        """
        if not self.Monde.Controleur.Monnaie.modif_valeur(mesure.cout * self.duree_mesure.get()):
            messagebox.showinfo("Action impossible", "Fonds insuffisants !") # Affichage d'une notification du message d'erreur
        else:
            self.ville.dico_mesures_ville[nom_mesure]["etat"] = 2
            mesure.duree_activation = self.duree_mesure.get()
            mesure.delai_restant = mesure.delai
            self.Monde.texte += f"La mesure {nom_mesure} a été appliquée à {self.ville.nom}\n\n"
            if mesure.impact_politique != 0:
                fen_popup.destroy()
                self.Monde.maj_aff_popularite(mesure.impact_politique)
                self.Monde.Controleur.Popularite.popularite += mesure.impact_politique
                self.Monde.texte += f"Votre popularité est maintenant de {round(100*self.Monde.Controleur.Popularite.popularite, 2)}%.\n\n"
                self.afficher_boutons_mesures()


    def get_description_mesure(self, nom_mesure):
        """
        Renvoie une petite phrase descriptive pour aider le joueur.
        
        Args : 
            nom_mesure (str) : nom de la mesure à activer
            
        Return : 
            (str) descripition de la mesureà activer
        """
        dico_desc = {
            "Port du masque": "Diminue légèrement les transmissions locales.",
            "Confinement": "Réduit drastiquement les contacts locaux mais coûte très cher économiquement (baisse du PUB).",
            "Développement hôpitaux": "Augmente le taux de guérison et réduit fortement la mortalité dans la ville.",
            "Mise en quarantaine": "Isole complètement la ville des autres. Efficace mais PUB réduit à néant.",
            "Campagne de prévention": "Diminue la propagation. Coût faible, conseillé en début d'épidémie.",
            "Boost économique": "Augmente la production économique (PUB) de la ville pour compenser les pertes.",
            "Usines": "Diminue le coût des mesures Port du masque et Développement hôpitaux, et augmente leur efficacité dans les villes voisines situées dans le rayon d'influence de la ville.",
            "Base militaire": "Augmente fortement l’efficacité des mesures Confinement et Mise en quarantaine dans les villes situées dans le rayon d'influence de la ville.",
        }
        return dico_desc.get(nom_mesure, "Modifie les paramètres de propagation ou l'économie de la ville.")

    
    def ouvrir_info_propagation(self):
        """
        Ouvre une fenêtre présentant un tableau croisé des coefficients :
        Valeurs initiales -> Multiplicateurs des mesures -> Valeurs effectives finales.
        """
        fen_prop = tk.Toplevel(self)
        fen_prop.title(f"Analyse des propagations - {self.ville.nom}")
        fen_prop.geometry("850x400") 
        
        tk.Label(fen_prop, text=f"📊 Matrice d'impact des mesures : {self.ville.nom}", 
                 font=("Arial", 12, "bold"), fg="#2c3e50").pack(pady=15)
        
        grille = tk.Frame(fen_prop)
        grille.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        virus = self.controleur.Virus
        
        colonnes = ["β (Transm.)", "α (Incubation)", "γ (Guérison)", "δ (Perte Imm.)", "μ (Mortalité)", "φ (Économie)"]
        cles_attr = ["beta", "alpha", "gamma", "delta", "mu", "phi"]
        
        tk.Label(grille, text="Paramètres", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        for j, col in enumerate(colonnes):
            tk.Label(grille, text=col, font=("Arial", 10, "bold")).grid(row=0, column=j+1, padx=10, pady=5)
            
        tk.Label(grille, text="Valeurs initiales", font=("Arial", 10, "italic"), fg="gray").grid(row=1, column=0, sticky="w", padx=10)
        valeurs_initiales = [virus.beta, virus.alpha, virus.gamma, virus.delta, virus.mu, 1.0]
        
        for j, val in enumerate(valeurs_initiales):
            tk.Label(grille, text=f"{val:.4f}", font=("Arial", 10, "italic"), fg="gray").grid(row=1, column=j+1)
            
        row_idx = 2
        for nom_mesure, donnees in self.ville.dico_mesures_ville.items():
            if donnees["etat"] == 3:
                mesure = donnees["mesure"]
                tk.Label(grille, text=f"↳ {nom_mesure}", font=("Arial", 10)).grid(row=row_idx, column=0, sticky="w", padx=10)
                
                for j, attr in enumerate(cles_attr):
                    val_mult = getattr(mesure, attr)
                    if val_mult == 1.0:
                        lbl = tk.Label(grille, text="x 1.0", font=("Arial", 9), fg="#bdc3c7")
                    else:
                        lbl = tk.Label(grille, text=f"x {val_mult:.2f}", font=("Arial", 10, "bold"), fg="#2980b9")
                    lbl.grid(row=row_idx, column=j+1, pady=3)
                row_idx += 1
                
        ttk.Separator(grille, orient='horizontal').grid(row=row_idx, column=0, columnspan=len(colonnes)+1, sticky='ew', pady=10)
        row_idx += 1
        
        tk.Label(grille, text="VALEURS EFFECTIVES", font=("Arial", 10, "bold"), fg="#c0392b").grid(row=row_idx, column=0, sticky="w", padx=10)
        
        mults = self.ville.get_multiplicateurs_mesures()
        valeurs_effectives = [
            virus.beta * mults["beta"],
            virus.alpha * mults["alpha"],
            virus.gamma * mults["gamma"],
            virus.delta * mults["delta"],
            virus.mu * mults["mu"],
            mults["phi"]
        ]
        
        for j, val_eff in enumerate(valeurs_effectives):
            tk.Label(grille, text=f"{val_eff:.4f}", font=("Arial", 11, "bold"), fg="#c0392b").grid(row=row_idx, column=j+1)
            
        tk.Button(fen_prop, text="Fermer", command=fen_prop.destroy, font=("Arial", 10)).pack(pady=10)
        
    
    def ouvrir_graphique_propagation(self):
        """
        Ouvre une fenêtre affichant les courbes détaillées (Euler) de l'épidémie locale.
        """
        fen_graph = tk.Toplevel(self)
        fen_graph.title(f"Évolution de l'épidémie - {self.ville.nom}")
        fen_graph.geometry("800x600")
        
        # Création de la figure Matplotlib
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Récupération des listes générées par l'historique
        jours = self.ville.historique["t"]
        infectes = [100 * i for i in self.ville.historique["I"]]
        decedes = [100*d for d in self.ville.historique["D"]]
        
        # Calcul de la population totale (Pop initiale - Population décédée)
        pop_totale = [100 - d for d in decedes]
        
        # Tracé des 3 courbes avec la résolution d'Euler
        ax.plot(jours, pop_totale, label="Population Vivante", color="#27ae60", linewidth=2)
        ax.plot(jours, infectes, label="Population Infectée", color="#e74c3c", linewidth=2.5)
        ax.plot(jours, decedes, label="Population Décédée", color="#2c3e50", linewidth=2)
        
        # Habillage du graphique
        ax.set_xlabel("Jours de propagation")
        ax.set_ylabel("Population (%)")
        ax.set_title(f"Dynamique d'infection à {self.ville.nom}")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Intégration de la figure Matplotlib dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=fen_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Button(fen_graph, text="Fermer", command=fen_graph.destroy, font=("Arial", 10)).pack(pady=10)


class Carnet_de_bord(tk.Tk):
    
    def __init__(self, Monde, l_cdb, h_cdb, text):
        """
        Initialise la fenêtre secondaire liée au carnet de bord.
        
        Args :
            Monde (Monde) : fenêtre principale
            l_cdb (int) : largeur de la fenêtre secondaire
            h_cdb (int) : hauteur de la fenêtre secondaire
            text (str) : texte à afficher dans le carnet de bord

        """
        super().__init__()
        self.title("Carnet de bord")
        self.geometry(f"{l_cdb}x{h_cdb}")
        
        self.text = tk.StringVar(self, "Bienvenue dans ton Carnet de Bord !\n\n*** Tour 1 - Jour 1 ***\n\n" + text)
        
        self.Controleur = Monde.Controleur
        self.scrolledText = sc.ScrolledText(self)
        self.scrolledText.pack()
        self.scrolledText.insert("end", self.text.get())
        
        bouton_quitter = tk.Button(self, text='Quitter', command=self.destroy).pack()
        
        

class Debut_jeu(tk.Tk):
    
    def __init__(self, Controleur):
        """
        Initialise la fenêtre de début de jeu, celle avec le choix du niveau de difficulté et du virus. 
        
        Args : 
            Controleur (Controleur) : Controleur du jeu
        """
        super().__init__()
        self.title("Sélection du niveau")
        self.geometry("1200x200")
        
        self.Controleur = Controleur
        self.niveau_min = 1
        self.niveau_max = 4
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
 
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        
        # Variable liée au curseur (on utilise IntVar car la résolution est de 1)
        self.valeur_niveau = tk.IntVar(value=0)
        scale = tk.Scale(self, orient='horizontal', from_= self.niveau_min, to = self.niveau_max, resolution=1, tickinterval=25, length=1000, label='Choix du niveau',variable = self.valeur_niveau)
        scale.grid(row=0, column=1, columnspan=4)
        
        self.niveau_1 = tk.Label(text='Facile')
        self.niveau_1.grid(row=1, column=0,columnspan=2)
        
        self.niveau_2 = tk.Label(text='Moyen')
        self.niveau_2.grid(row=1, column=2)
        
        self.niveau_3 = tk.Label(text='Difficile')
        self.niveau_3.grid(row=1, column=3)
        
        self.niveau_4 = tk.Label(text='Extrême')
        self.niveau_4.grid(row=1, column=4,columnspan=5)
        
        self.bouton_valider = tk.Button(self, text="Valider le niveau", command=self.init_niveau)
        self.bouton_valider.grid(row=2,column=1,columnspan=4)
        
        
    def init_niveau(self):
        """
        Affiche les boutons de choix du virus en fonction du niveau de difficulté choisi.
        """
        niveau = self.valeur_niveau.get()
        self.Controleur.niveau = niveau

        if niveau == 1: 
            self.bouton_grippe=tk.Button(self, text="Grippe Saisonnière", command=lambda *args:self.init_virus("Grippe Saisonnière"))
            self.bouton_grippe.grid(row=2, column=0,columnspan=2)
            self.bouton_rhume=tk.Button(self, text="Rhinovirus (Rhume)", command=lambda *args:self.init_virus("Rhinovirus (Rhume)"))
            self.bouton_rhume.grid(row=3, column=0,columnspan=2)

        elif niveau == 2: 
            self.bouton_delta=tk.Button(self, text="SARS-CoV-2 Delta", command=lambda *args:self.init_virus("SARS-CoV-2 Delta"))
            self.bouton_delta.grid(row=2, column=2)
            self.bouton_kappa=tk.Button(self, text="SARS-CoV-2 Kappa", command=lambda *args:self.init_virus("SARS-CoV-2 Kappa"))
            self.bouton_kappa.grid(row=3, column=2)
       
        elif niveau == 3: 
            self.bouton_rougeole=tk.Button(self, text="Rougeole", command=lambda *args:self.init_virus("Rougeole"))
            self.bouton_rougeole.grid(row=2, column=3)
            self.bouton_peste=tk.Button(self, text="Peste Pulmonaire", command=lambda *args:self.init_virus("Peste Pulmonaire"))
            self.bouton_peste.grid(row=3, column=3)
       
        elif niveau == 4: 
            self.bouton_ebola=tk.Button(self, text="Ebola", command=lambda *args:self.init_virus("Ebola"))
            self.bouton_ebola.grid(row=2, column=4,columnspan=5)
            self.bouton_necro=tk.Button(self, text="Nécro-virus", command=lambda *args:self.init_virus("Nécro-virus"))
            self.bouton_necro.grid(row=3, column=4,columnspan=5)
 
            
    def init_virus(self, virus):
        """
        Initialise dans le controleur le virus choisi.
        
        Args :
            virus(str) : nom du virus choisi par le joueur
        """
        self.Controleur.Virus = self.Controleur.virus[virus]
        self.destroy()


class Fin_de_tour(tk.Tk):
    
    def __init__(self, Monde, l_fdt, h_fdt):
        """
        Initialise la fenêtre secondaire liée à la fin du tour, celle où le joueur choisit notamment le nombre de jours qu'il souhaite passer.
        
        Args : 
            Monde (Monde) : fenêtre principale
            l_fdt (int) : largeur de la fenêtre secondaire
            h_fdt (int) : hauteur de la fenêtre secondaire
        """
        super().__init__()
        self.title("Fin de tour")
        self.geometry(f"{l_fdt}x{h_fdt}")
        self.Monde = Monde
        
        self.nb_jours = tk.IntVar(self, self.Monde.nb_jours_passes)
        label = tk.Label(self, text='Combien de jours souhaitez-vous laisser passer avant votre prochain tour ?').pack(side=tk.TOP, fill='x')
        scale = tk.Scale(self, variable=self.nb_jours, orient=tk.HORIZONTAL, from_=1, to=10, length=0.8*l_fdt, command=self.maj_nb_jours).pack(side=tk.TOP)
        
        self.texte_gains = tk.StringVar(self, f'Gains estimés pour ce nombre de jours : {formatage(self.nb_jours.get()**2 * Monde.Controleur.Reseau.PMB()/10)}')
        self.label_gains = tk.Label(self, text=self.texte_gains.get())
        self.label_gains.pack(side=tk.TOP, fill='x')
        bouton_valider = tk.Button(self, text='Valider', command=self.valider).pack(fill='x')
        
    
    def maj_nb_jours(self, event):
        """
        Calcule et affiche le gain estimé en fonction du nombre de jours passés.
        
        Args :
            event (tkinter.Event) : événement de changement de la variable nb_jours
        """
        self.label_gains.config(text=f'Gains estimés pour ce nombre de tours : {formatage(self.nb_jours.get()**2 * self.Monde.Controleur.Reseau.PMB()/10)}')
        
        
    def valider(self):
        """
        Réalise toutes les actions liées à la fin du tour : propagation du virus, application des effets des mesures de soutien, mise à jour et affichage des informations comme la monnaie, les jauges etc.
        """
        dico_mesures = self.Monde.Controleur.dico_mesures
        
        nb_jours = self.nb_jours.get()
        self.Monde.nb_jours_passes = nb_jours
        self.Monde.texte += f"Population totale : {formatage(100*self.Monde.Controleur.Reseau.pop_mondiale_ref, monnaie=False)} habitants\n"
        self.Monde.texte += f"Population infectée : {round(100 * self.Monde.Controleur.Propagation.pop_infectee / self.Monde.Controleur.Reseau.pop_mondiale_ref, 3)} % \n"
        self.Monde.texte += f"Population décédée : {round(100 * self.Monde.Controleur.Propagation.pop_decedee / self.Monde.Controleur.Reseau.pop_mondiale_ref, 3)} % \n\n"
        self.Monde.texte += f"Fin du tour {self.Monde.Controleur.tour}\n\n"
        self.Monde.Controleur.tour += 1
        self.Monde.Controleur.Propagation.propagation(nb_jours)
        self.Monde.Controleur.jour += nb_jours
        
        self.Monde.carte.delete("all")
        self.Monde.carte.create_image(0, 0, anchor="nw", image=self.Monde.bg_img)
        self.Monde.Controleur.afficher_villes()
        self.Monde.maj_affichage_jours()
        self.Monde.maj_aff_jauges()
        
        self.Monde.texte += f"*** Tour {self.Monde.Controleur.tour} - Jour {self.Monde.Controleur.jour} ***\n\n"
        self.Monde.Controleur.Monnaie.modif_valeur(self.nb_jours.get()**2*self.Monde.Controleur.Reseau.PMB()/10)
        self.Monde.label_monnaie.config(text=f"{formatage(self.Monde.Controleur.Monnaie.valeur)}")
        self.Monde.Controleur.Popularite.impact_popularite()
        
        self.Monde.Controleur.Reseau.effet_mesure()
        dico_mesures["Recherche d'un vaccin"].maj_etape(nb_jours)
        dico_mesures["Recherche d'un vaccin"].maj_parametres(dico_mesures)
        
        avancer = self.Monde.Controleur.fin_de_jeu()
        self.destroy()
        if avancer != "continue" :
            self.Monde.ouvrir_fdp(avancer) 
            

class Fin_de_partie(tk.Tk):

    def __init__(self, Monde, l_fdp, h_fdp, resultat):
        """
        Initialise la fenêtre secondaire liée à la fin de partie.
        
        Args :
            Monde (Monde) : fenêtre principale
            l_fdp (int) : largeur de la fenêtre 
            h_fdp (int) : hauteur de la fenêtre
            resulat (str) : résultat indiquant si le joueur a gagné ou a perdu
        """
        super().__init__()
        self.title("Fin de partie")
        self.geometry(f"{l_fdp}x{h_fdp}")
        
        self.Controleur = Monde.Controleur
        
        # Titre selon résultat
        if resultat == "gagné":
            titre = "Vous avez gagné !!!"
            couleur = "green"
        else:
            titre = "Vous avez perdu..."
            couleur = "red"
        
        tk.Label(self, text=titre, font=("Arial", 16, "bold"), fg=couleur).pack(pady=15)
        
        # Statistiques
        pop_mondiale_ref = self.Controleur.Reseau.pop_mondiale_ref
        pop_infectee = self.Controleur.Propagation.pop_infectee
        pop_decedee = self.Controleur.Propagation.pop_decedee
        if pop_mondiale_ref > 0 :
            taux_1 = round(100 * pop_infectee / pop_mondiale_ref, 2)
            taux_2 = round(100 * pop_decedee / pop_mondiale_ref, 2)
        else : 
            taux = 0
        
        stats = (
            f"Jours écoulés       : {self.Controleur.jour}\n"
            f"Tours joués         : {self.Controleur.tour}\n"
            f"Population mondiale : {formatage(pop_mondiale_ref, monnaie=False)} hab\n"
            f"Population infectée : {formatage(pop_infectee, monnaie=False)} hab\n"
            f"Taux d'infection    : {taux_1} %\n"
            f"Taux de mortalité   : {taux_2} %\n"
            f"Monnaie restante    : {formatage(self.Controleur.Monnaie.valeur)}\n"
            f"Virus               : {self.Controleur.Virus.nom}\n"
        )
        
        texte_stats = tk.Label(self, text=stats, font=("Courier", 11), justify=tk.LEFT)
        texte_stats.pack(padx=20, pady=10)
        
        # Carnet de bord
        cdb = tk.Label(self, text="Journal de bord :", font=("Arial", 11, "bold"))
        cdb.pack()
        journal = sc.ScrolledText(self, height=8)
        journal.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        journal.insert("end", Monde.texte)
        journal.config(state="disabled")
        
        quitter = tk.Button(self, text="Quitter", font=("Arial", 11), command=self.detruire)
        quitter.pack(fill='both')
        
    
    def detruire(self):
        """
        Détruit des fenêtres Monde et Fin de partie
        """
        self.Controleur.Monde.destroy()
        self.destroy()
        

# Fonctions utiles pour les classes

def formatage(valeur_brute, monnaie=True):
    """
    Convertit une grande valeur numérique en une chaîne de caractères lisible 
    avec des suffixes (M, Md, T) et 2 décimales.
    
    Args:
        valeur_brute (int/float): La valeur de PUB à formater.
        monnaie (bool) : indique si le nombre a formater est un prix (pour l'ajout du $)
        
    Returns:
        str: La valeur formatée (ex: "1.69 T $", "87.81 Md $").
    """
    if valeur_brute >= 1_000_000_000_000:  # Trillions (Mille Milliards)
        valeur = valeur_brute / 1_000_000_000_000
        suffixe = "T"
    elif valeur_brute >= 1_000_000_000:    # Milliards
        valeur = valeur_brute / 1_000_000_000
        suffixe = "Md"
    elif valeur_brute >= 1_000_000:        # Millions
        valeur = valeur_brute / 1_000_000
        suffixe = "M"
    elif valeur_brute >= 1_000:            # Milliers
        valeur = valeur_brute / 1_000
        suffixe = "K"
    else:
        valeur = float(valeur_brute)
        suffixe = ""
    valeur_formatee = f"{valeur:.2f} {suffixe}"
    if monnaie:
       valeur_formatee += " $"
       
    return valeur_formatee
        
