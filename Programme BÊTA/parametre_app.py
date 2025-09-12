from app_ressource import * 
from update_database import con, curseur

def a_propos(account_id, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="À propos", font=(font_secondaire, taille1))
    Titre.pack(pady=20)

    frame_slogan = ctk.CTkFrame(app, fg_color="transparent")
    frame_slogan.pack(padx=10, pady=(20, 10))
    slogan = ctk.CTkLabel(frame_slogan, text="Sprintia est conçue pour t'aider avant et après un entraînement\n\n" \
    "Sprintia est développé par Gabriel Chapet",
                          font=(font_principale, taille2))
    slogan.pack()

    conteneur = ctk.CTkFrame(app, fg_color=couleur_fond, corner_radius=corner1,
                             border_width=border1, border_color=couleur1)
    conteneur.pack(fill="both", expand=True, padx=25, pady=25)
    sous_titre= ctk.CTkLabel(conteneur, text="Pourquoi j'ai créé Sprintia ?", font=(font_secondaire, taille1))
    sous_titre.pack(pady=10)
    pourquoi = ctk.CTkLabel(conteneur, text="J'ai lancé Sprintia parce que pour moi, on n'a pas besoin de dépenser des fortunes pour avoir de la qualité. C'est un peu comme avec" \
                        " les montres connectées : on ne devrait pas être obligé d'acheter la toute dernière et la plus chère pour pouvoir profiter des dernières fonctionnalités." \
                        " De plus, certains constructeurs de montre connectées ce permettre de mettre un abonnement pour pouvoir bénificié de tout les fonctionnalités !" \
                        " Du coup, j'ai décidé de créer Sprintia pour faire les choses à ma manière !",
                        font=(font_principale, taille2), wraplength=950)
    pourquoi.pack(padx=10)
    sous_titre2= ctk.CTkLabel(conteneur, text="Qui suis-je ?", font=(font_secondaire, taille1))
    sous_titre2.pack(pady=10)
    quisuisje = ctk.CTkLabel(conteneur, 
                            text="J'adore le sport, la tech et l'imformatique. Ce que j'adore dans le sport," \
                            " c'est les algorithmes qui vont m'aider à m'entraîner et à progresser dans mon sport, sans avoir de coach." \
                            " Je développe Sprintia pour vous aider à vous entraîner gratuitement sans matériel. Le seul matériel requis" \
                            " pour faire fonctionner les algorithmes c'est une montre avec un chrono ou même un smartphone peut suffire pour utiliser Sprintia." \
                            " Mais pour avoir un suivi plus complet, tu peux utiliser ton téléphone pour le GPS en course, vélo au moins tu pourras intégrer plus de données" \
                            " dans Sprintia !",
                            font=(font_principale, taille2),  wraplength=950)
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

    conteneur_patch_note = ctk.CTkFrame(boite2, fg_color=couleur2, corner_radius=corner1)
    conteneur_patch_note.pack(expand=True, fill="both", pady=(10, 15), padx=25)
    patch_note = ctk.CTkScrollableFrame(conteneur_patch_note, fg_color="transparent", scrollbar_button_color=couleur1,
                                           scrollbar_button_hover_color=couleur1_hover)
    patch_note.pack(expand=True, fill="both", pady=10, padx=10)

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
    • Optimisation du code.
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

    conteneur_patch_note = ctk.CTkFrame(boite2, fg_color=couleur2, corner_radius=corner1)
    conteneur_patch_note.pack(expand=True, fill="both", pady=(10, 15), padx=25)
    patch_note = ctk.CTkScrollableFrame(conteneur_patch_note, fg_color="transparent", scrollbar_button_color=couleur1,
                                           scrollbar_button_hover_color=couleur1_hover)
    patch_note.pack(expand=True, fill="both", pady=10, padx=10)

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
    • La sidebar adopte un nouveau look plus proche l'adn de Sprintia.
    • Simplication et amélioration de l'ergonomie pour la modification de ton compte.
    • Plus besoin d'éditeur de code pour lancer Sprintia, désormais tu n'as qu'à double-cliquer sur le fichier "Sprintia.vbs".
    • Tu peux désormais créer un raccourci sur ton bureau pour lancer Sprintia plus rapidement et avec une icône.
    • 80 caractères maximum pour ta bio.
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

    conteneur_patch_note = ctk.CTkFrame(boite2, fg_color=couleur2, corner_radius=corner1)
    conteneur_patch_note.pack(expand=True, fill="both", pady=(10, 15), padx=25)
    patch_note = ctk.CTkScrollableFrame(conteneur_patch_note, fg_color="transparent", scrollbar_button_color=couleur1,
                                           scrollbar_button_hover_color=couleur1_hover)
    patch_note.pack(expand=True, fill="both", pady=10, padx=10)

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
        6. Texte explicatif sur la VMA et son utilité."""
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

    app.bind('<Return>', lambda event: envoyer())
    avis_entry = ctk.CTkTextbox(app, corner_radius=corner1, fg_color=couleur2, font=(font_principale, taille2),
                                scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover, text_color=couleur1,
                                border_color=couleur1, border_width=border1)
    avis_entry.pack(expand=True, fill="both", padx=80, pady=20)
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
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: envoyer())
    button_check.pack(padx=5, pady=(10, 40))

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

    app.bind('<Return>', lambda event: envoyer())
    avis_entry = ctk.CTkTextbox(app, corner_radius=corner1, fg_color=couleur2, font=(font_principale, taille2),
                                scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover, text_color=couleur1,
                                border_color=couleur1, border_width=border1)
    avis_entry.pack(expand=True, fill="both", padx=80, pady=20)
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
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: envoyer())
    button_check.pack(padx=5, pady=(10, 40))

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

    app.bind('<Return>', lambda event: envoyer())
    avis_entry = ctk.CTkTextbox(app, corner_radius=corner1, fg_color=couleur2, font=(font_principale, taille2),
                                scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover, text_color=couleur1,
                                border_color=couleur1, border_width=border1)
    avis_entry.pack(expand=True, fill="both", padx=80, pady=20)
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
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: envoyer())
    button_check.pack(padx=5, pady=(10, 40))

def modifier_password(account_id, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame_titre = ctk.CTkFrame(app, fg_color="transparent")
    frame_titre.pack(pady=20, padx=10)
    Titre = ctk.CTkLabel(frame_titre ,text="Mot de passe oublié", font=(font_secondaire, taille1))
    Titre.pack(side="left", padx=5)
    button_back = ctk.CTkButton(frame_titre, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), mon_compte(account_id, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(side="left", padx=20)

    frame2 = ctk.CTkFrame(app, fg_color="transparent")        
    frame2.pack(pady=(10, 20))
    carte = ctk.CTkFrame(app, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)        
    carte.pack(pady=(10, 20))

    info = ctk.CTkLabel(frame2 ,text="Mot de passe oublié ? Pas de panique, remplis le formulaire ci-dessus et ton mot de passe sera modifié.",
                         font=(font_secondaire, taille2), wraplength=800)
    info.pack(padx=50)

    app.bind('<Return>', lambda event: new_username(account_id))
    password_entry = ctk.CTkEntry(carte, placeholder_text="Nouveau mot de passe", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=widht_expressive, show="*")
    password_entry.pack(pady=(12, 5), padx=11)
    password_entry2 = ctk.CTkEntry(carte, placeholder_text="Confirme ton nouveau mot de passe", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=widht_expressive, show="*")
    password_entry2.pack(pady=(5, 12), padx=11)
    def new_username(account_id):
        new_password = password_entry.get()
        new_password2 = password_entry2.get()
        password_encode = new_password.encode("UTF-8")
        if new_password == new_password2:
            try:
                if not password_entry or not password_entry2:
                    messagebox.showerror("Erreur", "Le mots de passe ne peut pas être vide. Merci de remplir tous les champs !")
                    return
                else:
                    if (password_valide(new_password)):
                        sha256 = hashlib.sha256()
                        sha256.update(password_encode)
                        hashed_password = sha256.hexdigest()
                        con.execute("UPDATE Account SET password = ? WHERE id = ?", (hashed_password, account_id))
                        con.commit()
                        messagebox.showinfo("Enregistré", "Ton mots de passe à bien été modifié !")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur base de données", "Erreur de base de données lors du changement de ton mot de passe !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
        else:
            messagebox.showerror("Erreur", "Les mots de passe saisis ne correspondent pas !")
    button_check = ctk.CTkButton(carte, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                            corner_radius=corner1, height=button_height, font=(font_principale, taille2), text_color=couleur1,
                            command=lambda: new_username(account_id))
    button_check.pack(fill="x", pady=(2, 12), padx=10)

def supprimer_compte(account_id, inscription, app):
    try:
        curseur.execute("DELETE FROM Pauses_v2 WHERE account_id = ?", (account_id,))

        curseur.execute("DELETE FROM Objectif WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Compétition WHERE account_id = ?", (account_id,))

        curseur.execute("DELETE FROM Activité WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Activité_extérieur WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Activité_running WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Activité_intérieur WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Activité_musculation WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Activité_football WHERE account_id = ?", (account_id,))

        curseur.execute("DELETE FROM Account WHERE id = ?", (account_id,))

        curseur.execute("DELETE FROM Aide_rpe WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Aide_bienvenue WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Aide_objectif WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Aide_compétition WHERE account_id = ?", (account_id,))
        curseur.execute("DELETE FROM Aide_podcast WHERE account_id = ?", (account_id,))
        con.commit()
        messagebox.showinfo("Opération réussi", "Compte supprimé avec succès ! Au revoir !")
        vider_fenetre(app)
        inscription()
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la suppression du compte !")
    except Exception as e:            
        messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye !")

def mon_compte(account_id, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre):
    def suppression_compte():
        reponse = messagebox.askyesno("Suppression de compte", "Es-tu sûr de vouloir supprimer ton compte ?\nToutes tes données seront perdues !")
        if reponse:
            supprimer_compte(account_id, inscription, app)
        else:
            return
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    titre = ctk.CTkLabel(app ,text="Mon compte", font=(font_secondaire, taille1))
    titre.pack(pady=20)

    boite = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner2, border_width=border1, border_color=couleur1)
    boite.pack(expand=True, fill="both", padx=80, pady=(20, 60))

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
                            scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover)
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
    button_mot_de_passe_oublié = ctk.CTkButton(frame_bouton, text="🔑 Mot de passe oublié", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), modifier_password(account_id, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_mot_de_passe_oublié.pack(side="left", padx=2)

def parametres(account_id, connexion, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)
    
    curseur.execute("SELECT username FROM Account WHERE id = ?", (account_id,))
    result = curseur.fetchone()
    username = result[0] if result else "Mon compte"

    def actu():
        reponse = messagebox.askokcancel("Confirmation", "Veux-tu que ton navigateur par défaut s'ouvre pour que tu puisses avoir accès aux actu sur Sprintia ?")
        if reponse:
            webbrowser.open("https://github.com/Gabriel0925/Sprintia/tree/main/Actu")
        else:
            pass
    def beta_testeur():
        messagebox.showinfo("Information", "Tu es déjà bêta testeur ! Merci pour ton aide précieuse au développement de Sprintia.")
        reponse = messagebox.askokcancel("Confirmation", "Veux-tu regarder si une nouvelle bêta est disponible ?")
        if reponse:
            webbrowser.open("https://github.com/Gabriel0925/Sprintia/tree/main/Programme%20B%C3%8ATA")
        else:
            pass
        #messagebox.showwarning("Information", "Ton navigateur va s'ouvrir pour que tu puisses télécharger le programme bêta. Juste un rappel important : une version bêta n’est pas adaptée à tous les utilisateurs. Je t’invite à bien consulter la documentation avant de commencer.")
        #webbrowser.open("https://github.com/Gabriel0925/Sprintia/tree/main/Programme%20B%C3%8ATA")

    Titre = ctk.CTkLabel(app ,text="Paramètres", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=50, pady=20)

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
                                    command=lambda: [vider_fenetre(app), mon_compte(account_id, inscription, app, sidebar_paramètre, exercice, charge_entraînement, predicteur_temps, parametre)])
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
    button_avis = ctk.CTkButton(frame_bouton3, text="📰 Actu Sprintia\n_______________________\n\nInfos récentes", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1, 
                                    command=actu)
    button_avis.pack(side="left", padx=10)   
    button_avis = ctk.CTkButton(frame_bouton3, text="🧪 Rejoindre la bêta\n_______________________\n\nFonctionnalités en avant-première", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1, 
                                    command=beta_testeur)
    button_avis.pack(side="left", padx=(0, 10))      
    button_deco = ctk.CTkButton(frame_bouton4, text="🚪Déconnexion\n_______________________\n\nSe déconnecter, couper le lien", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), connexion()])
    button_deco.pack(side="left", padx=10)
