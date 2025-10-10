from app_ressource import messagebox, sqlite3, version_entière, version_numéro
from update_database import con, curseur

def aide_objectif(account_id):
    try:
        curseur.execute("SELECT aide FROM Aide_objectif WHERE account_id = ?", (account_id,))
        result = curseur.fetchone()
        if result and result[0] == "fait": # result[0] = parce que fetchone renvoie ('fait',)
            pass
        else:
            appris = "fait"
            curseur.execute("INSERT INTO Aide_objectif (account_id, aide)VALUES (?, ?)", (account_id, appris))
            con.commit()
            messagebox.showinfo("Info sur le menu déroulant", "Lorsque tu modifies ton objectif, les menus déroulants se réinitialisent. Pense donc à sélectionner à nouveau une option pour 'Level Final' et 'Statut de l'objectif', même si tu les avais déjà définis lors de la création de l'objectif.")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def aide_compétition(account_id):
    try:
        curseur.execute("SELECT aide FROM Aide_compétition WHERE account_id = ?", (account_id,))
        result = curseur.fetchone()
        if result and result[0] == "fait": # result[0] = parce que fetchone renvoie ('fait',)
            pass
        else:
            appris = "fait"
            curseur.execute("INSERT INTO Aide_compétition (account_id, aide)VALUES (?, ?)", (account_id, appris))
            con.commit()
            messagebox.showinfo("Info sur le menu déroulant", "Lorsque tu modifies ta compétition, les menus déroulants se réinitialisent. Pense donc à sélectionner à nouveau une option pour 'Priorité', même si tu l'avais déjà défini lors de la création de la compétition.")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def aide_bienvenue(account_id):
    try:
        curseur.execute("SELECT aide FROM Aide_bienvenue WHERE account_id = ?", (account_id,))
        result = curseur.fetchone()
        if result and result[0] == "fait": # result[0] = parce que fetchone renvoie ('fait',)
            pass
        else:
            appris = "fait"
            curseur.execute("INSERT INTO Aide_bienvenue (account_id, aide)VALUES (?, ?)", (account_id, appris))
            con.commit()
            messagebox.showinfo(f"Bienvenue dans Sprintia {version_entière}", "Découvre toutes les nouveautés de Sprintia 3.2 dans le patch note dans les paramètres !")
            messagebox.showinfo("Info", "Toutes les nouveautés indiquées dans le patch note ne sont pas présentes d'un coup ! Elles arriveront au fur et à mesure des bêtas")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

