from app_ressource import * 
from update_database import con, curseur
from aide_app import aide_objectif, aide_compétition

def verifier_pause(account_id):
    #AND date_fin IS NULL = Cible uniquement les pause non terminés.
    try:
        curseur.execute("SELECT type FROM Pauses WHERE account_id = ?", (account_id,))
        result = curseur.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la vérification du mode d'analyse !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    
    return result[0] if result else None

def activer_pause(account_id, type_pause):
    try:
        curseur.execute("SELECT type FROM Pauses WHERE account_id = ?", (account_id,))
        result = curseur.fetchone()
        if result is not None:
            curseur.execute("UPDATE Pauses SET type = ? WHERE account_id = ?", (type_pause, account_id))
            con.commit()
            messagebox.showinfo("Enregistré", f"Pause {type_pause} activée !")
        else:
            curseur.execute("INSERT INTO Pauses (account_id, type) VALUES (?, ?)", (account_id, type_pause))
            con.commit()
            messagebox.showinfo("Enregistré", f"Pause {type_pause} activée !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", f"Erreur de base de données lors de l'activation de la pause {type_pause}.")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def arreter_pause(account_id):
    try:
        curseur.execute("UPDATE Pauses SET type = NULL WHERE account_id = ?", (account_id,))
        con.commit()
        messagebox.showinfo("Enregistré", "Reprise d'activité enregistrée ! Les analyses sont désormais activées !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de l'activation de la reprise d'activité.")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def pop_up_calendrier(app, date_entry):
    pop_up_calendrier = ctk.CTkToplevel(app, fg_color=couleur2)
    pop_up_calendrier.grab_set()
    pop_up_calendrier.title("Calendrier")
    pop_up_calendrier.geometry("400x400")
    pop_up_calendrier.resizable(False, False)
    pop_up_calendrier.bind("<Control-w>", lambda event: pop_up_calendrier.destroy())

    affichage_calendrier = tkcalendar.Calendar(pop_up_calendrier, selectmode="day", date_pattern="dd/MM/yyyy", 
                                               background=couleur_fond, foreground="white", headersbackground=couleur_fond, 
                                               normalbackground=couleur2, weekendbackground=couleur2,
                                               othermonthbackground=couleur_fond, othermonthwebackground=couleur_fond,
                                               bordercolor=couleur1, headersforeground=couleur1, selectbackground=couleur1,
                                               selectforeground="white", font=(font_principale, taille3))
    affichage_calendrier.pack(expand=True, fill="both", padx=5, pady=5)

    pop_up_calendrier.bind('<Return>', lambda event: valider_date(date_entry))

    def valider_date(date_entry):
        date_selectionnee = affichage_calendrier.get_date()
        pop_up_calendrier.destroy()
        date_entry.delete(0, 'end')
        date_entry.insert(0, f"{date_selectionnee}")
        return
    bouton_valider = ctk.CTkButton(pop_up_calendrier, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_secondaire, taille2), command=lambda: valider_date(date_entry))
    bouton_valider.pack(expand=True, fill="both", padx=5, pady=5)

