from app_ressource import messagebox, sqlite3

try:
    con = sqlite3.connect("data_base_test.db")
    curseur = con.cursor()
except sqlite3.Error as e:
    messagebox.showerror("Erreur", "Erreur de base de données lors de la connexion à la base de données !")
except Exception as e:
    messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

try:
    con_coach = sqlite3.connect("data_coach.db")
    curseur_coach = con_coach.cursor()
except sqlite3.Error as e:
    messagebox.showerror("Erreur", "Erreur de base de données lors du démarrage du coach ! As-tu bien téléchargé la base de données data_coach sur mon GitHub ?")
except Exception as e:
    messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye ! As-tu bien téléchargé la base de données data_coach sur mon GitHub ?")

def voir_si_besoin_de_transfert_de_données(quel_maj):
    if quel_maj == "3_0-3_1":
        table_maj = "Maj_base_de_donnée"
    else:
        table_maj = "Maj_base_de_donnée2"
    try:
        try:
            curseur.execute("SELECT username FROM Account")
            result_premiere = curseur.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données !")
            return
        if result_premiere:
            try:
                curseur.execute(f"SELECT action FROM {table_maj}")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données !")
            result_maj = curseur.fetchone()
            if result_maj and result_maj[0] == "fait": # result[0] = parce que fetchone renvoie ('fait',)
                return
            else:
                if quel_maj == "3_0-3_1":
                    transfert_data_running_Sprintia3_0_vers_Sprintia3_1_pour_indulgence_de_course()
                else:
                    transfert_data_Sprintia3_1_vers_Sprintia3_2_pour_nouveau_historique_d_activité()
        else:
            try:
                curseur.execute(f"INSERT INTO {table_maj} (action) VALUES ('fait')")
                con.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données !")
            return
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def maj_de_la_BDD_de_Sprintia_3_1_vers_Sprintia3_2():
    voir_si_besoin_de_transfert_de_données("3_1-3_2")
    try:
        curseur.execute("DROP TABLE Aide_podcast")
    except sqlite3.Error as e:
        pass
    try:
        curseur.execute("DROP TABLE Aide_RPE")
    except sqlite3.Error as e:
        pass

def maj_de_la_BDD_de_Sprintia_3_0_vers_Sprintia_3_1():
    voir_si_besoin_de_transfert_de_données("3_0-3_1")
    try:
        curseur.execute("DROP TABLE Pauses_v2")
    except sqlite3.Error as e:
        pass
    try:
        curseur.execute("DROP TABLE Aide")
    except sqlite3.Error as e:
        pass
    try:
        curseur.execute("ALTER TABLE Activité_football ADD COLUMN score TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Aide ADD COLUMN modifier_objectif TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Aide ADD COLUMN modifier_compétition TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Aide ADD COLUMN bienvenue TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN distance")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN répétitions")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN série")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN volume")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN équipement")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN lieu")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN dénivelé")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN fatigue")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN douleur")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN climat")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN nom")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN muscle_travaillé")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN distance")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN répétitions")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN série")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN volume")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN équipement")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN lieu")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN dénivelé")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN fatigue")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN douleur")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN climat")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN muscle_travaillé")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN humeur")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN but")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN passe_décisive")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN type_de_séances")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN fatigue")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN douleur")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN passe_décisive")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN type_de_séances")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN distance")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN dénivelé")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN climat")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN nom")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN humeur")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN but")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN douleur")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN climat")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN fatigue")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN muscle_travaillé")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN répétitions")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN série")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN volume")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN équipement")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN lieu")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN humeur")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN but")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN passe_décisive")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN type_de_séances")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité DROP COLUMN répétitions")
        curseur.execute("ALTER TABLE Activité DROP COLUMN série")
        curseur.execute("ALTER TABLE Activité DROP COLUMN volume")
        curseur.execute("ALTER TABLE Activité DROP COLUMN équipement")
        curseur.execute("ALTER TABLE Activité DROP COLUMN lieu")
        curseur.execute("ALTER TABLE Activité DROP COLUMN humeur")
        curseur.execute("ALTER TABLE Activité DROP COLUMN but")
        curseur.execute("ALTER TABLE Activité DROP COLUMN passe_décisive")
        curseur.execute("ALTER TABLE Activité DROP COLUMN type_de_séances")
        curseur.execute("ALTER TABLE Activité DROP COLUMN distance")
        curseur.execute("ALTER TABLE Activité DROP COLUMN description")
        curseur.execute("ALTER TABLE Activité DROP COLUMN nom")
        curseur.execute("ALTER TABLE Activité DROP COLUMN muscle_travaillé")
    except sqlite3.OperationalError:
        pass
    maj_de_la_BDD_de_Sprintia_3_1_vers_Sprintia3_2()

