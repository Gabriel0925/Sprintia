from app_ressource import * 
from update_database import con, curseur, con_coach, curseur_coach

def JRM_coach(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre
              , connexion, inscription):
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)
    option_style = ["Bienveillant (par défaut)", "Strict & Motivant", "Copain", "Inshape"]
    option_avatar = ["👨", "👧","🤖", "🥷", "🤡", "🤠", "🐵", "😺", "💀", "🥸", "👴", "👵", "👻", "🦐"]

    try:
        curseur_coach.execute("SELECT version, date_de_sortie FROM info")
        version_date_result = curseur_coach.fetchone()
        curseur.execute("SELECT nom_du_coach, style_du_coach, avatar FROM Coach WHERE account_id = ?", (account_id,))
        personnalité_du_coach = curseur.fetchone()
        if personnalité_du_coach:
            nom_coach_user = personnalité_du_coach[0]
            style_du_coach = personnalité_du_coach[1]
            avatar_du_coach = personnalité_du_coach[2]
        else:
            nom_coach_user = None
            style_du_coach = None
            avatar_du_coach = None
        if style_du_coach == "Inshape":
            table_personnalité = "phrase_exemple_inshape"
        elif style_du_coach == "Strict & Motivant":
            table_personnalité = "phrase_exemple_strict_mais_motivant"
        elif style_du_coach == "Copain":
            table_personnalité = "phrase_exemple_copain"
        else:
            table_personnalité = "phrase_exemple_bienveilllant"
        curseur_coach.execute(f"SELECT {table_personnalité} FROM phrase_exemple")
        phrase_exemple = curseur_coach.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Erreur de base de données", "Une erreur s'est produite lors de la requête de la version !")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur innatendu s'est produite !")
        return

    def maj_avatar_coach(choice):
        nom_coach_synchronisé = nom_coach_entry.get().strip()
        if nom_coach_synchronisé:
            pass
        else:
            nom_coach_synchronisé = nom_coach_user
        avatar_coach_synchronisé = choice
        text.configure(text=f"{avatar_coach_synchronisé} {nom_coach_synchronisé if nom_coach_synchronisé is not None else "JRM Coach"}")

    def maj_exemple_coach(choice):
        nom_coach_synchronisé = nom_coach_entry.get().strip()
        if nom_coach_synchronisé:
            pass
        else:
            nom_coach_synchronisé = nom_coach_user
        style_coach_synchronisé = choice
        if style_coach_synchronisé == "Inshape":
            table_personnalité = "phrase_exemple_inshape"
        elif style_coach_synchronisé == "Strict & Motivant":
            table_personnalité = "phrase_exemple_strict_mais_motivant"
        elif style_coach_synchronisé == "Copain":
            table_personnalité = "phrase_exemple_copain"
        else:
            table_personnalité = "phrase_exemple_bienveilllant"
        curseur_coach.execute(f"SELECT {table_personnalité} FROM phrase_exemple")
        phrase_exemple_synchronisé = curseur_coach.fetchone()[0]
        phrase_exemple_coach.configure(text=f"Salut, moi c’est {nom_coach_synchronisé if nom_coach_synchronisé is not None else "JRM Coach"}, ton coach sportif ! {phrase_exemple_synchronisé}")

    Titre = ctk.CTkLabel(app ,text="JRM Coach", font=(font_secondaire, taille1))
    Titre.pack(padx=10, pady=10)

    frame_tout = ctk.CTkFrame(app, fg_color="transparent", corner_radius=corner2, border_width=border1, border_color=couleur1)
    frame_tout.pack(pady=(20, 10))
    frame_version = ctk.CTkFrame(frame_tout, fg_color="transparent", corner_radius=corner2)
    frame_version.pack(padx=10, pady=(10, 5))
    frame_dev = ctk.CTkFrame(frame_tout, fg_color="transparent", corner_radius=corner2)
    frame_dev.pack(padx=10, pady=(5, 10))

    version = ctk.CTkLabel(frame_version, text="Version du JRM Coach : ",
                          font=(font_principale, taille2), text_color=couleur1)
    version.pack(side="left", padx=0, pady=5)
    num_version = ctk.CTkLabel(frame_version, text=f"{version_date_result[0] if version_date_result else "Version non identifiée"}",
                          font=(font_principale, taille2), text_color=couleur1)
    num_version.pack(side="left", padx=0, pady=5)
    nom_dev = ctk.CTkLabel(frame_dev, text=f"Date de sortie : {version_date_result[1] if version_date_result else "Date non identifiée"}",
                          font=(font_principale, taille2), text_color=couleur1)
    nom_dev.pack(side="right", padx=10, pady=5)

    boite_totale = ctk.CTkFrame(app, fg_color="transparent")
    boite_totale.pack(expand=True, fill="both", padx=10, pady=10)

    boite1 = ctk.CTkFrame(boite_totale, fg_color=couleur2, corner_radius=corner1, border_color=couleur1, border_width=border1)
    boite1.pack(side="left", expand=True, fill="both", padx=(10, 5), pady=10)

    app.bind('<Return>', lambda event: verification(connexion, inscription))
    nom_coach_entry = ctk.CTkEntry(boite1, placeholder_text=f"{nom_coach_user if nom_coach_user else "Nom de ton coach"}", border_color=couleur_fond, fg_color=couleur_fond,
                                    height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                    text_color=couleur1, width=220)
    nom_coach_entry.pack(expand=True, fill="both", side="top", padx=12, pady=(12, 2))
    style_coach_entry = ctk.CTkComboBox(boite1, values=option_style, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=220, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1,
                                    command=maj_exemple_coach)
    style_coach_entry.pack(expand=True, fill="both", side="top", padx=12, pady=2)
    style_coach_entry.set(f"{style_du_coach if style_du_coach else "Style de ton coach"}")
    avatar_coach_entry = ctk.CTkComboBox(boite1, values=option_avatar, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=220, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1,
                                    command=maj_avatar_coach)
    avatar_coach_entry.pack(expand=True, fill="both", side="top", padx=12, pady=2)
    avatar_coach_entry.set(f"{avatar_du_coach if avatar_du_coach else "Avatar de ton coach"}")

    def verification(connexion, inscription):
        nom_coach = nom_coach_entry.get().strip()
        style_coach = style_coach_entry.get().strip()
        avatar_coach = avatar_coach_entry.get().strip()
        if len(nom_coach) > 14:
            messagebox.showerror("Nom du coach trop long", "Le nom du coach ne doit pas dépasser 12 caractères !")
            return
        if not nom_coach:
            if nom_coach_user == None:
                messagebox.showerror("Champs vide", "Le champs 'Nom de ton coach' est obligatoire !") 
                return
            else:
                nom_coach = nom_coach_user
        if style_coach == "Style de ton coach":
            messagebox.showerror("Champs vide", "Le champs 'Style de ton coach' est obligatoire !") 
            return
        if style_coach == "Strict & Motivant":
            style_coach = "Strict"
        elif style_coach == "Bienveillant (par défaut)":
            style_coach = "Bienveillant"
        if avatar_coach == "Avatar de ton coach":
            messagebox.showerror("Champs vide", "Le champs 'Avatar de ton coach' est obligatoire !") 
            return
        if nom_coach == nom_coach_user and style_coach == style_du_coach and avatar_coach == avatar_du_coach:
            messagebox.showerror("Erreur", "Tu n'as pas modifié ton coach ! Essaie de modifier son nom, son style ou son avatar pour le personnaliser !")
            return
        sauvegarde(nom_coach, style_coach, avatar_coach, connexion, inscription)

    def sauvegarde(nom_coach, style_coach, avatar_coach, connexion, inscription):
        try:
            curseur.execute("SELECT account_id FROM Coach WHERE account_id = ?", (account_id,))
            result = curseur.fetchone()
            if result:
                curseur.execute("UPDATE Coach SET nom_du_coach = ?, style_du_coach = ?, avatar = ? WHERE account_id = ?", 
                                (nom_coach, style_coach, avatar_coach, account_id))
                con.commit()
            else:
                curseur.execute("INSERT INTO Coach (account_id, nom_du_coach, style_du_coach, avatar) VALUES (?, ?, ?, ?)", 
                                (account_id, nom_coach, style_coach, avatar_coach))
                con.commit()
            messagebox.showinfo("Succès", "Ton coach a bien été enregistré ! Maintenant, plus qu'à écouter le coach !")
            vider_fenetre(app)
            parametres(account_id, connexion, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur de base de données", "Une erreur s'est produite lors de l'insertion des données !")
            return
        except Exception as e:
            messagebox.showerror("Erreur innatendu", "Une erreur innatendu s'est produite !")
            return
    button_valider = ctk.CTkButton(boite1, text="💾 Enregistrer ton coach", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1, border_color=couleur2, border_width=border1,
                                    font=(font_principale, taille3),
                                    command=lambda : verification(connexion, inscription))
    button_valider.pack(expand=True, fill="both", side="top", padx=12, pady=(2, 12))

    boite2 = ctk.CTkFrame(boite_totale, fg_color="transparent", corner_radius=corner1, border_color=couleur1, border_width=border1)
    boite2.pack(side="right", fill="both", padx=(5, 10), pady=10)
    nom_frame = ctk.CTkFrame(boite2, fg_color="transparent", corner_radius=corner1)
    nom_frame.pack(side="top", fill="both", padx=12, pady=12)
    exemple_coach = ctk.CTkFrame(boite2, fg_color="transparent", corner_radius=corner1)
    exemple_coach.pack(side="top", fill="both", padx=12, pady=12)

    text = ctk.CTkLabel(nom_frame, text=f"{avatar_du_coach if avatar_du_coach is not None else "👨"} {nom_coach_user if nom_coach_user is not None else "JRM Coach"}", font=(font_secondaire, taille2), 
                        text_color=couleur1, wraplength=300, justify="left", anchor="w")
    text.pack(fill="both", padx=10, pady=10)
    phrase_exemple_coach = ctk.CTkLabel(exemple_coach, 
                                    text=f"Salut, moi c’est {nom_coach_user if nom_coach_user is not None else "JRM Coach"}, ton coach sportif ! {phrase_exemple[0]}",
                                    font=(font_principale, taille3), text_color=couleur1, wraplength=600, justify="left", anchor="w")
    phrase_exemple_coach.pack(fill="both", padx=10, pady=10)

def a_propos(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="À propos", font=(font_secondaire, taille1))
    Titre.pack(padx=10, pady=10)

    conteneur = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    conteneur.pack(fill="both", expand=True, padx=10, pady=10)

    sous_titre3= ctk.CTkLabel(conteneur, text="Sprintia c'est quoi ?", font=(font_secondaire, taille2)
                            , justify="left", text_color=couleur_text)
    sous_titre3.pack(pady=15)
    c_quoi = ctk.CTkLabel(conteneur, 
                            text="Sprintia est conçue pour t'aider avant et après une activité grâce à des algorithmes qui te permettront de mieux t’entraîner :\n" \
                            "\n◉ Charge d'entraînement :\n " \
                            "La charge d'entraînement va permettre aux sportifs d’adapter l’intensité et le volume de leurs entraînement futur et à venir. La charge d’entraînement permet de quantifier le stress physique imposé à un corps durant une période de une semaine.\n" \
                            "\n◉ Indulgence de course :\n " \
                            "L’indulgence de course t’aide à ajuster ton kilométrage des 7 derniers jours pour rester dans une progression optimale pour tes futures entraînement, sans dépasser ta limite. Tu peux ainsi continuer à t’améliorer tout en réduisant les risques de blessure.\n" \
                            "\n◉ Prédicteur de performance :\n " \
                            "Le prédicteur de performance estime tes temps sur n'importe quelle distance (5 km, 10 km, semi-marathon, marathon) à partir d’une course récente.",
                            font=(font_principale, taille2),  wraplength=950, justify="left")
    c_quoi.pack(padx=10, pady=10)
    sous_titre= ctk.CTkLabel(conteneur, text="Pourquoi j'ai créé Sprintia ?", font=(font_secondaire, taille2),
                            justify="left")
    sous_titre.pack(pady=15)
    pourquoi = ctk.CTkLabel(conteneur, text="J'ai lancé Sprintia parce que pour moi, on n'a pas besoin de dépenser des fortunes pour avoir de la qualité. C'est un peu comme avec" \
                        " les montres connectées : on ne devrait pas être obligé d'acheter la toute dernière et la plus chère pour pouvoir profiter des dernières fonctionnalités." \
                        " De plus, certains constructeurs de montre connectées ce permettre de mettre un abonnement mensuel pour pouvoir bénificié de toutes les fonctionnalités !" \
                        " Du coup, j'ai décidé de créer Sprintia pour faire les choses à ma manière !",
                        font=(font_principale, taille2), wraplength=950, justify="left")
    pourquoi.pack(padx=10)
    sous_titre2= ctk.CTkLabel(conteneur, text="Qui suis-je ?", font=(font_secondaire, taille2)
                            , justify="left")
    sous_titre2.pack(pady=15)
    quisuisje = ctk.CTkLabel(conteneur, 
                            text="J'adore le sport, la tech et l'imformatique. Ce que j'adore dans le sport," \
                            " c'est les algorithmes qui vont m'aider à m'entraîner et à progresser dans mon sport, sans avoir de coach." \
                            " Je développe Sprintia pour vous aider à vous entraîner gratuitement." \
                            " Sprintia est développé par GC.",
                            font=(font_principale, taille2),  wraplength=950, justify="left")
    quisuisje.pack(padx=10, pady=10)

def correction_bug(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    boite2 = ctk.CTkFrame(app, fg_color=couleur_fond)
    boite2.pack(side="right", expand=True, fill="both")
    header = ctk.CTkFrame(boite2, fg_color="transparent")
    header.pack(pady=10, padx=10)

    frame_tout = ctk.CTkFrame(boite2, fg_color="transparent", corner_radius=corner2, border_width=border1, border_color=couleur1)
    frame_tout.pack(pady=(20, 10))
    frame_version = ctk.CTkFrame(frame_tout, fg_color="transparent", corner_radius=corner2)
    frame_version.pack(padx=10, pady=(10, 5))
    frame_dev = ctk.CTkFrame(frame_tout, fg_color="transparent", corner_radius=corner2)
    frame_dev.pack(padx=10, pady=(5, 10))

    frame_boutons = ctk.CTkFrame(boite2, fg_color="transparent")
    frame_boutons.pack(pady=(20, 10), padx=20)

    conteneur_patch_note = ctk.CTkFrame(boite2, fg_color=couleur2, corner_radius=corner1, border_width=border1, border_color=couleur1)
    conteneur_patch_note.pack(expand=True, fill="both", pady=(10, 15), padx=10)
    patch_note = ctk.CTkScrollableFrame(conteneur_patch_note, fg_color="transparent", scrollbar_button_color=couleur1,
                                           scrollbar_button_hover_color=couleur1_hover)
    patch_note.pack(expand=True, fill="both", pady=12, padx=12)

    Titre = ctk.CTkLabel(header, text=f"Quoi de neuf dans Sprintia {version_numéro}", text_color=couleur_text, font=(font_secondaire, taille1))
    Titre.pack(side="left", padx=5)

    button_bug = ctk.CTkButton(frame_boutons, text="Nouvelles fonctionnalités", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, width=200,
                            command=lambda: [vider_fenetre(app), nouvelle_fonction(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_bug.pack(side="left", padx=2)
    button_fonction = ctk.CTkButton(frame_boutons, text="Améliorations", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, width=200,
                            command=lambda: [vider_fenetre(app), amélioration(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_fonction.pack(side="left", padx=2)
    button_avis = ctk.CTkButton(frame_boutons, text="✔️ Corrections de bugs", fg_color=couleur_fond, hover_color=couleur2_hover, text_color=couleur1,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), border_width=border1, border_color=couleur2, width=200,
                            command=lambda: [vider_fenetre(app), correction_bug(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_avis.pack(side="left", padx=2)

    version = ctk.CTkLabel(frame_version, text="Version Sprintia : ",
                          font=(font_principale, taille2), text_color=couleur1)
    version.pack(side="left", padx=0, pady=5)
    num_version = ctk.CTkLabel(frame_version, text=f"{version_entière}",
                          font=(font_principale, taille2), text_color=couleur1)
    num_version.pack(side="left", padx=0, pady=5)
    nom_dev = ctk.CTkLabel(frame_dev, text=f"Type : {type_de_maj}\nDate de sortie : {date_de_sortie}",
                          font=(font_principale, taille2), text_color=couleur1)
    nom_dev.pack(side="right", padx=10, pady=5)

    PatchNote = ctk.CTkLabel(patch_note, font=(font_principale, taille2), text_color=couleur1, wraplength=925, anchor="w", corner_radius=corner1,
    text=f"""🐛 Corrections de bugs et optimisation\n
    • Cliquer sur la croix (d'une boite de dialogue) ferme désormais la boîte de dialogue, au lieu d’ouvrir quand même l’application (ex : le site des actu de Sprintia).
    • Correction de fautes d'orthographe dans l'application.
    • Optimisation du code pour améliorer la maintenance.
    • Amélioration de la sécurité.
    • Code désormais plus robuste.
    • Correction d'un bug lors de la modification d'un objectif/compétition.
    • Correction d'un bug qui empêchait la mise en pause des analyses.
    • Correction d'un bug majeur qui ne supprime pas une activité.
    • Optimisation de l'interface en fonction de la taille de l'écran.
    • Correction d'un bug qui empêchait le retour à la ligne dans 'Contribue à améliorer Sprintia'.
    • Amélioration des vérifications d'enregistrement d'activité pour éviter les erreurs ou les bugs.
    • Correction d'un bug qui empêchait de valider avec la touche "Entrée" dans ajouter un objectif.
    • Correction d'un problème d'affichage mineur dans la charge d'entraînement, certains blocs dépassait légèrement de son conteneur.
    • Refonte back-end : découpage du gros fichier en plusieurs modules pour un code plus organisé."""
    , justify="left")
    PatchNote.pack(expand=True, fill="both", padx=5, pady=5)

def amélioration(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    boite2 = ctk.CTkFrame(app, fg_color=couleur_fond)
    boite2.pack(side="right", expand=True, fill="both")
    header = ctk.CTkFrame(boite2, fg_color="transparent")
    header.pack(pady=10, padx=10)

    frame_tout = ctk.CTkFrame(boite2, fg_color="transparent", corner_radius=corner2, border_width=border1, border_color=couleur1)
    frame_tout.pack(pady=(20, 10))
    frame_version = ctk.CTkFrame(frame_tout, fg_color="transparent", corner_radius=corner2)
    frame_version.pack(padx=10, pady=(10, 5))
    frame_dev = ctk.CTkFrame(frame_tout, fg_color="transparent", corner_radius=corner2)
    frame_dev.pack(padx=10, pady=(5, 10))

    frame_boutons = ctk.CTkFrame(boite2, fg_color="transparent")
    frame_boutons.pack(pady=(20, 10), padx=20)

    conteneur_patch_note = ctk.CTkFrame(boite2, fg_color=couleur2, corner_radius=corner1, border_width=border1, border_color=couleur1)
    conteneur_patch_note.pack(expand=True, fill="both", pady=(10, 15), padx=10)
    patch_note = ctk.CTkScrollableFrame(conteneur_patch_note, fg_color="transparent", scrollbar_button_color=couleur1,
                                           scrollbar_button_hover_color=couleur1_hover)
    patch_note.pack(expand=True, fill="both", pady=12, padx=12)

    Titre = ctk.CTkLabel(header, text=f"Quoi de neuf dans Sprintia {version_numéro}", text_color=couleur_text, font=(font_secondaire, taille1))
    Titre.pack(side="left", padx=5)

    button_bug = ctk.CTkButton(frame_boutons, text="Nouvelles fonctionnalités", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, width=200,
                            command=lambda: [vider_fenetre(app), nouvelle_fonction(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_bug.pack(side="left", padx=2)
    button_fonction = ctk.CTkButton(frame_boutons, text="✔️ Améliorations", fg_color=couleur_fond, hover_color=couleur2_hover, text_color=couleur1,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), border_width=border1, border_color=couleur2, width=200,
                            command=lambda: [vider_fenetre(app), amélioration(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_fonction.pack(side="left", padx=2)
    button_avis = ctk.CTkButton(frame_boutons, text="Corrections de bugs", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, width=200,
                            command=lambda: [vider_fenetre(app), correction_bug(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_avis.pack(side="left", padx=2)

    version = ctk.CTkLabel(frame_version, text="Version Sprintia : ",
                          font=(font_principale, taille2), text_color=couleur1)
    version.pack(side="left", padx=0, pady=5)
    num_version = ctk.CTkLabel(frame_version, text=f"{version_entière}",
                          font=(font_principale, taille2), text_color=couleur1)
    num_version.pack(side="left", padx=0, pady=5)
    nom_dev = ctk.CTkLabel(frame_dev, text=f"Type : {type_de_maj}\nDate de sortie : {date_de_sortie}",
                          font=(font_principale, taille2), text_color=couleur1)
    nom_dev.pack(side="right", padx=10, pady=5)

    PatchNote = ctk.CTkLabel(patch_note, font=(font_principale, taille2), text_color=couleur1, wraplength=925, anchor="w", corner_radius=corner1,
            text=f"""📊 Améliorations\n
    • Ajout d’une boîte de dialogue de confirmation avant l’ouverture d’app externe.
    • Ajustement de l'interface utilisateur avec Matérial 3 Expressive désormais plus présent.
    • Simplification et amélioration de l'ergonomie pour la modification de ton compte.
    • Plus besoin d'éditeur de code pour lancer Sprintia, désormais tu n'as qu'à double-cliquer sur le fichier "Sprintia.vbs".
    • Tu peux désormais créer un raccourci sur ton bureau pour lancer Sprintia plus rapidement et avec une icône.
    • 80 caractères maximum pour ta bio.
    • Nouveau style de tableau.
    • Suppresion de l'accès aux actualités de Sprintia parce que rien n'était posté.
    • Demande de l'ancien mot de passe lors de la modification du mot de passe.
    • De nouveaux caractères sont prises en charge pour les mots de passe ("!",  "@",  "#",  "$",  "%",  "^",  "&", "*", "(", ")", "-", "_", "=", "+", "[", "]",  "{", "}", ";", ":", ",", "<", ">", ".", "?").
    • Désormais, la Valeur de RPE par défaut est 1.
    • Les mots ne sont plus coupé dans les 'TextBox'.
    • Caractères maximum pour certains champs quand tu ajoutes une activité.
    • Ajout de plus de 10 choix de type d'entraînement pour plus que l'utilisateur ne soit plus perdu.
    • Ajout d'un calendrier pour choisir la date quand tu ajoutes une activité.
    • Tous les formats de date sont acceptés (JJ-MM-AAAA, JJ/MM/AAAA, JJ.MM.AAAA, JJ MM AAAA, JJ_MM_AAAA, JJ,MM,AAAA).
    • Quand tu saisis une distance, tu peux mettre des virgules, des espaces, des tirais du bas, "km" ou "KM" (ex : 10,5 km, 10 5, 10_5, 10.5).
    • Sprintia s'ouvre directement en plein écran.
    • La touche "Échap" permet de quitter le mode plein écran.
    • Design unifié peut importe si ton ordinateur est en mode sombre ou clair les couleurs ne s'adapteront plus ça permet de renforcer l'identité visuel de Sprintia.
    • Les boutons de retour inutiles ont été supprimés."""
    , justify="left")
    PatchNote.pack(expand=True, fill="both", padx=5, pady=5)

def nouvelle_fonction(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    boite2 = ctk.CTkFrame(app, fg_color=couleur_fond)
    boite2.pack(side="right", expand=True, fill="both")
    header = ctk.CTkFrame(boite2, fg_color="transparent")
    header.pack(pady=10, padx=10)

    frame_tout = ctk.CTkFrame(boite2, fg_color="transparent", corner_radius=corner2, border_width=border1, border_color=couleur1)
    frame_tout.pack(pady=(20, 10))
    frame_version = ctk.CTkFrame(frame_tout, fg_color="transparent", corner_radius=corner2)
    frame_version.pack(padx=10, pady=(10, 5))
    frame_dev = ctk.CTkFrame(frame_tout, fg_color="transparent", corner_radius=corner2)
    frame_dev.pack(padx=10, pady=(5, 10))

    frame_boutons = ctk.CTkFrame(boite2, fg_color="transparent")
    frame_boutons.pack(pady=(20, 10), padx=20)

    conteneur_patch_note = ctk.CTkFrame(boite2, fg_color=couleur2, corner_radius=corner1, border_width=border1, border_color=couleur1)
    conteneur_patch_note.pack(expand=True, fill="both", pady=(10, 15), padx=10)
    patch_note = ctk.CTkScrollableFrame(conteneur_patch_note, fg_color="transparent", scrollbar_button_color=couleur1,
                                           scrollbar_button_hover_color=couleur1_hover)
    patch_note.pack(expand=True, fill="both", pady=12, padx=12)

    Titre = ctk.CTkLabel(header, text=f"Quoi de neuf dans Sprintia {version_numéro}", text_color=couleur_text, font=(font_secondaire, taille1))
    Titre.pack(side="left", padx=5)

    button_bug = ctk.CTkButton(frame_boutons, text="✔️ Nouvelles fonctionnalités", fg_color=couleur_fond, hover_color=couleur2_hover, text_color=couleur1,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), border_width=border1, border_color=couleur2, width=200,
                            command=lambda: [vider_fenetre(app), nouvelle_fonction(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_bug.pack(side="left", padx=2)
    button_fonction = ctk.CTkButton(frame_boutons, text="Améliorations", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, width=200,
                            command=lambda: [vider_fenetre(app), amélioration(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_fonction.pack(side="left", padx=2)
    button_avis = ctk.CTkButton(frame_boutons, text="Corrections de bugs", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, width=200,
                            command=lambda: [vider_fenetre(app), correction_bug(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_avis.pack(side="left", padx=2)

    version = ctk.CTkLabel(frame_version, text="Version Sprintia : ",
                          font=(font_principale, taille2), text_color=couleur1)
    version.pack(side="left", padx=0, pady=5)
    num_version = ctk.CTkLabel(frame_version, text=f"{version_entière}",
                          font=(font_principale, taille2), text_color=couleur1)
    num_version.pack(side="left", padx=0, pady=5)
    nom_dev = ctk.CTkLabel(frame_dev, text=f"Type : {type_de_maj}\nDate de sortie : {date_de_sortie}",
                          font=(font_principale, taille2), text_color=couleur1)
    nom_dev.pack(side="right", padx=10, pady=5)

    PatchNote = ctk.CTkLabel(patch_note, font=(font_principale, taille2), text_color=couleur1, wraplength=925, anchor="w", corner_radius=corner1,
        text=f"""🆕 Nouvelles fonctionnalités\n
    • La fonction VMA fait peau neuve :
        1. Nouvelle interface : organisation en cadres,...
        2. Plusieurs tests disponibles : demi-Cooper, Cooper, Luc Léger, course de référence.
        3. Formats de temps élargis (hh:mm:ss, mm:ss, minutes).
        4. Tableau des zones enrichi avec allures, objectifs et exemples de séances.
        5. Nouveaux boutons : Sauvegarder & Historique.
        6. Texte explicatif sur la VMA et son utilité.\n
    • Auto-connect : plus besoin de te reconnecter à chaque lancement de Sprintia, tu restes connecté automatiquement.
    • JRM Coach te donne désormais tes stats sur la semaine.
    • Lors de la création de ton compte, tu ne peux plus choisir de mots jugé sensible par google (ex : connard,...).
    • Remplissage automatique de certains champs lors d'un enregistrement d'une activité, on l'aperçoit grâce à cette icône "💡".
    • Nouveau mode 'Libre' quand tu ajoutes une activité : les modes 'Extérieur' et 'Intérieur' se sont assemblés pour former le mode 'Libre' :
        1. Le mode 'Libre' peut-être utilisé si ton activité ne correspond pas aux modes 'Course', 'Musculation' ou 'Football'.\n
    • Arrivé de ton coach de sport qui est intégré à plusieurs endroits dans Sprintia :
        1. Il peut te donner des conseils, des infos, des phrases de motivation, et des tips sur Sprintia.
        2. Tu peux personnaliser le nom de ce coach.
        3. Choisis un style de coach (bienveillant, strict mais motivant, pote, inshape).
        4. Tu peux même choisir son avatar !\n"""
    , justify="left")
    PatchNote.pack(expand=True, fill="both", padx=5, pady=5)

def avis(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Contribue à améliorer Sprintia", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    info = ctk.CTkLabel(app ,text="📣 Nous te remercions pour ta contribution au développement de Sprintia." \
                "\nTu peux contribuer à améliorer Sprintia en signalant des bugs, en donnant ton avis ou en proposant de nouvelles fonctionnalités.",
                font=(font_principale, taille2), wraplength=800)
    info.pack(padx=50, pady=(20, 10))

    frame_boutons = ctk.CTkFrame(app, fg_color="transparent")
    frame_boutons.pack(pady=(20, 10), padx=20)
    button_bug = ctk.CTkButton(frame_boutons, text="Signaler un bug", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, width=200,
                            command=lambda: [vider_fenetre(app), signaler_bug(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_bug.pack(side="left", padx=2)
    button_fonction = ctk.CTkButton(frame_boutons, text="Proposer une fonction", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, width=200,
                            command=lambda: [vider_fenetre(app), proposer_fonction(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_fonction.pack(side="left", padx=2)
    button_avis = ctk.CTkButton(frame_boutons, text="✔️ Rédiger un avis", fg_color=couleur_fond, hover_color=couleur2_hover, text_color=couleur1,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), border_width=border1, border_color=couleur2,  width=200,
                            command=lambda: [vider_fenetre(app), avis(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_avis.pack(side="left", padx=2)
    
    avis_entry = ctk.CTkTextbox(app, corner_radius=corner1, fg_color=couleur2, font=(font_principale, taille2),
                                scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover, text_color=couleur1,
                                border_color=couleur1, border_width=border1, wrap="word")
    avis_entry.pack(expand=True, fill="both", padx=10, pady=(10, 5))
    avis_entry.insert("0.0", "Ton avis :\n")

    def envoyer():
        avis = avis_entry.get("1.0", "end").strip()
        if avis == "Ton avis :":
            messagebox.showerror("Avis vide", "Merci de renseigner le champ 'Avis' !")
            return
        #destinataire
        email_receiver = 'gabchap486@gmail.com'
        #objet
        subject = "Avis sur Sprintia"
        body = f"Message de l'utilisateur:\n{avis}"
        mailto_link = f"mailto:{email_receiver}?subject={quote(subject)}&body={quote(body)}"
        try:
            reponse = messagebox.askokcancel("Première étape terminée", "Veux-tu que ton application de mail par défaut s'ouvre pour que tu puisses envoyer cet avis ?")
            if reponse:
                webbrowser.open(mailto_link)
            else:
                pass
        except Exception as e:
            messagebox.showerror("Erreur", "Impossible d'ouvrir ton application mail. Vérifie que tu as une application pour gérer tes mails !")
    button_check = ctk.CTkButton(app, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=height_expressive, text_color=couleur1,
                                    font=(font_principale, taille2), border_width=border1, border_color=couleur2,
                                    command=lambda: envoyer())
    button_check.pack(padx=5, pady=(5, 10))

def proposer_fonction(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Contribue à améliorer Sprintia", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    info = ctk.CTkLabel(app ,text="📣 Nous te remercions pour ta contribution au développement de Sprintia." \
                "\nTu peux contribuer à améliorer Sprintia en signalant des bugs, en donnant ton avis ou en proposant de nouvelles fonctionnalités.",
                font=(font_principale, taille2), wraplength=800)
    info.pack(padx=50, pady=(20, 10))

    frame_boutons = ctk.CTkFrame(app, fg_color="transparent")
    frame_boutons.pack(pady=(20, 10), padx=20)
    button_bug = ctk.CTkButton(frame_boutons, text="Signaler un bug", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, width=200,
                            command=lambda: [vider_fenetre(app), signaler_bug(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_bug.pack(side="left", padx=2)
    button_fonction = ctk.CTkButton(frame_boutons, text="✔️ Proposer une fonction", fg_color=couleur_fond, hover_color=couleur2_hover, text_color=couleur1,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), border_width=border1, border_color=couleur2, width=200,
                            command=lambda: [vider_fenetre(app), proposer_fonction(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_fonction.pack(side="left", padx=2)
    button_avis = ctk.CTkButton(frame_boutons, text="Rédiger un avis", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, width=200,
                            command=lambda: [vider_fenetre(app), avis(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_avis.pack(side="left", padx=2)
    
    avis_entry = ctk.CTkTextbox(app, corner_radius=corner1, fg_color=couleur2, font=(font_principale, taille2),
                                scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover, text_color=couleur1,
                                border_color=couleur1, border_width=border1, wrap="word")
    avis_entry.pack(expand=True, fill="both", padx=10, pady=(10, 5))
    avis_entry.insert("0.0", "Description de ta fonctionnalité :\n")

    def envoyer():
        avis = avis_entry.get("1.0", "end").strip()
        if avis == "Description de ta fonctionnalité :":
            messagebox.showerror("Proposition de fonctionnalité vide", "Merci de renseigner le champ 'Fonctionnalité' !")
            return
        #destinataire
        email_receiver = 'gabchap486@gmail.com'
        #objet
        subject = "Proposition de nouvelle fonctionnalité"
        body = f"Message de l'utilisateur:\n{avis}"
        mailto_link = f"mailto:{email_receiver}?subject={quote(subject)}&body={quote(body)}"
        try:
            reponse = messagebox.askokcancel("Première étape terminée", "Veux-tu que ton application de mail par défaut s'ouvre pour que tu puisses envoyer cette proposition de nouvelle fonction ?")
            if reponse:
                webbrowser.open(mailto_link)
            else:
                pass
        except Exception as e:
            messagebox.showerror("Erreur", "Impossible d'ouvrir ton application mail. Vérifie que tu as une application pour gérer tes mails !")
    button_check = ctk.CTkButton(app, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=height_expressive, text_color=couleur1,
                                    font=(font_principale, taille2), border_width=border1, border_color=couleur2,
                                    command=lambda: envoyer())
    button_check.pack(padx=5, pady=(5, 10))

def signaler_bug(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Contribue à améliorer Sprintia", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    info = ctk.CTkLabel(app ,text="📣 Nous te remercions pour ta contribution au développement de Sprintia." \
                "\nTu peux contribuer à améliorer Sprintia en signalant des bugs, en donnant ton avis ou en proposant de nouvelles fonctionnalités.",
                font=(font_principale, taille2), wraplength=800)
    info.pack(padx=50, pady=(20, 10))

    frame_boutons = ctk.CTkFrame(app, fg_color="transparent")
    frame_boutons.pack(pady=(20, 10), padx=20)
    button_bug = ctk.CTkButton(frame_boutons, text="✔️ Signaler un bug", fg_color=couleur_fond, hover_color=couleur2_hover, text_color=couleur1,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), border_width=border1, border_color=couleur2, width=200,
                            command=lambda: [vider_fenetre(app), signaler_bug(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_bug.pack(side="left", padx=2)
    button_fonction = ctk.CTkButton(frame_boutons, text="Proposer une fonction", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, width=200,
                            command=lambda: [vider_fenetre(app), proposer_fonction(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_fonction.pack(side="left", padx=2)
    button_avis = ctk.CTkButton(frame_boutons, text="Rédiger un avis", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, width=200,
                            command=lambda: [vider_fenetre(app), avis(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_avis.pack(side="left", padx=2)

    avis_entry = ctk.CTkTextbox(app, corner_radius=corner1, fg_color=couleur2, font=(font_principale, taille2),
                                scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover, text_color=couleur1,
                                border_color=couleur1, border_width=border1, wrap="word")
    avis_entry.pack(expand=True, fill="both", padx=10, pady=(10, 5))
    avis_entry.insert("0.0", "Description du bug :\n")

    def envoyer():
        avis = avis_entry.get("1.0", "end").strip()
        if avis == "Description du bug :":
            messagebox.showerror("Description du bug vide", "Merci de renseigner le champ 'Description'.")
            return
        #destinataire
        email_receiver = 'gabchap486@gmail.com'
        #objet
        subject = "Rapport de bug"
        body = f"Message de l'utilisateur:\n{avis}"
        mailto_link = f"mailto:{email_receiver}?subject={quote(subject)}&body={quote(body)}"
        try:
            reponse = messagebox.askokcancel("Première étape terminée", "Veux-tu que ton application de mail par défaut s'ouvre pour que tu puisses envoyer ce rapport de bug ?")
            if reponse:
                webbrowser.open(mailto_link)
            else:
                pass
        except Exception as e:
            messagebox.showerror("Erreur", "Impossible d'ouvrir ton application mail. Vérifie que tu as une application pour gérer tes mails !")
    button_check = ctk.CTkButton(app, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=height_expressive, text_color=couleur1,
                                    font=(font_principale, taille2), border_width=border1, border_color=couleur2,
                                    command=lambda: envoyer())
    button_check.pack(padx=5, pady=(5, 10))

def modifier_password(account_id, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre, connexion):
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Modifier ton mot de passe", font=(font_secondaire, taille1))
    Titre.pack(padx=10, pady=10)

    carte = ctk.CTkFrame(app, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)        
    carte.pack(pady=(10, 20))

    app.bind('<Return>', lambda event: new_username(account_id, connexion))
    ancien_password_entry = ctk.CTkEntry(carte, placeholder_text="Mot de passe actuel", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=widht_expressive, show="*")
    ancien_password_entry.pack(pady=(12, 2), padx=12)
    password_entry = ctk.CTkEntry(carte, placeholder_text="Nouveau mot de passe", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=widht_expressive, show="*")
    password_entry.pack(pady=2, padx=12)
    password_entry2 = ctk.CTkEntry(carte, placeholder_text="Confirme ton nouveau mot de passe", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=widht_expressive, show="*")
    password_entry2.pack(pady=2, padx=12)

    def new_username(account_id, connexion):
        ancien_password = ancien_password_entry.get()
        ancien_password_encode = ancien_password.encode("UTF-8")
        new_password = password_entry.get()
        new_password2 = password_entry2.get()
        password_encode = new_password.encode("UTF-8")
        try:
            if not ancien_password:
                messagebox.showerror("Champs vide", "Le champs 'Mot de passe actuel' est obligatoire !")
                return              
            if not new_password:
                messagebox.showerror("Champs vide", "Le champs 'Nouveau mot de passe' est obligatoire !")
                return  
            if not new_password2:
                messagebox.showerror("Champs vide", "Le champs 'Confirme ton nouveau mot de passe' est obligatoire !")
                return
            if new_password != new_password2:           
                messagebox.showerror("Erreur", "Les mots de passe saisis ne correspondent pas !")
                return
            if (password_valide(new_password)):
                hashed_password = hashlib.sha256(password_encode).hexdigest()
                hashed_password_ancien = hashlib.sha256(ancien_password_encode).hexdigest()

                curseur.execute("SELECT password FROM Account WHERE id = ?", (account_id,))
                ancien_password = curseur.fetchone()
                if ancien_password[0] == hashed_password:
                    messagebox.showerror("Erreur", "Ton nouveau mot de passe est identique au précédent !")
                    return
                if ancien_password[0] == hashed_password_ancien:
                    pass
                else:
                    messagebox.showerror("Erreur", "Ton ancien mot de passe est incorrect !")
                    return
                reponse = messagebox.askyesno("Confirmation", "Es-tu sûr·e de vouloir modifier ton mot de passe ?")
                if reponse:
                    con.execute("UPDATE Account SET password = ? WHERE id = ?", (hashed_password, account_id))
                    con.commit()
                    messagebox.showinfo("Enregistré", "Ton mots de passe à bien été modifié ! Tu n'as plus qu'à te connecter.")
                    vider_fenetre(app)
                    auto_connect_deconnexion(connexion)
                else:
                    return
        except sqlite3.Error as e:
            messagebox.showerror("Erreur base de données", "Erreur de base de données lors de la modification de ton mot de passe !")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
            return

    frame_bouton = ctk.CTkFrame(carte, fg_color="transparent")
    frame_bouton.pack(expand=True, fill="both", padx=12, pady=(0, 12))
    button_check = ctk.CTkButton(frame_bouton, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner1, height=button_height, font=(font_principale, taille2), text_color=couleur1,
                            command=lambda: new_username(account_id, connexion))
    button_check.pack(side="left", expand=True, fill="x", pady=2, padx=(10, 1))
    button_back = ctk.CTkButton(frame_bouton, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille2),
                                    command=lambda: [vider_fenetre(app), mon_compte(account_id, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre, connexion)])
    button_back.pack(side="left", expand=True, fill="x", pady=2, padx=(1, 10))

def supprimer_compte(account_id, inscription, app):
    try:
        curseur.execute("DELETE FROM Account WHERE id = ?", (account_id,))
        curseur.execute("DELETE FROM Aide_bienvenue WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Aide_compétition WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Aide_objectif WHERE account_id = ?", (account_id,))
        curseur.execute("UPDATE Auto_connect SET statut = 'déconnexion'")
        curseur.execute("DELETE FROM Coach WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Compétition WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Historique_activité WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Historique_vma WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Objectif WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Pauses WHERE account_id = ?", (account_id,))
        con.commit()
        messagebox.showinfo("Opération réussi", "Compte supprimé avec succès ! Au revoir !")
        vider_fenetre(app)
        inscription()
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la suppression du compte !")
    except Exception as e:            
        messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye !")

def mon_compte(account_id, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre, connexion):
    def suppression_compte():
        reponse = messagebox.askyesno("Suppression de compte", "Es-tu sûr de vouloir supprimer ton compte ?\nToutes tes données seront perdues !")
        if reponse:
            supprimer_compte(account_id, inscription, app)
        else:
            return
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    titre = ctk.CTkLabel(app ,text="Mon compte", font=(font_secondaire, taille1))
    titre.pack(padx=10, pady=10)

    boite = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner1, border_width=border1, border_color=couleur1)
    boite.pack(expand=True, fill="both", padx=20, pady=20)

    sous_boite = ctk.CTkFrame(boite, fg_color="transparent", corner_radius=corner1)
    sous_boite.pack(expand=True, fill="both", padx=20, pady=(15, 10))
    sous_boite_info1 = ctk.CTkFrame(sous_boite, fg_color=couleur2, corner_radius=corner1)
    sous_boite_info1.pack(side="left", expand=True, fill="both", padx=5, pady=5)
    sous_boite_info2 = ctk.CTkFrame(sous_boite, fg_color=couleur_fond, corner_radius=corner1)
    sous_boite_info2.pack(side="right", expand=True, fill="both", padx=5, pady=5)

    sous_boite2 = ctk.CTkFrame(boite, fg_color="transparent", corner_radius=corner1)
    sous_boite2.pack(expand=True, fill="both", padx=20, pady=10)
    sous_boite2_info1 = ctk.CTkFrame(sous_boite2, fg_color=couleur2, corner_radius=corner1)
    sous_boite2_info1.pack(side="left", expand=True, fill="both", padx=5, pady=5)
    sous_boite2_info2 = ctk.CTkFrame(sous_boite2, fg_color=couleur_fond, corner_radius=corner1)
    sous_boite2_info2.pack(side="right", expand=True, fill="both", padx=5, pady=5)

    sous_boite3 = ctk.CTkFrame(boite, fg_color="transparent", corner_radius=corner1)
    sous_boite3.pack(expand=True, fill="both", padx=20, pady=5) 
    sous_boite3_info1 = ctk.CTkFrame(sous_boite3, fg_color=couleur2, corner_radius=corner1)
    sous_boite3_info1.pack(side="left", expand=True, fill="both", padx=5, pady=5)
    sous_boite3_info2 = ctk.CTkFrame(sous_boite3, fg_color=couleur_fond, corner_radius=corner1)
    sous_boite3_info2.pack(side="right", expand=True, fill="both", padx=5, pady=5)

    frame_bouton = ctk.CTkFrame(boite, fg_color="transparent")
    frame_bouton.pack(padx=20, pady=20)

    curseur.execute("SELECT username, sport, bio FROM Account WHERE id = ?", (account_id,))
    result = curseur.fetchone()
    if result:
        username = result[0]
        sport = result[1]
        bio = result[2]
    else:
        messagebox.showinfo("Erreur", "Aucun compte trouvé avec cet ID.")
        return

    LABEL_MIN_WIDTH = 425
    label_username = ctk.CTkLabel(sous_boite_info1, text=f"👤 Pseudo : ", width=LABEL_MIN_WIDTH, wraplength=400, font=(font_secondaire, taille1),
                                  justify="left", anchor="w", text_color=couleur1)
    label_username.pack(expand=True, fill="both", padx=(20, 10), pady=15)
    ton_username = ctk.CTkEntry(sous_boite_info2, placeholder_text=f"{username}", font=(font_principale, taille2), width=LABEL_MIN_WIDTH, 
                                placeholder_text_color=couleur1, fg_color=couleur_fond, corner_radius=corner1, border_color=couleur_fond,
                                text_color=couleur1)
    ton_username.pack(expand=True, fill="both", padx=(15, 20), pady=15)

    label_sport = ctk.CTkLabel(sous_boite2_info1, text=f"🏅 Sport favoris :", width=LABEL_MIN_WIDTH, font=(font_secondaire, taille1),
                               justify="left", anchor="w", text_color=couleur1)
    label_sport.pack(expand=True, fill="both", padx=(20, 10), pady=15)
    ton_sport = ctk.CTkEntry(sous_boite2_info2, placeholder_text=f"{sport if sport is not None else "Aucun sport favoris..."}", width=LABEL_MIN_WIDTH, font=(font_principale, taille2),
                            placeholder_text_color=couleur1, fg_color=couleur_fond, corner_radius=corner1, border_color=couleur_fond,
                            text_color=couleur1)
    ton_sport.pack(expand=True, fill="both", padx=(15, 20), pady=15)

    label_bio = ctk.CTkLabel(sous_boite3_info1, text=f"📝 Bio : ", width=LABEL_MIN_WIDTH, font=(font_secondaire, taille1), anchor="w",
                             justify="left", wraplength=400, text_color=couleur1)
    label_bio.pack(expand=True, fill="both", padx=(20, 10), pady=15)
    ta_bio = ctk.CTkTextbox(sous_boite3_info2, width=LABEL_MIN_WIDTH, font=(font_principale, taille2), height=150,
                            fg_color=couleur_fond, corner_radius=corner1, border_color=couleur_fond, text_color=couleur1,
                            scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover,
                            wrap="word")
    ta_bio.insert("0.0", f"{bio if bio is not None else "Aucune bio..."}")
    ta_bio.pack(padx=(15, 20), pady=15)

    def enregistré():
        new_username = ton_username.get().strip()
        new_sport = ton_sport.get().strip()
        new_bio = ta_bio.get("1.0", "end").strip() # 1 pour commencer à la première ligne, .0 pour commencer au premier caractère
        if len(new_bio) > 80:
            messagebox.showerror("Erreur", "Ta bio est trop longue ! (80 caractères maximum)")
            return
        if len(new_sport) > 20:
            messagebox.showerror("Erreur", "Ton sport favoris est trop long ! (20 caractères maximum)")
            return
        if not new_username:
            new_username = username
        pseudo = new_username.lower()
        if pseudo in mot_sensible:
            messagebox.showerror("Erreur", "Ton pseudo ne doit pas contenir de mots sensibles !")
            return
        if not new_sport:
            new_sport = sport
        if not new_bio:
            new_bio = bio
        if username == new_username and sport == new_sport and bio == new_bio:
            messagebox.showinfo("Aucune modification", "Aucune modification n'a été apportée à ton compte.")
            return
        try:
            con.execute("UPDATE Account SET username = ?, sport = ?, bio = ? WHERE id = ?", (new_username, new_sport, new_bio, account_id))
            con.commit()
            messagebox.showinfo("Opération réussi", "Ton compte a été mis à jour avec succès !")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erreur base de données", "Ce pseudo est déjà utilisé, réessaye avec un autre pseudo !")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de la mise à jour de ton compte !")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

    button_enregistrer = ctk.CTkButton(frame_bouton, text="💾 Enregistrer modification", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                         command=lambda: enregistré())
    button_enregistrer.pack(side="left", padx=2)
    button_supprimer = ctk.CTkButton(frame_bouton, text="🗑️  Supprimer mon compte", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=suppression_compte)
    button_supprimer.pack(side="left", padx=2)
    button_mot_de_passe_oublié = ctk.CTkButton(frame_bouton, text="✏️ Modifier ton mot de passe", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), modifier_password(account_id, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre, connexion)])
    button_mot_de_passe_oublié.pack(side="left", padx=2)

def auto_connect_deconnexion(connexion):
    try:
        curseur.execute("UPDATE Auto_connect SET statut = 'déconnexion'")
        con.commit()
    except sqlite3.Error as e:
        pass
    except Exception as e:
        pass
    connexion()

def parametres(account_id, connexion, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)
    
    try:
        curseur.execute("SELECT nom_du_coach, avatar FROM Coach WHERE account_id = ?", (account_id,))
        personnalité_du_coach = curseur.fetchone()
        if personnalité_du_coach:
            nom_coach_user = personnalité_du_coach[0]
            avatar_du_coach = personnalité_du_coach[1]
        else:
            nom_coach_user = None
            avatar_du_coach = None
        curseur.execute("SELECT username FROM Account WHERE id = ?", (account_id,))
        result = curseur.fetchone()
        username = result[0] if result else "Mon compte"
    except sqlite3.Error as e:
        messagebox.showerror("Erreur de base de données", "Une erreur de base de données s'est produite !")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur innatendu s'est produite !")
        return

    def beta_testeur():
        messagebox.showinfo("Information", "Tu es déjà bêta testeur ! Merci pour ton aide précieuse au développement de Sprintia.")
        reponse = messagebox.askyesno("Confirmation", "Veux-tu regarder si une nouvelle bêta est disponible ?")
        if reponse:
            webbrowser.open("https://github.com/Gabriel0925/Sprintia/tree/main/Programme%20B%C3%8ATA")
        else:
            pass
        #messagebox.showwarning("Information", "Ton navigateur va s'ouvrir pour que tu puisses télécharger le programme bêta. Juste un rappel important : une version bêta n’est pas adaptée à tous les utilisateurs. Je t’invite à bien consulter la documentation avant de commencer.")
        #webbrowser.open("https://github.com/Gabriel0925/Sprintia/tree/main/Programme%20B%C3%8ATA")

    Titre = ctk.CTkLabel(app ,text="Paramètres", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    frame_bouton = ctk.CTkFrame(app, fg_color="transparent")
    frame_bouton.pack(pady=(20,0), padx=10)
    frame_bouton1 = ctk.CTkFrame(frame_bouton, fg_color="transparent")
    frame_bouton1.pack(pady=(20,0), padx=10)
    frame_bouton2 = ctk.CTkFrame(frame_bouton, fg_color="transparent")
    frame_bouton2.pack(pady=(10,0), padx=10)
    frame_bouton3 = ctk.CTkFrame(frame_bouton, fg_color="transparent")
    frame_bouton3.pack(pady=(10,0), padx=10)
    frame_bouton4 = ctk.CTkFrame(frame_bouton, fg_color="transparent")
    frame_bouton4.pack(pady=(10,20), padx=10)

    button_autre = ctk.CTkButton(frame_bouton1, text=f"👤 {username}\n_______________________\n\nPseudo, sport favoris, bio, mot de passe",
                                    corner_radius=corner2, width=500, font=(font_principale, taille2), fg_color=couleur2, 
                                    hover_color=couleur2_hover, text_color=couleur1, 
                                    command=lambda: [vider_fenetre(app), mon_compte(account_id, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre, connexion)])
    button_autre.pack(side="left", padx=10)
    button_info = ctk.CTkButton(frame_bouton1, text="📢 À propos\n_______________________\n\nVersion Sprintia, qui suis-je", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1, 
                                    command=lambda: [vider_fenetre(app), a_propos(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_info.pack(side="left", padx=(0, 10))
    button_nouveauté = ctk.CTkButton(frame_bouton2, text=f"✨ Quoi de neuf dans Sprintia {version_numéro}\n_______________________\n\nType, date de sortie, nouveautés", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), nouvelle_fonction(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_nouveauté.pack(side="left", padx=10)
    button_avis = ctk.CTkButton(frame_bouton2, text="🤝 Contribue à améliorer Sprintia\n_______________________\n\nSignaler un bug, proposer une fonction, avis", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1, 
                                    command=lambda: [vider_fenetre(app), signaler_bug(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_avis.pack(side="left", padx=(0, 10))  
    button_avis = ctk.CTkButton(frame_bouton3, text="🧪 Rejoindre la bêta\n_______________________\n\nFonctionnalités en avant-première", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1, 
                                    command=beta_testeur)
    button_avis.pack(side="left", padx=10)      
    button_coach = ctk.CTkButton(frame_bouton3, text=f"{avatar_du_coach if avatar_du_coach is not None else "👨"} {nom_coach_user if nom_coach_user is not None else "JRM Coach"}\n_______________________\n\nPersonnalise ton coach", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), JRM_coach(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre, connexion, inscription)])
    button_coach.pack(side="left", padx=(0, 10))      
    button_deco = ctk.CTkButton(frame_bouton4, text="🚪Déconnexion\n_______________________\n\nSe déconnecter, couper le lien", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), auto_connect_deconnexion(connexion)])
    button_deco.pack()
