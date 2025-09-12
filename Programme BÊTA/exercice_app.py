from app_ressource import * 
from update_database import con, curseur
from aide_app import aide_rpe, aide_bienvenue

def supprimer_activité(account_id, période_str, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    vider_fenetre(app)
    sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=(20, 10))
    carte_connexion = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 

    Titre = ctk.CTkLabel(master=frame, text="Supprimer une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    app.bind('<Return>', lambda event: supression(account_id))
    choix_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="ID de l'activité à supprimer", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    choix_entry.pack(pady=10, side="left", padx=10)

    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack()
    boite3 = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=5)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
            curseur.execute("SELECT id_activité, sport, date_activité, durée, rpe FROM Activité WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC", (account_id, période_str))
            activites = curseur.fetchall()

            headers = ["ID", "Sport", "Date", "Durée", "RPE"]

            for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=130)
                label.grid(row=0, column=col_idx, padx=15, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)
            if activites:
                for row_idx, activite in enumerate(activites):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 2:
                            date_activité = datetime.strptime(data, '%Y-%m-%d')
                            data = date_activité.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=15, pady=15, sticky="ew")
            else:
                pas_donnees = ctk.CTkLabel(master=tableau_frame, text="Aucune activité enregistrée pour cette période.", font=(font_principale, taille1))
                pas_donnees.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de l'historique !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, veuillez réessayer !")
    def supression(account_id):
            choix = choix_entry.get().strip()
            try:
                choix_id_saisi = int(choix)
                ids_objectifs_disponibles = [obj[0] for obj in activites]

                if choix_id_saisi in ids_objectifs_disponibles:
                    objectif_id_db = choix_id_saisi
                    curseur.execute("DELETE FROM Activité WHERE id_activité = ? AND account_id = ?", (objectif_id_db, account_id))
                    con.commit()
                    messagebox.showinfo("Suppression réussie", "Activité supprimée avec succès.")
                    vider_fenetre(app)
                    exercice(account_id)
                else:
                    messagebox.showerror("Erreur", "L'ID de l'activité saisie n'existe pas ou n'appartient pas à votre compte.")
                    return
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la suppression de l'activité.")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, veuillez réessayer.")
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: supression(account_id))
    button_check.pack(side="left", padx=2, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: [vider_fenetre(app), exercice(account_id)])
    button_retour.pack(side="left", padx=2, pady=20)

