from app_ressource import * 
from update_database import con, curseur, con_coach, curseur_coach

def c_quoi_rpe():
    messagebox.showinfo("C'est quoi le RPE ?", 
                        "Le RPE, c'est une manière subjective de mesurer l'intensité de ton entraînement. " \
                        "En gros, tu notes l'effort que tu ressens sur une échelle de 1 à 10.\n\n" \
                        "◉ RPE : 1 = Facile\n" \
                        "◉ RPE : 2 = Facile\n" \
                        "◉ RPE : 3 = Facile\n" \
                        "◉ RPE : 4 = Modéré\n" \
                        "◉ RPE : 5 = Modéré\n" \
                        "◉ RPE : 6 = Modéré\n" \
                        "◉ RPE : 7 = Difficile\n" \
                        "◉ RPE : 8 = Difficile\n" \
                        "◉ RPE : 9 = Très Difficile\n" \
                        "◉ RPE : 10 = Effort Maximal")

def choisir_nb_aléatoire():
    try:
        curseur_coach.execute(f"SELECT nb_minimum FROM choisir_nb_aléatoire")
        nb_min = curseur_coach.fetchone()[0]
        curseur_coach.execute(f"SELECT nb_maximum FROM choisir_nb_aléatoire")
        nb_max = curseur_coach.fetchone()[0]
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur lors du choix du nombre pour génération du texte pour le coach !")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye !")
        return
    nombre = random.randint(nb_min, nb_max)
    return nombre

def coach_pour_ajouter_un_entraînement(boite, account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                                       Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                                       sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                                       rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                                       passe_d_entry, score_entry, but_entry, activité):
    
    curseur.execute("SELECT nom_du_coach, avatar FROM Coach WHERE account_id = ?", (account_id,))
    ton_coach = curseur.fetchone()
    if ton_coach:
        nom_du_coach = ton_coach[0]
        avatar_du_coach = ton_coach[1]
    else:
        nom_du_coach = None
        avatar_du_coach = None

    def générer_une_phrase():
        generation = ["question", "emoji", "phrase_de_motivation", "conseil_info", "promo_sprintia"]
        text_generer = ""
        text_totale_generer = ""
        try:
            curseur.execute("SELECT style_du_coach FROM Coach WHERE account_id = ?", (account_id,))
            style = curseur.fetchone()
            if style:
                if style[0] == "Inshape":
                    table_personnalité = "ajouter_activité_inshape"
                elif style[0] == "Strict":
                    table_personnalité = "ajouter_activité_strict_motivant"
                elif style[0] == "Copain":
                    table_personnalité = "ajouter_activité_copain"
                else:
                    table_personnalité = "ajouter_activité_bienveillant"
            else:
                    table_personnalité = "ajouter_activité_bienveillant"
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de génération de texte pour le coach !")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye !")
            return
        for text_coach in generation:
            nombre = choisir_nb_aléatoire()
            try:
                curseur_coach.execute(f"SELECT {text_coach} FROM {table_personnalité} WHERE id = ?", (nombre,))
                text_generer = curseur_coach.fetchone()[0]
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de génération de texte pour le coach !")
                return
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye !")
                return
            text_totale_generer = text_totale_generer+text_generer
        if len(text_totale_generer) > 500:
            return générer_une_phrase()
        return text_totale_generer

    text_totale_generer = générer_une_phrase()

    frame_coach = ctk.CTkFrame(boite, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur_fond)
    frame_coach.pack(fill="both", side="right", padx=(7, 25), pady=25)
    frame_embleme_coach = ctk.CTkFrame(master=frame_coach, fg_color="transparent")
    frame_embleme_coach.pack(fill="both", padx=12, pady=25)
    frame_phrase_du_coach = ctk.CTkFrame(master=frame_coach, fg_color="transparent")
    frame_phrase_du_coach.pack(fill="both", padx=12, pady=(25, 12))
                                    
    embleme_coach = ctk.CTkLabel(master=frame_embleme_coach, 
                                    text=f"{avatar_du_coach if avatar_du_coach else "👨"} {nom_du_coach if nom_du_coach else "JRM Coach"}",
                                    font=(font_secondaire, taille2), text_color=couleur1, wraplength=310, justify="left", anchor="w")
    embleme_coach.pack(expand=True, fill="both")
    phrase_du_coach = ctk.CTkLabel(master=frame_phrase_du_coach, 
                                    text=f"{text_totale_generer}",
                                    font=(font_principale, taille3), text_color=couleur1, 
                                    wraplength=310, justify="left", anchor="w")
    phrase_du_coach.pack(expand=True, fill="both")

def enregistrement_activité(account_id, app, exercice, date, duree, rpe, douleur, fatigue, climat, nom, sport, distance, denivele, allure, vmax, 
                            équipement, muscle_travaillé, répétitions, série, volume_total, lieu, humeur, but, passe_décisive, type_de_séances, score, type,
                            mode):
    if mode == "Libre":
        charge_de_base = duree * rpe
            
        modificateurs_douleur = [0.9, 1.05, 1.2, 1.4]
        modificateurs_climat = [0.95, 1.1, 1.05, 1.2]
            
        charge_d = charge_de_base * modificateurs_douleur[douleur]
        charge_c = charge_d * modificateurs_climat[climat]
        score_fatigue = 1 + (fatigue - 2.5) * 0.05
        charge = score_fatigue * charge_c
        try:
            curseur.execute("""INSERT INTO Historique_activité (date_activité, sport, durée, distance, rpe, charge, account_id, type, dénivelé, catégorie) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, float(f"{duree:.0f}"), distance, rpe, charge, account_id, nom, denivele, "libre"))
            con.commit()
            messagebox.showinfo("Succès", "Ton activité a bien été enregistrée !")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton activité !")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye !")
            return
    elif mode == "Course":
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
            curseur.execute("""INSERT INTO Historique_activité (date_activité, sport, durée, distance, rpe, charge, account_id, type, dénivelé, allure, vitesse_max, catégorie) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, float(f"{duree:.0f}"), distance, rpe, charge, account_id, type, denivele, allure, vmax, "course"))
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
    elif mode == "Musculation":                          
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
            curseur.execute("""INSERT INTO Historique_activité (date_activité, sport, durée, rpe, charge, account_id, muscle_travaillé, répétitions, série, volume, équipement, lieu, catégorie) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, float(f"{duree:.0f}"), rpe, charge, account_id, muscle_travaillé, répétitions, série, volume_total, équipement, lieu, "musculation"))
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
    else:
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
            curseur.execute("""INSERT INTO Historique_activité (date_activité, sport, durée, rpe, charge, account_id, humeur, but, passe_décisive, type, score, catégorie) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, float(f"{duree:.0f}"), rpe, charge, account_id, humeur, but, passe_décisive, type_de_séances, score, "football"))
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
    
    vider_fenetre(app)
    exercice(account_id)
 