def ajouter_compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=10)
    Titre = ctk.CTkLabel(master=frame ,text="Ajouter une compétition", font=(font_secondaire, taille1))
    Titre.pack(padx=10, pady=0)

    frame_tout = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(expand=True, fill="both", padx=12, pady=(12, 2))
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(expand=True, fill="both", padx=12, pady=2)
    frame3 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(expand=True, fill="both", padx=12, pady=2)
    frame4 = ctk.CTkFrame(master=frame_tout, fg_color="transparent")
    frame4.pack(expand=True, fill="both", padx=12, pady=(2, 12))

    option = ["Événement Principal", "Événement Secondaire", "Événement tertiaire"]
    app.bind('<Return>', lambda event: sql_ajouté(account_id))

    sport_entry = ctk.CTkEntry(master=frame1, placeholder_text="Sport", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=320)
    sport_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    frame_pour_date = ctk.CTkFrame(master=frame1, fg_color=couleur_fond, corner_radius=corner1)
    frame_pour_date.pack(expand=True, fill="both", side="left", padx=(0, 2))
    date_entry = ctk.CTkEntry(master=frame_pour_date, placeholder_text="Date", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=36, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=160)
    date_entry.pack(expand=True, fill="both", side="left", padx=(12,0), pady=12)
    button_pop_up_calendrier = ctk.CTkButton(frame_pour_date, text="📅 Calendrier", width=75, height=36, corner_radius=corner1, fg_color=couleur2,
                                            hover_color=couleur2_hover, font=(font_principale, taille3), text_color=couleur1,
                                            border_color=couleur2, border_width=border1,
                                            command=lambda: pop_up_calendrier(app, date_entry))
    button_pop_up_calendrier.pack(expand=True, fill="both", side="left", padx=(0, 12), pady=12)

    nom_entry = ctk.CTkEntry(master=frame2, placeholder_text="Nom de la compétition", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    nom_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    objectif_entry = ctk.CTkEntry(master=frame2, placeholder_text="Objectif", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    objectif_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    lieu_entry = ctk.CTkEntry(master=frame3, placeholder_text="Lieu (optionnel)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    lieu_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    priorite_entry = ctk.CTkComboBox(master=frame3, values=option, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=320, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    priorite_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    priorite_entry.set("Priorité")

    def sql_ajouté(account_id):
        nom = nom_entry.get().strip()
        date_str = date_entry.get().strip()
        sport = sport_entry.get().strip()
        objectif = objectif_entry.get().strip()
        lieu_avant = lieu_entry.get().strip()
        priorité = priorite_entry.get().strip()
        if priorité == "Priorité":
            messagebox.showerror("Champs vide", "Le champs 'Priorité' est obligatoire !")
            return
        if not lieu_avant :
            lieu = None
        else:
            lieu = lieu_avant

        if not nom:
            messagebox.showerror("Erreur", "Le nom de la compétition ne peut pas être vide !")
            return
        if not date_str:
            messagebox.showerror("Erreur", "La date de la compétition ne peut pas être vide !")
            return
        if not sport:
            messagebox.showerror("Erreur", "Le sport de la compétition ne peut pas être vide !")
            return
        if not objectif:
            messagebox.showerror("Erreur", "L'objectif de la compétition ne peut pas être vide !")
            return
        try:
            date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
            date = date_conversion.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur de format de date", "La date doit être au format JJ-MM-AAAA !")
            return
        else:
            try:
                curseur.execute("INSERT INTO Compétition (account_id, nom, date, sport, objectif, lieu, priorité) VALUES (?, ?, ?, ?, ?, ?, ?)", (account_id, nom, date, sport, objectif, lieu, priorité))
                con.commit()
                messagebox.showinfo("Enregistré", "Ta compétition a été enregistré, bonne chance !")
                vider_fenetre(app)
                compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de la compétition !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_enregistrer = ctk.CTkButton(master=frame4, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                                    command=lambda: sql_ajouté(account_id))
    button_enregistrer.pack(expand=True, fill="both", side="left", padx=2)
    button_back = ctk.CTkButton(master=frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                           command=lambda: [vider_fenetre(app), compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left", padx=2)

def supprimer_compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(master=app ,text="Supprimer une compétition", font=(font_secondaire, taille1))
    Titre.pack(padx=10, pady=10)

    frame_tout = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color="transparent")
    frame1.pack(pady=(12, 2), padx=12)
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color="transparent")
    frame2.pack(pady=(2, 12), padx=12)

    app.bind('<Return>', lambda event: supression(account_id))
    choix_entry = ctk.CTkEntry(master=frame1, placeholder_text="ID de la compétition", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    choix_entry.pack(expand=True, fill="both")
    
    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
    try:
        curseur.execute("SELECT id, sport, nom, date, lieu FROM Compétition WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        headers = ["ID", "Sport", "Nom", "Date", "Lieu"]
        for col_idx, header_text in enumerate(headers):
            label = ctk.CTkButton(tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                    fg_color=couleur_fond, corner_radius=corner2, text_color=couleur1,
                                    height=40, border_width=border2, border_color=couleur2, hover_color=couleur_fond)
            label.grid(row=0, column=col_idx, padx=5, pady=15, sticky="ew")
            tableau_frame.grid_columnconfigure(col_idx, weight=1)
        if result:
            for row_idx, activite in enumerate(result):
                for col_idx, data in enumerate(activite):
                    if col_idx == 3:
                        date = datetime.strptime(str(data), '%Y-%m-%d')
                        data = date.strftime('%d-%m-%Y')
                    label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=140)
                    label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=15, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=(font_principale, taille2))
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def supression(account_id):
            choix = choix_entry.get().strip()
            try:
                choix_id_saisi = int(choix)
                ids_competitions_disponibles = [comp[0] for comp in result]

                if choix_id_saisi in ids_competitions_disponibles:
                    competition_id_db = choix_id_saisi
                    curseur.execute("DELETE FROM Compétition WHERE id = ? AND account_id = ?", (competition_id_db, account_id))
                    con.commit()
                    messagebox.showinfo("Suppression réussie", "Compétition supprimée avec succès.")
                    vider_fenetre(app)
                    compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
                else:
                    messagebox.showerror("Erreur", "L'ID de la compétition saisie n'existe pas ou n'appartient pas à ton compte !")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la suppression de la compétition !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes compétitions !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_check = ctk.CTkButton(master=frame2, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: supression(account_id))
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_retour = ctk.CTkButton(master=frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: [vider_fenetre(app), compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_retour.pack(expand=True, fill="both", side="left")

def modifier_compétition_étape2(account_id, result_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):    
    id_modifier = result_id[0][0]
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)
    try:
        curseur.execute("SELECT date, sport, nom, objectif, lieu, priorité FROM Compétition WHERE id = ? AND account_id = ?",(id_modifier, account_id))
        data_compétition = curseur.fetchall()
        premiere_ligne = data_compétition[0]
        date1 = premiere_ligne[0]
        date_conversion = datetime.strptime(date1, "%Y-%m-%d")
        date_value = date_conversion.strftime("%d-%m-%Y")
        sport_value = premiere_ligne[1]
        nom_value = premiere_ligne[2]
        objectif_value = premiere_ligne[3]
        lieu_value = premiere_ligne[4]
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de ta compétition !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=10)
    Titre = ctk.CTkLabel(master=frame ,text="Modifier une compétition", font=(font_secondaire, taille1))
    Titre.pack(padx=10, pady=0)

    frame_tout = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(expand=True, fill="both", padx=12, pady=(12, 2))
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(expand=True, fill="both", padx=12, pady=2)
    frame3 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(expand=True, fill="both", padx=12, pady=2)
    frame4 = ctk.CTkFrame(master=frame_tout, fg_color="transparent")
    frame4.pack(expand=True, fill="both", padx=12, pady=(2, 12))

    option = ["Événement Principal", "Événement Secondaire", "Événement tertiaire"]
    app.bind('<Return>', lambda event: sql_ajouté(account_id))

    sport_entry = ctk.CTkEntry(master=frame1, placeholder_text=f"{sport_value}", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=320)
    sport_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    frame_pour_date = ctk.CTkFrame(master=frame1, fg_color=couleur_fond, corner_radius=corner1)
    frame_pour_date.pack(expand=True, fill="both", side="left", padx=(0, 2))
    date_entry = ctk.CTkEntry(master=frame_pour_date, placeholder_text=f"{date_value}", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=36, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=160)
    date_entry.pack(expand=True, fill="both", side="left", padx=(12,0), pady=12)
    button_pop_up_calendrier = ctk.CTkButton(frame_pour_date, text="📅 Calendrier", width=75, height=36, corner_radius=corner1, fg_color=couleur2,
                                            hover_color=couleur2_hover, font=(font_principale, taille3), text_color=couleur1,
                                            border_color=couleur2, border_width=border1,
                                            command=lambda: pop_up_calendrier(app, date_entry))
    button_pop_up_calendrier.pack(expand=True, fill="both", side="left", padx=(0, 12), pady=12)

    nom_entry = ctk.CTkEntry(master=frame2, placeholder_text=f"{nom_value}", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    nom_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    objectif_entry = ctk.CTkEntry(master=frame2, placeholder_text=f"{objectif_value}", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    objectif_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    lieu_entry = ctk.CTkEntry(master=frame3, placeholder_text=f"{lieu_value}", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    lieu_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    priorite_entry = ctk.CTkComboBox(master=frame3, values=option, height=height_expressive, font=(font_principale, taille2),
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=320, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    priorite_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    priorite_entry.set("Priorité")

    def sql_ajouté(account_id):
        nom = nom_entry.get().strip()
        date_str = date_entry.get().strip()
        sport = sport_entry.get().strip()
        objectif = objectif_entry.get().strip()
        lieu = lieu_entry.get().strip()
        priorité = priorite_entry.get().strip()

        if not sport:
            sport = sport_value
        if not date_str:
            date_str = date_value
        if not objectif:
            objectif = objectif_value
        if not nom:
            nom = nom_value
        if not lieu:
            lieu = lieu_value

        if priorité == "Priorité":
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Priorité' !")
            return
        try:
            date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
            date = date_conversion.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur de format de date", "La date doit être au format JJ-MM-AAAA !")
            return
        else:
            try:
                curseur.execute("UPDATE Compétition SET nom = ?, date = ?, sport = ?, objectif = ?, lieu = ?, priorité = ? WHERE id = ? AND account_id = ?", 
                                (nom, date, sport, objectif, lieu, priorité, id_modifier, account_id))
                con.commit()
                messagebox.showinfo("Enregistré", "Ta compétition a été modifiée avec succès !")
                vider_fenetre(app)
                compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de la compétition !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_enregistrer = ctk.CTkButton(master=frame4, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                                    command=lambda: sql_ajouté(account_id))
    button_enregistrer.pack(expand=True, fill="both", side="left", padx=2)
    button_back = ctk.CTkButton(master=frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                           command=lambda: [vider_fenetre(app), modifier_compétition_étape1(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left", padx=2)
    aide_compétition(account_id)

def modifier_compétition_étape1(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(master=app ,text="Modifier une compétition", font=(font_secondaire, taille1))
    Titre.pack(padx=10, pady=10)

    frame_tout = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color="transparent")
    frame1.pack(pady=(12, 2), padx=12)
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color="transparent")
    frame2.pack(pady=(2, 12), padx=12)

    app.bind('<Return>', lambda event: valider(account_id))
    choix_entry = ctk.CTkEntry(frame1, placeholder_text="ID de la compétition", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    choix_entry.pack(expand=True, fill="both")

    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
    try:
        curseur.execute("SELECT id, nom, date, sport, lieu, priorité FROM Compétition WHERE account_id = ?AND date >= ? ORDER BY date ASC", (account_id, date_actuelle))
        result = curseur.fetchall()
        headers = ["ID", "Nom", "Date", "Sport", "Lieu", "Priorité"]

        for col_idx, header_text in enumerate(headers): #_idx= index de colonne
            label = ctk.CTkButton(tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                    fg_color=couleur_fond, corner_radius=corner2, text_color=couleur1,
                                    height=40, border_width=border2, border_color=couleur2, hover_color=couleur_fond)
            label.grid(row=0, column=col_idx, padx=5, pady=15, sticky="ew")
            tableau_frame.grid_columnconfigure(col_idx, weight=1)
        if result:
            for row_idx, activite in enumerate(result):
                for col_idx, data in enumerate(activite):
                    if col_idx == 2:
                        date = datetime.strptime(data, '%Y-%m-%d')
                        data = date.strftime('%d-%m-%Y')
                    label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                         text_color=couleur_text, wraplength=140)
                    label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=15, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucune compétition futur n'a été enregistré", font=(font_principale, taille1))
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def valider(account_id):
            choix = choix_entry.get().strip()
            try:
                if not choix:
                    messagebox.showerror("Erreur", "ID ne peut pas être vide ! Merci de saisir un identifiant !")
                try:
                    id = int(choix)
                    if id < 0:
                        messagebox.showerror("Erreur", "ID doit être un nombre entier positif !")
                        return
                except:
                    messagebox.showerror("Erreur", "ID doit être un nombre entier positif !")
                    return

                curseur.execute("SELECT id FROM Compétition WHERE id = ? AND account_id = ?", (id, account_id))
                result_id = curseur.fetchall()
                if result_id:
                    vider_fenetre(app)
                    modifier_compétition_étape2(account_id, result_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
                else:
                    messagebox.showerror("Erreur", "ID de l'objectif saisi n'existe pas ou n'appartient pas à ton compte !")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de la compétition !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes compétitions !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, veuillez réessayer !")
    button_check = ctk.CTkButton(master=frame2, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: valider(account_id))
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_retour = ctk.CTkButton(master=frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_retour.pack(expand=True, fill="both", side="left")

def toute_compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    petite_boite = ctk.CTkFrame(master=app, fg_color="transparent")
    petite_boite.pack(padx=10, pady=10)
    Titre = ctk.CTkLabel(petite_boite, text="Toutes les compétitions", font=(font_secondaire, taille1))
    Titre.pack(side="left")
    button_retour = ctk.CTkButton(petite_boite, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), border_width=border2, border_color=couleur2,
                                    command=lambda: [vider_fenetre(app), compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_retour.pack(side="left", padx=(10, 0))


    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
    try:
            curseur.execute("SELECT nom, date, sport, objectif, lieu, priorité FROM Compétition WHERE account_id = ? ORDER BY date ASC", (account_id,))
            compétition_result = curseur.fetchall()

            headers = ["Nom", "Date", "Sport", "Objectif", "Lieu", "Priorité"]

            for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkButton(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                    fg_color=couleur_fond, corner_radius=corner2, text_color=couleur1,
                                    height=40, border_width=border2, border_color=couleur2, hover_color=couleur_fond)
                label.grid(row=0, column=col_idx, padx=5, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)

            if compétition_result:
                for row_idx, activite in enumerate(compétition_result):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 1:
                            date = datetime.strptime(data, '%Y-%m-%d')
                            data = date.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=140)
                        label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=15, sticky="ew")
            else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucune compétition n'a été enregistrée.", font=(font_principale, taille1))
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes compétitions !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    boite = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner2)
    boite.pack(side="top", fill="x", padx=10, pady=(10, 5))
    boite_semi_header = ctk.CTkFrame(master=boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header.pack(expand=True, fill="x", side="left", padx=(2, 10), pady=2)
    boite_semi_header2 = ctk.CTkFrame(master=boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header2.pack(expand=True, fill="x", side="right", padx=(0, 2), pady=2)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Charge d'entraînement":
            app.after(0, lambda: [vider_fenetre(app), charge_entraînement(account_id)])
        elif choix == "Objectif":
            app.after(0, lambda: [vider_fenetre(app), objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Compétition":
            app.after(0, lambda: [vider_fenetre(app), compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
        else:
            app.after(0, lambda: [vider_fenetre(app), indulgence_de_course(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    mode_activité = ctk.CTkSegmentedButton(master=boite_semi_header, values=["Charge d'entraînement", "Indulgence de course", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner2, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(expand=True, fill="x", side="right", padx=(2, 0), pady=5)
    mode_activité.set("Compétition")    
    button_autre = ctk.CTkButton(master=boite_semi_header2, text="🔚 Toutes les compétitions", fg_color=couleur2, hover_color=couleur2_hover,
                                    font=(font_principale, taille3), text_color=couleur1, height=button_height, corner_radius=corner1,
                                    width=260,
                                    command=lambda: [vider_fenetre(app), toute_compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_autre.pack(expand=True, fill="x", side="right", padx=(2, 5), pady=5)

    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack(pady=(20, 5))
    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))

    button_ajouter = ctk.CTkButton(master=frame_boutons, text="➕  Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, border_width=border2,
                           border_color=couleur2,
                           command=lambda: [vider_fenetre(app), ajouter_compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_ajouter.pack(side="left", padx=2)
    button_modifier = ctk.CTkButton(master=frame_boutons, text="✏️  Modifier", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, border_width=border2,
                           border_color=couleur2,
                           command=lambda: [vider_fenetre(app), modifier_compétition_étape1(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_modifier.pack_forget()
    button_delete = ctk.CTkButton(master=frame_boutons, text="🗑️  Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1, border_width=border2,
                           border_color=couleur2,
                           command=lambda: [vider_fenetre(app), supprimer_compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_delete.pack_forget()
    try:
            curseur.execute("SELECT nom, date, sport, objectif, lieu, priorité FROM Compétition WHERE account_id = ? AND date >= ? ORDER BY date ASC", (account_id, date_actuelle))
            compétition_result = curseur.fetchall()

            headers = ["Nom", "Date", "Sport", "Objectif", "Lieu", "Priorité"]

            for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkButton(tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                    fg_color=couleur_fond, corner_radius=corner2, text_color=couleur1,
                                    height=40, border_width=border2, border_color=couleur2, hover_color=couleur_fond)
                label.grid(row=0, column=col_idx, padx=5, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)

            if compétition_result:
                for row_idx, activite in enumerate(compétition_result):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 1:
                            date = datetime.strptime(data, '%Y-%m-%d')
                            data = date.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=140)
                        label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=15, sticky="ew")
                button_modifier.pack(side="left", padx=2)
                button_delete.pack(side="left", padx=2)
            else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucune compétition futur n'a été enregistrée.", font=(font_principale, taille1))
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes compétitions !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def ajouter_objectif(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=10)
    Titre = ctk.CTkLabel(master=frame ,text="Ajouter un objectif", font=(font_secondaire, taille1))
    Titre.pack(padx=10, pady=0)

    frame_tout = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(expand=True, fill="both", padx=12, pady=(12, 2))
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(expand=True, fill="both", padx=12, pady=2)
    frame3 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(expand=True, fill="both", padx=12, pady=2)
    frame4 = ctk.CTkFrame(master=frame_tout, fg_color="transparent")
    frame4.pack(expand=True, fill="both", padx=12, pady=(2, 12))

    options_statut = {"Pas encore démarré":"Pas encore démarré", "En cours": "En cours", "Atteint" : "Atteint", "Non-atteint" : "Non-atteint"}
    options_niveau = {"Débutant": "Débutant", "Fondations": "Fondations", "Intermédiaire" : "Intermédiaire", "Avancé": "Avancé", "Expert": "Expert", "Maîtrise": "Maîtrise"}

    app.bind('<Return>', lambda event: sql_ajouté(account_id))
    sport_entry = ctk.CTkEntry(master=frame1, placeholder_text="Sport", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=320)
    sport_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    frame_pour_date = ctk.CTkFrame(master=frame1, fg_color=couleur_fond, corner_radius=corner1)
    frame_pour_date.pack(expand=True, fill="both", side="left", padx=(0, 2))
    date_entry = ctk.CTkEntry(master=frame_pour_date, placeholder_text="Date", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=36, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=160)
    date_entry.pack(expand=True, fill="both", side="left", padx=(12,0), pady=12)
    button_pop_up_calendrier = ctk.CTkButton(frame_pour_date, text="📅 Calendrier", width=75, height=36, corner_radius=corner1, fg_color=couleur2,
                                            hover_color=couleur2_hover, font=(font_principale, taille3), text_color=couleur1,
                                            border_color=couleur2, border_width=border1,
                                            command=lambda: pop_up_calendrier(app, date_entry))
    button_pop_up_calendrier.pack(expand=True, fill="both", side="left", padx=(0, 12), pady=12)

    objectif_entry = ctk.CTkEntry(master=frame2, placeholder_text="Objectif", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    objectif_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    fréquence_entry = ctk.CTkEntry(master=frame2, placeholder_text="Fréquence d'entraî.", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=320)
    fréquence_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    niveau_entry = ctk.CTkComboBox(master=frame3, values=list(options_niveau.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=320, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    niveau_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    niveau_entry.set("Niveau actuel")
    statut_entry = ctk.CTkComboBox(master=frame3, values=list(options_statut.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=320, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    statut_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    statut_entry.set("Statut de l'objectif")

    def sql_ajouté(account_id):
        sport = sport_entry.get().strip()
        date_str = date_entry.get().strip()
        objectif = objectif_entry.get().strip()
        fréquence = fréquence_entry.get().strip()
        niveau_choisi = niveau_entry.get()
        niveau = niveau_entry.get().strip()
        statut_choisi = statut_entry.get()
        statut = statut_entry.get().strip()

        if niveau_choisi == "Niveau actuel":
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Niveau actuel' !")
            return
        if statut_choisi == "Statut de l'objectif":
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Statut de l'objectif' !")
            return
        if not sport:
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Sport' !")
            return
        if not date_str:
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Date' !")
            return
        if not objectif:
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Objectif' !")
            return
        if not fréquence:
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Fréquence' !")
            return
        if not niveau:
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Niveau actuel' !")
            return
        if not statut:
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Statut de l'objectif' !")
            return
        try:
            date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
            date = date_conversion.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "La date doit être au format JJ-MM-AAAA !")
            return
        else:
            try:
                curseur.execute("INSERT INTO Objectif (account_id, sport, date, objectif, fréquence, niveau_début, statut) VALUES (?, ?, ?, ?, ?, ?, ?)", (account_id, sport, date, objectif, fréquence, niveau, statut))
                con.commit()
                messagebox.showinfo("Enregistré", "Ton objectif a été enregistré, bonne chance !")
                vider_fenetre(app)
                objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton objectif !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_enregistrer = ctk.CTkButton(master=frame4, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                                        command=lambda: sql_ajouté(account_id))
    button_enregistrer.pack(expand=True, fill="both", side="left", padx=2)
    button_back = ctk.CTkButton(master=frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                           command=lambda: [vider_fenetre(app), objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left", padx=2)

def modifier_objectif_étape2(account_id, result_id, app,sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):    
    id_modifier = result_id[0][0]
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)
    try:
        curseur.execute("SELECT date, objectif, fréquence, sport FROM Objectif WHERE id = ? AND account_id = ?",(id_modifier, account_id))
        data_objectif = curseur.fetchall()
        premiere_ligne = data_objectif[0]
        date1 = premiere_ligne[0]
        date_conversion = datetime.strptime(date1, "%Y-%m-%d")
        date_value = date_conversion.strftime("%d-%m-%Y")
        objectif_value = premiere_ligne[1]
        frequence_value = premiere_ligne[2]
        sport_value = premiere_ligne[3]
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de ton objectif !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=10)
    Titre = ctk.CTkLabel(master=frame ,text="Modifier un objectif", font=(font_secondaire, taille1))
    Titre.pack(padx=10, pady=0)

    frame_tout = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(expand=True, fill="both", padx=12, pady=(12, 2))
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(expand=True, fill="both", padx=12, pady=2)
    frame3 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(expand=True, fill="both", padx=12, pady=2)
    frame4 = ctk.CTkFrame(master=frame_tout, fg_color="transparent")
    frame4.pack(expand=True, fill="both", padx=12, pady=(2, 12))

    options_statut = {"Pas encore démarré":"Pas encore démarré", "En cours": "En cours", "Atteint" : "Atteint", "Non-atteint" : "Non-atteint"}
    options_niveau = {"Débutant": "Débutant", "Fondations": "Fondations", "Intermédiaire" : "Intermédiaire", "Avancé": "Avancé", "Expert": "Expert", "Maîtrise": "Maîtrise"}

    app.bind('<Return>', lambda event: sql_ajouté(account_id))
    sport_entry = ctk.CTkEntry(master=frame1, placeholder_text=f"{sport_value}", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=320)
    sport_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    frame_pour_date = ctk.CTkFrame(master=frame1, fg_color=couleur_fond, corner_radius=corner1)
    frame_pour_date.pack(expand=True, fill="both", side="left", padx=(0, 2))
    date_entry = ctk.CTkEntry(master=frame_pour_date, placeholder_text=f"{date_value}", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=36, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=160)
    date_entry.pack(expand=True, fill="both", side="left", padx=(12,0), pady=12)
    button_pop_up_calendrier = ctk.CTkButton(frame_pour_date, text="📅 Calendrier", width=75, height=36, corner_radius=corner1, fg_color=couleur2,
                                            hover_color=couleur2_hover, font=(font_principale, taille3), text_color=couleur1,
                                            border_color=couleur2, border_width=border1,
                                            command=lambda: pop_up_calendrier(app, date_entry))
    button_pop_up_calendrier.pack(expand=True, fill="both", side="left", padx=(0, 12), pady=12)

    objectif_entry = ctk.CTkEntry(master=frame2, placeholder_text=f"{objectif_value}", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    objectif_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    fréquence_entry = ctk.CTkEntry(master=frame2, placeholder_text=f"{frequence_value}", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    fréquence_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    niveau_entry = ctk.CTkComboBox(master=frame3, values=list(options_niveau.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=320, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    niveau_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    niveau_entry.set("Level final")
    statut_entry = ctk.CTkComboBox(master=frame3, values=list(options_statut.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=320, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    statut_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    statut_entry.set("Statut de l'objectif")

    def sql_ajouté(account_id):
        sport = sport_entry.get().strip()
        date_str = date_entry.get().strip()
        objectif = objectif_entry.get().strip()
        fréquence = fréquence_entry.get().strip()
        niveau_choisi = niveau_entry.get()
        try:
            niveau = options_niveau[niveau_choisi]
        except Exception: 
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Niveau final' !")
            return
        statut_choisi = statut_entry.get()
        try:
            statut = options_statut[statut_choisi]
        except Exception:
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Statut de l'objectif' !")
            return
        if not sport:
            sport = sport_value
        if not date_str:
            date_str = date_value
        if not objectif:
            objectif = objectif_value
        if not fréquence:
            fréquence = frequence_value
        try:
            date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
            date = date_conversion.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "La date doit être au format JJ-MM-AAAA !")
            return
        else:
            try:
                curseur.execute("UPDATE Objectif SET sport = ?, date = ?, objectif = ?, fréquence = ?, niveau_fin = ?, statut = ? WHERE id = ? AND account_id = ?",
                    (sport, date, objectif, fréquence, niveau, statut, id_modifier, account_id))
                con.commit()
                messagebox.showinfo("Enregistré", "Ton objectif a été modifié avec succès!")
                vider_fenetre(app)
                objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de ton objectif !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_enregistrer = ctk.CTkButton(master=frame4, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                                        command=lambda: sql_ajouté(account_id))
    button_enregistrer.pack(expand=True, fill="both", side="left", padx=2)
    button_back = ctk.CTkButton(master=frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                           command=lambda: [vider_fenetre(app), modifier_objectif_étape1(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left", padx=2)
    aide_objectif(account_id)

def modifier_objectif_étape1(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(master=app ,text="Modifier un objectif", font=(font_secondaire, taille1))
    Titre.pack(padx=10, pady=10)

    frame_tout = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color="transparent")
    frame1.pack(pady=(12, 2), padx=12)
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color="transparent")
    frame2.pack(pady=(2, 12), padx=12)

    app.bind('<Return>', lambda event: valider(account_id))
    choix_entry = ctk.CTkEntry(frame1, placeholder_text="ID de l'objectif", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    choix_entry.pack(expand=True, fill="both")

    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
    try:
        curseur.execute("SELECT id, sport, date, niveau_début, niveau_fin, statut FROM Objectif WHERE account_id = ?AND date >= ? ORDER BY date ASC", (account_id, date_actuelle))
        result = curseur.fetchall()
        headers = ["ID", "Sport", "Date", "Level début", "Level fin", "Statut"]

        for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkButton(tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                    fg_color=couleur_fond, corner_radius=corner2, text_color=couleur1,
                                    height=40, border_width=border2, border_color=couleur2, hover_color=couleur_fond)
                label.grid(row=0, column=col_idx, padx=5, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)
        if result:
                for row_idx, activite in enumerate(result):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 2:
                            date = datetime.strptime(data, '%Y-%m-%d')
                            data = date.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=140)
                        label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=15, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré", font=(font_principale, taille1))
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def valider(account_id):
            choix = choix_entry.get().strip()
            try:
                if not choix:
                    messagebox.showerror("Erreur", "ID ne peut pas être vide ! Merci de saisir un identifiant !")
                try:
                    id = int(choix)
                    if id < 0:
                        messagebox.showerror("Erreur", "ID doit être un nombre entier positif !")
                        return
                except:
                    messagebox.showerror("Erreur", "ID doit être un nombre entier positif !")
                    return

                curseur.execute("SELECT id FROM Objectif WHERE id = ? AND account_id = ?", (id, account_id))
                result_id = curseur.fetchall()
                if result_id:
                    vider_fenetre(app)
                    modifier_objectif_étape2(account_id, result_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
                else:
                    messagebox.showerror("Erreur", "ID de l'objectif saisi n'existe pas ou n'appartient pas à ton compte !")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de l'objectif !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes objectifs !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, veuillez réessayer !")
    button_check = ctk.CTkButton(master=frame2, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: valider(account_id))
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_retour = ctk.CTkButton(master=frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_retour.pack(expand=True, fill="both", side="left")

def supprimer_objectif(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(master=app ,text="Supprimer un objectif", font=(font_secondaire, taille1))
    Titre.pack(padx=10, pady=10)

    frame_tout = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color="transparent")
    frame1.pack(pady=(12, 2), padx=12)
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color="transparent")
    frame2.pack(pady=(2, 12), padx=12)

    app.bind('<Return>', lambda event: supression(account_id))
    choix_entry = ctk.CTkEntry(master=frame1, placeholder_text="ID de l'objectif", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    choix_entry.pack(expand=True, fill="both")

    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
    try:
        curseur.execute("SELECT id, sport, date, objectif, statut FROM Objectif WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        headers = ["ID", "Sport", "Date", "Objectif", "Statut"]
        for col_idx, header_text in enumerate(headers):
            label = ctk.CTkButton(tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                    fg_color=couleur_fond, corner_radius=corner2, text_color=couleur1,
                                    height=40, border_width=border2, border_color=couleur2, hover_color=couleur_fond)
            label.grid(row=0, column=col_idx, padx=6, pady=15, sticky="ew")
            tableau_frame.grid_columnconfigure(col_idx, weight=1)
        if result:
            for row_idx, activite in enumerate(result):
                for col_idx, data in enumerate(activite):
                    if col_idx == 2:
                        date = datetime.strptime(str(data), '%Y-%m-%d')
                        data = date.strftime('%d-%m-%Y')
                    label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                    label.grid(row=row_idx + 1, column=col_idx, padx=6, pady=15, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=(font_principale, taille2))
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def supression(account_id):
            choix = choix_entry.get().strip()
            try:
                choix_id_saisi = int(choix)
                ids_objectifs_disponibles = [obj[0] for obj in result]

                if choix_id_saisi in ids_objectifs_disponibles:
                    objectif_id_db = choix_id_saisi
                    curseur.execute("DELETE FROM Objectif WHERE id = ? AND account_id = ?", (objectif_id_db, account_id))
                    con.commit()
                    messagebox.showinfo("Suppression réussie", "Objectif supprimé avec succès.")
                    vider_fenetre(app)
                    objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
                else:
                    messagebox.showerror("Erreur", "L'ID de l'objectif saisi n'existe pas ou n'appartient pas à ton compte !")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la suppression de l'objectif !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes objectifs !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_check = ctk.CTkButton(master=frame2, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: supression(account_id))
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_retour = ctk.CTkButton(master=frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: [vider_fenetre(app), objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_retour.pack(expand=True, fill="both", side="left")

def tout_objectif(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    petite_boite = ctk.CTkFrame(master=app, fg_color="transparent")
    petite_boite.pack(padx=10, pady=10)
    Titre = ctk.CTkLabel(petite_boite, text="Tous les objectifs", font=(font_secondaire, taille1))
    Titre.pack(side="left")
    button_retour = ctk.CTkButton(petite_boite, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), border_width=border2, border_color=couleur2,
                                    command=lambda: [vider_fenetre(app), objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_retour.pack(side="left", padx=(10, 0))

    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
    try:
            curseur.execute("SELECT sport, date, objectif, fréquence, niveau_début, niveau_fin, statut FROM Objectif WHERE account_id = ? ORDER BY date ASC", (account_id,))
            objectif_result = curseur.fetchall()

            headers = ["Sport", "Date", "Objectif", "Fréquence", "Level début", "Level fin", "Statut"]

            for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkButton(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                    fg_color=couleur_fond, corner_radius=corner2, text_color=couleur1,
                                    height=40, border_width=border2, border_color=couleur2, hover_color=couleur_fond)
                label.grid(row=0, column=col_idx, padx=5, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)
            if objectif_result:
                for row_idx, activite in enumerate(objectif_result):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 1:
                            date = datetime.strptime(data, '%Y-%m-%d')
                            data = date.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=140)
                        label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=15, sticky="ew")
            else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=(font_principale, taille1))
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes objectifs !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    boite = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner2)
    boite.pack(side="top", fill="x", padx=10, pady=(10, 5))
    boite_semi_header = ctk.CTkFrame(master=boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header.pack(expand=True, fill="x", side="left", padx=(2, 10), pady=2)
    boite_semi_header2 = ctk.CTkFrame(master=boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header2.pack(expand=True, fill="x", side="right", padx=(0, 2), pady=2)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Charge d'entraînement":
            app.after(0, lambda: [vider_fenetre(app), charge_entraînement(account_id)])
        elif choix == "Objectif":
            app.after(0, lambda: [vider_fenetre(app), objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Compétition":
            app.after(0, lambda: [vider_fenetre(app), compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
        else:
            app.after(0, lambda: [vider_fenetre(app), indulgence_de_course(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    mode_activité = ctk.CTkSegmentedButton(master=boite_semi_header, values=["Charge d'entraînement", "Indulgence de course", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner2, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(expand=True, fill="x", side="right", padx=(2, 0), pady=5)
    mode_activité.set("Objectif")
    button_autre = ctk.CTkButton(master=boite_semi_header2, text="🔚 Tous les objectifs", fg_color=couleur2, hover_color=couleur2_hover,
                                    font=(font_principale, taille3), text_color=couleur1, height=button_height, corner_radius=corner1,
                                    width=260,
                                    command=lambda: [vider_fenetre(app), tout_objectif(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_autre.pack(expand=True, fill="x", side="right", padx=(2, 5), pady=5)

    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack(pady=(20, 5))
    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))

    button_ajouter = ctk.CTkButton(master=frame_boutons, text="➕  Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, border_width=border2,
                           border_color=couleur2,
                           command=lambda: [vider_fenetre(app), ajouter_objectif(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_ajouter.pack(side="left", padx=2)
    button_modifier = ctk.CTkButton(master=frame_boutons, text="✏️  Modifier", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, border_width=border2,
                           border_color=couleur2,
                           command=lambda: [vider_fenetre(app), modifier_objectif_étape1(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_modifier.pack_forget()
    button_delete = ctk.CTkButton(master=frame_boutons, text="🗑️ Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, border_width=border2,
                           border_color=couleur2,
                           command=lambda: [vider_fenetre(app), supprimer_objectif(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_delete.pack_forget()

    try:
        curseur.execute("SELECT sport, date, objectif, fréquence, niveau_début, niveau_fin, statut FROM Objectif WHERE account_id = ? AND date >= ? ORDER BY date ASC", (account_id, date_actuelle))
        objectif_result = curseur.fetchall()

        headers = ["Sport", "Date", "Objectif", "Fréquence", "Level début", "Level fin", "Statut"]

        for col_idx, header_text in enumerate(headers): #_idx= index de colonne
            label = ctk.CTkButton(tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                    fg_color=couleur_fond, corner_radius=corner2, text_color=couleur1,
                                    height=40, border_width=border2, border_color=couleur2, hover_color=couleur_fond)
            label.grid(row=0, column=col_idx, padx=5, pady=15, sticky="ew")
            tableau_frame.grid_columnconfigure(col_idx, weight=1)
        if objectif_result:
            for row_idx, activite in enumerate(objectif_result):
                for col_idx, data in enumerate(activite):
                    if col_idx == 1:
                        date = datetime.strptime(data, '%Y-%m-%d')
                        data = date.strftime('%d-%m-%Y')
                    label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=140)
                    label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=15, sticky="ew")
            button_modifier.pack(side="left", padx=2)
            button_delete.pack(side="left", padx=2)
        else:
            pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=(font_principale, taille1))
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes objectifs!")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def mettre_en_pause_les_analyses(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre, mode):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(master=app ,text="Mettre en pause les analyses", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    info = ctk.CTkLabel(master=app ,text="Si tu as besoin de souffler, ou que tu t'es blessé, tu peux\nmettre en pause les " \
    "analyses pour te reposer et récupérer.", font=(font_principale, taille2))
    info.pack(padx=10, pady=10)

    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(pady=10, padx=10)

    frame_tout = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=10)
    frame1 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame1.pack(expand=True, fill="both", padx=12, pady=(12, 2))
    frame2 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame2.pack(expand=True, fill="both", padx=12, pady=(2, 12))

    result = verifier_pause(account_id)
    if result == "vacances":
        info_statut_actif = ctk.CTkLabel(master=frame, text=f"Ton statut d'entraînement actuel: Vacances", font=(font_principale, taille2))
        info_statut_actif.pack(padx=0, pady=10)
    elif result == "blessure":
        info_statut_actif = ctk.CTkLabel(master=frame, text=f"Ton statut d'entraînement actuel : Blessure", font=(font_principale, taille2))
        info_statut_actif.pack(padx=0, pady=10)
    elif result == "suspendre":
        info_statut_actif = ctk.CTkLabel(master=frame, text=f"Ton statut d'entraînement actuel : Suspendre", font=(font_principale, taille2))
        info_statut_actif.pack(padx=0, pady=10)
    else:
        info_statut = ctk.CTkLabel(master=frame, text="Ton statut d'entraînement actuel : Actif", font=(font_principale, taille2))
        info_statut.pack(padx=0, pady=10)

    app.bind('<Return>', lambda event: enregistrer_activité(account_id))
    options = ["Vacances", "Blessure", "Suspendre", "Reprendre les analyses"]
    combo_statut = ctk.CTkComboBox(master=frame1, values=options, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=350, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    combo_statut.pack()
    combo_statut.set("Raison")

    def enregistrer_activité(account_id):
        statut = combo_statut.get().strip()
        try:
            if statut == "Vacances":
                activer_pause(account_id, "vacances")
                vider_fenetre(app)
                charge_entraînement(account_id)
            elif statut == "Blessure":
                activer_pause(account_id, "blessure")
                vider_fenetre(app)
                charge_entraînement(account_id)
            elif statut == "Suspendre":
                activer_pause(account_id, "suspendre")
                vider_fenetre(app)
                charge_entraînement(account_id)
            elif statut == "Reprendre les analyses":
                arreter_pause(account_id)
                vider_fenetre(app)
                charge_entraînement(account_id)
            else:
                messagebox.showerror("Erreur", "Le champ 'Raison' ne peut pas être vide ! Merci de choisir une raison !")
                return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_check = ctk.CTkButton(master=frame2, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: enregistrer_activité(account_id))
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    if mode == "indulgence":
        button_retour = ctk.CTkButton(master=frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                        corner_radius=corner1, height=button_height, text_color=couleur1,
                                        font=(font_principale, taille3),
                                        command=lambda: [vider_fenetre(app), indulgence_de_course(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
        button_retour.pack(expand=True, fill="both", side="left", padx=0)
    else:
        button_retour = ctk.CTkButton(master=frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                        corner_radius=corner1, height=button_height, text_color=couleur1,
                                        font=(font_principale, taille3),
                                        command=lambda: [vider_fenetre(app), charge_entraînement(account_id)])
        button_retour.pack(expand=True, fill="both", side="left", padx=0)

def indulgence_de_course(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    boite = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner2)
    boite.pack(side="top", fill="x", padx=10, pady=(10, 5))
    boite_semi_header = ctk.CTkFrame(master=boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header.pack(expand=True, fill="x", side="left", padx=(2, 10), pady=2)
    boite_semi_header2 = ctk.CTkFrame(master=boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header2.pack(expand=True, fill="x", side="right", padx=(0, 2), pady=2)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Charge d'entraînement":
            app.after(0, lambda: [vider_fenetre(app), charge_entraînement(account_id)])
        elif choix == "Objectif":
            app.after(0, lambda: [vider_fenetre(app), objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Compétition":
            app.after(0, lambda: [vider_fenetre(app), compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
        else:
            app.after(0, lambda: [vider_fenetre(app), indulgence_de_course(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    mode_activité = ctk.CTkSegmentedButton(master=boite_semi_header, values=["Charge d'entraînement", "Indulgence de course", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner2, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(expand=True, fill="x", side="right", padx=(2, 0), pady=5)
    mode_activité.set("Indulgence de course")
    button_autre = ctk.CTkButton(master=boite_semi_header2, text="⏸️ Mettre en pause les analyses", fg_color=couleur2, hover_color=couleur2_hover,
                                    font=(font_principale, taille3), text_color=couleur1, height=button_height, corner_radius=corner1,
                                    command=lambda: [vider_fenetre(app), mettre_en_pause_les_analyses(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre, "indulgence")])
    button_autre.pack(expand=True, fill="x", side="right", padx=(2, 5), pady=5)

    D28J = date_actuelle - timedelta(days=28)
    D28J_str = D28J.strftime('%Y-%m-%d')
    curseur.execute("SELECT distance FROM Historique_activité WHERE account_id = ? AND catégorie = 'course' AND date_activité >= ?", (account_id, D28J_str))
    distance28J = [row[0] for row in curseur.fetchall()]
    distance_moyenne_des_derniers_28_jours = sum(distance28J) / 4 if distance28J else 0.00
    if distance_moyenne_des_derniers_28_jours < 10:
        distance_maximumconseillé_début = distance_moyenne_des_derniers_28_jours*1.18
        distance_maximumconseillé_fin = distance_moyenne_des_derniers_28_jours*1.25
    elif 10 <= distance_moyenne_des_derniers_28_jours <= 20:
        distance_maximumconseillé_début = distance_moyenne_des_derniers_28_jours*1.15
        distance_maximumconseillé_fin = distance_moyenne_des_derniers_28_jours*1.20
    elif 20 <= distance_moyenne_des_derniers_28_jours <= 40:
        distance_maximumconseillé_début = distance_moyenne_des_derniers_28_jours*1.12
        distance_maximumconseillé_fin = distance_moyenne_des_derniers_28_jours*1.15
    elif 40 <= distance_moyenne_des_derniers_28_jours <= 60:
        distance_maximumconseillé_début = distance_moyenne_des_derniers_28_jours*1.09
        distance_maximumconseillé_fin = distance_moyenne_des_derniers_28_jours*1.12
    else:
        distance_maximumconseillé_début = distance_moyenne_des_derniers_28_jours*1.06
        distance_maximumconseillé_fin = distance_moyenne_des_derniers_28_jours*1.10

    D7J = date_actuelle - timedelta(days=7)
    D7J_str = D7J.strftime('%Y-%m-%d')
    curseur.execute("SELECT distance FROM Historique_activité WHERE account_id = ? AND catégorie = 'course' AND date_activité >= ?", (account_id, D7J_str))
    distance7J = [row[0] for row in curseur.fetchall()]
    distance_des_derniers_7_jours = sum(distance7J) if distance7J else 0

    boite_distance_course_gauche = ctk.CTkFrame(master=app, border_width=border2, border_color=couleur1, corner_radius=corner1,
                                             fg_color=couleur_fond)
    boite_distance_course_gauche.pack(fill="both", expand=True, side="left", padx=(40, 10), pady=(30, 40))
    h1_boite_distance_course = ctk.CTkFrame(master=boite_distance_course_gauche, fg_color=couleur_fond)
    h1_boite_distance_course.pack(pady=5)

    boite_analyse_kilométrage = ctk.CTkFrame(master=boite_distance_course_gauche, border_width=border2, border_color=couleur1, corner_radius=corner1, fg_color=couleur2)
    boite_analyse_kilométrage.pack(fill="both", expand=True, padx=15, pady=5)
    distance_7_jours = ctk.CTkFrame(master=boite_analyse_kilométrage, corner_radius=corner1, fg_color=couleur1)
    distance_7_jours.pack(fill="both", expand=True, padx=12, pady=(12, 5))
    distance_maximum = ctk.CTkFrame(master=boite_analyse_kilométrage, corner_radius=corner1, fg_color=couleur1)
    distance_maximum.pack(fill="both", expand=True, padx=12, pady=(5, 12))

    boite_statut = ctk.CTkFrame(master=boite_distance_course_gauche, border_width=border2, border_color=couleur1, corner_radius=corner1, fg_color=couleur2)
    boite_statut.pack(fill="both", expand=True, padx=15, pady=(5, 15))
    h1_zone = ctk.CTkFrame(master=boite_statut, corner_radius=corner1, fg_color=couleur1)
    h1_zone.pack(fill="both", expand=True, padx=12, pady=(12, 5))
    interprétation = ctk.CTkFrame(master=boite_statut, corner_radius=corner1, fg_color=couleur1)
    interprétation.pack(fill="both", expand=True, pady=(5, 12), padx=12)

    boite_distance_course_droit = ctk.CTkFrame(master=app, border_width=border2, border_color=couleur1, corner_radius=corner1,
                                             fg_color=couleur_fond)
    boite_distance_course_droit.pack(fill="both", expand=True, side="right", padx=(10, 40), pady=(30, 40))

    boite_statut = ctk.CTkFrame(master=boite_distance_course_droit, border_width=border2, border_color=couleur1, corner_radius=corner1, fg_color=couleur2)
    boite_statut.pack(fill="both", expand=True, pady=15, padx=15)
    distance_moyenne_28J = ctk.CTkFrame(master=boite_statut, corner_radius=corner1, fg_color=couleur1)
    distance_moyenne_28J.pack(fill="both", expand=True, padx=12, pady=(12, 5))
    conseil = ctk.CTkFrame(master=boite_statut, corner_radius=corner1, fg_color=couleur1)
    conseil.pack(fill="both", expand=True, pady=(5, 12), padx=12)
    
    info = ctk.CTkFrame(master=boite_distance_course_droit, corner_radius=corner1, fg_color=couleur1)
    info.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    h1 = ctk.CTkLabel(master=h1_boite_distance_course, font=(font_secondaire, taille2), text="7 derniers jours")
    h1.pack(padx=10, pady=(5, 0))
    distance_7J = ctk.CTkLabel(distance_7_jours, text=f"Distance (7 jours) : {distance_des_derniers_7_jours:.2f} km", font=(font_principale , taille2),
                                    width=300, wraplength=300)
    distance_7J.pack(fill="both", expand=True, padx=10, pady=10)

    distance_moyenne_du_mois = ctk.CTkLabel(distance_moyenne_28J, text=f"Distance moyenne hebdo. (4 semaines) :\n{distance_moyenne_des_derniers_28_jours:.2f} km par semaine", font=(font_principale, taille2),
                                width=300, wraplength=500)
    distance_moyenne_du_mois.pack(fill="both", expand=True, padx=10, pady=10)  
    pause = verifier_pause(account_id)
    if pause == "blessure":
        Distance_maximal_conseillé = ctk.CTkLabel(distance_maximum, text=f"Distance maximale hebdo. conseillée : actuellement en pause", font=(font_secondaire, taille2),
                                        width=300, wraplength=300)
        Distance_maximal_conseillé.pack(fill="both", expand=True, padx=10, pady=10)
        zone = ctk.CTkLabel(master=h1_zone, text="⛑️ Mode blessure : suivi désactivé", font=(font_secondaire, taille2),
                                width=300, wraplength=300, text_color="#c60000")
        zone.pack(fill="both", expand=True, padx=10, pady=10)                 
        interprétation_zone = ctk.CTkLabel(master=interprétation, text="Tu es blessé pour le moment.", font=(font_principale, taille3),
                                        width=300, wraplength=300)
        interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)      
        conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Prends vraiment le temps de laisser ton corps se régénérer en profondeur, afin de revenir encore plus fort et plus déterminé que jamais.", font=(font_principale, taille3),
                                    width=300, wraplength=500)
        conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)
    elif pause == "vacances":
        Distance_maximal_conseillé = ctk.CTkLabel(distance_maximum, text=f"Distance maximale hebdo. conseillée : actuellement en pause", font=(font_secondaire, taille2),
                                        width=300, wraplength=300)
        Distance_maximal_conseillé.pack(fill="both", expand=True, padx=10, pady=10)
        zone = ctk.CTkLabel(master=h1_zone, text="🏖️ Mode vacances : pas d'analyse !", font=(font_secondaire, taille2),
                                width=300, wraplength=300, text_color="#6AC100")
        zone.pack(fill="both", expand=True, padx=10, pady=10)                 
        interprétation_zone = ctk.CTkLabel(master=interprétation, text="Tu es actuellement en vacances.", font=(font_principale, taille3),
                                        width=300, wraplength=300)
        interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)      
        conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Profite de cette pause pour te ressourcer, apprécier les moments de détente et les repas, et reviens encore plus motivé !", font=(font_principale, taille3),
                                    width=300, wraplength=500)
        conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)
    elif pause == "suspendre":
        Distance_maximal_conseillé = ctk.CTkLabel(distance_maximum, text=f"Distance maximale hebdo. conseillée : actuellement en pause", font=(font_secondaire , taille3),
                                        width=300, wraplength=300)
        Distance_maximal_conseillé.pack(fill="both", expand=True, padx=10, pady=10)
        zone = ctk.CTkLabel(master=h1_zone, text="💤 Mode suspension activé : aucune analyse en cours", font=(font_secondaire, taille2),
                                width=300, wraplength=300, text_color="#6AC100")
        zone.pack(fill="both", expand=True, padx=10, pady=10)                 
        interprétation_zone = ctk.CTkLabel(master=interprétation, text="Tes analyses sont temporairement en pause pendant ce mode suspension.", font=(font_principale, taille3),
                                        width=300, wraplength=300)
        interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)      
        conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Profite-en pour te reposer sans pression, on reprend les suivis dès ton retour à l’entraînement !", font=(font_principale, taille3),
                                    width=300, wraplength=500)
        conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)
    else:
        if distance_moyenne_des_derniers_28_jours == 0:
            Distance_maximal_conseillé = ctk.CTkLabel(distance_maximum, text=f"Distance maximale hebdo. conseillée :\nDonnées insuffisantes", font=(font_secondaire, taille2),
                                            width=300, wraplength=300)
            Distance_maximal_conseillé.pack(fill="both", expand=True, padx=10, pady=10)

            zone = ctk.CTkLabel(master=h1_zone, text="🚫 Données insuffisantes", font=(font_secondaire, taille2),
                                        width=300, wraplength=300, text_color="#c60000")
            zone.pack(fill="both", expand=True, padx=10, pady=10)              
            interprétation_zone = ctk.CTkLabel(master=interprétation, text="L'interprétation de votre zone d'indulgence de course ne peut pas être déterminée.", font=(font_principale, taille3),
                                            width=300, wraplength=300)
            interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)
                    
            conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Pour pouvoir obtenir des interprétations et des conseils de course. Fais une séance de sport pour lancer les analyses et évaluer ton indulgence de course.", font=(font_principale, taille3),
                                            width=300, wraplength=500)
            conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            Distance_maximal_conseillé = ctk.CTkLabel(distance_maximum, text=f"Distance maximale hebdo. conseillée :\n{distance_maximumconseillé_début:.1f} et {distance_maximumconseillé_fin:.1f} km", font=(font_secondaire, taille2),
                                            width=300, wraplength=300)
            Distance_maximal_conseillé.pack(fill="both", expand=True, padx=10, pady=10)

            if distance_moyenne_des_derniers_28_jours < distance_des_derniers_7_jours < distance_maximumconseillé_fin:
                zone = ctk.CTkLabel(master=h1_zone, text="🚀 Zone optimale pour progresser", font=(font_secondaire, taille2),
                                            width=300, wraplength=300, text_color="#00BA47")
                zone.pack(fill="both", expand=True, padx=10, pady=10)              
                interprétation_zone = ctk.CTkLabel(master=interprétation, text="Tu es en train de progresser en course, bravo ! Tu as fais le plus dur !", font=(font_principale, taille3),
                                                width=300, wraplength=300)
                interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)
                        
                conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Pour continuer à avancer et voir des résultats sur le long terme, fais en sorte de maintenir ce volume d’entraînement chaque semaine. C’est la régularité qui te permettra de progresser de manière stable, efficace et idéal pour éviter les blessures. Continue comme ça !", font=(font_principale, taille3),
                                                width=300, wraplength=500)
                conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)

            elif distance_des_derniers_7_jours > distance_maximumconseillé_fin:
                zone = ctk.CTkLabel(master=h1_zone, text="🤕 Zone optimale pour se blesser", font=(font_secondaire, taille2),
                                            width=300, wraplength=300, text_color="#c60000")
                zone.pack(fill="both", expand=True, padx=10, pady=10)              
                interprétation_zone = ctk.CTkLabel(master=interprétation, text="Ton volume kilométrique hebdomadaire est actuellement très élevé par rapport à d'habitude.", font=(font_principale, taille3),
                                                width=300, wraplength=300)
                interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)
                        
                conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Prends quelques jours de pause sans courir pour permettre à ton corps de bien récupérer. La course à pied sollicite énormément tes muscles et articulations, et enchaîner sans repos augmente le risque de blessure. Ce temps de récupération est essentiel pour revenir plus fort et éviter la surcharge.", font=(font_principale, taille3),
                                                width=300, wraplength=500)
                conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)

            elif distance_des_derniers_7_jours == distance_moyenne_des_derniers_28_jours:
                zone = ctk.CTkLabel(master=h1_zone, text="😴 Zone optimale pour stagner", font=(font_secondaire, taille2),
                                            width=300, wraplength=300, text_color="#00C073")
                zone.pack(fill="both", expand=True, padx=10, pady=10)              
                interprétation_zone = ctk.CTkLabel(master=interprétation, text="Ton volume est stable mais légèrement trop bas pour progresser. Tu maintiens ton niveau, mais tu risques de plafonner.", font=(font_principale, taille3),
                                                width=300, wraplength=300)
                interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)
                conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Augmente progressivement ton volume hebdomadaire. De petites augmentations régulières te permettront de sortir de la stagnation sans te blesser, et de retrouver une dynamique de progression.", font=(font_principale, taille3),
                                                width=300, wraplength=500)
                conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)

            else:
                zone = ctk.CTkLabel(master=h1_zone, text="⏬ Zone optimale pour perdre du niveau", font=(font_secondaire, taille2),
                                            width=300, wraplength=300, text_color="#C01802")
                zone.pack(fill="both", expand=True, padx=10, pady=10)              
                interprétation_zone = ctk.CTkLabel(master=interprétation, text="Ton volume kilométrique hebdomadaire est actuellement en dessous des niveaux optimaux pour progresser. Tu en fais moins que d'habitude !", font=(font_principale, taille3),
                                                width=300, wraplength=300)
                interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)
                        
                conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Si tu restes 3 à 4 jours sans courir alors que ton corps est habitué à un certain volume d’entraînement, tu risques de perdre en endurance et en progression. La course à pied demande une régularité pour maintenir tes capacités et continuer à avancer. Trop réduire ton entraînement peut te faire régresser.", font=(font_principale, taille3),
                                                width=300, wraplength=500)
                conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)

    titre_c_quoi = ctk.CTkLabel(master=info, text="C'est quoi l'indulgence de course ?", font=(font_secondaire, taille2), wraplength=500)
    titre_c_quoi.pack(fill="both", expand=True, pady=(10, 10), padx=10)
    c_quoi = ctk.CTkLabel(master=info, 
                          text="L’indulgence de course t’aide à ajuster ton kilométrage des 7 derniers jours pour rester dans une progression optimale, sans dépasser ta limite. Tu peux ainsi continuer à t’améliorer tout en réduisant les risques de blessure. Cette analyse est un guide, mais n’oublie jamais d’écouter les signaux de ton corps. Une fonctionnalité adaptée à tous les niveaux !",
                            font=(font_principale, taille3), wraplength=500)
    c_quoi.pack(fill="both", expand=True, padx=10, pady=(5, 10))

def aide_ajout_activité():
    messagebox.showinfo("Aide", "Pour ajouter une activité, rends-toi dans l'onglet 'Exercice' dans la barre latérale à gauche puis appuis sur le bouton 'Ajouter'.")
    return

def charge_d_entraînement(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    boite = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner2)
    boite.pack(side="top", fill="x", padx=10, pady=(10, 5))
    boite_semi_header = ctk.CTkFrame(master=boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header.pack(expand=True, fill="x", side="left", padx=(2, 10), pady=2)
    boite_semi_header2 = ctk.CTkFrame(master=boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header2.pack(expand=True, fill="x", side="right", padx=(0, 2), pady=2)

    fig = None
    canvas = None
    def fermer_graphique_pause(account_id):
        plt.close(fig)
        mettre_en_pause_les_analyses(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre, "charge")
    def fermer_graphique_mode():    
        nonlocal fig
        if fig:
            plt.close(fig)
            fig = None

    def mise_mode(choix):
        choix = mode_activité.get()
        if fig is None:
            if choix == "Charge d'entraînement":
                app.after(0, lambda: [vider_fenetre(app), charge_entraînement(account_id)])
            elif choix == "Indulgence de course":
                app.after(0, lambda: [vider_fenetre(app), indulgence_de_course(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
            elif choix == "Objectif":
                app.after(0, lambda: [vider_fenetre(app), objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
            elif choix == "Compétition":
                app.after(0, lambda: [vider_fenetre(app), compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
        else:
            if choix == "Charge d'entraînement":
                app.after(0, lambda: [fermer_graphique_mode(), vider_fenetre(app), charge_entraînement(account_id)])
            elif choix == "Indulgence de course":
                app.after(0, lambda: [fermer_graphique_mode(), vider_fenetre(app), indulgence_de_course(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
            elif choix == "Objectif":
                app.after(0, lambda: [fermer_graphique_mode(), vider_fenetre(app), objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
            elif choix == "Compétition":
                app.after(0, lambda: [fermer_graphique_mode(), vider_fenetre(app), compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    mode_activité = ctk.CTkSegmentedButton(master=boite_semi_header, values=["Charge d'entraînement", "Indulgence de course", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner2, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(expand=True, fill="x", side="right", padx=(2, 0), pady=5)
    mode_activité.set("Charge d'entraînement")
    button_autre = ctk.CTkButton(master=boite_semi_header2, text="⏸️ Mettre en pause les analyses", fg_color=couleur2, hover_color=couleur2_hover,
                                    font=(font_principale, taille3), text_color=couleur1, height=button_height, corner_radius=corner1,
                                    command=lambda: [vider_fenetre(app), fermer_graphique_pause(account_id)])
    button_autre.pack(expand=True, fill="x", side="right", padx=(2, 5), pady=5)

    charge_aigue = 0.0
    charge_chronique = 0.0
    try:
        ca = date_actuelle - timedelta(days=7)
        ca_str = ca.strftime('%Y-%m-%d')
        curseur.execute("SELECT charge FROM Historique_activité WHERE account_id = ? AND date_activité >= ?", (account_id, ca_str))
        charges_aigue = [row[0] for row in curseur.fetchall()]

        cc = date_actuelle - timedelta(days=28)
        cc_str = cc.strftime('%Y-%m-%d')
        curseur.execute("SELECT date_activité, charge FROM Historique_activité WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité ASC", (account_id, cc_str))
        data_pour_graphique = curseur.fetchall()

        charge_aigue = sum(charges_aigue) if charges_aigue else 0
        #On prend le 2ème élément des data pour graphique pour avoir les charges et ne pas prendre les dates
        charge_chronique = sum([row[1] for row in data_pour_graphique]) / 4 if data_pour_graphique else 0
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors du calcul de charge d'entraînement !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

    parent_frame = ctk.CTkFrame(master=app, fg_color="transparent")
    parent_frame.pack(fill="both", expand=True, pady=10)

    boite_charge_entraînement = ctk.CTkFrame(master=parent_frame, corner_radius=corner1, fg_color="transparent")
    boite_charge_entraînement.pack(fill="both", expand=True, side="left", padx=(10, 2), pady=(0, 10))

    boite_analyse = ctk.CTkFrame(master=boite_charge_entraînement, corner_radius=corner1, fg_color="transparent")
    boite_analyse.pack(fill="both", expand=True)

    aigue = ctk.CTkFrame(master=boite_analyse, corner_radius=corner1, fg_color=couleur_fond, border_color=couleur2, border_width=border2)
    aigue.pack(fill="both", expand=True, pady=(0,2))
    h1_result_optimale = ctk.CTkFrame(master=boite_analyse, corner_radius=corner1, fg_color=couleur_fond, border_color=couleur2, border_width=border2)
    h1_result_optimale.pack(fill="both", expand=True, pady=2)
    interprétation_conseil = ctk.CTkFrame(master=boite_analyse, corner_radius=corner1, fg_color=couleur_fond, border_color=couleur1, border_width=border2)
    interprétation_conseil.pack(fill="both", expand=True, pady=(2,0))
    
    boite = ctk.CTkFrame(master=parent_frame, corner_radius=corner1, fg_color="transparent")
    boite.pack(fill="both", expand=True, side="right", padx=10, pady=(2, 10))
    graphique = ctk.CTkFrame(master=boite, corner_radius=corner1, fg_color=couleur2, border_color=couleur1, border_width=border2)
    graphique.pack(fill="x", padx=0, pady=(0, 2))
    info = ctk.CTkFrame(master=boite, corner_radius=corner1, fg_color=couleur2, border_color=couleur1, border_width=border2)
    info.pack(fill="both", expand=True, padx=0, pady=(2, 0))

    result_analyse = ctk.CTkLabel(master=aigue, text=f"Charge (7 jours) : {charge_aigue:.1f}", font=(font_principale , taille2),
                                    width=300, wraplength=280, text_color=couleur1)
    result_analyse.pack(fill="both", expand=True, padx=12, pady=12)
    info_nom_coach = ctk.CTkLabel(master=interprétation_conseil, text="👨 JRM Coach", font=(font_secondaire, taille2), wraplength=280, text_color=couleur1,
                                  justify="left")
    info_nom_coach.pack(fill="both", expand=True, pady=(12, 0), padx=12)

    pause = verifier_pause(account_id)

    if pause == "blessure":
        catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="⛑️ Mode blessure : suivi désactivé", font=(font_principale, taille2),
                                        width=300, wraplength=280, text_color=couleur1)
        catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)           
        interpretation_statut = ctk.CTkLabel(master=interprétation_conseil, text="Tu es blessé pour le moment\n\n" \
        "Prends vraiment le temps de laisser ton corps se régénérer en profondeur, afin de revenir encore plus fort que jamais.", font=(font_principale, taille2),
                                    width=300, wraplength=280, justify="left", text_color=couleur1)
        interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12)
    elif pause == "vacances":
        catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🏖️ Mode vacances : pas d'analyse !", font=(font_principale, taille2),
                                        width=300, wraplength=280, text_color=couleur1)
        catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)          
        interpretation_statut = ctk.CTkLabel(master=interprétation_conseil, text="Tu es actuellement en vacances.\n\n" \
        "Profite de cette pause pour te ressourcer, apprécier les moments de détente et les repas, et reviens encore plus motivé !", font=(font_principale, taille2),
                                    width=300, wraplength=280, justify="left", text_color=couleur1)
        interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12)  
    elif pause == "suspendre":
        catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="💤 Mode suspension activé : aucune analyse en cours.", font=(font_principale, taille2),
                                        width=300, wraplength=280, text_color=couleur1)
        catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)
        interpretation_statut = ctk.CTkLabel(master=interprétation_conseil, text="Tes analyses sont temporairement en pause pendant ce mode.\n\n" \
        "Profite-en pour te reposer, on reprend les suivis dès ton retour à l’entraînement !", font=(font_principale, taille2), text_color=couleur1,
                                    width=300, wraplength=280, justify="left")
        interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12)
    else :
        if charge_chronique > 0:
            ratio = charge_aigue / charge_chronique
        else:
            ratio = None
        if ratio is not None:
            if ratio < 0.5: 
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🛌 Récupération active", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color=couleur1)
                catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)             
                interpretation_statut = ctk.CTkLabel(master=interprétation_conseil, text="Charge très basse. Tu laisse ton corps se reposer mais jusqu'à quand !\n\n" \
                "Fais une activité physique régulière pour reprendre en main ton entraînement et éviter de perdre ton niveau actuel.", font=(font_principale, taille2),
                                                width=300, wraplength=280, justify="left", text_color=couleur1)
                interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12)  
            elif 0.5 <= ratio <= 0.8:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="😴 Sous-entraînement", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color=couleur1)
                catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)             
                interpretation_statut = ctk.CTkLabel(master=interprétation_conseil, text="Tu es entrain de perdre du niveau, attention !\n\n" \
                "Tu pourrais augmenter légèrement l'intensité de tes entraînements si tu veux basculer en mode maintien et stabiliser tes performances.", font=(font_principale, taille2),
                                                width=300, wraplength=280, justify="left", text_color=couleur1)
                interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12)  
            elif 0.8 <= ratio <= 0.9:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🔄 Maintien", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color=couleur1)
                catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)             
                interpretation_statut = ctk.CTkLabel(master=interprétation_conseil, text="Charge adaptée pour conserver ton niveau\n\n" \
                "Allonge de 5 minutes tes séances pour basculer en mode progression optimale et améliorer tes performances.", font=(font_principale, taille2),
                                                width=300, wraplength=280, justify="left", text_color=couleur1)
                interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12) 
            elif 0.9 <= ratio <= 1.1:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🟢 Progression optimale", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color=couleur1)
                catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)             
                interpretation_statut = ctk.CTkLabel(master=interprétation_conseil, text="Charge idéale pour améliorer tes performances\n\n" \
                "Continue comme ça pour progresser ! Garde cette même régularité dans tes entraînements pour rester en mode progression optimale.", font=(font_principale, taille2),
                                                width=300, wraplength=280, justify="left", text_color=couleur1)
                interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12)
            elif 1.1 < ratio <= 1.3:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="💪 Progression élévée", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color=couleur1)
                catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)             
                interpretation_statut = ctk.CTkLabel(master=interprétation_conseil, text="Tu progresse vite mais fait attention aux blessures\n\n" \
                "Surveille bien la fatigue de ton corps pour éviter les blessures : en gardant cette charge deux semaines, le risque reste limité.",
                                                    font=(font_principale, taille2), width=300, wraplength=280, justify="left", text_color=couleur1)
                interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12) 
            else:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="⚠️ Surentraînement", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color=couleur1)
                catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)             
                interpretation_statut = ctk.CTkLabel(master=interprétation_conseil, text="Risque élevé de blessure\n\n" \
                "Prends 2 à 3 jours de pause pour laisser ton corps récupérer et réduire les risques de blessure.", font=(font_principale, taille2),
                                                width=300, wraplength=280, justify="left", text_color=couleur1)
                interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12) 
        else:
            catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🚫 Données insuffisantes", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color=couleur1)
            catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)             
            interpretation_statut = ctk.CTkLabel(master=interprétation_conseil, text="L'interprétation ne peut pas être déterminée.\n\n" \
            "Fais une séance de sport pour lancer les analyses et évaluer ta charge actuelle.", font=(font_principale, taille2),
                                                width=300, wraplength=280, justify="left", text_color=couleur1)
            interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12)  
    try:   
        if data_pour_graphique:
            dates_graphique = [datetime.strptime(row[0], '%Y-%m-%d') for row in data_pour_graphique]
            charges_graphique = [row[1] for row in data_pour_graphique]

            fig, ax = plt.subplots(figsize=(12, 4))
            # Fond bleu clair pour la figure et la zone du graphique
            fig.patch.set_facecolor(couleur2)
            ax.set_facecolor(couleur2)

            sns.lineplot(x=dates_graphique, y=charges_graphique, marker="o", color=couleur1, ax=ax)

            ax.axhline(y=charge_chronique, color=couleur1, linestyle="--", label="Charge chronique")

            ax.set_title("Évolution de la charge chronique")
            ax.set_xlabel("Date")
            ax.set_ylabel("Charge chronique") 
            canvas = FigureCanvasTkAgg(fig, master=graphique)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True , pady=20, padx=20)
        else:
            not_data = ctk.CTkFrame(master=graphique, corner_radius=corner1, fg_color=couleur1)
            not_data.pack(expand=True, fill="both", padx=10, pady=10)
            pas_de_données = ctk.CTkLabel(master=not_data, text="Pas assez de données pour afficher un graphique.\nAjoute quelques séances d'entraînement pour voir votre évolution !",
                                          font=(font_secondaire, taille2), wraplength=525)
            pas_de_données.pack(padx=15, pady=15)
            button_creer_activite = ctk.CTkButton(master=not_data, text="ℹ️  Aide", fg_color=couleur2, hover_color=couleur2_hover,
                                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                            command=aide_ajout_activité)
            button_creer_activite.pack(padx=(20, 2), pady=20)
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

    titre_c_quoi = ctk.CTkLabel(master=info, text="C'est quoi la charge d'entraînement ?", font=(font_secondaire, taille2), wraplength=600,
                                text_color=couleur1, justify="left")
    titre_c_quoi.pack(fill="both", expand=True, pady=12, padx=12)
    c_quoi = ctk.CTkLabel(master=info, 
                            text="La charge d'entraînement sert à optimiser ta progression sans te cramer, en trouvant le juste équilibre entre l'effort fourni et la récupération nécessaire. C'est ton meilleur ami pour éviter les blessures et planifier tes séances sportives intelligemment.",
                            font=(font_principale, taille2), wraplength=600, justify="left",
                            text_color=couleur1)
    c_quoi.pack(fill="both", expand=True, padx=12, pady=(5, 12))