def ajouter_activité_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}
    Options_climat = {"Normal": 0, "Chaud": 1, "Froid": 2, "Difficile": 3}
    Options_type = ["Normal", "Endurance", "Fractionné", "Spécifique", "Trail", "Ultrafond", "Compétition"]

    sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité",
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover,
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Course")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover,
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), exercice(account_id)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=(10, 20))
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=(10, 20))
    frame_champs5 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_champs5.pack(padx=10, pady=(40, 10))

    app.bind('<Return>', lambda event: enregistrer())

    date_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Date (JJ-MM-AAAA)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    date_entry.pack(side="left", padx=10)
    duree_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Durée (min)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    duree_entry.pack(side="left", padx=10)
    type_entry = ctk.CTkComboBox(master=frame_champs1, values=Options_type, font=(font_principale, taille3), height=button_height,
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    type_entry.pack(side="left", padx=10)
    type_entry.set("Type de séance")

    rpe_label = ctk.CTkLabel(master=frame_champs2, text="RPE : 5", font=(font_principale, taille3), text_color=couleur_text)
    rpe_label.pack(side="left", padx=(75, 0))
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs2, width=400, height=20, from_= 1, to= 10, number_of_steps= 9, command=valeur_rpe,
                              progress_color=couleur1, button_color=couleur1, button_hover_color=couleur1_hover,
                              corner_radius=10, button_length=15, fg_color=couleur_text)
    rpe_entry.pack(side="left", padx=(10, 0))
    distance_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Distance (km)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    distance_entry.pack(side="left", padx=(55, 10))

    fatigue_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_fatigue.keys()), font=(font_principale, taille3), height=button_height,
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    fatigue_entry.pack(side="left", padx=10)
    fatigue_entry.set("Fatigue post-entraînement")
    douleur_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_douleur.keys()), font=(font_principale, taille3), height=button_height,
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    douleur_entry.pack(side="left", padx=10)
    douleur_entry.set("Douleur post-entraînement")
    climat_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_climat.keys()), font=(font_principale, taille3), height=button_height,
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    climat_entry.pack(side="left", padx=10)
    climat_entry.set("Climat à l'entraînement")

    allure_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Allure (ex : 6:00 /km)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    allure_entry.pack(side="left", padx=10)
    denivele_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Dénivelé (m)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    denivele_entry.pack(side="left", padx=10)
    vmax_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Vitesse max (ex : 15.8)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    vmax_entry.pack(side="left", padx=10)

    def enregistrer():
        type = type_entry.get().strip()
        if type == "Type de séance":
            messagebox.showerror("Type manquant", "Séléctionne un type d'entraînement")
            return
        try:
            date_str = date_entry.get().strip()
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            if date_obj > datetime.now():
                messagebox.showerror("Erreur", "La date ne peut pas être dans le futur !")
                return
            date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide ! Utilisez JJ-MM-AAAA ! Avec des tirets !")

        sport = "Course"
        try:
            duree = int(duree_entry.get().strip())
            if duree <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Durée invalide (entier positif requis) !")
            return
        try:
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "RPE invalide (1-10 requis) !")
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        climat = Options_climat.get(climat_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        if fatigue is None:
            messagebox.showerror("Fatigue est vide", "La fatigue est obligatoire !")
            return
        if douleur is None:
            messagebox.showerror("Douleur est vide", "La douleur est obligatoire !")
            return
        if climat is None:
            messagebox.showerror("Climat est vide", "Le climat est obligatoire !")
            return
        denivele = None
        allure = allure_entry.get().strip()
        if not allure:
            allure = None
        vmax_str = vmax_entry.get().strip()
        if not vmax_str:
            vmax = None
        else:
            try:
                vmax = float(vmax_str)
                if vmax <= 0:
                    messagebox.showerror("Erreur", "La vitesse max doit être supérieure à 0 !")
                    return
            except ValueError:
                messagebox.showerror("Erreur", "La vitesse max est invalide (nombre positif requis) !")
                return
        try:
            dist_str = distance_entry.get().strip()
            if not dist_str:
                messagebox.showerror("Distance manquante", "La distance est obligatoire !")
                return
            if dist_str:
                distance = float(dist_str)
                if distance <= 0:
                    messagebox.showerror("Erreur", "La distance doit être supérieur à 0 !")
                    return
        except ValueError:
            messagebox.showerror("Erreur", "Distance invalide (nombre positif requis) !")
            return
        try:
            deniv_str = denivele_entry.get().strip()
            if deniv_str:
                denivele = int(deniv_str)
                if denivele <= 0:
                    messagebox.showerror("Erreur", "Le dénivelé doit être supérieur à 0. !")
                    return
        except ValueError:
            messagebox.showerror("Erreur", "Dénivelé invalide (entier positif requis) !")
            return

        charge_de_base = duree * rpe

        modificateurs_douleur = [0.9, 1.05, 1.2, 1.4]
        modificateurs_climat = [0.95, 1.1, 1.05, 1.2]
        if type == "Normal":
            coef = 1.0
        elif type == "Endurance":
            coef = 1.05
        elif type == "Fractionné" or "Spécifique":
            coef = 1.1
        elif type == "Trail" or "Compétition":
            coef = 1.25
        elif type == "Ultrafond":
            coef = 1.30

        charge_d = charge_de_base * modificateurs_douleur[douleur]
        charge_c = charge_d * modificateurs_climat[climat]
        score_fatigue = 1 + (fatigue - 2.5) * 0.05
        charge = (score_fatigue * charge_c)*coef
        try:
            curseur.execute("""INSERT INTO Activité_running (date_activité, sport, durée, distance, rpe, charge, account_id, nom, dénivelé, allure, vitesse_max) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, distance, rpe, charge, account_id, type, denivele, allure, vmax))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, rpe, charge, account_id) VALUES (?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id))
            con.commit()
            messagebox.showinfo("Succès", "Ton activité a bien été enregistrée !")
            vider_fenetre(app)
            exercice(account_id)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton activité.")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye.")
            return
    bouton_valider = ctk.CTkButton(master=frame_champs5, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)

def ajouter_activité_intérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}

    sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")        
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Intérieur")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover, 
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), exercice(account_id)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=(10, 20))
    frame_champs4 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=(40, 10))

    app.bind('<Return>', lambda event: enregistrer())

    date_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Date (JJ-MM-AAAA)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    date_entry.pack(side="left", padx=10)
    sport_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Sport", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    sport_entry.pack(side="left", padx=10)
    duree_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Durée (min)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    duree_entry.pack(side="left", padx=10)

    rpe_label = ctk.CTkLabel(master=frame_champs2, text="RPE : 5", font=(font_principale, taille3), text_color=couleur_text)
    rpe_label.pack(side="left", padx=(75, 0))
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs2, width=400, height=20, from_= 1, to= 10, number_of_steps= 9, command=valeur_rpe,
                              progress_color=couleur1, button_color=couleur1, button_hover_color=couleur1_hover,
                              corner_radius=10, button_length=15, fg_color=couleur_text)
    rpe_entry.pack(side="left", padx=(10, 0))
    nom_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Type", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    nom_entry.pack(side="left", padx=(55, 10))

    fatigue_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_fatigue.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    fatigue_entry.pack(side="left", padx=10)
    fatigue_entry.set("Fatigue post-entraînement")

    douleur_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_douleur.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    douleur_entry.pack(side="left", padx=10)
    douleur_entry.set("Douleur post-entraînement")

    def enregistrer():
        nom = nom_entry.get().strip()
        if len(nom) > 20:
            messagebox.showerror("Type trop long", "Le type de ton entraînement fait plus de 20 caractères")
            return
        if not nom:
            nom = None
        try:
            date_str = date_entry.get().strip()
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            if date_obj > datetime.now():
                messagebox.showerror("Erreur", "La date ne peut pas être dans le futur !")
                return
            date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez JJ-MM-AAAA.")
        
        sport = sport_entry.get().strip()
        if not sport:
            messagebox.showerror("Erreur", "Le sport est obligatoire !")
            return 
        try:
            duree = int(duree_entry.get().strip())
            if duree <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Durée invalide (entier positif requis) !")
            return 
        try:
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "RPE invalide (1-10 requis) !")
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        if fatigue is None:
            messagebox.showerror("Fatigue est vide", "La fatigue est obligatoire !")
            return
        if douleur is None:
            messagebox.showerror("Douleur est vide", "La douleur est obligatoire !")
            return
                                            
        charge_de_base = duree * rpe
        
        modificateurs_douleur = [0.9, 1.05, 1.2, 1.4]
        modificateurs_climat = [0.95, 1.1, 1.05, 1.2]
        
        charge_d = charge_de_base * modificateurs_douleur[douleur]
        score_fatigue = 1 + (fatigue - 2.5) * 0.05
        charge = score_fatigue * charge_d
        try:
            curseur.execute("""INSERT INTO Activité_intérieur (date_activité, sport, durée, rpe, charge, account_id, nom) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id, nom))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, rpe, charge, account_id) VALUES (?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id))
            con.commit()
            messagebox.showinfo("Succès", "Ton activité a bien été enregistrée !")
            vider_fenetre(app)
            exercice(account_id)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton activité.")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye.")
            return
    bouton_valider = ctk.CTkButton(master=frame_champs4, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)