def vérification_data_de_base_activité(account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                                       Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                                       sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                                       rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                                       passe_d_entry, score_entry, but_entry, mode):
    
    climat = nom = sport = distance = denivele = allure = vmax = type = équipement = None
    muscle_travaillé = répétitions = série = volume_total = lieu = humeur = but = passe_décisive = type_de_séances = score = type = None

    try:
        date_str = date_entry.get().strip().replace('/', '-').replace('.', '-').replace(',', '-').replace('_', '-').replace('💡', '').replace(' ', '')
        if not date_str:
            messagebox.showerror("Date est vide", "La date est obligatoire !")
            return
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
        if date_obj > datetime.now():
            messagebox.showerror("Erreur de date", "La date ne peut pas être dans le futur !")
            return
        date = date_obj.strftime('%Y-%m-%d')
    except ValueError as e:
        messagebox.showerror("Erreur de format", "Format de date invalide. Utilisez JJ-MM-AAAA.")
        return
    try:
        duree = duree_entry.get().strip()
        if not duree:
            messagebox.showerror("Durée est vide", "La durée est obligatoire !")
            return
        if ":" in duree:
            if len(duree.split(":")) == 3:
                heures, minutes, secondes = duree.split(':') # Split découpe le champs temps_autre en deux parties
                if len(heures) > 2 or len(minutes) > 2 or len(secondes) > 2:
                    messagebox.showerror("Erreur de format", "Le format de la durée doit être hh:mm:ss avec hh, mm et ss avec 2 chiffres maximum !")
                    return
                heure = int(heures)
                minute = int(minutes)
                seconde = int(secondes)
                if heure > 59 or minute > 59 or seconde > 59:
                    messagebox.showerror("Erreur de format", "Le format de la durée doit être hh:mm:ss avec hh, mm et ss inférieur à 60 !")
                    return
                duree = (heure*60) + minute + (seconde/60) # On convertit le temps en minutes
            elif len(duree.split(":")) == 2:
                minutes, secondes = duree.split(':')
                if len(minutes) > 2 or len(secondes) > 2:
                    messagebox.showerror("Erreur de format", "Le format de la durée doit être mm:ss avec mm et ss avec 2 chiffres maximum !")
                    return
                minute = int(minutes)
                seconde = int(secondes)
                if minute > 59 or seconde > 59:
                    messagebox.showerror("Erreur de format", "Le format de la durée doit être mm:ss avec mm et ss inférieur à 60 !")
                    return
                duree = minute + (seconde/60) # On convertit le temps en minutes
            else:
                messagebox.showerror("Erreur de format", "Le format de la durée doit être hh:mm:ss ou mm:ss !")
                return
        else:
            try:
                temps_conversion = int(duree)
                duree = temps_conversion
            except ValueError:
                messagebox.showerror("Erreur de format", "Le temps doit être un nombre (en minutes) ou au format hh:mm:ss ou mm:ss !")
                return
        if duree <= 0:
            messagebox.showerror("Erreur de durée", "La durée doit être supérieur à 0 !")
            return
    except ValueError:
        messagebox.showerror("Erreur de nombre entier pour la durée", "Le temps doit être un nombre (minutes) ou au format hh:mm:ss ou au format mm:ss !")
        return
    try:
        rpe = int(rpe_entry.get())
        if not 1 <= rpe <= 10:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erreur de RPE", "Le RPE est invalide, il doit être entre 1 et 10 !")
        return
    douleur = Options_douleur.get(douleur_entry.get().strip())
    fatigue = Options_fatigue.get(fatigue_entry.get().strip())
    if fatigue is None:
        messagebox.showerror("Fatigue est vide", "La fatigue est obligatoire !")
        return
    if douleur is None:
        messagebox.showerror("Douleur est vide", "La douleur est obligatoire !")
        return
    if mode == "Libre" or mode == "Course" or mode == "Football":
        climat = Options_climat.get(climat_entry.get().strip())
        if climat is None:
            messagebox.showerror("Climat est vide", "Le climat est obligatoire !")
            return
    if mode == "Libre":
        nom = type_entry.get().strip()
        if nom == "Type d'entraî.":
            messagebox.showerror("Type d'entraînement vide", "Le type d'entraînement est obligatoire !")
            return
        
        sport_input = sport_entry.get().strip()
        if not sport_input:
            messagebox.showerror("Sport est vide", "Le sport est obligatoire !")
            return
        try:
            float(sport_input)
            messagebox.showerror("Erreur de format", "Le sport doit être une chaîne de caractères, pas un nombre !")
            return
        except ValueError:
            pass
        if len(sport_input) > 50:
            messagebox.showerror("Erreur", "Le sport doit contenir entre 50 caractères !")
            return
        sport = sport_input
        distance = None
        try:
            dist_str = distance_entry.get().strip().replace(',', '.').replace(' ', '').replace('_', '').replace('km', '').replace('KM', '')
            if not dist_str:
                distance = None
            if dist_str:
                distance = float(dist_str)
                if distance <= 0:
                    messagebox.showerror("Erreur de distance", "La distance doit être supérieur à 0 !")
                    return
        except ValueError:
            messagebox.showerror("Erreur de distance", "Distance invalide (nombre positif requis) !")
            return
        
    if mode == "Libre" or mode == "Course":
        denivele = None        
        try:
            deniv_str = denivele_entry.get().strip().replace(' ', '').replace('m', '').replace('M', '')
            if not deniv_str:
                denivele = None
            if deniv_str:
                denivele = int(deniv_str)
                if denivele < 0:
                    raise ValueError   
        except ValueError:
            messagebox.showerror("Erreur de dénivelé", "Dénivelé invalide entier positif uniquement !")
            return
    if mode == "Course":
        sport = "Course"
        type = type_entry.get().strip()
        if type == "Type d'entraî.":
            messagebox.showerror("Type manquant", "Séléctionne un type d'entraînement !")
            return
        try:
            dist_str = distance_entry.get().strip().replace(',', '.').replace(' ', '').replace('_', '').replace('km', '').replace('KM', '')
            if not dist_str:
                messagebox.showerror("Distance est vide", "La distance est obligatoire dans le mode 'Course' !")
                return
            if dist_str:
                distance = float(dist_str)
                if distance <= 0:
                    messagebox.showerror("Erreur de distance", "La distance doit être supérieur à 0 !")
                    return
        except ValueError:
            messagebox.showerror("Erreur de distance", "Distance invalide (nombre positif requis) !")
            return
        allure = allure_entry.get().strip()
        if len(allure) > 20:
            messagebox.showerror("Erreur", "L'allure ne doit pas dépasser 20 caractères !")
            return
        if not allure:
            messagebox.showerror("Allure est vide", "L'allure est obligatoire dans le mode 'Course' !")
            return
        vmax_str = vmax_entry.get().strip().replace(",", ".").replace(" ", "").replace("km/h", "").replace("-", "")
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
    if mode == "Musculation":
        muscle_travaillé = muscle_entry.get().strip()
        répétitions = rep_entry.get().strip().replace(",", ".").replace(" ", "").replace("séries", "").replace("-", "")
        série = serie_entry.get().strip().replace(",", ".").replace(" ", "").replace("répétitions", "").replace("-", "")
        volume = volume_entry.get().strip().replace(",", ".").replace(" ", "").replace("kg", "").replace("-", "")
        if len(série) > 20:
            messagebox.showerror("Erreur", "Les séries ne doivent pas dépasser 20 caractères !")
            return
        if série:
            try:
                série = int(série)
                if série < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erreur", "Les série doivent être un nombre entier positif !")
                return
        else:
            série = None
        if len(muscle_travaillé) > 150:
            messagebox.showerror("Erreur", "Les muscles travaillés ne doivent pas dépasser 150 caractères !")
            return
        if not muscle_travaillé:
            messagebox.showerror("Muscle travaillé est vide", "Muscle travaillé est obligatoire dans le mode 'Musculation' !")
            return
        if len(répétitions) > 20:
            messagebox.showerror("Erreur", "Les répétitions ne doivent pas dépasser 20 caractères !")
            return
        if répétitions:
            try:
                répétitions = int(répétitions)
                if répétitions < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erreur", "Les répétitions doivent être un nombre entier positif !")
                return
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

        lieu = lieu_entry.get().strip()
        équipement = matos_entry.get().strip()
        if lieu is None:
            messagebox.showerror("Lieu est vide", "Le lieu de l'entraînement est obligatoire !")
            return
        if équipement == "Type d'entraî.":
            messagebox.showerror("Le type est vide", "Le type d'entraînement est obligatoire !")
            return
        sport = "Musculation"
    elif mode == "Football":
        humeur = humeur_entry.get().strip()
        passe_décisive1 = passe_d_entry.get().strip()
        type_de_séances = type_entry.get().strip()
        score = score_entry.get().strip()
        if type_de_séances == "Type d'entraî.":
            messagebox.showerror("Type de séances de foot est vide", "Le type de séance de foot est obligatoire !")
            return
        if len(humeur) > 50:
            messagebox.showerror("Erreur", "L'humeur ne doit pas dépasser 50 caractères !")
            return
        if not humeur:
            messagebox.showerror("Humeur est vide", "L'humeur est obligatoire dans le mode 'Football' !")
            return
        if len(score) > 40:
            messagebox.showerror("Erreur", "Le score ne doit pas dépasser 40 caractères !")
            return
        if not score:
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
        
        sport = "Football"
        if type_de_séances is None:
            messagebox.showerror("Type de séances de foot est vide", "Le type de séance de foot est obligatoire !")
            return
        
    if mode == "Libre":
        enregistrement_activité(account_id, app, exercice, date, duree, rpe, douleur, fatigue, climat, nom, sport, distance, denivele, allure, vmax, 
                            équipement, muscle_travaillé, répétitions, série, volume_total, lieu, humeur, but, passe_décisive, type_de_séances, score, type,
                            "Libre")
    elif mode == "Course":
        enregistrement_activité(account_id, app, exercice, date, duree, rpe, douleur, fatigue, climat, nom, sport, distance, denivele, allure, vmax, 
                            équipement, muscle_travaillé, répétitions, série, volume_total, lieu, humeur, but, passe_décisive, type_de_séances, score, type,
                            "Course")
    elif mode == "Musculation":
        enregistrement_activité(account_id, app, exercice, date, duree, rpe, douleur, fatigue, climat, nom, sport, distance, denivele, allure, vmax, 
                            équipement, muscle_travaillé, répétitions, série, volume_total, lieu, humeur, but, passe_décisive, type_de_séances, score, type,
                            "Musculation")
    else:
        enregistrement_activité(account_id, app, exercice, date, duree, rpe, douleur, fatigue, climat, nom, sport, distance, denivele, allure, vmax, 
                            équipement, muscle_travaillé, répétitions, série, volume_total, lieu, humeur, but, passe_décisive, type_de_séances, score, type,
                            "Football")

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

