from app_ressource import *
from update_database import con, curseur, création
from sidebar import sidebar_exercice, sidebar_performance, sidebar_outil, sidebar_paramètre
from exercice_app import exercice_accueil
from outil_app import outils        
from performance_app import charge_d_entraînement
from parametre_app import parametres

def parametre(account_id):
    parametres(account_id, connexion, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)

def predicteur_temps(account_id):
    outils(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre)

def charge_entraînement(account_id):
    charge_d_entraînement(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)

def exercice(account_id):
    exercice_accueil(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)

def connexion():
    cadre_connection = ctk.CTkFrame(app, fg_color=couleur_fond)        
    cadre_connection.pack(fill="both", expand=True)

    boite_géante = ctk.CTkFrame(cadre_connection, fg_color="transparent")        
    boite_géante.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    boite1 = ctk.CTkFrame(boite_géante, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color="transparent")        
    boite1.pack(side="left", pady=10, padx=20, fill="both", expand=True)
    titre = ctk.CTkFrame(boite1, fg_color="transparent")        
    titre.pack(pady=(20, 10), padx=20)
    message = ctk.CTkFrame(boite1, fg_color="transparent")        
    message.pack(pady=(0, 10), padx=10)
    frame_bouton = ctk.CTkFrame(boite1, fg_color="transparent")
    frame_bouton.pack(fill="x", pady=(20, 10), padx=20)
    carte_connexion = ctk.CTkFrame(boite1, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(fill="x", pady=(10, 20), padx=20)  
    boite2 = ctk.CTkFrame(boite_géante, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color="transparent")        
    boite2.pack(side="right", pady=10, padx=20, fill="both", expand=True)
    img = ctk.CTkFrame(boite2, fg_color="transparent")        
    img.pack(pady=27, padx=20)

    Titre = ctk.CTkLabel(titre ,text="Bienvenue sur Sprintia\n", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack()
    messages = ctk.CTkLabel(message ,text="Content de te revoir !", font=(font_principale, taille2), text_color=couleur_text)
    messages.pack()

    button_connection = ctk.CTkButton(frame_bouton, text="✔️ Connexion", fg_color=couleur_fond, hover_color=couleur2_hover, text_color=couleur1,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), border_width=border1, border_color=couleur2, 
                           command=lambda: [vider_fenetre(app), connexion()])
    button_connection.pack(expand=True, fill="x", side="left", padx=2)
    button_inscription = ctk.CTkButton(frame_bouton, text="Inscription", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                           command=lambda: [vider_fenetre(app), inscription()])
    button_inscription.pack(expand=True, fill="x", side="right", padx=2)

    app.bind('<Return>', lambda event: verifier_identifiants())
    username_entry = ctk.CTkEntry(carte_connexion, placeholder_text="Pseudo", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1)
    username_entry.pack(fill="x", pady=(12, 2), padx=10)
    password_entry = ctk.CTkEntry(carte_connexion, placeholder_text="Mot de passe", show="*", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1)
    password_entry.pack(fill="x", pady=2, padx=10)

    def verifier_identifiants():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Champs manquants", "Le pseudo et le mot de passe ne peuvent pas être vides")
            return
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        try:
            curseur.execute("SELECT id FROM Account WHERE username = ? AND password = ?", (username, hashed_password))
            result = curseur.fetchone()

            if result:
                account_id = result[0]
                vider_fenetre(app)
                exercice(account_id)
            else:
                messagebox.showerror("Erreur", "Identifiants incorrects, réessaye !")
        except sqlite3.Error as e:
            messagebox.showwarning("Erreur", "Erreur de base de données lors de la connexion à ton compte !")
        except Exception as e:
            messagebox.showwarning("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_valider = ctk.CTkButton(carte_connexion, text="Se connecter", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner1, height=button_height, font=(font_principale, taille2), text_color=couleur1,
                            command=verifier_identifiants)
    button_valider.pack(fill="x", pady=(2, 12), padx=10)

    mon_image_pil = Image.open(mode_image)
    largeur_img = 300
    hauteur_img = 400
    image_redimensionner = mon_image_pil.resize((largeur_img, hauteur_img), Image.Resampling.LANCZOS)
    CTk_image = ctk.CTkImage(light_image=image_redimensionner, dark_image=image_redimensionner, size=(largeur_img, hauteur_img))
    label_image = ctk.CTkLabel(img, image=CTk_image, text="")
    label_image.pack()

def inscription():
    cadre_inscription = ctk.CTkFrame(app, fg_color=couleur_fond)        
    cadre_inscription.pack(fill="both", expand=True)

    boite_géante = ctk.CTkFrame(cadre_inscription, fg_color="transparent")        
    boite_géante.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    boite1 = ctk.CTkFrame(boite_géante, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color="transparent")        
    boite1.pack(side="left", pady=10, padx=20, fill="both", expand=True)
    titre = ctk.CTkFrame(boite1, fg_color="transparent")        
    titre.pack(pady=(20, 10), padx=20)
    message = ctk.CTkFrame(boite1, fg_color="transparent")        
    message.pack(pady=(0, 10), padx=10)
    frame_bouton = ctk.CTkFrame(boite1, fg_color="transparent")
    frame_bouton.pack(fill="x", pady=(20, 10), padx=20)
    carte_inscription = ctk.CTkFrame(boite1, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_inscription.pack(fill="x", pady=(10, 20), padx=20)  
    boite2 = ctk.CTkFrame(boite_géante, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color="transparent")        
    boite2.pack(side="right", pady=10, padx=20, fill="both", expand=True)
    img = ctk.CTkFrame(boite2, fg_color="transparent")        
    img.pack(pady=70, padx=20)

    Titre = ctk.CTkLabel(titre ,text="Bienvenue sur Sprintia\n", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack()
    message = ctk.CTkLabel(message ,text="Prêt à atteindre tes objectifs sportifs ? Tu es au bon endroit !", font=(font_principale, taille2), 
                           text_color=couleur_text, wraplength=400)
    message.pack()

    button_connection = ctk.CTkButton(frame_bouton, text="Connexion", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                           command=lambda: [vider_fenetre(app), connexion()])
    button_connection.pack(expand=True, fill="x", side="left", padx=1)
    button_inscription = ctk.CTkButton(frame_bouton, text="✔️  Inscription", fg_color=couleur_fond, hover_color=couleur2_hover, text_color=couleur1,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), border_width=border1, border_color=couleur2, 
                           command=lambda: [vider_fenetre(app), inscription()])
    button_inscription.pack(expand=True, fill="x", side="right", padx=1)

    app.bind('<Return>', lambda event: verifier_identifiants_connexion())
    username_entry = ctk.CTkEntry(carte_inscription, placeholder_text="Pseudo", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1)
    username_entry.pack(fill="x", pady=(12, 2), padx=10)
    password_entry = ctk.CTkEntry(carte_inscription, placeholder_text="Mot de passe", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, show="*")
    password_entry.pack(fill="x", pady=2, padx=10)
    password_confirm= ctk.CTkEntry(carte_inscription, placeholder_text="Confirmer mot de passe", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, show="*")
    password_confirm.pack(fill="x", pady=2, padx=10)
    
    def verifier_identifiants_connexion():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        password_confirmation = password_confirm.get().strip()
        password_encode = password.encode("UTF-8")
        try:
            if not username_entry or not password_entry:
                messagebox.showerror("Champs manquants", "Le pseudo et le mot de passe ne peuvent pas être vides !")
                return
            if password != password_confirmation:
                messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas !")
                return
            if (password_valide(password)):
                sha256 = hashlib.sha256()
                sha256.update(password_encode)
                hashed_password = sha256.hexdigest()
                curseur.execute("INSERT INTO Account (username, password) VALUES (?, ?)", (username, hashed_password))
                con.commit()
                account_id = curseur.lastrowid
                messagebox.showinfo("Inscription réussie", f"Bienvenue {username} !")
                vider_fenetre(app)
                exercice(account_id)
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erreur", "Ce pseudo est déjà utilisé. Essaye d'en utiliser un autre !")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'inscription !")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_valider = ctk.CTkButton(carte_inscription, text="S'incrire", fg_color=couleur2, hover_color=couleur2_hover,
                                corner_radius=corner1, height=button_height, font=(font_principale, taille2), text_color=couleur1,
                                command=verifier_identifiants_connexion)
    button_valider.pack(fill="x", pady=(2, 12), padx=10)

    mon_image_pil = Image.open(mode_image)
    largeur_img = 300
    hauteur_img = 400
    image_redimensionner = mon_image_pil.resize((largeur_img, hauteur_img), Image.Resampling.LANCZOS)
    CTk_image = ctk.CTkImage(light_image=image_redimensionner, dark_image=image_redimensionner, size=(largeur_img, hauteur_img))
    label_image = ctk.CTkLabel(img, image=CTk_image, text="")
    label_image.pack()

def auto_connect():
    try:
        curseur.execute("SELECT statut FROM Auto_connect")
        result_statut = curseur.fetchone()
        statut = result_statut[0] if result_statut else None
        if statut == "déconnexion":
            connexion()
        elif statut == "" or statut is None:
            connexion()
        else:
            account_id = result_statut[0] 
            exercice(account_id)  
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors du lancement de Auto-connect !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = ctk.CTk(fg_color=couleur_fond)
    app.geometry("1050x600")
    app.title("Sprintia")
    création()
    auto_connect()
    app.protocol("WM_DELETE_WINDOW", lambda: fermer_app(app, con))
    app.bind("<Control-w>", lambda event: fermer_app(app, con))
    app.after(450, lambda: app.state("zoomed"))
    app.bind("<Escape>", lambda event: app.state("normal"))
    app.mainloop()