def ajouter_activité_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    Options_matos = ["Poids de corps", "Avec équipement"]
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}
    Options_lieu = {"Salle de sport": "salle de sport", "Domicile": "domicile", "Extérieur": "extérieur"}

    sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")        
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Musculation")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover, 
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), exercice(account_id)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=10)
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=(10, 20))
    frame_champs5 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_champs5.pack(padx=10, pady=(40, 10))

    app.bind('<Return>', lambda event: enregistrer())

    date_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Date (JJ-MM-AAAA)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    date_entry.pack(side="left", padx=10)
    duree_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Durée (min)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    duree_entry.pack(side="left", padx=10)
    matos_entry = ctk.CTkComboBox(master=frame_champs1, values=Options_matos, font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    matos_entry.pack(side="left", padx=10)
    matos_entry.set("Type d'entraînement")

    rpe_label = ctk.CTkLabel(master=frame_champs2, text="RPE : 5", font=(font_principale, taille3), text_color=couleur_text)
    rpe_label.pack(side="left", padx=(75, 0))
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs2, width=400, height=20, from_= 1, to= 10, number_of_steps= 9, command=valeur_rpe,
                              progress_color=couleur1, button_color=couleur1, button_hover_color=couleur1_hover,
                              corner_radius=10, button_length=15, fg_color=couleur_text)
    rpe_entry.pack(side="left", padx=(10, 0))
    muscle_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Muscle travaillé", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    muscle_entry.pack(side="left", padx=(55, 10))

    fatigue_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_fatigue.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    fatigue_entry.pack(side="left", padx=10)
    fatigue_entry.set("Fatigue post-entraînement")

    douleur_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_douleur.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    douleur_entry.pack(side="left", padx=10)
    douleur_entry.set("Douleur post-entraînement")
    lieu_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_lieu.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    lieu_entry.pack(side="left", padx=10)
    lieu_entry.set("Lieu de la séance")

    rep_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Nombre total de répétitions", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    rep_entry.pack(side="left", padx=10)
    serie_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Nombre total de série", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    serie_entry.pack(side="left", padx=10)
    volume_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Volume total (ex : 5.5 kg)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    volume_entry.pack(side="left", padx=10)

    def enregistrer():
        muscle_travaillé = muscle_entry.get().strip()
        répétitions = rep_entry.get().strip()
        série = serie_entry.get().strip()
        volume = volume_entry.get().strip()
        if not série:
            série = None
        if not muscle_travaillé:
            muscle_travaillé = None
        if not répétitions:
            répétitions = None
        if volume:
            try:
                volume_total = float(volume)
                if volume_total < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erreur", "Volume total invalide (entier positif requis) !")
                return
        else:
            volume_total = None
        try:
            date_str = date_entry.get().strip()
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            if date_obj > datetime.now():
                messagebox.showerror("Erreur", "La date ne peut pas être dans le futur !")
                return
            date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez JJ-MM-AAAA.")
        
        try:
            duree = int(duree_entry.get().strip())
            if duree <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Durée invalide (entier positif requis) !")
            return 
        try:
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "RPE invalide (1-10 requis) !")
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        lieu = Options_lieu.get(lieu_entry.get().strip())
        équipement = matos_entry.get().strip()
        if fatigue is None:
            messagebox.showerror("Fatigue est vide", "La fatigue est obligatoire !")
            return
        if douleur is None:
            messagebox.showerror("Douleur est vide", "La douleur est obligatoire !")
            return
        if lieu is None:
            messagebox.showerror("Lieu est vide", "Le lieu est obligatoire !")
            return
        if équipement == "Type d'entraînement":
            messagebox.showerror("Le type est vide", "Le type d'entraînement est obligatoire !")
            return
        sport = "Musculation"
                                            
        charge_de_base = duree * rpe
        
        modificateurs_douleur = [0.9, 1.05, 1.2, 1.4]
        if équipement == "Avec équipement":
            facteur_matos = 1.1
        else:
            facteur_matos = 1.0
        
        charge_d = charge_de_base * modificateurs_douleur[douleur]
        charge_c = charge_d * facteur_matos
        score_fatigue = 1 + (fatigue - 2.5) * 0.05
        charge = score_fatigue * charge_c
        try:
            curseur.execute("""INSERT INTO Activité_musculation (date_activité, sport, durée, rpe, charge, account_id, muscle_travaillé, répétitions, série, volume, équipement, lieu) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id, muscle_travaillé, répétitions, série, volume_total, équipement, lieu))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, rpe, charge, account_id) VALUES (?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id))
            con.commit()
            messagebox.showinfo("Succès", "Ton activité a bien été enregistrée !")
            vider_fenetre(app)
            exercice(account_id)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton activité.")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye.")
            return
    bouton_valider = ctk.CTkButton(master=frame_champs5, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)

def ajouter_activité_fooball(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_climat = {"Normal": 0, "Chaud": 1, "Froid": 2, "Difficile": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}
    Options_type = ["Entraînement", "Match", "Tournoi", "City"]

    sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame1 = ctk.CTkFrame(master=app, corner_radius=20, fg_color="transparent")        
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Football")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover, 
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), exercice(account_id)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=10)
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=(10, 20))
    frame_champs5 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_champs5.pack(padx=10, pady=(40, 10))

    app.bind('<Return>', lambda event: enregistrer())

    date_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Date (JJ-MM-AAAA)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    date_entry.pack(side="left", padx=10)
    duree_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Durée (min)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    duree_entry.pack(side="left", padx=10)
    type_entry = ctk.CTkComboBox(master=frame_champs1, values=Options_type, font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    type_entry.pack(side="left", padx=10)
    type_entry.set("Type de séance de foot")

    rpe_label = ctk.CTkLabel(master=frame_champs2, text="RPE : 5", font=(font_principale, taille3), text_color=couleur_text)
    rpe_label.pack(side="left", padx=(75, 0))
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs2, width=400, height=20, from_= 1, to= 10, number_of_steps= 9, command=valeur_rpe,
                              progress_color=couleur1, button_color=couleur1, button_hover_color=couleur1_hover,
                              corner_radius=10, button_length=15, fg_color=couleur_text)
    rpe_entry.pack(side="left", padx=(10, 0))
    humeur_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Humeur d'après match", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    humeur_entry.pack(side="left", padx=(55, 10))

    fatigue_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_fatigue.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    fatigue_entry.pack(side="left", padx=10)
    fatigue_entry.set("Fatigue post-entraînement")

    douleur_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_douleur.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    douleur_entry.pack(side="left", padx=10)
    douleur_entry.set("Douleur post-entraînement")
    climat_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_climat.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    climat_entry.pack(side="left", padx=10)
    climat_entry.set("Climat à l'entraînement")

    but_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Nombre de but", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    but_entry.pack(side="left", padx=10)
    passe_d_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Nombre de passe décisive", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    passe_d_entry.pack(side="left", padx=10)
    score_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Score (ex : 3-2)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    score_entry.pack(side="left", padx=10)

    def enregistrer():
        humeur = humeur_entry.get().strip()
        passe_décisive1 = passe_d_entry.get().strip()
        type_de_séances = type_entry.get().strip()
        score = score_entry.get().strip()
        if type_de_séances == "Type de séance de foot":
            messagebox.showerror("Type de séances de foot est vide", "Le type de séance de foot est obligatoire !")
            return
        if humeur:
            pass
        else:
            humeur = None
        if score:
            pass
        else:
            score = None
        if passe_décisive1:
            try:
                passe_décisive = int(passe_décisive1)
                if passe_décisive < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erreur", "Nombre de passe décisive invalide (entier positif requis) !")
                return
        else:
            passe_décisive = None
        but1 = but_entry.get().strip()
        if but1:
            try:
                but = int(but1)
                if but < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erreur", "Nombre de but invalide (entier positif requis) !")
                return
        else:
            but = None
        try:
            date_str = date_entry.get().strip()
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            if date_obj > datetime.now():
                messagebox.showerror("Erreur", "La date ne peut pas être dans le futur !")
                return
            date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez JJ-MM-AAAA.")
        
        sport = "Football"
        try:
            duree = int(duree_entry.get().strip())
            if duree <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Durée invalide (entier positif requis) !")
            return 
        try:
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "RPE invalide (1-10 requis) !")
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        climat = Options_climat.get(climat_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        if fatigue is None:
            messagebox.showerror("Fatigue est vide", "La fatigue est obligatoire !")
            return
        if douleur is None:
            messagebox.showerror("Douleur est vide", "La douleur est obligatoire !")
            return
        if climat is None:
            messagebox.showerror("Climat est vide", "Le climat est obligatoire !")
            return
        if type_de_séances is None:
            messagebox.showerror("Type de séances de foot est vide", "Le type de séance de foot est obligatoire !")
            return

        if type_de_séances == "Entraînement":  
            coef_foot = 1        
        elif type_de_séances == "Match":
            coef_foot = 1.2
        elif type_de_séances == "City":
            coef_foot = 0.9
        else:  
            coef_foot = 1.4
        charge_de_base = duree * rpe
        
        modificateurs_douleur = [0.9, 1.05, 1.2, 1.4]
        modificateurs_climat = [0.95, 1.1, 1.05, 1.2]
        
        charge_d = charge_de_base * modificateurs_douleur[douleur]
        charge_c = charge_d * modificateurs_climat[climat]
        score_fatigue = 1 + (fatigue - 2.5) * 0.05
        charge_av = score_fatigue * charge_c
        charge =  charge_av*coef_foot
        try:
            curseur.execute("""INSERT INTO Activité_football (date_activité, sport, durée, rpe, charge, account_id, humeur, but, passe_décisive, type_de_séances, score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id, humeur, but, passe_décisive, type_de_séances, score))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, rpe, charge, account_id) VALUES (?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id))
            con.commit()
            messagebox.showinfo("Succès", "Ton activité a bien été enregistrée !")
            vider_fenetre(app)
            exercice(account_id)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton activité.")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye.")
            return
    bouton_valider = ctk.CTkButton(master=frame_champs5, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)