def maj_de_la_BDD_de_Sprintia_2_0_vers_Sprintia_3_0():
    try:
        curseur.execute("ALTER TABLE Compétition ADD COLUMN lieu TEXT")
    except sqlite3.OperationalError:
        pass  
    try:
        curseur.execute("ALTER TABLE Objectif ADD COLUMN niveau_fin TEXT")
    except sqlite3.OperationalError:
        pass  
    try:
        curseur.execute("ALTER TABLE Compétition ADD COLUMN priorité TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Account ADD COLUMN sport TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Account ADD COLUMN bio TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN muscle_travaillé TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN répétitions TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN série TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN volume TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN équipement TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN lieu TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN humeur TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN but TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN passe_décisive TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN type_de_séances TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité DROP COLUMN allure")
    except sqlite3.Error as e:
        pass
    maj_de_la_BDD_de_Sprintia_3_0_vers_Sprintia_3_1()

def maj_de_la_BDD_de_Sprintia_1_3_vers_Sprintia_2_0():
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN nom TEXT")
    except sqlite3.OperationalError:
        pass
    maj_de_la_BDD_de_Sprintia_2_0_vers_Sprintia_3_0()

def maj_de_la_BDD_de_Sprintia_1_2_vers_Sprintia_1_3():
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN distance NUMERIC")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN dénivelé NUMERIC")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN allure TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN description TEXT")
    except sqlite3.OperationalError:
        pass
    maj_de_la_BDD_de_Sprintia_1_3_vers_Sprintia_2_0()

def maj_de_la_BDD_de_Sprintia_1_1_vers_Sprintia_1_2():
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN date_activité TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("UPDATE Activité SET date_activité = date")
        con.commit()
    except sqlite3.Error as e:
        pass
    maj_de_la_BDD_de_Sprintia_1_2_vers_Sprintia_1_3()

