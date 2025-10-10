from app_ressource import * 
from update_database import con, curseur

def proteine_quotidienne():
    messagebox.showinfo("Bientôt disponible", "Cette fonction seras disponible dans quelques semaines !\n" \
    "Pour le moment, on peaufine cette fonctionnalité !")
    return

def calculateur_imc(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_outil(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Calculateur IMC", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    carte_connexion = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_imc())
    poids_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Poids (kg)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    poids_entry.pack(pady=(11, 5), padx=10)
    taille_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Taille (cm)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    taille_entry.pack(pady=(5, 11), padx=10)

    cadre_result = ctk.CTkFrame(master=app, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Ta confidentialité est notre priorité : nous calculons ton temps de course directement sur ton appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1, wraplength=800)
    result.pack(padx=50, pady=10)

    def calcul_imc():
        try:
            poids = float(poids_entry.get().strip())
            taille_conversion = float(taille_entry.get().strip())
            taille = taille_conversion/100

            if poids <= 0 or taille <= 0:
                messagebox.showerror("Erreur", "La taille et le poids doivent être supérieur à 0 !")
                return
            if not poids or not taille:
                messagebox.showerror("Erreur", "La taille et le poids ne peuvent pas être vides !")
                return
            else:
                imc = poids / (taille ** 2)

                if imc <= 18.5:
                    interprétation = "Ton IMC se situe dans la zone de maigreur. Cela peut correspondre à ta morphologie naturelle, mais si tu ressens de la fatigue ou des inquiétudes, un avis médical peut être utile pour vérifier ton état de santé global."
                elif 18.5 <= imc <= 24.999:
                    interprétation = "Super, ton IMC est dans la zone de corpulence normale ! C’est un bon indicateur, mais n’oublie pas que la santé dépend aussi d’autres facteurs comme l’équilibre alimentaire, l’activité physique et le bien-être général."
                elif 25 <= imc <= 29.999:
                    interprétation = "Ton IMC est dans la zone de surpoids. Cela peut être lié à différents facteurs (morphologie, mode de vie, génétique, etc.). Si tu le souhaites, un professionnel peut t’aider à faire le point sur tes habitudes."
                elif 30 <= imc <= 34.999:
                    interprétation = "Ton IMC indique une obésité modérée. Cela ne définit pas ta santé à lui seul, mais un accompagnement personnalisé (médecin, nutritionniste) peut t’aider à trouver un équilibre adapté à tes besoins."
                elif 35 <= imc <= 39.999:
                    interprétation = "Ton IMC est dans la zone d’obésité sévère. Pour aborder cela de manière globale, un suivi médical ou nutritionnel peut te soutenir dans une démarche adaptée et bienveillante."
                elif imc >= 40:
                    interprétation = "Ton IMC se situe dans la zone d’obésité de grade 3. C’est une situation où un suivi médical régulier est important pour ta santé. N’hésite pas à en parler à un professionnel."
                else:
                    interprétation = "Une erreur est survenue, réesaye plus tard."
                    
                result.configure(text=f"Ton IMC est : {imc:.2f}\n\n{interprétation}",
                                 anchor="w", justify="left")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye.")
    button_check = ctk.CTkButton(master=app, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: calcul_imc())
    button_check.pack(padx=10, pady=10)

def estimation_VO2MAX(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_outil(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Estimation VO2max", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    carte_connexion = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_VO2MAX(account_id))
    vma_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="VMA", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    vma_entry.pack(pady=(11, 5), padx=10)

    combo_genre = ctk.CTkComboBox(master=carte_connexion, values=["Homme", "Femme"], font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    combo_genre.pack(pady=5, padx=10)
    combo_genre.set("Sélectionne ton genre")

    age_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Âge", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    age_entry.pack(pady=(5, 11), padx=10)

    cadre_result = ctk.CTkFrame(master=app, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Ta confidentialité est notre priorité : nous calculons ton temps de course\n directement sur ton appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1)
    result.pack(padx=50, pady=10)

    def calcul_VO2MAX(account_id):
        try:
            vma = float(vma_entry.get().strip())
            age = float(age_entry.get().strip())
            genre = combo_genre.get().strip()

            if vma <= 0:
                messagebox.showerror("Erreur", "La VMA doit être supérieur à 0 !")
                return
            if age < 14:
                messagebox.showerror("Erreur", "L'âge minimum pour cette fonction est de 14 ans !")
                return
            if not vma or not age:
                messagebox.showerror("Erreur", "La VMA et l'âge ne peuvent pas être vides !")
                return
            else:
                vo2max = vma*3.5
                if genre == "Homme":
                    if 14 <= age <= 17 :
                        if vo2max >= 58:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 54 <= vo2max <= 58:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 50 <= vo2max <= 53:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 46 <= vo2max <= 49:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 18 <= age <= 25 :
                        if vo2max >= 56:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 52 <= vo2max <= 56:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 48 <= vo2max <= 51:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 44 <= vo2max <= 47:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 26 <= age <= 35 :
                        if vo2max >= 51:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 47 <= vo2max <= 51:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 43 <= vo2max <= 46:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 39 <= vo2max <= 42:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 36 <= age <= 45 :
                        if vo2max >= 45:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 41 <= vo2max <= 45:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 37 <= vo2max <= 40:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 33 <= vo2max <= 36:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 46 <= age <= 55 :
                        if vo2max >= 41:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 37 <= vo2max <= 41:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 33 <= vo2max <= 36:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 29 <= vo2max <= 32:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 56 <= age <= 65 :
                        if vo2max >= 37:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 33 <= vo2max <= 37:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 29 <= vo2max <= 32:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 25 <= vo2max <= 28:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if age >= 65 :
                        if vo2max >= 33:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 29 <= vo2max <= 33:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 25 <= vo2max <= 28:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 21 <= vo2max <= 24:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                elif genre == "Femme":
                    if 14 <= age <= 17 :
                        if vo2max >= 52:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 48 <= vo2max <= 52:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 44 <= vo2max <= 47:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 40 <= vo2max <= 43:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 18 <= age <= 25 :
                        if vo2max >= 48:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 44 <= vo2max <= 48:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 40 <= vo2max <= 43:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 36 <= vo2max <= 39:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 26 <= age <= 35 :
                        if vo2max >= 42:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 38 <= vo2max <= 42:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 34 <= vo2max <= 37:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 30 <= vo2max <= 33:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 36 <= age <= 45 :
                        if vo2max >= 37:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 33 <= vo2max <= 37:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 29 <= vo2max <= 32:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 25 <= vo2max <= 28:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 46 <= age <= 55 :
                        if vo2max >= 34:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 30 <= vo2max <= 34:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 26 <= vo2max <= 29:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 22 <= vo2max <= 25:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 56 <= age <= 65 :
                        if vo2max >= 30:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 26 <= vo2max <= 30:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 22 <= vo2max <= 25:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 18 <= vo2max <= 21:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if age >= 65 :
                        if vo2max >= 27:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 23 <= vo2max <= 27:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 19 <= vo2max <= 22:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 15 <= vo2max <= 18:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                else:
                    interprétation = "Sexe non valide. Séléctionne 'Homme' ou 'Femme'."
                result.configure(text=f"Ton VO2max est de {vo2max:.2f} mL/min/kg.\n\n{interprétation}", wraplength=800,
                                 anchor="w", justify="left")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
            return
    button_check = ctk.CTkButton(master=app, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_VO2MAX(account_id))
    button_check.pack(padx=10, pady=20)

def historique_vma():
    messagebox.showinfo("Bientôt disponible", "Cette fonction seras disponible dans quelques semaines !\n" \
    "Pour le moment, enregistre ta VMA pour pouvoir utiliser les nouveaux algorythmes dès qu'ils seront sorties !")
    return

def estimation_VMA(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_outil(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Estimation VMA", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    boite1 = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    boite1.pack(side="top", fill="both", expand=True, pady=(5, 0), padx=10)
    carte_connexion = ctk.CTkFrame(boite1, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=10) 
    app.bind('<Return>', lambda event: calcul_VMA())
    
    distance_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Distance (km)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=275)
    distance_entry.pack_forget()
    temps_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Temps", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=275)
    temps_entry.pack_forget()
    
    def remplissage_placeholder(choice):
        choice = test_spécifique.get()
        # On vide les champs pour les remplir ensuite
        distance_entry.delete(0, "end")
        temps_entry.delete(0, "end")

        # On remplit les champs en fonction du test sélectionné
        if choice == "Test demi-Cooper (6 min) (Recommandé)":
            temps_entry.insert(0, "6")
            distance_entry.insert(0, "Distance (km)")
        elif choice == "Test Cooper (12 min)":
            temps_entry.insert(0, "12")
            distance_entry.insert(0, "Distance (km)")
        elif choice == "Test Luc Léger (2 km)":
            distance_entry.insert(0, "2")
            temps_entry.insert(0, "Temps (min)")
        else:
            distance_entry.insert(0, "Distance (km)")
            temps_entry.insert(0, "Temps (min)")

    test_spécifique = ctk.CTkComboBox(master=carte_connexion, values=["Test demi-Cooper (6 min) (Recommandé)", "Test Cooper (12 min)", "Test Luc Léger (2 km)", "Course de référence (moins précise)"],
                                    font=(font_principale, taille3), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1,
                                    command=remplissage_placeholder)
    test_spécifique.pack(pady=(12, 2), padx=12)
    test_spécifique.set("Sélectionne un test")
    distance_entry.pack(expand=True, fill="both", pady=2, padx=12)
    temps_entry.pack(expand=True, fill="both", pady=2, padx=12)

    cadre_result = ctk.CTkFrame(master=boite1, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)
    cadre_result.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=10)
    frame_result = ctk.CTkFrame(cadre_result, fg_color=couleur2, corner_radius=corner1)
    frame_result.pack(side="top", expand=True, fill="both", pady=(12, 10), padx=10)
    frame_bouton = ctk.CTkFrame(cadre_result, corner_radius=corner1, fg_color=couleur2)
    frame_bouton.pack(side="top", pady=(2, 5))

    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))

    c_quoi_la_vma = "C'est quoi la VMA ?\n\nLa Vitesse Maximale Aérobie (VMA) est la vitesse de course à laquelle ton corps atteint sa consommation maximale d'oxygène (VO2max). " \
                    "Connaître ta VMA te permet de mieux structurer tes entraînements, " \
                    "d'optimiser tes performances et de prévenir les blessures en évitant le surentraînement."
    result = ctk.CTkLabel(master=frame_result, text=f"{c_quoi_la_vma}",
                           font=(font_principale, taille2), text_color=couleur1, wraplength=650, justify="left", anchor="w")
    result.pack(expand=True, fill="both", padx=15, pady=5)

    headers = ["Zone", "Allure", "Objectif", "Séances type"]
    contenu_tableau = [
            ["Zone 1", "Aucune donnée", "Travail de récupération", "1h à 70% de VMA"],
            ["Zone 2", "Aucune donnée", "Travailler son endurance (endurance fondamental)", "45 min à 80% de VMA"],
            ["Zone 3", "Aucune donnée", "Seuil aérobie", "4 x 1200m à 88% avec 2 min de récup"],
            ["Zone 4", "Aucune donnée", "Seuil anaérobie", "10 x 30/30 sec à 100%"],
            ["Zone 5", "Aucune donnée", "Travail de la vitesse pure (sprint)", "15 x 20/40 sec à 110%"],
        ]
    
    def calcul_VMA():
        type_test_spécifique = test_spécifique.get().strip()
        if type_test_spécifique == "Sélectionne un test":
            messagebox.showerror("Erreur", "Tu dois sélectionner un test !")
            return
        try:
            distance = float(distance_entry.get().strip())
        except ValueError:
            messagebox.showerror("Erreur", "La distance doit être un nombre (km)")
            return
        try:
            temps_autre = temps_entry.get().strip()
            if not distance or not temps_autre:
                messagebox.showerror("Erreur", "La distance ou le temps ne peuvent pas être vides !")
                return
            if ":" in temps_autre:
                if len(temps_autre.split(":")) == 3:
                    heures, minutes, secondes = temps_autre.split(':') # Split découpe le champs temps_autre en deux parties
                    if len(heures) > 2 or len(minutes) > 2 or len(secondes) > 2:
                        messagebox.showerror("Erreur", "Le format du temps doit être hh:mm:ss avec hh, mm et ss avec 2 chiffres maximum")
                        return
                    heure = int(heures)
                    minute = int(minutes)
                    seconde = int(secondes)
                    if heure > 59 or minute > 59 or seconde > 59:
                        messagebox.showerror("Erreur", "Le format du temps doit être hh:mm:ss avec hh, mm et ss inférieur à 60")
                        return
                    temps = (heure*60) + minute + (seconde/60) # On convertit le temps en minutes
                elif len(temps_autre.split(":")) == 2:
                    minutes, secondes = temps_autre.split(':') # Split découpe le champs temps_autre en deux parties
                    if len(minutes) > 2 or len(secondes) > 2:
                        messagebox.showerror("Erreur", "Le format du temps doit être mm:ss avec mm et ss avec 2 chiffres maximum")
                        return
                    minute = int(minutes)
                    seconde = int(secondes)
                    if minute > 59 or seconde > 59:
                        messagebox.showerror("Erreur", "Le format du temps doit être mm:ss avec mm et ss inférieur à 60")
                        return
                    temps = minute + (seconde/60) # On convertit le temps en minutes
                else:
                    messagebox.showerror("Erreur", "Le format du temps doit être hh:mm:ss ou mm:ss")
                    return
            else:
                try:
                    temps_conversion = int(temps_autre)
                    temps = temps_conversion
                except ValueError:
                    messagebox.showerror("Erreur", "Le temps doit être un nombre (minutes) ou au format hh:mm:ss ou mm:ss")
                    return
            if distance <= 0 or temps <= 0:
                messagebox.showerror("Erreur", "La distance et le temps doivent être supérieur à 0 !")
                return
        except ValueError:
            messagebox.showerror("Erreur", "Le temps doit être un nombre (minutes) ou au format hh:mm:ss ou au format mm:ss.")
            return
        if type_test_spécifique == "Test demi-Cooper (6 min) (Recommandé)":
            if temps != 6:
                messagebox.showerror("Erreur", "Pour le test demi-Cooper, le temps doit être de 6 minutes !")
                return
            distance_en_mètre = distance * 1000 
            vma_estimée = distance_en_mètre / 100
        elif type_test_spécifique == "Test de Cooper (12 min)":
            if temps != 12:
                messagebox.showerror("Erreur", "Pour le test de Cooper, le temps doit être de 12 minutes !")
                return
            distance_en_mètre = distance * 1000 
            vma_estimée = distance_en_mètre / 200
        elif type_test_spécifique == "Test Luc Léger (2 km)":
            if distance != 2:
                messagebox.showerror("Erreur", "Pour le test Luc Léger, la distance doit être de 2 km !")
                return
            vma_estimée = distance / (temps/60)
        else:
            if distance > 20:
                messagebox.showerror("Erreur", "Pour une course de référence, la distance ne doit pas dépasser 20 km !")
                return
            if temps < 2:
                messagebox.showerror("Erreur", "Pour une course de référence, le temps doit être supérieur à 2 minutes !")
                return
            # Formule basée sur le modèle de Peronnet & Thibault
            vitesse_moyenne = distance / (temps / 60) # Vitesse moyenne en km/h
            facteur_correction = 0.95 + 0.05 * math.exp(-temps / 600) # math.exp() = fonction exponentielle "e"
            vma_estimée = vitesse_moyenne / facteur_correction

        debut_zone1 = vma_estimée * 0.50
        fin_zone1 = vma_estimée * 0.60
        debut_zone2 = vma_estimée * 0.60
        fin_zone2 = vma_estimée * 0.75
        debut_zone3 = vma_estimée * 0.75
        fin_zone3 = vma_estimée * 0.85
        debut_zone4 = vma_estimée * 0.85
        fin_zone4 = vma_estimée * 0.95
        debut_zone5 = vma_estimée * 0.95

        servir_de_vma = "La VMA (Vitesse Maximale Aérobie) est un indicateur clé pour les coureurs et les sportifs d’endurance. La VMA permet de définir des zones d’intensité pour varier tes entraînements (voir tableau). Réévalue ta VMA tous les 2-3 mois pour ajuster tes allures d’entraînement."
        result.configure(text=f"VMA estimée : {vma_estimée:.1f} km/h.\n\n{servir_de_vma}",
                             anchor="w", justify="left", wraplength=620)
        
        contenu_tableau = [
            ["Zone 1", f"{debut_zone1:.1f} - {fin_zone1:.1f} km/h", "Travail de récupération", "1h à 70% de VMA"],
            ["Zone 2", f"{debut_zone2:.1f} - {fin_zone2:.1f} km/h", "Travailler son endurance (endurance fondamental)", "45 min à 80% de VMA"],
            ["Zone 3", f"{debut_zone3:.1f} - {fin_zone3:.1f} km/h", "Seuil aérobie", "4 x 1200m à 88% avec 2 min de récup"],
            ["Zone 4", f"{debut_zone4:.1f} - {fin_zone4:.1f} km/h", "Seuil anaérobie", "10 x 30/30 sec à 100%"],
            ["Zone 5", f"{debut_zone5:.1f} - {vma_estimée:.1f} km/h", "Travail de la vitesse pure (sprint)", "15 x 20/40 sec à 110%"],
        ]

        for widget in tableau_frame.winfo_children():
            widget.destroy()
        for col, header_text in enumerate(headers):
            header_label = ctk.CTkButton(tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                fg_color=couleur_fond, corner_radius=corner1, text_color=couleur1,
                                height=40, border_width=border2, border_color=couleur2, hover_color=couleur_fond)
            header_label.grid(row=0, column=col, padx=10, pady=15)
            tableau_frame.grid_columnconfigure(col, weight=1)
        for row_index, contenu_tableau_text in enumerate(contenu_tableau):
            for col_index, data in enumerate(contenu_tableau_text):
                data_label = ctk.CTkLabel(tableau_frame, text=data, font=(font_principale, taille3),
                                        text_color=couleur_text, wraplength=200)
                data_label.grid(row=row_index+1, column=col_index, padx=15, pady=5)
        return vma_estimée

    for col, header_text in enumerate(headers):       
            header_label = ctk.CTkButton(tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                fg_color=couleur_fond, corner_radius=corner2, text_color=couleur1,
                                height=40, border_width=border2, border_color=couleur2, hover_color=couleur_fond)
            header_label.grid(row=0, column=col, padx=10, pady=15)
            tableau_frame.grid_columnconfigure(col, weight=1)

    for row_index, contenu_tableau_text in enumerate(contenu_tableau):
        for col_index, data in enumerate(contenu_tableau_text):
            label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                text_color=couleur_text, wraplength=200)
            label.grid(row=row_index + 1, column=col_index, padx=15, pady=15, sticky="ew")

    def sauvegarder_vma():
        try:
            vma_estimée = calcul_VMA()
        except:
            return
        if not vma_estimée:
            messagebox.showerror("Erreur", "Tu dois d'abord calculer ta VMA avant de la sauvegarder !")
            return
        try:
            curseur.execute("SELECT date from Historique_vma WHERE account_id = ?", (account_id,))
            dernière_date = curseur.fetchone()
            if dernière_date == None:
                pass
            else:
                dernière_date = dernière_date[0]
            
            # Formate l'objet date_actuelle en chaîne de caractères 'AAAA-MM-JJ'
            date_actuelle_formatée = date_actuelle.strftime('%Y-%m-%d')
            if dernière_date == date_actuelle_formatée:
                messagebox.showerror("Erreur", "Tu as déjà sauvegardé une VMA aujourd'hui ! Réessaie demain.")
                return
            curseur.execute("INSERT INTO Historique_vma (account_id, vma, date) VALUES (?, ?, ?)", (account_id, vma_estimée, date_actuelle))
            con.commit()
            messagebox.showinfo("Succès", "Ta VMA a été sauvegardée dans ton historique !")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Une erreur s'est produite lors de la sauvegarde de ta VMA.")
            return
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur innatendu s'est produite, réessaye !{e}")
            return

    button_sauvegarde = ctk.CTkButton(frame_bouton, text="💾 Sauvegarder", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=sauvegarder_vma)
    button_sauvegarde.pack(side="left", padx=2, pady=(2, 10))
    button_historique = ctk.CTkButton(frame_bouton, text="📊 Historique", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=historique_vma)
    button_historique.pack(side="left", padx=2, pady=(2, 10))

    button_check = ctk.CTkButton(carte_connexion, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: calcul_VMA())
    button_check.pack(expand=True, fill="both", padx=12, pady=(2, 12))

def zone_cardiaque(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_outil(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Zones cardiaque", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    carte_connexion = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_zone(account_id))
    age_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Âge", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    age_entry.pack(pady=10, padx=10)

    cadre_result = ctk.CTkFrame(master=app, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Ta confidentialité est notre priorité : nous calculons ton temps de course\n directement sur ton appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1)
    result.pack(padx=50, pady=10)

    def calcul_zone(account_id):
        try:
            age = int(age_entry.get().strip())
            fc_max = 220 - age

            if age <= 0:
                messagebox.showerror("Erreur", "L'âge doit être supérieur à 0 !")
            if not age:
                messagebox.showerror("Erreur", "L'âge ne peut pas être vide !")
            debut_zone1 = fc_max*0.50
            fin_zone1 = fc_max*0.60
            Zone1 = f"Zone 1 : Récupération active - {debut_zone1:.0f}bpm à {fin_zone1:.0f}bpm"
            debut_zone2 = fc_max*0.60
            fin_zone2 = fc_max*0.70
            Zone2 = f"Zone 2 : Fondamentale, endurance de base | {debut_zone2:.0f}bpm à {fin_zone2:.0f}bpm"
            debut_zone3 = fc_max*0.70
            fin_zone3 = fc_max*0.80
            Zone3 = f"Zone 3 : Seuil aérobie, endurance active | {debut_zone3:.0f}bpm à {fin_zone3:.0f}bpm"
            debut_zone4 = fc_max*0.80
            fin_zone4 = fc_max*0.90
            Zone4 = f"Zone 4 :  Seuil anaérobie, résistance dure | {debut_zone4:.0f}bpm à {fin_zone4:.0f}bpm"
            debut_zone5 = fc_max*0.90
            Zone5 = f"Zone 5 : Vitesse maximale aérobie, puissance maximale | {debut_zone5:.0f}bpm à {fc_max:.0f}bpm"
            FC_max = f"Fréquence cardiaque maximum : {fc_max:.0f}bpm"

            result.configure(text=f"Tes Zones de Fréquence Cardiaque\n\n{Zone1}\n{Zone2}\n{Zone3}\n{Zone4}\n{Zone5}\n{FC_max}",
                                 anchor="w", justify="left")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_check = ctk.CTkButton(master=app, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_zone(account_id))
    button_check.pack(padx=10, pady=10)

def prédicteur_performance(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_outil(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Prédicteur de performance", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    Info = ctk.CTkLabel(master=app ,text="N'oublie pas que cette prédiction est une estimation basée sur la\nthéorie"\
                         " et peut varier en fonction de nombreux facteurs\nle jour de la course !", font=(font_secondaire, taille2),
                         text_color=couleur_text)
    Info.pack(padx=50, pady=10)

    carte_connexion = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_temps(account_id))
    vma_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="VMA", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    vma_entry.pack(pady=(11, 5), padx=10)
    distance_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Distance (km)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    distance_entry.pack(pady=(5, 11), padx=10)

    cadre_result = ctk.CTkFrame(master=app, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Ta confidentialité est notre priorité : nous calculons ton temps de course\n directement sur ton appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1)
    result.pack(padx=50, pady=10)

    def calcul_temps(account_id):
        try:
            distance = float(distance_entry.get().strip())
            vma = float(vma_entry.get().strip())

            if distance <= 0 or vma <=0:
                messagebox.showerror("Erreur", "La distance et le temps doivent être supérieur à 0 !")
                return
            if not distance or not vma:
                messagebox.showerror("Erreur", "La distance et la vma ne peuvent pas être vides !")
                return
            if distance <= 2:
                vitesse_moyenne = vma*0.98
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"
            elif 2 <= distance <= 3:
                vitesse_moyenne = vma*0.94
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"
            elif 3 <= distance <= 6:
                vitesse_moyenne = vma*0.82
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"
            elif 6 <= distance <= 12:
                vitesse_moyenne = vma*0.77
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"
            elif 12 <= distance <= 25:
                vitesse_moyenne = vma*0.72
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"
            elif 21.0975 <= distance <= 42.195:
                vitesse_moyenne = vma*0.62
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"
            else:
                vitesse_moyenne = vma*0.55
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"

            result.configure(text=f"{interpretation}",
                                 anchor="w", justify="left")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_check = ctk.CTkButton(master=app, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_temps(account_id))
    button_check.pack(padx=10, pady=10)

def outils(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_outil(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Outils", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    frame_bouton = ctk.CTkFrame(app, fg_color="transparent")
    frame_bouton.pack(pady=(20,0), padx=10)
    frame_bouton1 = ctk.CTkFrame(frame_bouton, fg_color="transparent")
    frame_bouton1.pack(pady=(20,0), padx=10)
    frame_bouton2 = ctk.CTkFrame(frame_bouton, fg_color="transparent")
    frame_bouton2.pack(pady=(10,0), padx=10)
    frame_bouton3 = ctk.CTkFrame(frame_bouton, fg_color="transparent")
    frame_bouton3.pack(pady=(10,20), padx=10)

    button_autre = ctk.CTkButton(frame_bouton1, text="⏱️ Prédicteur de performance\n_______________________\n\nDécouvre ton temps au semi-marathon,...",
                                    corner_radius=corner2, width=500, font=(font_principale, taille2), fg_color=couleur2, 
                                    hover_color=couleur2_hover, text_color=couleur1, 
                                    command=lambda: [vider_fenetre(app), prédicteur_performance(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_autre.pack(side="left", padx=10)
    button_info = ctk.CTkButton(frame_bouton1, text="❤️ Zones cardiaque\n_______________________\n\nDécouvre tes zones de fréquence cardiaque", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1, 
                                    command=lambda: [vider_fenetre(app), zone_cardiaque(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_info.pack(side="left", padx=(0, 10))
    button_nouveauté = ctk.CTkButton(frame_bouton2, text="⚖️ Calculateur IMC\n_______________________\n\nDécouvre ton IMC avec une interprétation", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), calculateur_imc(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_nouveauté.pack(side="left", padx=10)
    button_avis = ctk.CTkButton(frame_bouton2, text="🚀 Estimation VMA\n_______________________\n\nDécouvre ta VMA et tes zones d'allure", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1, 
                                    command=lambda: [vider_fenetre(app), estimation_VMA(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_avis.pack(side="left", padx=(0, 10))
    button_avis = ctk.CTkButton(frame_bouton3, text="🫁 Estimation VO2max\n_______________________\n\nDécouvre ton VO2max via ta vma", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1, 
                                    command=lambda: [vider_fenetre(app), estimation_VO2MAX(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_avis.pack(side="left", padx=10)   
    button_avis = ctk.CTkButton(frame_bouton3, text="🍗 Protéine quotidienne\n_______________________\n\nDécouvre la qté. de protéines à consommer", 
                                    fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, width=500, font=(font_principale, taille2),
                                    text_color=couleur1,
                                    command=proteine_quotidienne)
    button_avis.pack(side="left", padx=(0, 10))