def ajouter_activité_extérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_climat = {"Normal": 0, "Chaud": 1, "Froid": 2, "Difficile": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}

    sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame1 = ctk.CTkFrame(master=app, corner_radius=20, fg_color="transparent")        
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Extérieur")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover, 
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), exercice(account_id)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=10)
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=(10, 20))
    frame_champs5 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_champs5.pack(padx=10, pady=(40, 10))

    app.bind('<Return>', lambda event: enregistrer())

    date_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Date (JJ-MM-AAAA)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    date_entry.pack(side="left", padx=10)
    sport_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Sport", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    sport_entry.pack(side="left", padx=10)
    duree_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Durée (min)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    duree_entry.pack(side="left", padx=10)

    rpe_label = ctk.CTkLabel(master=frame_champs2, text="RPE : 5", font=(font_principale, taille3), text_color=couleur_text)
    rpe_label.pack(side="left", padx=(75, 0))
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs2, width=400, height=20, from_= 1, to= 10, number_of_steps= 9, command=valeur_rpe,
                              progress_color=couleur1, button_color=couleur1, button_hover_color=couleur1_hover,
                              corner_radius=10, button_length=15, fg_color=couleur_text)
    rpe_entry.pack(side="left", padx=(10, 0))
    nom_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Type", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    nom_entry.pack(side="left", padx=(55, 10))

    fatigue_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_fatigue.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    fatigue_entry.pack(side="left", padx=10)
    fatigue_entry.set("Fatigue post-entraînement")

    douleur_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_douleur.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    douleur_entry.pack(side="left", padx=10)
    douleur_entry.set("Douleur post-entraînement")
    climat_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_climat.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    climat_entry.pack(side="left", padx=10)
    climat_entry.set("Climat à l'entraînement")

    distance_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Distance (km)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    distance_entry.pack(side="left", padx=10)
    denivele_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Dénivelé (m)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    denivele_entry.pack(side="left", padx=10)

    def enregistrer():
        nom = nom_entry.get().strip()
        if len(nom) > 20:
            messagebox.showerror("Type trop long", "Le type de votre entraînement fait plus de 20 caractères")
            return
        if not nom:
            nom = None
        try:
            date_str = date_entry.get().strip()
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            if date_obj > datetime.now():
                messagebox.showerror("Erreur", "La date ne peut pas être dans le futur !")
                return
            date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez JJ-MM-AAAA.")
            return
        
        sport = sport_entry.get().strip()
        if not sport:
            messagebox.showerror("Erreur", "Le sport est obligatoire !")
            return 
        try:
            duree = int(duree_entry.get().strip())
            if duree <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Durée invalide (entier positif requis) !")
            return 
        try:
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "RPE invalide (1-10 requis) !")
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        climat = Options_climat.get(climat_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        if fatigue is None:
            messagebox.showerror("Fatigue est vide", "La fatigue est obligatoire !")
            return
        if douleur is None:
            messagebox.showerror("Douleur est vide", "La douleur est obligatoire !")
            return
        if climat is None:
            messagebox.showerror("Climat est vide", "Le climat est obligatoire !")
            return
        distance = None
        denivele = None
        try:
            dist_str = distance_entry.get().strip()
            if dist_str:
                distance = float(dist_str)
                if distance <= 0:
                    messagebox.showerror("Erreur", "La distance doit être supérieur à 0 !")
                    return
        except ValueError:
            messagebox.showerror("Erreur", "Distance invalide (nombre positif requis) !")
            return
        try:
            deniv_str = denivele_entry.get().strip()
            if deniv_str:
                denivele = int(deniv_str)
                if denivele <= 0:
                    messagebox.showerror("Erreur", "Le dénivelé doit être supérieur à 0. !")
                    return       
        except ValueError:
            messagebox.showerror("Erreur", "Dénivelé invalide (entier positif requis) !")
            return
                                            
        charge_de_base = duree * rpe
        
        modificateurs_douleur = [0.9, 1.05, 1.2, 1.4]
        modificateurs_climat = [0.95, 1.1, 1.05, 1.2]
        
        charge_d = charge_de_base * modificateurs_douleur[douleur]
        charge_c = charge_d * modificateurs_climat[climat]
        score_fatigue = 1 + (fatigue - 2.5) * 0.05
        charge = score_fatigue * charge_c
        try:
            curseur.execute("""INSERT INTO Activité_extérieur (date_activité, sport, durée, distance, rpe, charge, account_id, nom, dénivelé) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, distance, rpe, charge, account_id, nom, denivele))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, rpe, charge, account_id) VALUES (?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id))
            con.commit()
            messagebox.showinfo("Succès", "Ton activité a bien été enregistrée !")
            vider_fenetre(app)
            exercice(account_id)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton activité.")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye.")
            return
    bouton_valider = ctk.CTkButton(master=frame_champs5, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)
    aide_rpe(account_id)

def interface_exercice(account_id, type_de_catégorie, headers, requête_sql, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    global periode_séléctionner #global = pour dire que la variable existe en dehors de la fonction et que je vais la modifier
    sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)
    boite2 = ctk.CTkFrame(master=app, fg_color="transparent", corner_radius=corner3)
    boite2.pack(side="top", fill="x", pady=20)
    topbar = ctk.CTkFrame(master=boite2, fg_color="transparent", corner_radius=corner3)
    topbar.pack(anchor="center")
    element_topbar = ctk.CTkFrame(master=topbar, fg_color="transparent")
    element_topbar.pack()

    boite_semi_header = ctk.CTkFrame(master=app, fg_color="transparent")
    boite_semi_header.pack(side="top", pady=10)

    boite3 = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)

    button_supprimer = ctk.CTkButton(master=element_topbar, text="🗑️ Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: supprimer_activité(account_id, avoir_periode(combo_periode.get(), options_periode), app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre))
    button_supprimer.pack(side="right", padx=2, pady=5)
    button_creer_activite = ctk.CTkButton(master=element_topbar, text="➕ Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_creer_activite.pack(side="right", padx=(20, 2), pady=5)
    info = ctk.CTkLabel(master=element_topbar, text="Historique d'entraînement", font=(font_secondaire, taille1), text_color=couleur_text)
    info.pack(side="right", padx=20)
    options_periode = {"1 semaine": 7, "1 mois": 30, "3 mois": 90, "6 mois": 180, "1 an": 365, "Tout voir (non recommandé)": 9999}
    combo_periode = ctk.CTkComboBox(master=element_topbar, values=list(options_periode.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur2, button_color=couleur2, fg_color=couleur2,
                                    corner_radius=corner2, width=220, dropdown_fg_color=couleur2, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    combo_periode.pack(side="right", padx=(10, 20), pady=5)
    def avoir_periode(selection_text, options_dict):
        jours_a_soustraire = options_dict[selection_text]
        date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
        return date_debut.strftime('%Y-%m-%d')
    
    def mise_mode(choix):
        choix = mode_activité.get()
        navigation = {
            "Extérieur": lambda: [vider_fenetre(app), exercice_extérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)],
            "Intérieur": lambda: [vider_fenetre(app), exercice_intérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)],
            "Musculation": lambda: [vider_fenetre(app), exercice_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)],
            "Football": lambda: [vider_fenetre(app), exercice_football(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)],
            "Tous": lambda: [vider_fenetre(app), exercice_accueil(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)],
            "Course": lambda: [vider_fenetre(app), exercice_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)]
        }
        app.after(0, navigation[choix])

    mode_activité = ctk.CTkSegmentedButton(master=boite_semi_header, values=["Tous", "Extérieur", "Intérieur", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set(type_de_catégorie)
    if type_de_catégorie == "Musculation":
        wraplength_tableau = 100
    elif type_de_catégorie == "Tous":
        wraplength_tableau = 180
    elif type_de_catégorie == "Course":
        wraplength_tableau = 100
    else:
        wraplength_tableau = 130

    if type_de_catégorie == "Musculation":
        padx_tableau = 2
        conversion_format_date = 0
    elif type_de_catégorie == "Tous":
        padx_tableau = 15
        conversion_format_date = 1
    elif type_de_catégorie == "Course":
        padx_tableau = 2
        conversion_format_date = 0
    elif type_de_catégorie == "Intérieur":
        padx_tableau = 15
        conversion_format_date = 1
    elif type_de_catégorie == "Football":
        padx_tableau = 8
        conversion_format_date = 0
    elif type_de_catégorie == "Extérieur":
        padx_tableau = 10
        conversion_format_date = 1

    def mettre_a_jour_historique(selection):
        global periode_séléctionner
        periode_séléctionner = selection
        for widget in tableau_frame.winfo_children():
            widget.grid_remove()
        try:
            jours_a_soustraire = options_periode[selection]
            date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
            période_str_pour_requete = date_debut.strftime('%Y-%m-%d')
            curseur.execute(f"{requête_sql}", (account_id, période_str_pour_requete))
            activites = curseur.fetchall()
            for colonne, header_text in enumerate(headers):
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=wraplength_tableau)
                label.grid(row=0, column=colonne, padx=padx_tableau, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(colonne, weight=1)
            if activites:
                for ligne, activite in enumerate(activites):
                    for colonne, data in enumerate(activite):
                        if colonne == conversion_format_date:
                            data = datetime.strptime(str(data), '%Y-%m-%d').strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=ligne + 1, column=colonne, padx=10, pady=15, sticky="ew")
            else:
                pas_donnees = ctk.CTkLabel(master=tableau_frame, text="Aucune activité enregistrée pour cette période.", font=(font_principale, taille1))
                pas_donnees.grid(row=1, column=0, columnspan=len(headers), pady=20)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de ton historique !")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    combo_periode.configure(command=mettre_a_jour_historique)
    combo_periode.set(periode_séléctionner)
    mettre_a_jour_historique(periode_séléctionner)
    aide_bienvenue(account_id)

def exercice_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    requête_sql = "SELECT date_activité, durée, rpe, nom, distance, allure, dénivelé, vitesse_max FROM Activité_running WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Date", "Durée", "RPE", "Type", "Distance", "Allure", "Dénivelé", "Vitesse max"]
    interface_exercice(account_id, "Course", headers, requête_sql, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)

def exercice_intérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    requête_sql = "SELECT sport, date_activité, durée, rpe, nom FROM Activité_intérieur WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Sport", "Date", "Durée", "RPE", "Type"]
    interface_exercice(account_id, "Intérieur", headers, requête_sql, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)

def exercice_football(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    requête_sql = "SELECT date_activité, durée, rpe, type_de_séances, humeur, but, passe_décisive, score FROM Activité_football WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Date", "Durée", "RPE", "Type", "Humeur", "But", "Passe D", "Score"]
    interface_exercice(account_id, "Football", headers, requête_sql, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)

def exercice_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    requête_sql = "SELECT date_activité, lieu, durée, rpe, équipement, muscle_travaillé, répétitions, série, volume FROM Activité_musculation WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Date", "Lieu", "Durée", "RPE", "Type", "Muscle", "Rép", "Série", "Volume"]
    interface_exercice(account_id, "Musculation", headers, requête_sql, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)

def exercice_extérieur(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    requête_sql = "SELECT sport, date_activité, durée, rpe, nom, distance, dénivelé FROM Activité_extérieur WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Sport", "Date", "Durée", "RPE", "Type", "Distance", "Dénivelé"]
    interface_exercice(account_id, "Extérieur", headers, requête_sql, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)

def exercice_accueil(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    requête_sql = "SELECT sport, date_activité, durée, rpe, ROUND(charge, 1) FROM Activité WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Sport", "Date", "Durée", "RPE", "Charge d'entraînement"]
    interface_exercice(account_id, "Tous", headers, requête_sql, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)
