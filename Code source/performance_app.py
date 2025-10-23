from app_ressource import * 
from update_database import con, curseur

def verifier_pause(account_id):
    #AND date_fin IS NULL = Cible uniquement les pause non terminés.
    try:
        curseur.execute("SELECT type FROM Pauses WHERE account_id = ?", (account_id,))
        result = curseur.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la vérification du mode d'analyse !")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
        return
    
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
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
        return

def arreter_pause(account_id):
    try:
        curseur.execute("UPDATE Pauses SET type = NULL WHERE account_id = ?", (account_id,))
        con.commit()
        messagebox.showinfo("Enregistré", "Reprise d'activité enregistrée ! Les analyses sont désormais activées !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de l'activation de la reprise d'activité.")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
        return

def pop_up_calendrier(app, date_entry):
    pop_up_calendrier = ctk.CTkToplevel(app, fg_color=couleur2)
    pop_up_calendrier.grab_set()
    pop_up_calendrier.title("Calendrier")
    pop_up_calendrier.geometry("400x400")
    pop_up_calendrier.resizable(False, False)
    pop_up_calendrier.bind("<Control-w>", lambda event: pop_up_calendrier.destroy())

    affichage_calendrier = tkcalendar.Calendar(pop_up_calendrier, selectmode="day", date_pattern="dd/MM/yyyy", 
                                               background=couleur_fond, foreground=couleur_text, headersbackground=couleur_fond, 
                                               normalbackground=couleur2, weekendbackground=couleur2,
                                               othermonthbackground=couleur_fond, othermonthwebackground=couleur_fond,
                                               bordercolor=couleur1, headersforeground=couleur1, selectbackground=couleur1,
                                               selectforeground=couleur_text, font=(font_principale, taille3))
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

    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(pady=10)
    Titre = ctk.CTkLabel(frame ,text="Ajouter une compétition", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=0)

    frame_tout = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(expand=True, fill="both", padx=12, pady=(12, 2))
    frame2 = ctk.CTkFrame(frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(expand=True, fill="both", padx=12, pady=2)
    frame3 = ctk.CTkFrame(frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(expand=True, fill="both", padx=12, pady=2)
    frame4 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame4.pack(expand=True, fill="both", padx=12, pady=(2, 12))

    option = ["Événement Principal", "Événement Secondaire", "Événement tertiaire", "Autre"]
    
    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: sql_ajouté(account_id))

    sport_entry = ctk.CTkEntry(frame1, placeholder_text="Sport", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=320)
    sport_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    frame_pour_date = ctk.CTkFrame(frame1, fg_color=couleur_fond, corner_radius=corner1)
    frame_pour_date.pack(expand=True, fill="both", side="left", padx=(0, 2))
    date_entry = ctk.CTkEntry(frame_pour_date, placeholder_text="Date", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=36, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=160)
    date_entry.pack(expand=True, fill="both", side="left", padx=(12,0), pady=12)
    button_pop_up_calendrier = ctk.CTkButton(frame_pour_date, text="📅 Calendrier", width=75, height=36, corner_radius=corner1, fg_color=couleur2,
                                            hover_color=couleur2_hover, font=(font_principale, taille3), text_color=couleur1,
                                            border_color=couleur2, border_width=border1,
                                            command=lambda: pop_up_calendrier(app, date_entry))
    button_pop_up_calendrier.pack(expand=True, fill="both", side="left", padx=(0, 12), pady=12)

    nom_entry = ctk.CTkEntry(frame2, placeholder_text="Nom de la compétition", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    nom_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    objectif_entry = ctk.CTkEntry(frame2, placeholder_text="Objectif", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    objectif_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    lieu_entry = ctk.CTkEntry(frame3, placeholder_text="Lieu (optionnel)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    lieu_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    priorite_entry = ctk.CTkComboBox(frame3, values=option, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=320, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    priorite_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    priorite_entry.set("Priorité")

    def sql_ajouté(account_id):
        nom = nom_entry.get().strip()
        date_str = date_entry.get().strip().replace('/', '-').replace('.', '-').replace(',', '-').replace('_', '-').replace(' ', '')
        sport = sport_entry.get().strip()
        objectif = objectif_entry.get().strip()
        lieu_avant = lieu_entry.get().strip()
        priorité = priorite_entry.get().strip()
        if not sport:
            messagebox.showerror("Sport est vide", "Le sport est obligatoire !")
            return
        if len(sport) > 50:
            messagebox.showerror("Erreur", "Le nom du sport ne doit pas dépasser 50 caractères !")
            return
        try:
            float(sport)
            messagebox.showerror("Erreur de format", "Le sport doit être une chaîne de caractères, pas un nombre !")
            return
        except ValueError:
            pass

        if not date_str:
            messagebox.showerror("Erreur", "La date de la compétition ne peut pas être vide !")
            return 
        try:
            date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
            date = date_conversion.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur de format de date", "La date doit être au format JJ-MM-AAAA !")
            return

        if not nom:
            messagebox.showerror("Erreur", "Le nom de la compétition ne peut pas être vide !")
            return
        if len(nom) > 60:
            messagebox.showerror("Erreur de longueur", "Le nom de la compétition ne peut pas dépasser 60 caractères !")
            return
        if not objectif:
            messagebox.showerror("Erreur", "L'objectif de la compétition ne peut pas être vide !")
            return
        if len(objectif) > 100:
            messagebox.showerror("Erreur de longueur", "L'objectif de la compétition ne peut pas dépasser 100 caractères !")
            return
        
        if not lieu_avant :
            lieu = None
        else:
            lieu = lieu_avant
        if lieu is not None:
            if len(lieu) > 60:
                messagebox.showerror("Erreur de longueur", "Le lieu de la compétition ne peut pas dépasser 60 caractères !")
                return
            
        if priorité == "Priorité":
            messagebox.showerror("Champs vide", "Le champs 'Priorité' est obligatoire !")
            return
        if not priorité in option:
            messagebox.showerror("Erreur de sélection", "Le champs 'Priorité' doit être une des options proposées !")
            return
        try:
            curseur.execute("INSERT INTO Compétition (account_id, nom, date, sport, objectif, lieu, priorité) VALUES (?, ?, ?, ?, ?, ?, ?)", (account_id, nom, date, sport, objectif, lieu, priorité))
            con.commit()
            messagebox.showinfo("Enregistré", "Ta compétition a été enregistré, bonne chance !")
            vider_fenetre(app)
            compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de la compétition !")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
            return
        
    button_enregistrer = ctk.CTkButton(frame4, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                                    command=lambda: sql_ajouté(account_id))
    button_enregistrer.pack(expand=True, fill="both", side="left", padx=2)
    button_back = ctk.CTkButton(frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                           command=lambda: [vider_fenetre(app), compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left", padx=2)

def supprimer_compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Supprimer une compétition", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    frame_tout = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame1.pack(pady=(12, 2), padx=12)
    frame2 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame2.pack(pady=(2, 12), padx=12)

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: supression(account_id))
    choix_entry = ctk.CTkEntry(frame1, placeholder_text="ID de la compétition", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    choix_entry.pack(expand=True, fill="both")
    
    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))

    if periode_séléctionner_performance_competition == "Compétition passée":
        parametre_requete_sql = "account_id = ? ORDER BY date ASC"
        parametre_requete_sql_valeurs = (account_id,)
    else:
        parametre_requete_sql = "account_id = ? AND date >= ? ORDER BY date ASC"
        parametre_requete_sql_valeurs = (account_id, date_actuelle)
    try:
        curseur.execute(f"SELECT id, nom, date, sport, lieu, priorité FROM Compétition WHERE {parametre_requete_sql}", parametre_requete_sql_valeurs)
        result = curseur.fetchall()
        headers = ["ID", "Nom", "Date", "Sport", "Lieu", "Priorité"]
        for col_idx, header_text in enumerate(headers):
            label = ctk.CTkButton(tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                    fg_color=couleur_fond, corner_radius=corner2, text_color=couleur1,
                                    height=40, border_width=border2, border_color=couleur2, hover_color=couleur_fond)
            label.grid(row=0, column=col_idx, padx=5, pady=15, sticky="ew")
            tableau_frame.grid_columnconfigure(col_idx, weight=1)
        if result:
            for row_idx, activite in enumerate(result):
                for col_idx, data in enumerate(activite):
                    if col_idx == 2:
                        date = datetime.strptime(str(data), '%Y-%m-%d')
                        data = date.strftime('%d-%m-%Y')
                    label = ctk.CTkLabel(tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=140)
                    label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=15, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=(font_principale, taille1), text_color=couleur_text)
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def supression(account_id):
            choix = choix_entry.get().strip()
            if not choix:
                messagebox.showerror("Champs vide", "Le champs 'ID de la compétition' est obligatoire, il ne peut pas être vide.")
                return
            try:
                choix_id_saisi = int(choix)
                if choix_id_saisi < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erreur de conversion", "L'ID de la compétition doit être un nombre entier positif.")
                return
            ids_competitions_disponibles = [comp[0] for comp in result]
            try:
                if choix_id_saisi in ids_competitions_disponibles:
                    competition_id_db = choix_id_saisi
                    curseur.execute("DELETE FROM Compétition WHERE id = ? AND account_id = ?", (competition_id_db, account_id))
                    con.commit()
                    messagebox.showinfo("Suppression réussie", "Compétition supprimée avec succès.")
                    vider_fenetre(app)
                    compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
                else:
                    messagebox.showerror("Erreur", "L'ID de la compétition saisie n'existe pas ou n'appartient pas à ton compte !")
                    return
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la suppression de la compétition !")
                return
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
                return
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes compétitions !")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
        return
    button_check = ctk.CTkButton(frame2, text="Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: supression(account_id))
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_retour = ctk.CTkButton(frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
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
        priorite_value = premiere_ligne[5]
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de ta compétition !")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
        return

    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(pady=10)
    Titre = ctk.CTkLabel(frame ,text="Modifier une compétition", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=0)

    frame_tout = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(expand=True, fill="both", padx=12, pady=(12, 2))
    frame2 = ctk.CTkFrame(frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(expand=True, fill="both", padx=12, pady=2)
    frame3 = ctk.CTkFrame(frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(expand=True, fill="both", padx=12, pady=2)
    frame4 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame4.pack(expand=True, fill="both", padx=12, pady=(2, 12))

    option = ["Événement Principal", "Événement Secondaire", "Événement tertiaire", "Autre"]
    
    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: sql_ajouté(account_id))

    sport_entry = ctk.CTkEntry(frame1, placeholder_text="Sport", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=320)
    sport_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    sport_entry.insert(0, f"{sport_value if sport_value is not None else "Sport"}")
    frame_pour_date = ctk.CTkFrame(frame1, fg_color=couleur_fond, corner_radius=corner1)
    frame_pour_date.pack(expand=True, fill="both", side="left", padx=(0, 2))
    date_entry = ctk.CTkEntry(frame_pour_date, placeholder_text="Date", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=36, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=160)
    date_entry.pack(expand=True, fill="both", side="left", padx=(12,0), pady=12)
    date_entry.insert(0, f"{date_value if date_value is not None else "Date"}")
    button_pop_up_calendrier = ctk.CTkButton(frame_pour_date, text="📅 Calendrier", width=75, height=36, corner_radius=corner1, fg_color=couleur2,
                                            hover_color=couleur2_hover, font=(font_principale, taille3), text_color=couleur1,
                                            border_color=couleur2, border_width=border1,
                                            command=lambda: pop_up_calendrier(app, date_entry))
    button_pop_up_calendrier.pack(expand=True, fill="both", side="left", padx=(0, 12), pady=12)

    nom_entry = ctk.CTkEntry(frame2, placeholder_text="Nom de la compétition", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    nom_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    nom_entry.insert(0, f"{nom_value if nom_value is not None else "Nom de la compétition"}")
    objectif_entry = ctk.CTkEntry(frame2, placeholder_text="Objectif", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    objectif_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    objectif_entry.insert(0, f"{objectif_value if objectif_value is not None else "Objectif"}")

    lieu_entry = ctk.CTkEntry(frame3, placeholder_text="Lieu (optionnel)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    lieu_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    lieu_entry.insert(0, f"{lieu_value if lieu_value is not None else "Lieu (optionnel)"}")

    priorite_entry = ctk.CTkComboBox(frame3, values=option, height=height_expressive, font=(font_principale, taille2),
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=320, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    priorite_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    priorite_entry.set(f"{priorite_value if priorite_value is not None else 'Priorité'}")

    def sql_ajouté(account_id):
        nom = nom_entry.get().strip()
        date_str = date_entry.get().strip().replace('/', '-').replace('.', '-').replace(',', '-').replace('_', '-').replace(' ', '')
        sport = sport_entry.get().strip()
        objectif = objectif_entry.get().strip()
        lieu = lieu_entry.get().strip()
        priorité = priorite_entry.get().strip()

        if not sport:
            sport = sport_value
        if len(sport) > 50:
            messagebox.showerror("Erreur", "Le nom du sport ne doit pas dépasser 50 caractères !")
            return
        try:
            float(sport)
            messagebox.showerror("Erreur de format", "Le sport doit être une chaîne de caractères, pas un nombre !")
            return
        except ValueError:
            pass

        if not date_str:
            date_str = date_value
        try:
            date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
            date = date_conversion.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur de format de date", "La date doit être au format JJ-MM-AAAA !")
            return

        if not nom:
            nom = nom_value
        if len(nom) > 60:
            messagebox.showerror("Erreur de longueur", "Le nom de la compétition ne peut pas dépasser 60 caractères !")
            return
        if not objectif:
            objectif = objectif_value
        if len(objectif) > 100:
            messagebox.showerror("Erreur de longueur", "L'objectif de la compétition ne peut pas dépasser 100 caractères !")
            return
        if not lieu:
            lieu = lieu_value
        if lieu is not None:
            if len(lieu) > 60:
                messagebox.showerror("Erreur de longueur", "Le lieu de la compétition ne peut pas dépasser 60 caractères !")
                return
            
        if priorité == "Priorité":
            messagebox.showerror("Champs vide", "Le champs 'Priorité' est obligatoire !")
            return
        if not priorité in option:
            messagebox.showerror("Erreur de sélection", "Le champs 'Priorité' doit être une des options proposées !")
            return
        try:
            curseur.execute("UPDATE Compétition SET nom = ?, date = ?, sport = ?, objectif = ?, lieu = ?, priorité = ? WHERE id = ? AND account_id = ?", 
                            (nom, date, sport, objectif, lieu, priorité, id_modifier, account_id))
            con.commit()
            messagebox.showinfo("Enregistré", "Ta compétition a été modifiée avec succès !")
            vider_fenetre(app)
            compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de la compétition !")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
            return
        
    button_enregistrer = ctk.CTkButton(frame4, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                                    command=lambda: sql_ajouté(account_id))
    button_enregistrer.pack(expand=True, fill="both", side="left", padx=2)
    button_back = ctk.CTkButton(frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                           command=lambda: [vider_fenetre(app), modifier_compétition_étape1(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left", padx=2)

def modifier_compétition_étape1(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Modifier une compétition", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    frame_tout = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame1.pack(pady=(12, 2), padx=12)
    frame2 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame2.pack(pady=(2, 12), padx=12)

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: valider(account_id))
    choix_entry = ctk.CTkEntry(frame1, placeholder_text="ID de la compétition", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    choix_entry.pack(expand=True, fill="both")

    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))

    if periode_séléctionner_performance_competition == "Compétition passée":
        parametre_requete_sql = "account_id = ? ORDER BY date ASC"
        parametre_requete_sql_valeurs = (account_id,)
    else:
        parametre_requete_sql = "account_id = ? AND date >= ? ORDER BY date ASC"
        parametre_requete_sql_valeurs = (account_id, date_actuelle)

    try:
        curseur.execute(f"SELECT id, nom, date, sport, lieu, priorité FROM Compétition WHERE {parametre_requete_sql}", parametre_requete_sql_valeurs)
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
                    label = ctk.CTkLabel(tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                         text_color=couleur_text, wraplength=140)
                    label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=15, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(tableau_frame, text="Aucune compétition future n'a été enregistré", font=(font_principale, taille1), text_color=couleur_text)
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def valider(account_id):
            choix = choix_entry.get().strip()
            try:
                if not choix:
                    messagebox.showerror("Erreur", "ID ne peut pas être vide ! Merci de saisir un identifiant !")
                    return
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
                    return
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de la compétition !")
                return
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
                return
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes compétitions !")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, veuillez réessayer !")
        return
    button_check = ctk.CTkButton(frame2, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: valider(account_id))
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_retour = ctk.CTkButton(frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_retour.pack(expand=True, fill="both", side="left")

def compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    boite = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner2)
    boite.pack(side="top", padx=10, pady=(10, 5))
    boite_semi_header = ctk.CTkFrame(boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header.pack(fill="x", side="left", padx=(2, 10), pady=2)
    boite_semi_header2 = ctk.CTkFrame(boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header2.pack(fill="x", side="right", padx=(0, 2), pady=2)

    def maj_pour_tableau(choix):
        choix = combo_periode.get()
        global periode_séléctionner_performance_competition
        periode_séléctionner_performance_competition = choix
        if choix == "Compétition passée":
            parametre_requete_sql = "account_id = ? ORDER BY date ASC"
            parametre_requete_sql_valeurs = (account_id,)
        else:
            parametre_requete_sql = "account_id = ? AND date >= ? ORDER BY date ASC"
            parametre_requete_sql_valeurs = (account_id, date_actuelle)

        for widget in tableau_frame.winfo_children():
            widget.grid_remove()
        try:
            curseur.execute(f"SELECT nom, date, sport, objectif, lieu, priorité FROM Compétition WHERE {parametre_requete_sql}", parametre_requete_sql_valeurs)
            objectif_result = curseur.fetchall()

            headers = ["Nom", "Date", "Sport", "Objectif", "Lieu", "Priorité"]

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
                        label = ctk.CTkLabel(tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                                text_color=couleur_text, wraplength=140)
                        label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=15, sticky="ew")
                button_modifier.pack(side="left", padx=2)
                button_delete.pack(side="left", padx=2)
            else:
                pas_données = ctk.CTkLabel(tableau_frame, text="Aucune compétition future n'a été enregistrée.", font=(font_principale, taille1), text_color=couleur_text)
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes compétitions !")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
            return

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
    mode_activité = ctk.CTkSegmentedButton(boite_semi_header, values=["Charge d'entraînement", "Indulgence de course", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner2, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(expand=True, fill="x", side="right", padx=(2, 0), pady=5)
    mode_activité.set("Compétition")    

    options_periode = ["Compétition future", "Compétition passée"]
    combo_periode = ctk.CTkComboBox(boite_semi_header2, values=options_periode, font=(font_principale, taille2), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=300, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1,
                                    command=maj_pour_tableau)
    combo_periode.pack(expand=True, fill="x", side="right", padx=(2, 5), pady=5)
    combo_periode.set(f"{periode_séléctionner_performance_competition}")

    frame_boutons = ctk.CTkFrame(app, fg_color="transparent")
    frame_boutons.pack(pady=(20, 5))
    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))

    button_ajouter = ctk.CTkButton(frame_boutons, text="➕  Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), text_color=couleur1, border_width=border2,
                           border_color=couleur2,
                           command=lambda: [vider_fenetre(app), ajouter_compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_ajouter.pack(side="left", padx=2)
    button_modifier = ctk.CTkButton(frame_boutons, text="✏️  Modifier", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), text_color=couleur1, border_width=border2,
                           border_color=couleur2,
                           command=lambda: [vider_fenetre(app), modifier_compétition_étape1(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_modifier.pack_forget()
    button_delete = ctk.CTkButton(frame_boutons, text="🗑️  Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), text_color=couleur1, border_width=border2,
                           border_color=couleur2,
                           command=lambda: [vider_fenetre(app), supprimer_compétition(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_delete.pack_forget()

    maj_pour_tableau(periode_séléctionner_performance_competition)

def ajouter_objectif(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(pady=10)
    Titre = ctk.CTkLabel(frame ,text="Ajouter un objectif", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=0)

    frame_tout = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(expand=True, fill="both", padx=12, pady=(12, 2))
    frame2 = ctk.CTkFrame(frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(expand=True, fill="both", padx=12, pady=2)
    frame3 = ctk.CTkFrame(frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(expand=True, fill="both", padx=12, pady=2)
    frame4 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame4.pack(expand=True, fill="both", padx=12, pady=(2, 12))

    options_statut = ["Pas encore démarré", "En cours", "Atteint", "Non-atteint"]
    options_niveau = ["Débutant", "Fondations", "Intermédiaire", "Avancé", "Expert", "Maîtrise"]

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: sql_ajouté(account_id))
    sport_entry = ctk.CTkEntry(frame1, placeholder_text="Sport", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=320)
    sport_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    frame_pour_date = ctk.CTkFrame(frame1, fg_color=couleur_fond, corner_radius=corner1)
    frame_pour_date.pack(expand=True, fill="both", side="left", padx=(0, 2))
    date_entry = ctk.CTkEntry(frame_pour_date, placeholder_text="Date", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=36, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=160)
    date_entry.pack(expand=True, fill="both", side="left", padx=(12,0), pady=12)
    button_pop_up_calendrier = ctk.CTkButton(frame_pour_date, text="📅 Calendrier", width=75, height=36, corner_radius=corner1, fg_color=couleur2,
                                            hover_color=couleur2_hover, font=(font_principale, taille3), text_color=couleur1,
                                            border_color=couleur2, border_width=border1,
                                            command=lambda: pop_up_calendrier(app, date_entry))
    button_pop_up_calendrier.pack(expand=True, fill="both", side="left", padx=(0, 12), pady=12)

    objectif_entry = ctk.CTkEntry(frame2, placeholder_text="Objectif", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    objectif_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    fréquence_entry = ctk.CTkEntry(frame2, placeholder_text="Fréquence d'entraî.", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=320)
    fréquence_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    niveau_entry = ctk.CTkComboBox(frame3, values=options_niveau, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=320, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    niveau_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    niveau_entry.set("Niveau actuel")
    statut_entry = ctk.CTkComboBox(frame3, values=options_statut, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=320, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    statut_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    statut_entry.set("Statut de l'objectif")

    def sql_ajouté(account_id):
        sport = sport_entry.get().strip()
        date_str = date_entry.get().strip().replace('/', '-').replace('.', '-').replace(',', '-').replace('_', '-').replace(' ', '')
        objectif = objectif_entry.get().strip()
        fréquence = fréquence_entry.get().strip()
        niveau = niveau_entry.get().strip()
        statut = statut_entry.get().strip()

        if not sport:
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Sport' !")
            return
        if len(sport) > 50:
            messagebox.showerror("Erreur", "Le nom du sport ne doit pas dépasser 50 caractères !")
            return
        try:
            float(sport)
            messagebox.showerror("Erreur de format", "Le sport doit être une chaîne de caractères, pas un nombre !")
            return
        except ValueError:
            pass
        if not date_str:
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Date' !")
            return
        try:
            date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
            date = date_conversion.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "La date doit être au format JJ-MM-AAAA !")
            return
        if not objectif:
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Objectif' !")
            return
        if len(objectif) > 100:
            messagebox.showerror("Erreur", "L'objectif ne doit pas dépasser 100 caractères !")
            return
        if not fréquence:
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Fréquence' !")
            return
        if len(fréquence) > 50:
            messagebox.showerror("Erreur", "La fréquence ne doit pas dépasser 50 caractères !")
            return

        if niveau == "Niveau actuel":
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Niveau actuel' !")
            return
        if not niveau in options_niveau:
            messagebox.showerror("Erreur", "Merci de choisir un niveau valide dans la liste déroulante !")
            return
        if statut == "Statut de l'objectif":
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Statut de l'objectif' !")
            return
        if not statut in options_statut:
            messagebox.showerror("Erreur", "Merci de choisir un statut valide dans la liste déroulante !")
            return
        
        try:
            curseur.execute("INSERT INTO Objectif (account_id, sport, date, objectif, fréquence, niveau_début, statut) VALUES (?, ?, ?, ?, ?, ?, ?)", (account_id, sport, date, objectif, fréquence, niveau, statut))
            con.commit()
            messagebox.showinfo("Enregistré", "Ton objectif a été enregistré, bonne chance !")
            vider_fenetre(app)
            objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton objectif !")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
            return
        
    button_enregistrer = ctk.CTkButton(frame4, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                                        command=lambda: sql_ajouté(account_id))
    button_enregistrer.pack(expand=True, fill="both", side="left", padx=2)
    button_back = ctk.CTkButton(frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                           command=lambda: [vider_fenetre(app), objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left", padx=2)

def modifier_objectif_étape2(account_id, result_id, app,sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):    
    id_modifier = result_id[0][0]
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)
    try:
        curseur.execute("SELECT date, objectif, fréquence, sport, statut FROM Objectif WHERE id = ? AND account_id = ?",(id_modifier, account_id))
        data_objectif = curseur.fetchall()
        premiere_ligne = data_objectif[0]
        date1 = premiere_ligne[0]
        date_conversion = datetime.strptime(date1, "%Y-%m-%d")
        date_value = date_conversion.strftime("%d-%m-%Y")

        objectif_value = premiere_ligne[1]
        frequence_value = premiere_ligne[2]
        sport_value = premiere_ligne[3]
        statut_value = premiere_ligne[4]
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de ton objectif !")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
        return

    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(pady=10)
    Titre = ctk.CTkLabel(frame ,text="Modifier un objectif", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=0)

    frame_tout = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(expand=True, fill="both", padx=12, pady=(12, 2))
    frame2 = ctk.CTkFrame(frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(expand=True, fill="both", padx=12, pady=2)
    frame3 = ctk.CTkFrame(frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(expand=True, fill="both", padx=12, pady=2)
    frame4 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame4.pack(expand=True, fill="both", padx=12, pady=(2, 12))

    options_statut = ["Pas encore démarré", "En cours", "Atteint", "Non-atteint"]
    options_niveau = ["Débutant", "Fondations", "Intermédiaire", "Avancé", "Expert", "Maîtrise"]

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: sql_ajouté(account_id))
    sport_entry = ctk.CTkEntry(frame1, placeholder_text="Sport", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=320)
    sport_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    sport_entry.insert(0, f"{sport_value if sport_value is not None else "Sport"}")
    frame_pour_date = ctk.CTkFrame(frame1, fg_color=couleur_fond, corner_radius=corner1)
    frame_pour_date.pack(expand=True, fill="both", side="left", padx=(0, 2))
    date_entry = ctk.CTkEntry(frame_pour_date, placeholder_text="Date", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=36, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=160)
    date_entry.pack(expand=True, fill="both", side="left", padx=(12,0), pady=12)
    date_entry.insert(0, f"{date_value if date_value is not None else "Date"}")
    button_pop_up_calendrier = ctk.CTkButton(frame_pour_date, text="📅 Calendrier", width=75, height=36, corner_radius=corner1, fg_color=couleur2,
                                            hover_color=couleur2_hover, font=(font_principale, taille3), text_color=couleur1,
                                            border_color=couleur2, border_width=border1,
                                            command=lambda: pop_up_calendrier(app, date_entry))
    button_pop_up_calendrier.pack(expand=True, fill="both", side="left", padx=(0, 12), pady=12)

    objectif_entry = ctk.CTkEntry(frame2, placeholder_text="Objectif", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    objectif_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    objectif_entry.insert(0, f"{objectif_value if objectif_value is not None else "Objectif"}")
    fréquence_entry = ctk.CTkEntry(frame2, placeholder_text="Fréquence d'entraî.", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=320)
    fréquence_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    fréquence_entry.insert(0, f"{frequence_value if frequence_value is not None else "Fréquence d'entraî."}")

    niveau_entry = ctk.CTkComboBox(frame3, values=options_niveau, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=320, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    niveau_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    niveau_entry.set("Level final")
    statut_entry = ctk.CTkComboBox(frame3, values=options_statut, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=320, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    statut_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    statut_entry.set(f"{statut_value if statut_value is not None else "Statut de l'objectif"}")

    def sql_ajouté(account_id):
        sport = sport_entry.get().strip()
        date_str = date_entry.get().strip().replace('/', '-').replace('.', '-').replace(',', '-').replace('_', '-').replace(' ', '')
        objectif = objectif_entry.get().strip()
        fréquence = fréquence_entry.get().strip()
        niveau = niveau_entry.get().strip()
        statut = statut_entry.get().strip()

        if not sport:
            sport = sport_value
        if len(sport) > 50:
            messagebox.showerror("Erreur", "Le nom du sport ne doit pas dépasser 50 caractères !")
            return
        try:
            float(sport)
            messagebox.showerror("Erreur de format", "Le sport doit être une chaîne de caractères, pas un nombre !")
            return
        except ValueError:
            pass
        if not date_str:
            date_str = date_value
        try:
            date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
            date = date_conversion.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "La date doit être au format JJ-MM-AAAA !")
            return
        if not objectif:
            objectif = objectif_value
        if len(objectif) > 100:
            messagebox.showerror("Erreur", "L'objectif ne doit pas dépasser 100 caractères !")
            return
        if not fréquence:
            fréquence = frequence_value
        if len(fréquence) > 50:
            messagebox.showerror("Erreur", "La fréquence ne doit pas dépasser 50 caractères !")
            return

        if niveau == "Niveau actuel":
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Niveau actuel' !")
            return
        if not niveau in options_niveau:
            messagebox.showerror("Erreur", "Merci de choisir un niveau valide dans la liste déroulante !")
            return
        if statut == "Statut de l'objectif":
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Statut de l'objectif' !")
            return
        if not statut in options_statut:
            messagebox.showerror("Erreur", "Merci de choisir un statut valide dans la liste déroulante !")
            return
        
        try:
            curseur.execute("UPDATE Objectif SET sport = ?, date = ?, objectif = ?, fréquence = ?, niveau_fin = ?, statut = ? WHERE id = ? AND account_id = ?",
                    (sport, date, objectif, fréquence, niveau, statut, id_modifier, account_id))
            con.commit()
            messagebox.showinfo("Enregistré", "Ton objectif a été modifié avec succès!")
            vider_fenetre(app)
            objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de ton objectif !")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
            return
        
    button_enregistrer = ctk.CTkButton(frame4, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                                        command=lambda: sql_ajouté(account_id))
    button_enregistrer.pack(expand=True, fill="both", side="left", padx=2)
    button_back = ctk.CTkButton(frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), width=320,
                           command=lambda: [vider_fenetre(app), modifier_objectif_étape1(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left", padx=2)

def modifier_objectif_étape1(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Modifier un objectif", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    frame_tout = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame1.pack(pady=(12, 2), padx=12)
    frame2 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame2.pack(pady=(2, 12), padx=12)

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: valider(account_id))
    choix_entry = ctk.CTkEntry(frame1, placeholder_text="ID de l'objectif", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    choix_entry.pack(expand=True, fill="both")

    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
    
    if periode_séléctionner_performance_objectif == "Objectif passé":
        parametre_requete_sql = "account_id = ? ORDER BY date ASC"
        parametre_requete_sql_valeurs = (account_id,)
    else:
        parametre_requete_sql = "account_id = ? AND date >= ? ORDER BY date ASC"
        parametre_requete_sql_valeurs = (account_id, date_actuelle)
    try:
        curseur.execute(f"SELECT id, sport, date, niveau_début, niveau_fin, statut FROM Objectif WHERE {parametre_requete_sql}", parametre_requete_sql_valeurs)
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
                        label = ctk.CTkLabel(tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=140)
                        label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=15, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(tableau_frame, text="Aucun objectif futur n'a été enregistré", font=(font_principale, taille1), text_color=couleur_text)
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes objectifs !")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, veuillez réessayer !")
        return

    def valider(account_id):
        choix = choix_entry.get().strip()
        try:
            if not choix:
                messagebox.showerror("Erreur", "ID ne peut pas être vide ! Merci de saisir un identifiant !")
                return
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
                return
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de l'objectif !")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
            return
    button_check = ctk.CTkButton(frame2, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: valider(account_id))
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_retour = ctk.CTkButton(frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_retour.pack(expand=True, fill="both", side="left")

def supprimer_objectif(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Supprimer un objectif", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    frame_tout = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame1.pack(pady=(12, 2), padx=12)
    frame2 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame2.pack(pady=(2, 12), padx=12)

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: supression(account_id))
    choix_entry = ctk.CTkEntry(frame1, placeholder_text="ID de l'objectif", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    choix_entry.pack(expand=True, fill="both")

    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))

    if periode_séléctionner_performance_objectif == "Objectif passé":
        parametre_requete_sql = "account_id = ? ORDER BY date ASC"
        parametre_requete_sql_valeurs = (account_id,)
    else:
        parametre_requete_sql = "account_id = ? AND date >= ? ORDER BY date ASC"
        parametre_requete_sql_valeurs = (account_id, date_actuelle)
    try:
        curseur.execute(f"SELECT id, sport, date, niveau_début, niveau_fin, statut FROM Objectif WHERE {parametre_requete_sql}", parametre_requete_sql_valeurs)
        result = curseur.fetchall()
        headers = ["ID", "Sport", "Date", "Level début", "Level fin", "Statut"]
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
                    label = ctk.CTkLabel(tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                    label.grid(row=row_idx + 1, column=col_idx, padx=6, pady=15, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=(font_principale, taille1), text_color=couleur_text)
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def supression(account_id):
            choix = choix_entry.get().strip()
            if not choix:
                messagebox.showerror("Champs vide", "Le champs 'ID de l'objectif' est obligatoire, il ne peut pas être vide.")
                return
            try:
                choix_id_saisi = int(choix)
                if choix_id_saisi < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erreur de conversion", "L'ID de l'objectif doit être un nombre entier positif.")
                return
            ids_objectifs_disponibles = [obj[0] for obj in result]
            try:
                if choix_id_saisi in ids_objectifs_disponibles:
                    objectif_id_db = choix_id_saisi
                    curseur.execute("DELETE FROM Objectif WHERE id = ? AND account_id = ?", (objectif_id_db, account_id))
                    con.commit()
                    messagebox.showinfo("Suppression réussie", "Objectif supprimé avec succès.")
                    vider_fenetre(app)
                    objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
                else:
                    messagebox.showerror("Erreur", "L'ID de l'objectif saisi n'existe pas ou n'appartient pas à ton compte !")
                    return
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la suppression de l'objectif !")
                return
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
                return
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes objectifs !")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
        return
    button_check = ctk.CTkButton(frame2, text="Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: supression(account_id))
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_retour = ctk.CTkButton(frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: [vider_fenetre(app), objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_retour.pack(expand=True, fill="both", side="left")

def objectifs(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    global periode_séléctionner_performance_objectif

    boite = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner2)
    boite.pack(side="top", padx=10, pady=(10, 5))
    boite_semi_header = ctk.CTkFrame(boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header.pack(fill="x", side="left", padx=(2, 10), pady=2)
    boite_semi_header2 = ctk.CTkFrame(boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header2.pack(fill="x", side="right", padx=(0, 2), pady=2)

    def maj_pour_tableau(choix):
        choix = combo_periode.get()
        global periode_séléctionner_performance_objectif
        periode_séléctionner_performance_objectif = choix
        if choix == "Objectif passé":
            parametre_requete_sql = "account_id = ? ORDER BY date ASC"
            parametre_requete_sql_valeurs = (account_id,)
        else:
            parametre_requete_sql = "account_id = ? AND date >= ? ORDER BY date ASC"
            parametre_requete_sql_valeurs = (account_id, date_actuelle)

        for widget in tableau_frame.winfo_children():
            widget.grid_remove()
        try:
            curseur.execute(f"SELECT sport, date, objectif, fréquence, niveau_début, niveau_fin, statut FROM Objectif WHERE {parametre_requete_sql}", parametre_requete_sql_valeurs)
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
                        label = ctk.CTkLabel(tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                                text_color=couleur_text, wraplength=140)
                        label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=15, sticky="ew")
                button_modifier.pack(side="left", padx=2)
                button_delete.pack(side="left", padx=2)
            else:
                pas_données = ctk.CTkLabel(tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=(font_principale, taille1), text_color=couleur_text)
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes objectifs !")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
            return
            
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
    mode_activité = ctk.CTkSegmentedButton(boite_semi_header, values=["Charge d'entraînement", "Indulgence de course", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner2, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(expand=True, fill="x", side="right", padx=(2, 0), pady=5)
    mode_activité.set("Objectif")

    options_periode = ["Objectif futur", "Objectif passé"]
    combo_periode = ctk.CTkComboBox(boite_semi_header2, values=options_periode, font=(font_principale, taille2), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=300, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1,
                                    command=maj_pour_tableau)
    combo_periode.pack(expand=True, fill="x", side="right", padx=(2, 5), pady=5)
    combo_periode.set(f"{periode_séléctionner_performance_objectif}")

    frame_boutons = ctk.CTkFrame(app, fg_color="transparent")
    frame_boutons.pack(pady=(20, 5))
    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))

    button_ajouter = ctk.CTkButton(frame_boutons, text="➕  Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, border_width=border2,
                           border_color=couleur2,
                           command=lambda: [vider_fenetre(app), ajouter_objectif(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_ajouter.pack(side="left", padx=2)

    def recup_result_combo():
        result_combo = combo_periode.get()
        vider_fenetre(app)
        modifier_objectif_étape1(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)  

    button_modifier = ctk.CTkButton(frame_boutons, text="✏️  Modifier", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, border_width=border2,
                           border_color=couleur2,
                           command=recup_result_combo)
    button_modifier.pack_forget()
    button_delete = ctk.CTkButton(frame_boutons, text="🗑️ Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, border_width=border2,
                           border_color=couleur2,
                           command=lambda: [vider_fenetre(app), supprimer_objectif(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_delete.pack_forget()
    maj_pour_tableau(f"{periode_séléctionner_performance_objectif}")

def mettre_en_pause_les_analyses(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre, mode):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Mettre en pause les analyses", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    info = ctk.CTkLabel(app ,text="Si tu as besoin de souffler, ou que tu t'es blessé, tu peux\nmettre en pause les " \
    "analyses pour te reposer et récupérer.", font=(font_principale, taille2), text_color=couleur_text)
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
        info_statut_actif = ctk.CTkLabel(frame, text=f"Ton statut d'entraînement actuel: Vacances", font=(font_principale, taille2), text_color=couleur_text)
        info_statut_actif.pack(padx=0, pady=10)
    elif result == "blessure":
        info_statut_actif = ctk.CTkLabel(frame, text=f"Ton statut d'entraînement actuel : Blessure", font=(font_principale, taille2), text_color=couleur_text)
        info_statut_actif.pack(padx=0, pady=10)
    elif result == "suspendre":
        info_statut_actif = ctk.CTkLabel(frame, text=f"Ton statut d'entraînement actuel : Suspendre", font=(font_principale, taille2), text_color=couleur_text)
        info_statut_actif.pack(padx=0, pady=10)
    else:
        info_statut = ctk.CTkLabel(frame, text="Ton statut d'entraînement actuel : Actif", font=(font_principale, taille2), text_color=couleur_text)
        info_statut.pack(padx=0, pady=10)

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: enregistrer_activité(account_id))
    options = ["Suspendre", "Vacances", "Blessure", "Reprendre les analyses"]
    combo_statut = ctk.CTkComboBox(frame1, values=options, font=(font_principale, taille2), height=height_expressive, 
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
            elif statut == "Blessure":
                activer_pause(account_id, "blessure")
            elif statut == "Suspendre":
                activer_pause(account_id, "suspendre")
            elif statut == "Reprendre les analyses":
                arreter_pause(account_id)
            else:
                messagebox.showerror("Erreur", "Le champ 'Raison' ne peut pas être vide ! Merci de choisir une raison !")
                return
            
            vider_fenetre(app)
            if mode == "indulgence":
                indulgence_de_course(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)
            else:
                charge_entraînement(account_id)
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
            return
    button_check = ctk.CTkButton(frame2, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: enregistrer_activité(account_id))
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    if mode == "indulgence":
        button_retour = ctk.CTkButton(frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                        corner_radius=corner1, height=button_height, text_color=couleur1,
                                        font=(font_principale, taille3),
                                        command=lambda: [vider_fenetre(app), indulgence_de_course(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre)])
        button_retour.pack(expand=True, fill="both", side="left", padx=0)
    else:
        button_retour = ctk.CTkButton(frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                        corner_radius=corner1, height=button_height, text_color=couleur1,
                                        font=(font_principale, taille3),
                                        command=lambda: [vider_fenetre(app), charge_entraînement(account_id)])
        button_retour.pack(expand=True, fill="both", side="left", padx=0)

def indulgence_de_course(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    boite = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner2)
    boite.pack(side="top", padx=10, pady=(10, 5))
    boite_semi_header = ctk.CTkFrame(boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header.pack(fill="x", side="left", padx=(2, 10), pady=2)
    boite_semi_header2 = ctk.CTkFrame(boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header2.pack(fill="x", side="right", padx=(0, 2), pady=2)

    try:
        curseur.execute("SELECT nom_du_coach, avatar FROM Coach WHERE account_id = ?", (account_id,))
        ton_coach = curseur.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Une erreur est survenue lors de la récupération des informations du coach.")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur innatendue s'est produite !")
        return
    if ton_coach:
        nom_du_coach = ton_coach[0]
        avatar_du_coach = ton_coach[1]
    else:
        nom_du_coach = None
        avatar_du_coach = None

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
    mode_activité = ctk.CTkSegmentedButton(boite_semi_header, values=["Charge d'entraînement", "Indulgence de course", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner2, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(expand=True, fill="x", side="right", padx=(2, 0), pady=5)
    mode_activité.set("Indulgence de course")
    button_autre = ctk.CTkButton(boite_semi_header2, text="⏸️ Mettre en pause les analyses", fg_color=couleur2, hover_color=couleur2_hover,
                                    font=(font_principale, taille3), text_color=couleur1, height=button_height, corner_radius=corner1,
                                    width=200,
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

    boite_haut = ctk.CTkFrame(app, fg_color="transparent")
    boite_haut.pack(side="top", padx=10, pady=(20, 5))
    boite_bas = ctk.CTkFrame(app, fg_color="transparent")
    boite_bas.pack(side="top", padx=10, pady=(5, 10))

    frame_distance_7_jours = ctk.CTkFrame(boite_haut, fg_color="transparent", corner_radius=corner1, border_width=border1, border_color=couleur2)
    frame_distance_7_jours.pack(side="left", expand=True, fill="both", padx=(0, 5))
    frame_distance_28_jours = ctk.CTkFrame(boite_haut, fg_color="transparent", corner_radius=corner1, border_width=border1, border_color=couleur2)
    frame_distance_28_jours.pack(side="left", expand=True, fill="both", padx=5)
    frame_distance_maximum_hebdo = ctk.CTkFrame(boite_haut, fg_color="transparent", corner_radius=corner1, border_width=border1, border_color=couleur2)
    frame_distance_maximum_hebdo.pack(side="left", expand=True, fill="both", padx=(5, 0))

    frame_jrm_coach = ctk.CTkFrame(boite_bas, fg_color="transparent", corner_radius=corner1, border_width=border1, border_color=couleur1)
    frame_jrm_coach.pack(side="left", expand=True, fill="both", padx=(0, 5))
    frame_info = ctk.CTkFrame(boite_bas, fg_color=couleur2, corner_radius=corner1, border_width=border1, border_color=couleur1)
    frame_info.pack(side="left", expand=True, fill="both", padx=(5, 0))

    distance_7J = ctk.CTkLabel(frame_distance_7_jours, text=f"Distance (7j) :\n{distance_des_derniers_7_jours:.2f} km", font=(font_principale , taille2),
                                    width=300, wraplength=300, text_color=couleur1)
    distance_7J.pack(fill="both", expand=True, padx=12, pady=12)

    distance_moyenne_du_mois = ctk.CTkLabel(frame_distance_28_jours, text=f"Moyenne hebdo. (4 sem.) :\n{distance_moyenne_des_derniers_28_jours:.2f} km/semaine", font=(font_principale, taille2),
                                width=300, wraplength=325, text_color=couleur1)
    distance_moyenne_du_mois.pack(fill="both", expand=True, padx=12, pady=12) 

    info_nom_coach = ctk.CTkLabel(frame_jrm_coach, text=f"{avatar_du_coach if avatar_du_coach is not None else "👨"} {nom_du_coach if nom_du_coach else "JRM Coach"}",
                                  font=(font_secondaire, taille2), wraplength=280, text_color=couleur1,
                                  justify="left")
    info_nom_coach.pack(fill="both", expand=True, pady=(12, 25), padx=12)

    pause = verifier_pause(account_id)
    
    if pause == "blessure":
        Distance_maximal_conseillé = ctk.CTkLabel(frame_distance_maximum_hebdo, text="Distance hebdo. conseillée :\nactuellement en pause",
                                            width=300, wraplength=325, text_color=couleur1, font=(font_secondaire, taille2))
        Distance_maximal_conseillé.pack(fill="both", expand=True, padx=12, pady=12)
        interpretation_jrm_coach = ctk.CTkLabel(frame_jrm_coach, 
                            text="⛑️ Mode blessure\n\n" \
                            "Tes analyses sont en pause le temps de ta récupération. L’important maintenant, c’est de bien te soigner et de suivre les conseils médicaux. Sprintia sera là pour t’aider à reprendre en sécurité quand tu seras rétabli.",
                                    font=(font_principale, taille2), width=325, wraplength=385, text_color=couleur1, justify="left")
        interpretation_jrm_coach.pack(fill="both", expand=True, padx=12, pady=12)    
    elif pause == "vacances":
        Distance_maximal_conseillé = ctk.CTkLabel(frame_distance_maximum_hebdo, text="Distance hebdo. conseillée :\nactuellement en pause",
                                            width=300, wraplength=325, text_color=couleur1, font=(font_secondaire, taille2))
        Distance_maximal_conseillé.pack(fill="both", expand=True, padx=12, pady=12)
        interpretation_jrm_coach = ctk.CTkLabel(frame_jrm_coach, 
                            text="🏖️ Mode vacances\n\n" \
                            "En mode vacances, tes analyses sont suspendues. Parfait pour souffler et déconnecter ! À ton retour, Sprintia t’accompagnera pour une reprise en douceur. Bonnes vacances et bon repos !",
                                    font=(font_principale, taille2), width=325, wraplength=385, text_color=couleur1, justify="left")
        interpretation_jrm_coach.pack(fill="both", expand=True, padx=12, pady=12)  
    elif pause == "suspendre":
        Distance_maximal_conseillé = ctk.CTkLabel(frame_distance_maximum_hebdo, text="Distance hebdo. conseillée :\nactuellement en pause", font=(font_secondaire, taille2),
                                            width=300, wraplength=325, text_color=couleur1)
        Distance_maximal_conseillé.pack(fill="both", expand=True, padx=12, pady=12)
        interpretation_jrm_coach = ctk.CTkLabel(frame_jrm_coach, 
                            text="💤 Mode suspension activé\n\n" \
                            "Tu as mis tes analyses en pause. Parfait pour faire une coupure sans pression ! Quand tu seras prêt à reprendre, Sprintia sera là pour t’aider à repartir sur de bonnes bases.",
                                    font=(font_principale, taille2), width=325, wraplength=385, text_color=couleur1, justify="left")
        interpretation_jrm_coach.pack(fill="both", expand=True, padx=12, pady=12)    
    else:
        if distance_moyenne_des_derniers_28_jours == 0:
            Distance_maximal_conseillé = ctk.CTkLabel(frame_distance_maximum_hebdo, text="Distance hebdo. conseillée :\nDonnées insuffisantes", font=(font_secondaire, taille2),
                                            width=300, wraplength=325, text_color=couleur1)
            Distance_maximal_conseillé.pack(fill="both", expand=True, padx=12, pady=12)

            interpretation_jrm_coach = ctk.CTkLabel(frame_jrm_coach, 
                                text="🚫 Données insuffisantes\n\n" \
                                "Sprintia n’a pas encore assez de données pour analyser ton indulgence de course. Pas de panique : après quelques sorties enregistrées, tu auras des conseils pour progresser en toute sécurité.",
                                    font=(font_principale, taille2), width=325, wraplength=385, text_color=couleur1, justify="left")
            interpretation_jrm_coach.pack(fill="both", expand=True, padx=12, pady=12) 
        else:
            Distance_maximal_conseillé = ctk.CTkLabel(frame_distance_maximum_hebdo, text=f"Distance hebdo. conseillée :\n{distance_maximumconseillé_début:.1f} - {distance_maximumconseillé_fin:.1f} km", font=(font_secondaire, taille2),
                                            width=300, wraplength=325, text_color=couleur1)
            Distance_maximal_conseillé.pack(fill="both", expand=True, padx=12, pady=12)

            if distance_moyenne_des_derniers_28_jours < distance_des_derniers_7_jours < distance_maximumconseillé_fin:
                interpretation_jrm_coach = ctk.CTkLabel(frame_jrm_coach, 
                                    text="🚀 Zone optimale pour progresser\n\n" \
                                    "Bravo, tu es dans la zone idéale pour t’améliorer sans te mettre en danger ! Ton kilométrage est bien dosé : continue comme ça pour booster tes performances en douceur. Pense à varier les plaisirs (allure, dénivelé, etc.) pour maximiser tes progrès.",
                                    font=(font_principale, taille2), width=325, wraplength=385, text_color=couleur1, justify="left")
                interpretation_jrm_coach.pack(fill="both", expand=True, padx=12, pady=12)  

            elif distance_des_derniers_7_jours > distance_maximumconseillé_fin:
                interpretation_jrm_coach = ctk.CTkLabel(frame_jrm_coach, 
                                    text="🤕 Zone optimale pour se blesser\n\n" \
                                    "Attention, ton kilométrage est trop élevé par rapport à tes habitudes ! À ce rythme, le risque de blessure augmente sérieusement. Prends du recul : réduis ton volume ou alterne avec des séances plus légères pour éviter la surcharge.",
                                    font=(font_principale, taille2), width=325, wraplength=385, text_color=couleur1, justify="left")
                interpretation_jrm_coach.pack(fill="both", expand=True, padx=12, pady=12)    

            elif distance_des_derniers_7_jours == distance_moyenne_des_derniers_28_jours:
                interpretation_jrm_coach = ctk.CTkLabel(frame_jrm_coach, text="😴 Zone optimale pour stagner\n\n" \
                                    "Ton kilométrage actuel te permet de maintenir ton niveau sans risque, mais sans réelle progression. C’est idéal pour une phase de transition ou de récupération. Si tu veux relancer ta progression, augmente légèrement ton volume d'entraînement.",
                                    font=(font_principale, taille2), width=325, wraplength=385, text_color=couleur1, justify="left")
                interpretation_jrm_coach.pack(fill="both", expand=True, padx=12, pady=12)  
            else:
                interpretation_jrm_coach = ctk.CTkLabel(frame_jrm_coach, 
                                    text="⏬ Zone optimale pour perdre du niveau\n\n" \
                                    "Ton kilométrage est en dessous de tes habitudes ces derniers jours. Si c’est un choix, profite-en pour te reposer ou travailler d’autres aspects (renforcement, technique). Sinon, augmente doucement pour éviter une baisse de forme trop marquée.",
                                    font=(font_principale, taille2), width=325, wraplength=385, text_color=couleur1, justify="left")
                interpretation_jrm_coach.pack(fill="both", expand=True, padx=12, pady=12)     

    titre_c_quoi = ctk.CTkLabel(frame_info, text="C'est quoi l'indulgence de course ?", font=(font_secondaire, taille2), wraplength=600,
                                text_color=couleur1, justify="left")
    titre_c_quoi.pack(fill="both", expand=True, pady=12, padx=12)
    c_quoi = ctk.CTkLabel(frame_info, 
                          text="L’indulgence de course t’aide à ajuster ton kilométrage des 7 derniers jours pour rester dans une progression optimale, sans dépasser ta limite.\n\nTu peux ainsi continuer à t’améliorer tout en réduisant les risques de blessure. Cette analyse est un guide, mais n’oublie jamais d’écouter les signaux de ton corps.",
                            font=(font_principale, taille2), text_color=couleur1,  wraplength=600, justify="left")
    c_quoi.pack(fill="both", expand=True, padx=12, pady=(25, 12))

def aide_ajout_activité():
    messagebox.showinfo("Aide", "Pour ajouter un entraînement, rends-toi dans l'onglet 'Entraînement' (dans la barre latérale à gauche) puis appuis sur le bouton 'Ajouter'.")
    return

def charge_d_entraînement(account_id, app, sidebar_performance, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    boite = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner2)
    boite.pack(side="top", padx=10, pady=(10, 5))
    boite_semi_header = ctk.CTkFrame(boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header.pack(fill="x", side="left", padx=(2, 10), pady=2)
    boite_semi_header2 = ctk.CTkFrame(boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header2.pack(fill="x", side="right", padx=(0, 2), pady=2)

    try:
        curseur.execute("SELECT nom_du_coach, avatar FROM Coach WHERE account_id = ?", (account_id,))
        ton_coach = curseur.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Une erreur est survenue lors de la récupération des informations du coach.")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur innatendue s'est produite !")
        return
    if ton_coach:
        nom_du_coach = ton_coach[0]
        avatar_du_coach = ton_coach[1]
    else:
        nom_du_coach = None
        avatar_du_coach = None

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
    mode_activité = ctk.CTkSegmentedButton(boite_semi_header, values=["Charge d'entraînement", "Indulgence de course", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner2, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(expand=True, fill="x", side="right", padx=(2, 0), pady=5)
    mode_activité.set("Charge d'entraînement")
    button_autre = ctk.CTkButton(boite_semi_header2, text="⏸️ Mettre en pause les analyses", fg_color=couleur2, hover_color=couleur2_hover,
                                    font=(font_principale, taille3), text_color=couleur1, height=button_height, corner_radius=corner1,
                                    width=200,
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
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
        return

    parent_frame = ctk.CTkFrame(app, fg_color="transparent")
    parent_frame.pack(pady=10)

    boite_charge_entraînement = ctk.CTkFrame(parent_frame, corner_radius=corner1, fg_color="transparent")
    boite_charge_entraînement.pack(fill="both", expand=True, side="left", padx=(10, 2), pady=(0, 10))

    boite_analyse = ctk.CTkFrame(boite_charge_entraînement, corner_radius=corner1, fg_color="transparent")
    boite_analyse.pack(fill="both", expand=True)

    aigue = ctk.CTkFrame(boite_analyse, corner_radius=corner1, fg_color=couleur_fond, border_color=couleur2, border_width=border2)
    aigue.pack(fill="both", expand=True, pady=(0, 5))
    chronique = ctk.CTkFrame(boite_analyse, corner_radius=corner1, fg_color=couleur_fond, border_color=couleur2, border_width=border2)
    chronique.pack(fill="both", expand=True, pady=5)
    h1_result_optimale = ctk.CTkFrame(boite_analyse, corner_radius=corner1, fg_color=couleur_fond, border_color=couleur2, border_width=border2)
    h1_result_optimale.pack(fill="both", expand=True, pady=5)
    interprétation_conseil = ctk.CTkFrame(boite_analyse, corner_radius=corner1, fg_color=couleur_fond, border_color=couleur1, border_width=border2)
    interprétation_conseil.pack(fill="both", expand=True, pady=(5,0))
    
    boite = ctk.CTkFrame(parent_frame, corner_radius=corner1, fg_color="transparent")
    boite.pack(side="right", padx=10, pady=(2, 10))
    graphique = ctk.CTkFrame(boite, corner_radius=corner1, fg_color=couleur2, border_color=couleur1, border_width=border2)
    graphique.pack(fill="both", pady=(0, 5))
    info = ctk.CTkFrame(boite, corner_radius=corner1, fg_color=couleur2, border_color=couleur1, border_width=border2)
    info.pack(fill="both", expand=True, side="left", pady=(5, 0))

    result_analyse = ctk.CTkLabel(aigue, text=f"Charge (7 jours) : {charge_aigue:.1f}", font=(font_principale , taille2),
                                    width=300, wraplength=280, text_color=couleur1)
    result_analyse.pack(fill="both", expand=True, padx=12, pady=12)
    result_analyse = ctk.CTkLabel(chronique, text=f"Charge chronique : {charge_chronique:.1f}", font=(font_principale , taille2),
                                    width=300, wraplength=280, text_color=couleur1)
    result_analyse.pack(fill="both", expand=True, padx=12, pady=12)
    info_nom_coach = ctk.CTkLabel(interprétation_conseil, text=f"{avatar_du_coach if avatar_du_coach is not None else "👨"} {nom_du_coach if nom_du_coach else "JRM Coach"}",
                                  font=(font_secondaire, taille2), wraplength=280, text_color=couleur1,
                                  justify="left")
    info_nom_coach.pack(fill="both", expand=True, pady=(12, 0), padx=12)

    pause = verifier_pause(account_id)

    if pause == "blessure":
        catégorie_statut = ctk.CTkLabel(h1_result_optimale, text="⛑️ Mode blessure", font=(font_principale, taille2),
                                        width=300, wraplength=280, text_color=couleur1)
        catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)           
        interpretation_statut = ctk.CTkLabel(interprétation_conseil, text="Tu es blessé pour le moment\n\n" \
                                    "Prends vraiment le temps de laisser ton corps se régénérer en profondeur, afin de revenir encore plus fort que jamais.", font=(font_principale, taille2),
                                    width=300, wraplength=280, justify="left", text_color=couleur1)
        interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12)
    elif pause == "vacances":
        catégorie_statut = ctk.CTkLabel(h1_result_optimale, text="🏖️ Mode vacances", font=(font_principale, taille2),
                                        width=300, wraplength=280, text_color=couleur1)
        catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)          
        interpretation_statut = ctk.CTkLabel(interprétation_conseil, text="Tu es actuellement en vacances.\n\n" \
        "Profite de cette pause pour te ressourcer, apprécier les moments de détente et les repas, et reviens encore plus motivé !", font=(font_principale, taille2),
                                    width=300, wraplength=280, justify="left", text_color=couleur1)
        interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12)  
    elif pause == "suspendre":
        catégorie_statut = ctk.CTkLabel(h1_result_optimale, text="💤 Mode suspension activé", font=(font_principale, taille2),
                                        width=300, wraplength=280, text_color=couleur1)
        catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)
        interpretation_statut = ctk.CTkLabel(interprétation_conseil, text="Tes analyses sont temporairement en pause pendant ce mode.\n\n" \
        "Profite-en pour te reposer, on reprend les suivis dès ton retour à l’entraînement !", font=(font_principale, taille2), text_color=couleur1,
                                    width=300, wraplength=280, justify="left")
        interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12)
    else :
        if charge_chronique > 0:
            ratio = charge_aigue / charge_chronique
        else:
            ratio = None
        if ratio is not None:
            if ratio <= 0.9:
                catégorie_statut = ctk.CTkLabel(h1_result_optimale, text="😴 Sous-entraînement", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color=couleur1)
                catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)             
                interpretation_statut = ctk.CTkLabel(interprétation_conseil, text="Tu es entrain de perdre du niveau, attention !\n\n" \
                "Tu pourrais augmenter l'intensité de tes entraînements si tu veux basculer en mode progression optimale et améliorer tes performances.", font=(font_principale, taille2),
                                                width=300, wraplength=280, justify="left", text_color=couleur1)
                interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12) 
            elif 0.9 <= ratio <= 1.3:
                catégorie_statut = ctk.CTkLabel(h1_result_optimale, text="🟢 Progression optimale", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color=couleur1)
                catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)             
                interpretation_statut = ctk.CTkLabel(interprétation_conseil, text="Charge idéale pour améliorer tes performances\n\n" \
                "Continue comme ça pour progresser ! Garde cette même régularité dans tes entraînements pour rester en mode progression optimale.", font=(font_principale, taille2),
                                                width=300, wraplength=280, justify="left", text_color=couleur1)
                interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12)
            else:
                catégorie_statut = ctk.CTkLabel(h1_result_optimale, text="⚠️ Surentraînement", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color=couleur1)
                catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)             
                interpretation_statut = ctk.CTkLabel(interprétation_conseil, text="Risque élevé de blessure\n\n" \
                "Prends quelques jours de pause pour laisser ton corps récupérer et réduire les risques de blessure.", font=(font_principale, taille2),
                                                width=300, wraplength=280, justify="left", text_color=couleur1)
                interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12) 
        else:
            catégorie_statut = ctk.CTkLabel(h1_result_optimale, text="🚫 Données insuffisantes", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color=couleur1)
            catégorie_statut.pack(fill="both", expand=True, padx=12, pady=12)             
            interpretation_statut = ctk.CTkLabel(interprétation_conseil, text="L'interprétation ne peut pas être déterminée.\n\n" \
            "Fais une séance de sport pour lancer les analyses et évaluer ta charge actuelle.", font=(font_principale, taille2),
                                                width=300, wraplength=280, justify="left", text_color=couleur1)
            interpretation_statut.pack(fill="both", expand=True, padx=12, pady=12)  
    try:   
        if data_pour_graphique:
            dates_graphique = [datetime.strptime(row[0], '%Y-%m-%d') for row in data_pour_graphique]
            charges_graphique = [row[1] for row in data_pour_graphique]

            fig, ax = plt.subplots(figsize=(10, 4))
            # Fond bleu clair pour la figure et la zone du graphique
            fig.patch.set_facecolor(couleur2)
            ax.set_facecolor(couleur2)

            sns.lineplot(x=dates_graphique, y=charges_graphique, marker="o", color=couleur1, ax=ax)

            ax.axhline(y=charge_chronique, color=couleur1, linestyle="--", label="Charge chronique")

            ax.set_title("Évolution de la charge chronique")
            ax.set_xlabel("Date")
            ax.set_ylabel("Charge chronique") 
            canvas = FigureCanvasTkAgg(fig, graphique)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20, padx=20)
        else:
            not_data = ctk.CTkFrame(graphique, corner_radius=corner1, fg_color=couleur2)
            not_data.pack(expand=True, fill="both", padx=12, pady=12)
            pas_de_données = ctk.CTkLabel(not_data, text="L’algorithme a besoin de plus de données pour te donner des conseils et afficher ton graphique.\n\nAjoute quelques séances d'entraînement pour voir l'évolution de ta charge d'entraînement au cours du temps.",
                                          font=(font_secondaire, taille2), text_color=couleur1, wraplength=600, justify="left")
            pas_de_données.pack(padx=15, pady=15)
            button_creer_activite = ctk.CTkButton(not_data, text="👉 Besoin d'aide ?", fg_color=couleur2, hover_color=couleur2_hover,
                                            corner_radius=corner1, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                            command=aide_ajout_activité)
            button_creer_activite.pack(padx=(20, 2), pady=20)
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
        return

    titre_c_quoi = ctk.CTkLabel(info, text="C'est quoi la charge d'entraînement ?", font=(font_secondaire, taille2), wraplength=600,
                                text_color=couleur1, justify="left")
    titre_c_quoi.pack(pady=12, padx=12)
    c_quoi = ctk.CTkLabel(info, 
                            text="La charge d'entraînement sert à optimiser ta progression sans te cramer, en trouvant le juste équilibre entre l'effort fourni et la récupération nécessaire. C'est ton meilleur ami pour éviter les blessures et planifier tes séances sportives intelligemment.",
                            font=(font_principale, taille2), wraplength=600, justify="left",
                            text_color=couleur1)
    c_quoi.pack(padx=12, pady=(25, 12))
