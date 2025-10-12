from app_ressource import *

def sidebar_exercice(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre):
    boite1 = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur_fond)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur_fond, hover_color=couleur2_hover, height=button_height, width=button_width, text_color=couleur1,
                                    anchor="w", command=lambda: [vider_fenetre(app), exercice(account_id)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), charge_entraînement(account_id)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outils", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)
def sidebar_performance(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre):
    boite1 = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur_fond)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), exercice(account_id)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur_fond, hover_color=couleur2_hover, height=button_height, width=button_width, text_color=couleur1,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), charge_entraînement(account_id)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outils", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)
def sidebar_outil(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre):
    boite1 = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur_fond)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), exercice(account_id)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), charge_entraînement(account_id)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outils", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur_fond, hover_color=couleur2_hover, height=button_height, width=button_width, text_color=couleur1,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)
def sidebar_paramètre(account_id, app, exercice, charge_entraînement, predicteur_temps, parametre):
    boite1 = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur_fond)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), exercice(account_id)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), charge_entraînement(account_id)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outils", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur_fond, hover_color=couleur2_hover, height=button_height, width=button_width, text_color=couleur1,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)