def supprimer_entraînement(account_id, période_str, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    vider_fenetre(app)
    sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=10, padx=10)
    frame_tout = ctk.CTkFrame(app, fg_color=couleur2, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame_tout.pack(pady=(20, 0), padx=10)
    frame1 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame1.pack(pady=(12, 2), padx=12)
    frame2 = ctk.CTkFrame(frame_tout, fg_color="transparent")
    frame2.pack(pady=(2, 12), padx=12)

    Titre = ctk.CTkLabel(master=frame, text="Supprimer un entraînement", 
                font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack()

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: supression(account_id))
    choix_entry = ctk.CTkEntry(master=frame1, placeholder_text="ID de l'entraî.", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    choix_entry.pack(expand=True, fill="both")

    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
    try:
        curseur.execute("SELECT id_activité, sport, date_activité, durée, rpe FROM Historique_activité WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC", (account_id, période_str))
        activites = curseur.fetchall()
        headers = ["ID", "Sport", "Date", "Durée", "RPE"]

        for colonne, header_text in enumerate(headers):
            tableau_frame.grid_columnconfigure(colonne, weight=1)        
            header_label = ctk.CTkButton(tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                fg_color=couleur_fond, corner_radius=corner2, text_color=couleur1,
                                height=40, border_width=border2, border_color=couleur2, hover_color=couleur_fond)
            header_label.grid(row=0, column=colonne, padx=10, pady=15)
            tableau_frame.grid_columnconfigure(colonne, weight=1)

        if activites:
            for ligne, activite in enumerate(activites):
                for colonne, data in enumerate(activite):
                    if colonne == 2:
                        data = datetime.strptime(str(data), '%Y-%m-%d').strftime('%d-%m-%Y')
                    label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                         text_color=couleur_text, wraplength=140)
                    label.grid(row=ligne + 1, column=colonne, padx=15, pady=15, sticky="ew")
        else:
            pas_donnees = ctk.CTkLabel(master=tableau_frame, text="Aucune activité enregistrée pour cette période.", font=(font_principale, taille1),
                                       text_color=couleur_text)
            pas_donnees.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de l'historique !")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, veuillez réessayer !")
        return

    def supression(account_id):
            choix = choix_entry.get().strip()
            if not choix:
                messagebox.showerror("Champs vide", "Le champs 'ID de l'entraî est obligatoire, il ne peut pas être vide.")
                return
            try:
                choix_id_saisi = int(choix)
                if choix_id_saisi < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erreur de conversion", "L'ID de l'entraî doit être un nombre entier positif.")
                return
            ids_objectifs_disponibles = [obj[0] for obj in activites]
            try:
                if choix_id_saisi in ids_objectifs_disponibles:
                    objectif_id_db = choix_id_saisi
                    curseur.execute("DELETE FROM Historique_activité WHERE id_activité = ? AND account_id = ?", (objectif_id_db, account_id))
                    con.commit()
                    messagebox.showinfo("Suppression réussie", "Activité supprimée avec succès.")
                    vider_fenetre(app)
                    exercice(account_id)
                else:
                    messagebox.showerror("Erreur", "L'ID de l'entraî saisie n'existe pas ou n'appartient pas à votre compte.")
                    return
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la suppression de l'entraî.")
                return
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye.")
                return

    button_check = ctk.CTkButton(master=frame2, text="Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: supression(account_id))
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_back = ctk.CTkButton(master=frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), border_width=border2, border_color=couleur2,
                                    command=lambda: [vider_fenetre(app), exercice_accueil(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left")

def ajouter_entraînement_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}
    Options_climat = {"Normal": 0, "Chaud": 1, "Froid": 2, "Difficile": 3}
    Options_type = ["Récupération", "Fun", "Normal", "Endurance", "Seuil", "Fractionné", "Spécifique", "Trail", "Ultrafond", "Compétition"]

    sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame1.pack(padx=10, pady=10)
    navbar = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner2)
    navbar.pack(pady=(10, 5))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter un entraînement",
                font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack()

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Libre":
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_libre(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_fooball(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Libre", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover,
                                           corner_radius=corner2, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left", padx=(5, 2))
    mode_activité.set("Course")
    button_rpe = ctk.CTkButton(master=navbar, text="📊 C'est quoi le RPE ?", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=c_quoi_rpe)
    button_rpe.pack(expand=True, fill="x", side="right", padx=10, pady=5)

    boite = ctk.CTkFrame(app, fg_color="transparent")
    boite.pack()
    frame_activité = ctk.CTkFrame(boite, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(side="left", padx=(25, 5), pady=25)

    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=12, pady=(12, 2))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=12, pady=2)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=12, pady=20)
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=12, pady=2)
    frame_champs5 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs5.pack(padx=12, pady=2)
    frame_champs6 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs6.pack(padx=12, pady=2)
    frame_bouton = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_bouton.pack(expand=True, fill="both", padx=12, pady=(0, 12))

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: vérification_data_de_base_activité(account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                                       Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                                       sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                                       rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                                       passe_d_entry, score_entry, but_entry, "Course"))

    frame_pour_date = ctk.CTkFrame(master=frame_champs1, fg_color=couleur_fond, corner_radius=corner1)
    frame_pour_date.pack(expand=True, fill="both", side="left", padx=(0, 2))
    date_entry = ctk.CTkEntry(master=frame_pour_date, placeholder_text="Date", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=36, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=180)
    date_entry.pack(expand=True, fill="both", side="left", padx=(12,0), pady=12)
    date_entry.insert(0, f"💡 {date_actuelle_format.replace("-", "/")}")
    button_pop_up_calendrier = ctk.CTkButton(frame_pour_date, text="📅 Calendrier", width=70, height=36, corner_radius=corner1, fg_color=couleur2,
                                            hover_color=couleur2_hover, font=(font_principale, taille3), text_color=couleur1,
                                            border_color=couleur2, border_width=border1,
                                            command=lambda: pop_up_calendrier(app, date_entry))
    button_pop_up_calendrier.pack(expand=True, fill="both", side="left", padx=(0, 12), pady=12)
    duree_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Durée", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=275)
    duree_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    distance_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Distance (km)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=310)
    distance_entry.pack(expand=True, fill="both", side="left", padx=2)
    type_entry = ctk.CTkComboBox(master=frame_champs2, values=Options_type, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    type_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    type_entry.set("Type d'entraî.")

    rpe_label = ctk.CTkLabel(master=frame_champs3, text="RPE : 1", font=(font_principale, taille2), text_color=couleur_fond)
    rpe_label.pack(expand=True, fill="x", side="left", padx=12)
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs3, width=500, height=30, from_= 1, to= 10, number_of_steps= 9, command=valeur_rpe,
                              progress_color=couleur_fond, button_color=couleur_fond, button_hover_color=couleur2_hover,
                              corner_radius=5, button_length=20, fg_color=couleur1, 
                              # La variable DoubleVar met la valeur du RPE à 1
                              variable=ctk.DoubleVar(value=1))
    rpe_entry.pack(expand=True, fill="x", side="left", padx=12)

    fatigue_entry = ctk.CTkComboBox(master=frame_champs4, values=list(Options_fatigue.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    fatigue_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    fatigue_entry.set("Fatigue post-entraî.")
    douleur_entry = ctk.CTkComboBox(master=frame_champs4, values=list(Options_douleur.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    douleur_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    douleur_entry.set("Douleur post-entraî.")

    climat_entry = ctk.CTkComboBox(master=frame_champs5, values=list(Options_climat.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    climat_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    climat_entry.set("Climat à l'entraî.")
    allure_entry = ctk.CTkEntry(master=frame_champs5, placeholder_text="Allure (ex : 6:00 /km)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=310)
    allure_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))

    denivele_entry = ctk.CTkEntry(master=frame_champs6, placeholder_text="Dénivelé (m)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=310)
    denivele_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    vmax_entry = ctk.CTkEntry(master=frame_champs6, placeholder_text="Vitesse max", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=310)
    vmax_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    sport_entry = None
    muscle_entry = None
    rep_entry = None
    serie_entry = None
    volume_entry = None
    Options_lieu = None
    lieu_entry = None
    matos_entry = None   
    humeur_entry = None
    passe_d_entry = None
    score_entry = None
    but_entry = None 

    bouton_valider = ctk.CTkButton(master=frame_bouton, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1, border_color=couleur2, border_width=border1,
                                    font=(font_principale, taille3), width=310,
                            command=lambda : vérification_data_de_base_activité(account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                            Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                            sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                            rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                            passe_d_entry, score_entry, but_entry, "Course"))
    bouton_valider.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_back = ctk.CTkButton(master=frame_bouton, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1, width=310,
                                    font=(font_principale, taille3), border_width=border2, border_color=couleur2,
                                    command=lambda: [vider_fenetre(app), exercice_accueil(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left")

    coach_pour_ajouter_un_entraînement(boite, account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                                       Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                                       sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                                       rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                                       passe_d_entry, score_entry, but_entry, "Course")

def ajouter_entraînement_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    Options_matos = ["Poids de corps", "Avec équipement", "Mixte"]
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}
    Options_lieu = ["Domicile", "Salle de sport", "Gymnase", "Street Workout", "Extérieur", "Autre"]

    sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame1.pack(padx=10, pady=10)
    navbar = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner2)
    navbar.pack(pady=(10, 5))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter un entraînement",
                font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack()

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Libre":
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_libre(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_fooball(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Libre", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover,
                                           corner_radius=corner2, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left", padx=(5, 2))
    mode_activité.set("Musculation")
    button_rpe = ctk.CTkButton(master=navbar, text="📊 C'est quoi le RPE ?", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=c_quoi_rpe)
    button_rpe.pack(expand=True, fill="x", side="right", padx=10, pady=5)

    boite = ctk.CTkFrame(app, fg_color="transparent")
    boite.pack()
    frame_activité = ctk.CTkFrame(boite, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(side="left", padx=(25, 5), pady=25)

    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=12, pady=(12, 2))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=12, pady=2)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=12, pady=20)
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=12, pady=2)
    frame_champs5 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs5.pack(padx=12, pady=2)
    frame_champs6 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs6.pack(padx=12, pady=2)
    frame_bouton = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_bouton.pack(expand=True, fill="both", padx=12, pady=(0, 12))

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: vérification_data_de_base_activité(account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                                       Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                                       sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                                       rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                                       passe_d_entry, score_entry, but_entry, "Musculation"))

    frame_pour_date = ctk.CTkFrame(master=frame_champs1, fg_color=couleur_fond, corner_radius=corner1)
    frame_pour_date.pack(expand=True, fill="both", side="left", padx=(0, 2))
    date_entry = ctk.CTkEntry(master=frame_pour_date, placeholder_text="Date", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=36, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=180)
    date_entry.pack(expand=True, fill="both", side="left", padx=(12,0), pady=12)
    date_entry.insert(0, f"💡 {date_actuelle_format.replace("-", "/")}")
    button_pop_up_calendrier = ctk.CTkButton(frame_pour_date, text="📅 Calendrier", width=70, height=36, corner_radius=corner1, fg_color=couleur2,
                                            hover_color=couleur2_hover, font=(font_principale, taille3), text_color=couleur1,
                                            border_color=couleur2, border_width=border1,
                                            command=lambda: pop_up_calendrier(app, date_entry))
    button_pop_up_calendrier.pack(expand=True, fill="both", side="left", padx=(0, 12), pady=12)
    duree_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Durée", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=275)
    duree_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    matos_entry = ctk.CTkComboBox(master=frame_champs2, values=Options_matos, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    matos_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    matos_entry.set("Type d'entraî.")
    muscle_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Muscle travaillé", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=310)
    muscle_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    rpe_label = ctk.CTkLabel(master=frame_champs3, text="RPE : 1", font=(font_principale, taille2), text_color=couleur_fond)
    rpe_label.pack(expand=True, fill="x", side="left", padx=12)
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs3, width=500, height=30, from_= 1, to= 10, number_of_steps= 9, command=valeur_rpe,
                              progress_color=couleur_fond, button_color=couleur_fond, button_hover_color=couleur2_hover,
                              corner_radius=5, button_length=20, fg_color=couleur1, 
                              # La variable DoubleVar met la valeur du RPE à 1
                              variable=ctk.DoubleVar(value=1))
    rpe_entry.pack(expand=True, fill="x", side="left", padx=12)

    fatigue_entry = ctk.CTkComboBox(master=frame_champs4, values=list(Options_fatigue.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    fatigue_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    fatigue_entry.set("Fatigue post-entraî.")
    douleur_entry = ctk.CTkComboBox(master=frame_champs4, values=list(Options_douleur.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    douleur_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    douleur_entry.set("Douleur post-entraî.")

    lieu_entry = ctk.CTkComboBox(master=frame_champs5, values=Options_lieu, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    lieu_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    lieu_entry.set("Lieu de l'entraî.")
    rep_entry = ctk.CTkEntry(master=frame_champs5, placeholder_text="Nb. total de répétitions", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=310)
    rep_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    serie_entry = ctk.CTkEntry(master=frame_champs6, placeholder_text="Nb. total de séries", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=310)
    serie_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    volume_entry = ctk.CTkEntry(master=frame_champs6, placeholder_text="Volume total (kg)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=310)
    volume_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    Options_climat = None
    climat_entry = None
    type_entry = None
    sport_entry = None
    distance_entry = None
    denivele_entry = None
    allure_entry = None
    vmax_entry = None
    humeur_entry = None
    passe_d_entry = None
    score_entry = None
    but_entry = None

    bouton_valider = ctk.CTkButton(master=frame_bouton, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1, border_color=couleur2, border_width=border1,
                                    font=(font_principale, taille3), width=310,
                            command=lambda : vérification_data_de_base_activité(account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                            Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                            sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                            rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                            passe_d_entry, score_entry, but_entry, "Musculation"))
    bouton_valider.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_back = ctk.CTkButton(master=frame_bouton, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1, width=310,
                                    font=(font_principale, taille3), border_width=border2, border_color=couleur2,
                                    command=lambda: [vider_fenetre(app), exercice_accueil(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left")

    coach_pour_ajouter_un_entraînement(boite, account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                                       Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                                       sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                                       rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                                       passe_d_entry, score_entry, but_entry, "Musculation")

def ajouter_entraînement_fooball(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_climat = {"Normal": 0, "Chaud": 1, "Froid": 2, "Difficile": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}
    Options_type = ["Entraînement", "Match", "Tournoi", "Futsal", "City", "Autre"]

    sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame1.pack(padx=10, pady=10)
    navbar = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner2)
    navbar.pack(pady=(10, 5))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter un entraînement",
                font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack()

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Libre":
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_libre(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_fooball(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Libre", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover,
                                           corner_radius=corner2, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left", padx=(5, 2))
    mode_activité.set("Football")
    button_rpe = ctk.CTkButton(master=navbar, text="📊 C'est quoi le RPE ?", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=c_quoi_rpe)
    button_rpe.pack(expand=True, fill="x", side="right", padx=(15, 5), pady=5)

    boite = ctk.CTkFrame(app, fg_color="transparent")
    boite.pack()
    frame_activité = ctk.CTkFrame(boite, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(side="left", padx=(25, 5), pady=25)

    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=12, pady=(12, 2))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=12, pady=2)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=12, pady=20)
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=12, pady=2)
    frame_champs5 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs5.pack(padx=12, pady=2)
    frame_champs6 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs6.pack(padx=12, pady=2)
    frame_bouton = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_bouton.pack(padx=12, pady=(0, 12))

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: vérification_data_de_base_activité(account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                                       Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                                       sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                                       rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                                       passe_d_entry, score_entry, but_entry, "Football"))

    frame_pour_date = ctk.CTkFrame(master=frame_champs1, fg_color=couleur_fond, corner_radius=corner1)
    frame_pour_date.pack(expand=True, fill="both", side="left", padx=(0, 2))
    date_entry = ctk.CTkEntry(master=frame_pour_date, placeholder_text="Date", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=36, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=180)
    date_entry.pack(expand=True, fill="both", side="left", padx=(12,0), pady=12)
    date_entry.insert(0, f"💡 {date_actuelle_format.replace("-", "/")}")
    button_pop_up_calendrier = ctk.CTkButton(frame_pour_date, text="📅 Calendrier", width=70, height=36, corner_radius=corner1, fg_color=couleur2,
                                            hover_color=couleur2_hover, font=(font_principale, taille3), text_color=couleur1,
                                            border_color=couleur2, border_width=border1,
                                            command=lambda: pop_up_calendrier(app, date_entry))
    button_pop_up_calendrier.pack(expand=True, fill="both", side="left", padx=(0, 12), pady=12)
    duree_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Durée", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=275)
    duree_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    type_entry = ctk.CTkComboBox(master=frame_champs2, values=Options_type, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    type_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    type_entry.set("Type d'entraî.")
    humeur_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Humeur post-match", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=310)
    humeur_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    rpe_label = ctk.CTkLabel(master=frame_champs3, text="RPE : 1", font=(font_principale, taille2), text_color=couleur_fond)
    rpe_label.pack(expand=True, fill="x", side="left", padx=12)
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs3, width=500, height=30, from_= 1, to= 10, number_of_steps= 9, command=valeur_rpe,
                              progress_color=couleur_fond, button_color=couleur_fond, button_hover_color=couleur2_hover,
                              corner_radius=5, button_length=20, fg_color=couleur1, 
                              # La variable DoubleVar met la valeur du RPE à 1
                              variable=ctk.DoubleVar(value=1))
    rpe_entry.pack(expand=True, fill="x", side="left", padx=12)

    fatigue_entry = ctk.CTkComboBox(master=frame_champs4, values=list(Options_fatigue.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    fatigue_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    fatigue_entry.set("Fatigue post-entraî.")
    douleur_entry = ctk.CTkComboBox(master=frame_champs4, values=list(Options_douleur.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    douleur_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    douleur_entry.set("Douleur post-entraî.")

    climat_entry = ctk.CTkComboBox(master=frame_champs5, values=list(Options_climat.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    climat_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    climat_entry.set("Climat à l'entraî.")
    score_entry = ctk.CTkEntry(master=frame_champs5, placeholder_text="Score (ex : 3-2)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=310)
    score_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    but_entry = ctk.CTkEntry(master=frame_champs6, placeholder_text="Nb. but", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=310)
    but_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    passe_d_entry = ctk.CTkEntry(master=frame_champs6, placeholder_text="Nb. passe décisive", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=310)
    passe_d_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    sport_entry = None
    distance_entry = None
    denivele_entry = None
    allure_entry = None
    vmax_entry = None
    muscle_entry = None
    rep_entry = None
    serie_entry = None
    volume_entry = None
    Options_lieu = None
    lieu_entry = None
    matos_entry = None

    bouton_valider = ctk.CTkButton(master=frame_bouton, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1, border_color=couleur2, border_width=border1,
                                    font=(font_principale, taille3), width=310,
                            command=lambda : vérification_data_de_base_activité(account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                            Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                            sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                            rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                            passe_d_entry, score_entry, but_entry, "Football"))
    bouton_valider.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_back = ctk.CTkButton(master=frame_bouton, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1, width=310,
                                    font=(font_principale, taille3), border_width=border2, border_color=couleur2,
                                    command=lambda: [vider_fenetre(app), exercice_accueil(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left")

    coach_pour_ajouter_un_entraînement(boite, account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                                       Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                                       sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                                       rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                                       passe_d_entry, score_entry, but_entry, "Football")

def ajouter_entraînement_libre(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_climat = {"Normal": 0, "Chaud": 1, "Froid": 2, "Difficile": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}
    options_type = ["Étirement", "Léger", "Récupération", "Modéré", "Brûle Graisse", "Cardio", "Tabata", "Intense", "Sortie longue", "Expédition", "Sport d'équipe", "Fun", "Autre"]

    sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame1.pack(padx=10, pady=10)
    navbar = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner2)
    navbar.pack(pady=(10, 5))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter un entraînement", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack()

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Libre":
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_libre(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_fooball(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_entraînement_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Libre", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover,
                                           corner_radius=corner2, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left", padx=(5, 2))
    mode_activité.set("Libre")
    button_rpe = ctk.CTkButton(master=navbar, text="📊 C'est quoi le RPE ?", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=c_quoi_rpe)
    button_rpe.pack(expand=True, fill="x", side="right", padx=10, pady=5)

    boite = ctk.CTkFrame(app, fg_color="transparent")
    boite.pack()
    frame_activité = ctk.CTkFrame(boite, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(side="left", padx=(25, 5), pady=25)

    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=12, pady=(12, 2))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=12, pady=2)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=12, pady=20)
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=12, pady=2)
    frame_champs5 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs5.pack(padx=12, pady=2)
    frame_bouton = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_bouton.pack(expand=True, fill="both", padx=12, pady=(0, 12))

    allure_entry = None
    vmax_entry = None

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: vérification_data_de_base_activité(account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                                       Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                                       sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                                       rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                                       passe_d_entry, score_entry, but_entry, "Libre"))

    frame_pour_date = ctk.CTkFrame(master=frame_champs1, fg_color=couleur_fond, corner_radius=corner1)
    frame_pour_date.pack(expand=True, fill="both", side="left", padx=(0, 2))
    date_entry = ctk.CTkEntry(master=frame_pour_date, placeholder_text="Date", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=36, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=180)
    date_entry.pack(expand=True, fill="both", side="left", padx=(12,0), pady=12)
    date_entry.insert(0, f"💡 {date_actuelle_format.replace("-", "/")}")
    button_pop_up_calendrier = ctk.CTkButton(frame_pour_date, text="📅 Calendrier", width=70, height=36, corner_radius=corner1, fg_color=couleur2,
                                            hover_color=couleur2_hover, font=(font_principale, taille3), text_color=couleur1,
                                            border_color=couleur2, border_width=border1,
                                            command=lambda: pop_up_calendrier(app, date_entry))
    button_pop_up_calendrier.pack(expand=True, fill="both", side="left", padx=(0, 12), pady=12)
    sport_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Sport", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=275)
    sport_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    duree_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Durée", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=205)
    duree_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    distance_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Distance (km)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=205)
    distance_entry.pack(expand=True, fill="both", side="left", padx=2)
    denivele_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Dénivelé (m)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color=couleur1,
                                  text_color=couleur1, width=205)
    denivele_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))

    rpe_label = ctk.CTkLabel(master=frame_champs3, text="RPE : 1", font=(font_principale, taille2), text_color=couleur_fond)
    rpe_label.pack(expand=True, fill="x", side="left", padx=12)
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs3, width=500, height=30, from_= 1, to= 10, number_of_steps= 9, command=valeur_rpe,
                              progress_color=couleur_fond, button_color=couleur_fond, button_hover_color=couleur2_hover,
                              corner_radius=5, button_length=20, fg_color=couleur1, 
                              # La variable DoubleVar met la valeur du RPE à 1
                              variable=ctk.DoubleVar(value=1))
    rpe_entry.pack(expand=True, fill="x", side="left", padx=12)

    type_entry = ctk.CTkComboBox(master=frame_champs4, values=options_type, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    type_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    type_entry.set("Type d'entraî.")
    fatigue_entry = ctk.CTkComboBox(master=frame_champs4, values=list(Options_fatigue.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    fatigue_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    fatigue_entry.set("Fatigue post-entraî.")

    douleur_entry = ctk.CTkComboBox(master=frame_champs5, values=list(Options_douleur.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    douleur_entry.pack(expand=True, fill="both", side="left", padx=(0, 2))
    douleur_entry.set("Douleur post-entraî.")
    climat_entry = ctk.CTkComboBox(master=frame_champs5, values=list(Options_climat.keys()), font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=310, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    climat_entry.pack(expand=True, fill="both", side="left", padx=(2, 0))
    climat_entry.set("Climat à l'entraî.")

    muscle_entry = None
    rep_entry = None
    serie_entry = None
    volume_entry = None
    Options_lieu = None
    lieu_entry = None
    matos_entry = None
    humeur_entry = None
    passe_d_entry = None
    score_entry = None
    but_entry = None

    bouton_valider = ctk.CTkButton(master=frame_bouton, text="💾 Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1, border_color=couleur2, border_width=border1,
                                    font=(font_principale, taille3), width=310,
                            command=lambda : vérification_data_de_base_activité(account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                            Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                            sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                            rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                            passe_d_entry, score_entry, but_entry, "Libre"))
    bouton_valider.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_back = ctk.CTkButton(master=frame_bouton, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1, width=310,
                                    font=(font_principale, taille3), border_width=border2, border_color=couleur2,
                                    command=lambda: [vider_fenetre(app), exercice_accueil(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left")

    coach_pour_ajouter_un_entraînement(boite, account_id, app, exercice, date_entry, duree_entry, rpe_entry, douleur_entry, fatigue_entry, 
                                       Options_fatigue, Options_douleur, Options_climat, climat_entry, type_entry, 
                                       sport_entry, distance_entry, denivele_entry, allure_entry, vmax_entry, muscle_entry,
                                       rep_entry, serie_entry, volume_entry,Options_lieu, lieu_entry, matos_entry, humeur_entry,
                                       passe_d_entry, score_entry, but_entry, "Libre")

def interface_exercice(account_id, type_de_catégorie, headers, requête_sql, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    global periode_séléctionner #global = pour dire que la variable existe en dehors de la fonction et que je vais la modifier
    sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    besoin_phrase_coach = True
    try:
        date_debut_période = date_actuelle - timedelta(days=7)
        période_pour_requete = date_debut_période.strftime('%Y-%m-%d')
        curseur.execute("SELECT nom_du_coach, avatar, style_du_coach FROM Coach WHERE account_id = ?", (account_id,))
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
        style_du_coach = ton_coach[2]
    else:
        nom_du_coach = None
        avatar_du_coach = None
        style_du_coach = "Bienveillant"
    
    try:
        curseur_coach.execute(f"SELECT {style_du_coach} FROM analyse_activité")
        phrase_coach = curseur_coach.fetchone()[0]
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Une erreur est survenue lors de la génération de l'analyse du coach !")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur innatendue s'est produite !")
        return

    boite_titre = ctk.CTkFrame(master=app, fg_color="transparent", corner_radius=corner3)
    boite_titre.pack(side="top", fill="x", padx=10, pady=10)

    boite = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner2)
    boite.pack(side="top", padx=10, pady=(10, 5))
    boite_semi_header = ctk.CTkFrame(master=boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header.pack(expand=True, fill="x", side="left", padx=(2, 10), pady=2)
    boite_semi_header2 = ctk.CTkFrame(master=boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header2.pack(expand=True, fill="x", side="left", padx=2, pady=2)
    boite_semi_header3 = ctk.CTkFrame(master=boite, fg_color=couleur2, corner_radius=corner2)
    boite_semi_header3.pack(expand=True, fill="x", side="right", padx=(0, 2), pady=2)

    frame_analyse_coach = ctk.CTkFrame(app, fg_color="transparent", corner_radius=corner1, border_width=border1, border_color=couleur1,
                                       height=125)
    frame_analyse_coach.pack(side="top", padx=10, pady=(5, 0))

    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                              scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(2, 10))

    info = ctk.CTkLabel(master=boite_titre, text="Entraînement", font=(font_secondaire, taille1), text_color=couleur_text)
    info.pack()
    
    def mise_mode(choix):
        choix = mode_activité.get()
        navigation = {
            "Libre": lambda: [vider_fenetre(app), exercice_libre(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)],
            "Musculation": lambda: [vider_fenetre(app), exercice_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)],
            "Football": lambda: [vider_fenetre(app), exercice_football(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)],
            "Tous": lambda: [vider_fenetre(app), exercice_accueil(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)],
            "Course": lambda: [vider_fenetre(app), exercice_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)]
        }
        app.after(0, navigation[choix])
    mode_activité = ctk.CTkSegmentedButton(master=boite_semi_header, values=["Tous", "Libre", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner2, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(expand=True, fill="x", side="right", padx=(2, 0), pady=5)
    mode_activité.set(type_de_catégorie)

    options_periode = {"1 semaine": 7, "1 mois": 30, "3 mois": 90, "6 mois": 180, "1 an": 365, "Tout voir (non recommandé)": 9999}
    combo_periode = ctk.CTkComboBox(master=boite_semi_header2, values=list(options_periode.keys()), font=(font_principale, taille2), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=200, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    combo_periode.pack(expand=True, fill="x", side="left", padx=2, pady=5)
    def avoir_periode(selection_text, options_dict):
        jours_a_soustraire = options_dict[selection_text]
        date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
        return date_debut.strftime('%Y-%m-%d')
    
    button_supprimer = ctk.CTkButton(master=boite_semi_header3, text="🗑️ Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: supprimer_entraînement(account_id, avoir_periode(combo_periode.get(), options_periode), app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre))
    button_supprimer.pack(expand=True, fill="x", side="right", padx=(2, 5), pady=5)
    button_creer_activite = ctk.CTkButton(master=boite_semi_header3, text="➕ Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: [vider_fenetre(app), ajouter_entraînement_libre(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_creer_activite.pack(expand=True, fill="x", side="right", padx=2, pady=5)
    
    if type_de_catégorie == "Course" or type_de_catégorie == "Football" or type_de_catégorie == "Musculation":
        wraplength_tableau = 110
        padx_tableau = 3
        conversion_format_date = 0
    else:
        wraplength_tableau = 140
        padx_tableau = 3
        conversion_format_date = 1
        
    if type_de_catégorie == "Course":
        recherche = "course"
        mode = "de course "
        data_rechercher = "durée, distance, dénivelé"
        parametre_rechercher = "account_id = ? AND catégorie = ? AND date_activité >= ? ORDER BY date_activité DESC"
        resultat_rechercher = (account_id, recherche, période_pour_requete)
    elif type_de_catégorie == "Football":
        recherche = "football"
        mode = "de football "
        data_rechercher = "durée, but, passe_décisive"
        parametre_rechercher = "account_id = ? AND catégorie = ? AND date_activité >= ? ORDER BY date_activité DESC"
        resultat_rechercher = (account_id, recherche, période_pour_requete)
    elif type_de_catégorie == "Musculation":
        recherche = "musculation"
        mode = "de musculation "
        data_rechercher = "durée, répétitions, série, volume"
        parametre_rechercher = "account_id = ? AND catégorie = ? AND date_activité >= ? ORDER BY date_activité DESC"
        resultat_rechercher = (account_id, recherche, période_pour_requete)
    elif type_de_catégorie == "Libre":
        recherche = "libre"
        mode = "avec le mode libre "
        data_rechercher = "durée, rpe, distance, dénivelé"
        parametre_rechercher = "account_id = ? AND catégorie = ? AND date_activité >= ? ORDER BY date_activité DESC"
        resultat_rechercher = (account_id, recherche, période_pour_requete)
    else:
        data_rechercher = "durée, rpe"
        mode = ""
        parametre_rechercher = "account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
        resultat_rechercher = (account_id, période_pour_requete)

    try:
        curseur.execute(f"SELECT {data_rechercher} FROM Historique_activité WHERE {parametre_rechercher}", resultat_rechercher)
        stats = curseur.fetchall()
        if stats is not None:
            if type_de_catégorie == "Course":
                total_durée = sum([statistique[0] for statistique in stats if statistique[0] is not None])
                total_distance = sum([statistique[1] for statistique in stats if statistique[1] is not None])
                total_dénivelé = sum([statistique[2] for statistique in stats if statistique[2] is not None])
                nombre_activités = len(stats)
                analyse = f"Au cours des sept derniers jours, tu as effectué {total_durée:.0f} minutes d'entraînement en {nombre_activités:.0f} entraînements."\
                          f" Ta distance totale est de {total_distance:.2f} km avec un dénivelé total de {total_dénivelé:.0f} m."
            elif type_de_catégorie == "Football":
                total_durée = sum([statistique[0] for statistique in stats if statistique[0] is not None])
                total_but = sum([statistique[1] for statistique in stats if statistique[1] is not None])
                total_passe_décisive = sum([statistique[2] for statistique in stats if statistique[2] is not None])
                nombre_activités = len(stats)
                analyse = f"Au cours des sept derniers jours, tu as effectué {total_durée:.0f} minutes d'entraînement en {nombre_activités:.0f} entraînements."\
                          f" Tu as marqué {total_but:.0f} buts et réalisé {total_passe_décisive:.0f} passes décisives."
            elif type_de_catégorie == "Musculation":
                total_durée = sum([statistique[0] for statistique in stats if statistique[0] is not None])
                total_répétitions = sum([statistique[1] for statistique in stats if statistique[1] is not None])
                total_séries = sum([statistique[2] for statistique in stats if statistique[2] is not None])
                total_volume = sum([statistique[3] for statistique in stats if statistique[3] is not None])
                nombre_activités = len(stats)
                analyse = f"Au cours des sept derniers jours, tu as effectué {total_durée:.0f} minutes d'entraînement en {nombre_activités:.0f} entraînements."\
                          f" Tu as réalisé {total_répétitions:.0f} répétitions en {total_séries:.0f} séries pour un volume total de {total_volume:.0f} kg."
            elif type_de_catégorie == "Libre":  
                total_durée = sum([statistique[0] for statistique in stats if statistique[0] is not None])
                total_rpe = sum([statistique[1] for statistique in stats if statistique[1] is not None])
                total_distance = sum([statistique[2] for statistique in stats if statistique[2] is not None])
                total_dénivelé = sum([statistique[3] for statistique in stats if statistique[3] is not None])
                nombre_activités = len(stats)
                moyenne_rpe = total_rpe / nombre_activités if nombre_activités > 0 else 0
                analyse = f"Au cours des sept derniers jours, tu as effectué {total_durée:.0f} minutes d'entraînement en {nombre_activités:.0f} entraînements."\
                          f" Ton RPE moyen cette semaine est de {moyenne_rpe:.1f}. Ta distance totale est de {total_distance:.2f} km avec un dénivelé total de {total_dénivelé:.0f} m"
            else:
                total_durée = sum([statistique[0] for statistique in stats if statistique[0] is not None])
                total_rpe = sum([statistique[1] for statistique in stats if statistique[1] is not None])
                nombre_activités = len(stats)
                moyenne_rpe = total_rpe / nombre_activités if nombre_activités > 0 else 0
                analyse = f"Au cours des sept derniers jours, tu as effectué {total_durée:.0f} minutes d'entraînement en {nombre_activités:.0f} entraînements."\
                          f" Ton RPE moyen cette semaine est de {moyenne_rpe:.1f}."
        else:
            total_durée = 0
            moyenne_rpe = 0
            nombre_activités = 0
            total_distance = 0
            total_dénivelé = 0
            total_but = 0
            total_passe_décisive = 0
            total_répétitions = 0
            total_séries = 0
            total_volume = 0
        if nombre_activités == 0:
            besoin_phrase_coach = None
            analyse = f"Tu n'as pas encore enregistré d'entraînement {mode}cette semaine. Commence dès maintenant pour que je puisse analyser ta semaine d'entraînement !" \
            " N'oublie pas que la régularité est la clé du succès ! 💪"
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Une erreur est survenue lors de la récupération des informations du coach.")
        return
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur innatendue s'est produite !")
        return
        
    label_coach1 = ctk.CTkLabel(frame_analyse_coach, text=f"{avatar_du_coach if avatar_du_coach is not None else "👨"} {nom_du_coach if nom_du_coach else "JRM Coach"}", wraplength=975, font=(font_principale, taille2), 
                                text_color=couleur1, justify="left")
    label_coach1.pack(padx=12, pady=(12, 4), anchor="w")
    label_coach2 = ctk.CTkLabel(frame_analyse_coach, 
                                text=f"{analyse} {phrase_coach if besoin_phrase_coach is not None else ""}", 
                                wraplength=1000, justify="left", font=(font_principale, taille3), text_color=couleur1)
    label_coach2.pack(padx=12, pady=(4, 12), anchor="w")

    def mettre_a_jour_historique(selection):
        global periode_séléctionner
        periode_séléctionner = selection
        for widget in tableau_frame.winfo_children():
            widget.grid_remove()
        try:
            jours_a_soustraire = options_periode[selection]
            date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
            période_str_pour_requete = date_debut.strftime('%Y-%m-%d')
            if type_de_catégorie == "Tous":
                curseur.execute(f"{requête_sql}", (account_id, période_str_pour_requete))
                activites = curseur.fetchall()
            else:
                curseur.execute(f"{requête_sql}", (account_id, recherche, période_str_pour_requete))
                activites = curseur.fetchall()

            for colonne, header_text in enumerate(headers):        
                header_label = ctk.CTkButton(tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                    fg_color=couleur_fond, corner_radius=corner2, text_color=couleur1,
                                    height=40, border_width=border2, border_color=couleur2, hover_color=couleur_fond)
                header_label.grid(row=0, column=colonne, padx=padx_tableau, pady=15)
                tableau_frame.grid_columnconfigure(colonne, weight=1)

            if activites:
                for ligne, activite in enumerate(activites):
                    for colonne, data in enumerate(activite):

                        if colonne == conversion_format_date:
                            data = datetime.strptime(str(data), '%Y-%m-%d').strftime('%d-%m-%Y')

                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=wraplength_tableau)
                        label.grid(row=ligne + 1, column=colonne, padx=padx_tableau, pady=15, sticky="ew")
            else:
                pas_donnees = ctk.CTkLabel(master=tableau_frame, text="Aucune activité enregistrée pour cette période.", font=(font_principale, taille1),
                                           text_color=couleur_text)
                pas_donnees.grid(row=1, column=0, columnspan=len(headers), pady=20)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de ton historique !")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
            return
    combo_periode.configure(command=mettre_a_jour_historique)
    combo_periode.set(periode_séléctionner)
    mettre_a_jour_historique(periode_séléctionner)

def exercice_course(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    requête_sql = "SELECT date_activité, durée, rpe, type, distance, allure, dénivelé, vitesse_max FROM Historique_activité WHERE account_id = ?  AND catégorie = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Date", "Durée", "RPE", "Type", "Distance", "Allure", "Dénivelé", "Vmax"]
    interface_exercice(account_id, "Course", headers, requête_sql, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)

def exercice_football(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    requête_sql = "SELECT date_activité, durée, rpe, type, humeur, but, passe_décisive, score FROM Historique_activité WHERE account_id = ?  AND catégorie = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Date", "Durée", "RPE", "Type", "Humeur", "But", "Passe D", "Score"]
    interface_exercice(account_id, "Football", headers, requête_sql, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)

def exercice_musculation(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    requête_sql = "SELECT date_activité, durée, rpe, équipement, muscle_travaillé, lieu, répétitions, série, volume FROM Historique_activité WHERE account_id = ? AND catégorie = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Date", "Durée", "RPE", "Type", "Muscle", "Lieu", "Rép", "Série", "Volume"]
    interface_exercice(account_id, "Musculation", headers, requête_sql, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)

def exercice_libre(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    requête_sql = "SELECT sport, date_activité, durée, rpe, type, distance, dénivelé FROM Historique_activité WHERE account_id = ?  AND catégorie = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Sport", "Date", "Durée", "RPE", "Type", "Distance", "Dénivelé"]
    interface_exercice(account_id, "Libre", headers, requête_sql, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)

def exercice_accueil(account_id, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre):
    requête_sql = "SELECT sport, date_activité, durée, rpe, ROUND(charge, 1) FROM Historique_activité WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Sport", "Date", "Durée", "RPE", "Charge d'entraînement"]
    try:
        curseur.execute("SELECT statut FROM Auto_connect")
        result_statut = curseur.fetchone()
        if not result_statut:
            curseur.execute("INSERT INTO Auto_connect (statut) VALUES (?)", (account_id,))
            con.commit()
        else:  
            curseur.execute("UPDATE Auto_connect SET statut = ?", (account_id,))
            con.commit()
    except sqlite3.Error as e:
        pass
    except Exception as e:
        pass
    interface_exercice(account_id, "Tous", headers, requête_sql, app, sidebar_exercice, exercice, charge_entraînement, predicteur_temps, parametre)
