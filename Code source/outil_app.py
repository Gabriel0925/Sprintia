from app_ressource import * 
from update_database import con, curseur

def proteine_quotidienne(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_outil(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Protéine quotidienne", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    boite1 = ctk.CTkFrame(app, fg_color="transparent")
    boite1.pack(side="top", pady=(5, 0), padx=10)
    carte_connexion = ctk.CTkFrame(boite1, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=(10, 5)) 

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: calcul_nb_proteine())

    poid_entry = ctk.CTkEntry(carte_connexion, placeholder_text="Poids (kg)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    poid_entry.pack(expand=True, fill="both", pady=(12, 2), padx=12)
    niveau_activite_genre_entry = ctk.CTkComboBox(carte_connexion, 
                                    values=["Sédentaire", "Activité physique légère", "Sportif d'endurance", "Sportif de Musculation (maintien de la masse)", "Sportif en prise de masse"], 
                                    font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=280, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    niveau_activite_genre_entry.pack(expand=True, fill="both", pady=2, padx=12)
    niveau_activite_genre_entry.set("Niveau d'activité")

    cadre_result = ctk.CTkFrame(boite1, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)
    cadre_result.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=(5, 10))
    frame_result = ctk.CTkFrame(cadre_result, fg_color=couleur2, corner_radius=corner1)
    frame_result.pack(side="top", expand=True, fill="both", pady=12, padx=12)

    c_quoi_les_proteines_quotidienne = "C'est quoi l'outil Protéine quotidienne ?\n\nL’outil Protéine quotidienne t’indique la quantité optimale de protéines à consommer chaque jour"\
                        " (en g), en fonction de ton poids et de ton niveau d’activité. Il t’aide à adapter ton alimentation pour préserver ta masse musculaire,"\
                        " améliorer ta récupération et soutenir le bon fonctionnement de ton organisme." 
    result = ctk.CTkLabel(frame_result, 
                            text=f"{c_quoi_les_proteines_quotidienne}",
                            font=(font_principale, taille2), text_color=couleur1, wraplength=600, justify="left", anchor="w")
    result.pack(expand=True, fill="both", padx=15, pady=5)

    def calcul_nb_proteine():
        poids_entry = poid_entry.get().strip().replace(',', '.').replace(' ', '').replace('_', '').replace('kg', '').replace('KG', '')
        if not poids_entry:
            messagebox.showerror("Champs vide", "Le poids est obligatoire, il ne doit pas être vide !")
            return
        try:
            poid = float(poids_entry)
            if poid <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur de conversion", "Le poids doit être un nombre supérieur à 0 !")
            return
        niveau_activite_genre = niveau_activite_genre_entry.get().strip()
        if niveau_activite_genre == "Niveau d'activité":
            messagebox.showerror("Champs vide", "Le niveau d'activité est obligatoire, il ne doit pas être vide !")
            return
        if niveau_activite_genre == "Sédentaire":
            coefficient = 0.83
        elif niveau_activite_genre == "Activité physique légère":
            coefficient = 1.0
        elif niveau_activite_genre == "Sportif d'endurance":
            coefficient = 1.4
        elif niveau_activite_genre == "Sportif de Musculation (maintien de la masse)":
            coefficient = 1.7
        else:
            coefficient = 2.0

        result_nb_proteine = poid*coefficient

        if niveau_activite_genre == "Sédentaire":
            interprétation = f"Protéine quotidienne recommandée : {result_nb_proteine:.0f} g/jour\n\nCette quantité de protéine par jour permettera à ton corps de bien fonctionner, sans effort physique intense."
        elif niveau_activite_genre == "Activité physique légère":
            interprétation = f"Protéine quotidienne recommandée : {result_nb_proteine:.0f} g/jour\n\nCette quantité de protéine par jour te permettera de maintenir ta masse musculaire avec ton activité quotidienne modérée."
        elif niveau_activite_genre == "Sportif d'endurance":
            interprétation = f"Protéine quotidienne recommandée : {result_nb_proteine:.0f} g/jour\n\nCette quantité de protéine par jour te permettera de soutenir la réparation et le renouvellement de tes muscles après l'entraînement."
        elif niveau_activite_genre == "Sportif de Musculation (maintien de la masse)":
            interprétation = f"Protéine quotidienne recommandée : {result_nb_proteine:.0f} g/jour\n\nCette quantité de protéine par jour te permettera de maintenir ta masse musculaire et optimiser ta récupération."
        else:
            interprétation = f"Protéine quotidienne recommandée : {result_nb_proteine:.0f} g/jour\n\nCette quantité de protéine par jour te permettera de maximiser la construction de tes muscles et atteindre ton objectif de volume."

        result.configure(text=interprétation)

    frame2 = ctk.CTkFrame(carte_connexion, fg_color="transparent")
    frame2.pack(expand=True, fill="both", pady=(2, 12), padx=12)
    button_check = ctk.CTkButton(frame2, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_nb_proteine())
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_back = ctk.CTkButton(frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), outils(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left")

def calculateur_imc(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_outil(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Calculateur IMC", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    boite1 = ctk.CTkFrame(app, fg_color="transparent")
    boite1.pack(side="top", pady=(5, 0), padx=10)
    carte_connexion = ctk.CTkFrame(boite1, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=(10, 5)) 

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: calcul_imc())

    poids_entry = ctk.CTkEntry(carte_connexion, placeholder_text="Poids (kg)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    poids_entry.pack(expand=True, fill="both", pady=(12, 2), padx=12)
    taille_entry = ctk.CTkEntry(carte_connexion, placeholder_text="Taille (cm)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    taille_entry.pack(expand=True, fill="both", pady=2, padx=12)

    cadre_result = ctk.CTkFrame(boite1, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)
    cadre_result.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=(5, 10))
    frame_result = ctk.CTkFrame(cadre_result, fg_color=couleur2, corner_radius=corner1)
    frame_result.pack(side="top", expand=True, fill="both", pady=12, padx=12)

    c_quoi_le_calculateur_imc = "C'est quoi le calculateur d'IMC ?\n\nLe calculateur d’IMC (Indice de Masse Corporelle) a pour objectif de te donner une estimation rapide de ta" \
                                " corpulence, en te situant dans des catégories comme 'maigreur', 'surpoids',... Les catégories peuvent être un peu difficiles à comprendre," \
                                " mais Sprintia te donne une interprétation qui rend les catégories plus simples à comprendre."
    result = ctk.CTkLabel(frame_result, 
                            text=f"{c_quoi_le_calculateur_imc}",
                            font=(font_principale, taille2), text_color=couleur1, wraplength=600, justify="left", anchor="w")
    result.pack(expand=True, fill="both", padx=15, pady=5)

    def calcul_imc():
        poids_avnt_conversion = poids_entry.get().strip().replace(',', '.').replace(' ', '').replace('_', '').replace('kg', '').replace('KG', '')
        taille_conversion_avt_conversion = taille_entry.get().strip().replace(',', '.').replace(' ', '').replace('_', '').replace('cm', '').replace('CM', '')
        if not poids_avnt_conversion:
            messagebox.showerror("Champs vide", "Le poids est obligatoire, il ne doit pas être vide !")
            return
        try:
            poids = float(poids_avnt_conversion)
            if poids <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur de conversion", "Le poids doit être un nombre supérieur à 0 !")
            return
        if not taille_conversion_avt_conversion:
            messagebox.showerror("Champs vide", "La taille est obligatoire, il ne doit pas être vide !")
            return
        try:
            taille_conversion = float(taille_conversion_avt_conversion)
            if taille_conversion <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur de conversion", "La taille doit être un nombre supérieur à 0 !")
            return
        
        taille = taille_conversion/100
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
                    
        result.configure(text=f"Ton IMC est : {imc:.2f} kg/m²\n\n{interprétation}")
    
    frame2 = ctk.CTkFrame(carte_connexion, fg_color="transparent")
    frame2.pack(expand=True, fill="both", pady=(2, 12), padx=12)
    button_check = ctk.CTkButton(frame2, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_imc())
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_back = ctk.CTkButton(frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), outils(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left")

def estimation_VO2MAX(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_outil(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)
    option_genre = ["Homme", "Femme"]

    Titre = ctk.CTkLabel(app ,text="Estimation VO2max", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    boite1 = ctk.CTkFrame(app, fg_color="transparent")
    boite1.pack(side="top", pady=(5, 0), padx=10)
    carte_connexion = ctk.CTkFrame(boite1, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=(10, 5)) 

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: calcul_VO2MAX())

    vma_entry = ctk.CTkEntry(carte_connexion, placeholder_text="VMA", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    vma_entry.pack(expand=True, fill="both", pady=(12, 2), padx=12)

    combo_genre = ctk.CTkComboBox(carte_connexion, values=option_genre, font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=280, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    combo_genre.pack(expand=True, fill="both", pady=2, padx=12)
    combo_genre.set("Genre")
    age_entry = ctk.CTkEntry(carte_connexion, placeholder_text="Âge", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    age_entry.pack(expand=True, fill="both", pady=2, padx=12)

    cadre_result = ctk.CTkFrame(boite1, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)
    cadre_result.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=(5, 10))
    frame_result = ctk.CTkFrame(cadre_result, fg_color=couleur2, corner_radius=corner1)
    frame_result.pack(side="top", expand=True, fill="both", pady=12, padx=12)

    c_quoi_le_predicteur_performance = "C'est quoi l'estimation VO2max ?\n\nLe VO2max représente le volume maximal d’oxygène que ton corps peut utiliser pendant un effort intense." \
                                        " L'estimation VO2max te permet de te donner une estimation de ton VO2max grâce à ta VMA." \
                                        " Mais, il va encore plus loin en te donnant une zone/catégorie et une interprétation en fonction de ton genre et de ton âge."
    result = ctk.CTkLabel(frame_result, 
                            text=f"{c_quoi_le_predicteur_performance}",
                            font=(font_principale, taille2), text_color=couleur1, wraplength=600, justify="left", anchor="w")
    result.pack(expand=True, fill="both", padx=15, pady=5)

    def calcul_VO2MAX():
        vma_avt_conversion = vma_entry.get().strip().replace(',', '.').replace(' ', '').replace('_', '').replace('vma', '').replace('VMA', '')
        genre = combo_genre.get().strip()
        age_avt_conversion = age_entry.get().strip().replace("âge", "").replace("ÂGE", "").replace("age", "").replace("AGE", "").replace(" ", "")
        if not vma_avt_conversion:
            messagebox.showerror("Champs vide", "La VMA est obligatoire, il ne doit pas être vide !")
            return
        if genre == "Genre":
            messagebox.showerror("Champs vide", "Le genre est obligatoire, il ne doit pas être vide !")
            return
        if not genre in option_genre:
            messagebox.showerror("Erreur", "Le genre n'est pas reconnu, séléctionne une option valide !")
            return
        if not age_avt_conversion:
            messagebox.showerror("Champs vide", "L'âge est obligatoire, il ne doit pas être vide !")
            return
        try:
            vma = float(vma_avt_conversion)
            if vma <= 0:
                raise ValueError
        except ValueError:    
            messagebox.showerror("Erreur de conversion", "La VMA doit être un nombre supérieur à 0 !")
            return
        try:
            age = int(age_avt_conversion)
            if age < 14:
                messagebox.showerror("Erreur", "Tu dois avoir 14 ans pour pouvoir utiliser cette fonctionnalité !")
                return
        except ValueError:  
            messagebox.showerror("Erreur de conversion", "L'âge doit être un nombre entier !")
            return
      
        vo2max = vma*3.5
        if genre == "Homme":
            if 14 <= age <= 17 :
                if vo2max >= 58:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 54 <= vo2max <= 58:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 50 <= vo2max <= 53:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 46 <= vo2max <= 49:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
            if 18 <= age <= 25 :
                if vo2max >= 56:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 52 <= vo2max <= 56:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 48 <= vo2max <= 51:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 44 <= vo2max <= 47:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
            if 26 <= age <= 35 :
                if vo2max >= 51:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 47 <= vo2max <= 51:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 43 <= vo2max <= 46:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 39 <= vo2max <= 42:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
            if 36 <= age <= 45 :
                if vo2max >= 45:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 41 <= vo2max <= 45:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 37 <= vo2max <= 40:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 33 <= vo2max <= 36:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
            if 46 <= age <= 55 :
                if vo2max >= 41:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 37 <= vo2max <= 41:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 33 <= vo2max <= 36:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 29 <= vo2max <= 32:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
            if 56 <= age <= 65 :
                if vo2max >= 37:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 33 <= vo2max <= 37:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 29 <= vo2max <= 32:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 25 <= vo2max <= 28:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
            if age >= 65 :
                if vo2max >= 33:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 29 <= vo2max <= 33:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 25 <= vo2max <= 28:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 21 <= vo2max <= 24:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
        elif genre == "Femme":
            if 14 <= age <= 17 :
                if vo2max >= 52:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 48 <= vo2max <= 52:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 44 <= vo2max <= 47:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 40 <= vo2max <= 43:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
            if 18 <= age <= 25 :
                if vo2max >= 48:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 44 <= vo2max <= 48:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 40 <= vo2max <= 43:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 36 <= vo2max <= 39:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
            if 26 <= age <= 35 :
                if vo2max >= 42:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 38 <= vo2max <= 42:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 34 <= vo2max <= 37:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 30 <= vo2max <= 33:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
            if 36 <= age <= 45 :
                if vo2max >= 37:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 33 <= vo2max <= 37:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 29 <= vo2max <= 32:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 25 <= vo2max <= 28:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
            if 46 <= age <= 55 :
                if vo2max >= 34:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 30 <= vo2max <= 34:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 26 <= vo2max <= 29:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 22 <= vo2max <= 25:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
            if 56 <= age <= 65 :
                if vo2max >= 30:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 26 <= vo2max <= 30:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 22 <= vo2max <= 25:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 18 <= vo2max <= 21:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
            if age >= 65 :
                if vo2max >= 27:
                    interprétation = "Supérieur, ton VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire."
                elif 23 <= vo2max <= 27:
                    interprétation = "Excellent, tu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                elif 19 <= vo2max <= 22:
                    interprétation = "Bon, ton VO2max est bonne pour ton âge, témoignant d'une condition physique solide."
                elif 15 <= vo2max <= 18:
                    interprétation = "Moyen, ton VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                else:
                    interprétation = "Faible, ton VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                
        message_en_plus = "Refais cette estimation tous les 2-3 mois pour voir ta progression."
        result.configure(text=f"VO2max estimée : {vo2max:.2f}\n\n{interprétation} {message_en_plus}")
    
    frame2 = ctk.CTkFrame(carte_connexion, fg_color="transparent")
    frame2.pack(expand=True, fill="both", pady=(2, 12), padx=12)
    button_check = ctk.CTkButton(frame2, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_VO2MAX())
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_back = ctk.CTkButton(frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), outils(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left")

def estimation_VMA(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_outil(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)
    option_test_vma = ["Test demi-Cooper (6 min) (Recommandé)", "Test Cooper (12 min)", "Test Luc Léger (2 km)", "Course de référence (moins précise)"]

    Titre = ctk.CTkLabel(app ,text="Estimation VMA", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    boite1 = ctk.CTkFrame(app, fg_color="transparent")
    boite1.pack(side="top", pady=(5, 0), padx=10)
    carte_connexion = ctk.CTkFrame(boite1, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=(10, 5)) 
    
    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: calcul_VMA())
    
    distance_entry = ctk.CTkEntry(carte_connexion, placeholder_text="Distance (km)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    distance_entry.pack_forget()
    temps_entry = ctk.CTkEntry(carte_connexion, placeholder_text="Durée", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    temps_entry.pack_forget()
    
    def remplissage_placeholder(choice):
        choice = test_spécifique.get()
        # On vide les champs pour les remplir ensuite
        distance_entry.configure(state="normal")
        temps_entry.configure(state="normal")
        distance_entry.delete(0, "end")
        temps_entry.delete(0, "end")

        # On remplit les champs en fonction du test sélectionné
        if choice == "Test demi-Cooper (6 min) (Recommandé)":
            temps_entry.insert(0, "6")
            temps_entry.configure(state="disabled")
            distance_entry.configure(placeholder_text="Distance (km)")
        elif choice == "Test Cooper (12 min)":
            temps_entry.insert(0, "12")
            temps_entry.configure(state="disabled")
            distance_entry.configure(placeholder_text="Distance (km)")
        elif choice == "Test Luc Léger (2 km)":
            distance_entry.insert(0, "2")
            distance_entry.configure(state="disabled")
            temps_entry.configure(placeholder_text="Temps (min)")
        else:
            temps_entry.configure(placeholder_text="Temps (min)")
            distance_entry.configure(placeholder_text="Distance (km)")

    test_spécifique = ctk.CTkComboBox(carte_connexion, values=option_test_vma,
                                    font=(font_principale, taille2), height=height_expressive, 
                                    state="readonly", border_width=border1, border_color=couleur_fond, button_color=couleur_fond, fg_color=couleur_fond,
                                    corner_radius=corner1, width=280, dropdown_fg_color=couleur_fond, dropdown_font=(font_principale, taille2),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1, 
                                    command=remplissage_placeholder)
    test_spécifique.pack(expand=True, fill="both", pady=(12, 2), padx=12)
    test_spécifique.set("Test")
    distance_entry.pack(expand=True, fill="both", pady=2, padx=12)
    temps_entry.pack(expand=True, fill="both", pady=2, padx=12)

    cadre_result = ctk.CTkFrame(boite1, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)
    cadre_result.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=(5, 10))
    frame_result = ctk.CTkFrame(cadre_result, fg_color=couleur2, corner_radius=corner1)
    frame_result.pack(side="top", expand=True, fill="both", pady=12, padx=12)

    tableau_frame = ctk.CTkScrollableFrame(app, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))

    c_quoi_la_vma = "C'est quoi la VMA ?\n\nLa Vitesse Maximale Aérobie (VMA) est la vitesse de course à laquelle ton corps atteint sa consommation maximale d'oxygène (VO2max). " \
                    "Connaître ta VMA te permet de mieux structurer tes entraînements, " \
                    "d'optimiser tes performances et de prévenir les blessures en évitant le surentraînement."
    result = ctk.CTkLabel(frame_result, text=f"{c_quoi_la_vma}",
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
        distance_avt_conversion = distance_entry.get().strip().replace(',', '.').replace(' ', '').replace('_', '').replace('km', '').replace('KM', '')
        if type_test_spécifique == "Test":
            messagebox.showerror("Erreur", "Tu dois sélectionner un test !")
            return
        if not type_test_spécifique in option_test_vma:
            messagebox.showerror("Erreur", "Le test de VMA n'est pas reconnu, séléctionne une option valide !")
            return
        if not distance_avt_conversion:
            messagebox.showerror("Champs vide", "La distance est obligatoire, elle ne peut pas être vide !")
            return
        try:
            distance = float(distance_avt_conversion)
        except ValueError:
            messagebox.showerror("Erreur", "La distance doit être un nombre (km)")
            return
        try:
            temps_autre = temps_entry.get().strip()
            if not temps_autre:
                messagebox.showerror("Erreur", "Le temps ne peut pas être vide !")
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
            if  3 >= distance >= 42.2 :
                messagebox.showerror("Erreur", "Pour une course de référence, la distance ne doit pas dépasser 42,20 km !")
                return
            if temps < 12:
                messagebox.showerror("Erreur", "Pour une course de référence, le temps doit être supérieur à 12 minutes !")
                return
            vitesse_moyenne = distance / (temps / 60) # Vitesse moyenne en km/h
            if 3.0 >= distance >= 3.5:
                coefficient_ajustement = 0.95
            elif 3.5001 >= distance >= 6.0:
                coefficient_ajustement = 0.92
            elif 6.0001 >= distance >= 12.0:
                coefficient_ajustement = 0.89
            elif 12.0001 >= distance >= 22.0:
                coefficient_ajustement = 0.82
            else:
                coefficient_ajustement = 0.77
            vma_estimée = vitesse_moyenne / coefficient_ajustement

        debut_zone1 = vma_estimée * 0.50
        fin_zone1 = vma_estimée * 0.60
        debut_zone2 = vma_estimée * 0.60
        fin_zone2 = vma_estimée * 0.75
        debut_zone3 = vma_estimée * 0.75
        fin_zone3 = vma_estimée * 0.85
        debut_zone4 = vma_estimée * 0.85
        fin_zone4 = vma_estimée * 0.95
        debut_zone5 = vma_estimée * 0.95

        servir_de_vma = "La VMA (Vitesse Maximale Aérobie) est un indicateur clé pour les coureurs et les sportifs d’endurance. Elle permet de définir des zones d’intensité pour varier tes entraînements (voir tableau). Réévalue ta VMA tous les 2-3 mois pour ajuster tes allures d’entraînement et voir si tu as progressé."
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
                                fg_color=couleur_fond, corner_radius=corner2, text_color=couleur1,
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
            label = ctk.CTkLabel(tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                text_color=couleur_text, wraplength=200)
            label.grid(row=row_index + 1, column=col_index, padx=15, pady=15, sticky="ew")

    frame2 = ctk.CTkFrame(carte_connexion, fg_color="transparent")
    frame2.pack(expand=True, fill="both", pady=(2, 12), padx=12)
    button_check = ctk.CTkButton(frame2, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_VMA())
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_back = ctk.CTkButton(frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), outils(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left")

def zone_cardiaque(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_outil(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Zones cardiaque", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    boite1 = ctk.CTkFrame(app, fg_color="transparent")
    boite1.pack(side="top", pady=(5, 0), padx=10)
    carte_connexion = ctk.CTkFrame(boite1, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=(10, 5)) 

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: calcul_zone())

    age_entry = ctk.CTkEntry(carte_connexion, placeholder_text="Âge", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    age_entry.pack(expand=True, fill="both", pady=(12, 2), padx=12)

    cadre_result = ctk.CTkFrame(boite1, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)
    cadre_result.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=(5, 10))
    frame_result = ctk.CTkFrame(cadre_result, fg_color=couleur2, corner_radius=corner1)
    frame_result.pack(side="top", expand=True, fill="both", pady=12, padx=12)

    c_quoi_les_zones_fc = "C'est quoi les Zones de fréquence cardiaque ?\n\nLes Zones cardiaque te permet de calculer tes zones de fréquence cardiaque" \
                        " en fonction de ton âge, pour optimiser ton entraînement. Les zones de fréquence cardiaque servent à optimiser " \
                        "ton entraînement en fonction de tes objectifs (endurance, perte de poids, performance,...)"
    result = ctk.CTkLabel(frame_result, 
                            text=f"{c_quoi_les_zones_fc}",
                            font=(font_principale, taille2), text_color=couleur1, wraplength=600, justify="left", anchor="w")
    result.pack(expand=True, fill="both", padx=15, pady=5)

    def calcul_zone():
        age_avt_conversion = age_entry.get().strip().replace("âge", "").replace("ÂGE", "").replace("age", "").replace("AGE", "").replace(" ", "")
        if not age_avt_conversion:
            messagebox.showerror("Champs vide", "L'âge est obligatoire, il ne peut pas être vide !")
            return
        try:
            age = int(age_avt_conversion)
            if age <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur de conversion", "L'âge doit être un nombre entier positif !")
            return
        
        fc_max = 220 - age
        debut_zone1 = fc_max*0.50
        fin_zone1 = fc_max*0.60
        Zone1 = f"Zone 1 : Récupération | {debut_zone1:.0f} bpm à {fin_zone1:.0f} bpm"
        debut_zone2 = fc_max*0.60
        fin_zone2 = fc_max*0.70
        Zone2 = f"Zone 2 : Endurance fondamentale | {debut_zone2:.0f} bpm à {fin_zone2:.0f} bpm"
        debut_zone3 = fc_max*0.70
        fin_zone3 = fc_max*0.80
        Zone3 = f"Zone 3 : Seuil aérobie | {debut_zone3:.0f} bpm à {fin_zone3:.0f} bpm"
        debut_zone4 = fc_max*0.80
        fin_zone4 = fc_max*0.90
        Zone4 = f"Zone 4 :  Seuil anaérobie | {debut_zone4:.0f} bpm à {fin_zone4:.0f} bpm"
        debut_zone5 = fc_max*0.90
        Zone5 = f"Zone 5 : Puissance maximale | {debut_zone5:.0f} bpm à {fc_max:.0f} bpm"
        FC_max = f"\nFréquence cardiaque maximum : {fc_max:.0f} bpm"

        result.configure(text=f"Tes Zones de Fréquence Cardiaque :\n\n{Zone1}\n{Zone2}\n{Zone3}\n{Zone4}\n{Zone5}\n{FC_max}")
    
    frame2 = ctk.CTkFrame(carte_connexion, fg_color="transparent")
    frame2.pack(expand=True, fill="both", pady=(2, 12), padx=12)
    button_check = ctk.CTkButton(frame2, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_zone())
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_back = ctk.CTkButton(frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), outils(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left")

def prédicteur_performance(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre):
    sidebar_outil(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre)

    Titre = ctk.CTkLabel(app ,text="Prédicteur de performance", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=10, pady=10)

    boite1 = ctk.CTkFrame(app, fg_color="transparent")
    boite1.pack(side="top", pady=(5, 0), padx=10)
    carte_connexion = ctk.CTkFrame(boite1, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=(10, 5)) 

    # On retire le raccourci 'Entrée' pour éviter une erreur
    app.unbind('<Return>')
    app.bind('<Return>', lambda event: calcul_temps())
    vma_entry = ctk.CTkEntry(carte_connexion, placeholder_text="VMA", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    vma_entry.pack(expand=True, fill="both", pady=(12, 2), padx=12)
    distance_entry = ctk.CTkEntry(carte_connexion, placeholder_text="Distance (km)", border_color=couleur_fond, fg_color=couleur_fond,
                                  height=height_expressive, font=(font_principale, taille2), corner_radius=corner1, placeholder_text_color =couleur1,
                                  text_color=couleur1, width=280)
    distance_entry.pack(expand=True, fill="both", pady=2, padx=12)

    cadre_result = ctk.CTkFrame(boite1, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)
    cadre_result.pack(side="left", expand=True, fill="both", pady=(10, 0), padx=(5, 10))
    frame_result = ctk.CTkFrame(cadre_result, fg_color=couleur2, corner_radius=corner1)
    frame_result.pack(side="top", expand=True, fill="both", pady=12, padx=12)

    c_quoi_le_predicteur_performance = "C'est quoi le Prédicteur de performance ?\n\nLe Prédicteur de performance te permet d'estimer ton temps de course en fonction de ta VMA et de la distance choisie." \
                                        " C'est un outil pratique pour évaluer tes performances potentielles avant une course." \
                                        " Mais, n'oublie pas que cette prédiction est une estimation basée sur la théorie et peut varier en fonction de nombreux facteurs le jour de la course !"
    result = ctk.CTkLabel(frame_result, 
                            text=f"{c_quoi_le_predicteur_performance}",
                            font=(font_principale, taille2), text_color=couleur1, wraplength=600, justify="left", anchor="w")
    result.pack(expand=True, fill="both", padx=15, pady=5)

    def calcul_temps():
        distance_avt_conversion = distance_entry.get().strip().replace(',', '.').replace(' ', '').replace('_', '').replace('km', '').replace('KM', '')
        vma_avt_conversion = vma_entry.get().strip().replace(',', '.').replace(' ', '').replace('_', '').replace('vma', '').replace('VMA', '')
        if not vma_avt_conversion:
            messagebox.showerror("Champs vide", "La VMA est obligatoire, elle ne doit pas être vide !")
            return
        if not distance_avt_conversion:
            messagebox.showerror("Champs vide", "La distance est obligatoire, elle ne doit pas être vide !")
            return
        try:
            vma = float(vma_avt_conversion)
            if vma <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur de conversion", "La distance doit être un nombre positif !")
            return
        try:
            distance = float(distance_avt_conversion)
            if distance <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur de conversion", "La distance doit être un nombre positif !")
            return
        if distance <= 2:
            vitesse_moyenne = vma*0.98
            temps_calculer = distance/vitesse_moyenne
            heure = int(temps_calculer)
            minute_calculer = (temps_calculer-heure)*60
            minutes = int(minute_calculer)
            seconde = (minute_calculer-minutes)*60
        elif 2 <= distance <= 3:
            vitesse_moyenne = vma*0.94
            temps_calculer = distance/vitesse_moyenne
            heure = int(temps_calculer)
            minute_calculer = (temps_calculer-heure)*60
            minutes = int(minute_calculer)
            seconde = (minute_calculer-minutes)*60
        elif 3 <= distance <= 6:
            vitesse_moyenne = vma*0.82
            temps_calculer = distance/vitesse_moyenne
            heure = int(temps_calculer)
            minute_calculer = (temps_calculer-heure)*60
            minutes = int(minute_calculer)
            seconde = (minute_calculer-minutes)*60
        elif 6 <= distance <= 12:
            vitesse_moyenne = vma*0.77
            temps_calculer = distance/vitesse_moyenne
            heure = int(temps_calculer)
            minute_calculer = (temps_calculer-heure)*60
            minutes = int(minute_calculer)
            seconde = (minute_calculer-minutes)*60
        elif 12 <= distance <= 25:
            vitesse_moyenne = vma*0.72
            temps_calculer = distance/vitesse_moyenne
            heure = int(temps_calculer)
            minute_calculer = (temps_calculer-heure)*60
            minutes = int(minute_calculer)
            seconde = (minute_calculer-minutes)*60
        elif 21.0975 <= distance <= 42.195:
            vitesse_moyenne = vma*0.62
            temps_calculer = distance/vitesse_moyenne
            heure = int(temps_calculer)
            minute_calculer = (temps_calculer-heure)*60
            minutes = int(minute_calculer)
            seconde = (minute_calculer-minutes)*60
        else:
            vitesse_moyenne = vma*0.55
            temps_calculer = distance/vitesse_moyenne
            heure = int(temps_calculer)
            minute_calculer = (temps_calculer-heure)*60
            minutes = int(minute_calculer)
            seconde = (minute_calculer-minutes)*60

        interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s\n\nCette prédiction peut te servir de base pour te fixer des objectifs précis et"\
                        " structurer tes séances : du fractionné pour améliorer ta vitesse ou des sorties longues pour améliorer ton endurance,..." \
                        " Réévalue toutes les 2-3 semaines pour affiner ton entraînement."

        result.configure(text=interpretation)
    
    frame2 = ctk.CTkFrame(carte_connexion, fg_color="transparent")
    frame2.pack(expand=True, fill="both", pady=(2, 12), padx=12)
    button_check = ctk.CTkButton(frame2, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_temps())
    button_check.pack(expand=True, fill="both", side="left", padx=(0, 2))
    button_back = ctk.CTkButton(frame2, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner1, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), outils(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_back.pack(expand=True, fill="both", side="left")

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
                                    command=lambda: [vider_fenetre(app), proteine_quotidienne(account_id, app, sidebar_outil, exercice, charge_entraînement, predicteur_temps, parametre)])
    button_avis.pack(side="left", padx=(0, 10))