def transfert_data_Sprintia3_1_vers_Sprintia3_2_pour_nouveau_historique_d_activité():
    appris = "fait"
    try:
        curseur.execute("CREATE TABLE IF NOT EXISTS Activité (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,rpe INTEGER,charge INTEGER,FOREIGN KEY (account_id)REFERENCES Account (id) );")
        curseur.execute("CREATE TABLE IF NOT EXISTS Activité_extérieur (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC,dénivelé INTEGER,rpe INTEGER,charge INTEGER,nom TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );")
        curseur.execute("CREATE TABLE IF NOT EXISTS Activité_intérieur (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,rpe INTEGER,charge INTEGER,nom TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );")
        curseur.execute("CREATE TABLE IF NOT EXISTS Activité_running (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC, vitesse_max NUMERIC, dénivelé INTEGER,rpe INTEGER,charge INTEGER,nom TEXT, allure TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );")
        curseur.execute("CREATE TABLE IF NOT EXISTS Activité_musculation (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,muscle_travaillé TEXT, répétitions TEXT, série TEXT, volume NUMERIC, équipement TEXT, lieu  TEXT,rpe INTEGER,charge INTEGER,FOREIGN KEY (account_id)REFERENCES Account (id) );")
        curseur.execute("CREATE TABLE IF NOT EXISTS Activité_football (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER, score TEXT, rpe INTEGER,charge INTEGER,humeur TEXT, but TEXT, passe_décisive TEXT, type_de_séances TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );")
    except sqlite3.Error:
        pass
    try:
        curseur.execute("INSERT INTO Historique_activité (account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, type, catégorie) SELECT account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom , 'libre' FROM Activité_extérieur")
        curseur.execute("INSERT INTO Historique_activité (account_id, date_activité, sport, durée, rpe, charge, type, catégorie) SELECT account_id, date_activité, sport, durée, rpe, charge, nom, 'libre' FROM Activité_intérieur")
        curseur.execute("INSERT INTO Historique_activité (account_id, date_activité, sport, durée, rpe, charge, humeur, but, passe_décisive, type, score, catégorie) SELECT account_id, date_activité, sport, durée, rpe, charge, humeur, but, passe_décisive, type_de_séances, score, 'football' FROM Activité_football")
        curseur.execute("INSERT INTO Historique_activité (account_id, date_activité, sport, durée, rpe, charge, muscle_travaillé, répétitions, série, volume, équipement, lieu, catégorie) SELECT account_id, date_activité, sport, durée, rpe, charge, muscle_travaillé, répétitions, série, volume, équipement, lieu, 'musculation' FROM Activité_musculation")
        curseur.execute("INSERT INTO Historique_activité (account_id, date_activité, sport, durée, rpe, charge, distance, vitesse_max, dénivelé, type, allure, catégorie) SELECT account_id, date_activité, sport, durée, rpe, charge, distance, vitesse_max, dénivelé, nom, allure, 'course' FROM Activité_running")


        curseur.execute("DROP TABLE Activité_intérieur")
        curseur.execute("DROP TABLE Activité_extérieur")
        curseur.execute("DROP TABLE Activité_football")
        curseur.execute("DROP TABLE Activité_running")
        curseur.execute("DROP TABLE Activité_musculation")
        curseur.execute("DROP TABLE Activité")
        con.commit()

        curseur.execute("INSERT INTO Maj_base_de_donnée2 (action) VALUES (?)", (appris,))
        con.commit()
        return
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la mise à jour de ta base de donnée !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def transfert_data_running_Sprintia3_0_vers_Sprintia3_1_pour_indulgence_de_course():
    try:
        curseur.execute("CREATE TABLE IF NOT EXISTS Activité_running (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC, vitesse_max NUMERIC, dénivelé INTEGER,rpe INTEGER,charge INTEGER,nom TEXT, allure TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );")
    except sqlite3.Error:
        pass
    # Tous les sports qui veulent dire course à pied
    sport_première_étape = "course"
    sport_deuxième_étape = "pied"
    sport = "course"
    trail = "trail"
    ultrafond = "ultrafond"
    sport2_première_étape = "course"
    sport2_deuxième_étape = "piste"
    sport3_première_étape = "tapis"
    sport3_deuxième_étape = "course"
    appris = "fait"
    try:
        # Le %% ça créer une recherche et le LIKE ça va faire une recherche qui contient "course" et "pied" ça veut dire que peut importe ce qu'il y a au milieu ca le transferera quand meme
        # On fais la migration des données de course à pied dans la nouvelle table Activité_running
        curseur.execute("INSERT INTO Activité_running (account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom) SELECT account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom FROM Activité WHERE LOWER(sport) LIKE ? AND LOWER(sport) LIKE ?", (f"%{sport_première_étape}%", f"%{sport_deuxième_étape}%"))
        curseur.execute("INSERT INTO Activité_running (account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom) SELECT account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom FROM Activité WHERE LOWER(sport) LIKE ? AND LOWER(sport) LIKE ?", (f"%{sport2_première_étape}%", f"%{sport2_deuxième_étape}%"))
        curseur.execute("INSERT INTO Activité_running (account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom) SELECT account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom FROM Activité WHERE LOWER(sport) LIKE ? AND LOWER(sport) LIKE ?", (f"%{sport3_première_étape}%", f"%{sport3_deuxième_étape}%"))
        curseur.execute("INSERT INTO Activité_running (account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom) SELECT account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom FROM Activité WHERE LOWER(sport) = ?", (sport,))
        curseur.execute("INSERT INTO Activité_running (account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom) SELECT account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom FROM Activité WHERE LOWER(sport) = ?", (trail,))
        curseur.execute("INSERT INTO Activité_running (account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom) SELECT account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom FROM Activité WHERE LOWER(sport) = ?", (ultrafond,))
        
        # On met un repère dans la base de donnée pour dire que la mise à jour a été faite
        curseur.execute("INSERT INTO Maj_base_de_donnée (action) VALUES (?)", (appris,))
        con.commit()
        try:
            curseur.execute("ALTER TABLE Activité DROP COLUMN distance TEXT")
        except sqlite3.OperationalError:
            pass
        return
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la migration de ta base de donnée !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def création():
    # Identifiant
    curseur.execute("CREATE TABLE IF NOT EXISTS Account (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL, sport TEXT, bio TEXT)")
        
    # Historique_activité (Libre, Course, Musculation, Football)
    curseur.execute("""CREATE TABLE IF NOT EXISTS Historique_activité (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,rpe INTEGER,charge INTEGER,        
                    distance NUMERIC,dénivelé INTEGER,type TEXT, 
                    vitesse_max NUMERIC, allure TEXT,
                    muscle_travaillé TEXT, répétitions TEXT, série TEXT, volume NUMERIC, équipement TEXT, lieu TEXT,
                    score TEXT, humeur TEXT, but TEXT, passe_décisive TEXT,
                    catégorie TEXT, FOREIGN KEY (account_id)REFERENCES Account (id));""")
        
    # Planification
    curseur.execute("CREATE TABLE IF NOT EXISTS Compétition (id INTEGER PRIMARY KEY AUTOINCREMENT,nom TEXT NOT NULL,date TEXT NOT NULL,sport TEXT NOT NULL,objectif TEXT NOT NULL, lieu TEXT,priorité TEXT,account_id INTEGER,FOREIGN KEY (account_id) REFERENCES Account(id))")
    curseur.execute("CREATE TABLE IF NOT EXISTS Objectif (id INTEGER PRIMARY KEY AUTOINCREMENT,sport TEXT NOT NULL,date TEXT NOT NULL,objectif TEXT NOT NULL,fréquence TEXT NOT NULL,niveau_début TEXT NOT NULL,niveau_fin TEXT,statut TEXT, account_id INTEGER,FOREIGN KEY (account_id) REFERENCES Account(id))")
    curseur.execute("CREATE TABLE IF NOT EXISTS Pauses (id INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER NOT NULL,type TEXT,FOREIGN KEY (account_id) REFERENCES Account(id))")

    # Aide
    curseur.execute("CREATE TABLE IF NOT EXISTS Aide_bienvenue (account_id INTEGER NOT NULL,aide TEXT, FOREIGN KEY (account_id) REFERENCES Account(id))")
    curseur.execute("CREATE TABLE IF NOT EXISTS Aide_objectif (account_id INTEGER NOT NULL,aide TEXT, FOREIGN KEY (account_id) REFERENCES Account(id))")
    curseur.execute("CREATE TABLE IF NOT EXISTS Aide_compétition (account_id INTEGER NOT NULL,aide TEXT, FOREIGN KEY (account_id) REFERENCES Account(id))")
    
    # Transfert de données
    curseur.execute("CREATE TABLE IF NOT EXISTS Maj_base_de_donnée (action TEXT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Maj_base_de_donnée2 (action TEXT)")

    # Connection automatique
    curseur.execute("CREATE TABLE IF NOT EXISTS Auto_connect (statut TEXT)")

    # Personalisation Coach
    curseur.execute("CREATE TABLE IF NOT EXISTS Coach (account_id INTEGER NOT NULL, nom_du_coach TEXT, style_du_coach TEXT, avatar TEXT)")

    con.commit()
    maj_de_la_BDD_de_Sprintia_1_1_vers_Sprintia_1_2()
