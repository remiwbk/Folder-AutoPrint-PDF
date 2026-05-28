import os
import subprocess
import shutil
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

# ======================
# CONFIGURATION GLOBALE
# ======================

# --- Visionneurs PDF ---
VISIONNEURS = {
    "SumatraPDF": [
        os.path.join(os.environ['LOCALAPPDATA'], 'SumatraPDF', 'SumatraPDF.exe'),
        os.path.join(os.environ['ProgramFiles'], 'SumatraPDF', 'SumatraPDF.exe'),
        os.path.join(os.environ['ProgramFiles(x86)'], 'SumatraPDF', 'SumatraPDF.exe'),
    ],
    "Adobe Reader": [
        os.path.join(os.environ['ProgramFiles'], 'Adobe', 'Acrobat Reader DC', 'Reader', 'AcroRd32.exe'),
        os.path.join(os.environ['ProgramFiles(x86)'], 'Adobe', 'Acrobat Reader DC', 'Reader', 'AcroRd32.exe'),
    ],
    "Foxit Reader": [
        os.path.join(os.environ['ProgramFiles(x86)'], 'Foxit Software', 'Foxit PDF Reader', 'FoxitPDFReader.exe'),
    ],
}

# --- Liens de téléchargement ---
LIENS_TELECHARGEMENT = {
    "SumatraPDF": "https://www.sumatrapdfreader.org/free-pdf-reader",
    "Adobe Reader": "https://get.adobe.com/fr/reader/",
    "Foxit Reader": "https://www.foxit.com/pdf-reader/",
}

# ======================
# FONCTIONS UTILITAIRES
# ======================

def trouver_fichier(chemins_possibles):
    """Trouve le premier fichier existant dans une liste de chemins."""
    for chemin in chemins_possibles:
        if os.path.isfile(chemin):
            return chemin
    return None

def lister_imprimantes():
    """Liste les imprimantes disponibles avec WMIC (sans win32print)."""
    try:
        result = subprocess.run(
            ["wmic", "printer", "get", "name"],
            capture_output=True,
            text=True,
            check=True
        )
        # Nettoie la sortie (supprime les lignes vides et "Name")
        imprimantes = [
            line.strip() for line in result.stdout.split("\n")
            if line.strip() and line.strip().lower() != "name"
        ]
        return imprimantes if imprimantes else ["Imprimante par défaut"]
    except:
        return ["Imprimante par défaut"]

def telecharger_visionneur(visionneur):
    """Ouvre le lien de téléchargement du visionneur spécifié."""
    if visionneur in LIENS_TELECHARGEMENT:
        webbrowser.open(LIENS_TELECHARGEMENT[visionneur])
    else:
        messagebox.showwarning("Avertissement", f"Aucun lien de téléchargement connu pour {visionneur}.")

# ======================
# FONCTION D'IMPRESSION
# ======================

def imprimer_pdfs(dossier, archiver, nom_imprimante, visionneur):
    """
    Imprime tous les PDF d'un dossier avec le visionneur et l'imprimante spécifiés.
    """
    # Trouver le visionneur
    visionneur_chemin = trouver_fichier(VISIONNEURS[visionneur])
    if not visionneur_chemin:
        messagebox.showerror(
            "Erreur",
            f"{visionneur} non trouvé.\nSouhaitez-vous le télécharger ?"
        )
        if messagebox.askyesno("Téléchargement", f"Télécharger {visionneur} ?"):
            telecharger_visionneur(visionneur)
        return False

    # Préparer le dossier d'archivage
    dossier_archive = os.path.join(dossier, "Archives")
    if archiver and not os.path.isdir(dossier_archive):
        os.makedirs(dossier_archive)

    # Lister les PDF
    fichiers_pdf = [
        f for f in os.listdir(dossier)
        if f.lower().endswith('.pdf') and os.path.isfile(os.path.join(dossier, f))
    ]

    if not fichiers_pdf:
        messagebox.showwarning("Avertissement", f"Aucun PDF trouvé dans {dossier}.")
        return False

    # Imprimer chaque PDF
    for fichier in fichiers_pdf:
        chemin_pdf = os.path.join(dossier, fichier)
        try:
            # Commande selon le visionneur
            if visionneur == "SumatraPDF":
                if nom_imprimante:
                    commande = f'"{visionneur_chemin}" -print-to "{nom_imprimante}" "{chemin_pdf}"'
                else:
                    commande = f'"{visionneur_chemin}" -print-to-default "{chemin_pdf}"'
            elif visionneur in ["Adobe Reader", "Foxit Reader"]:
                if nom_imprimante:
                    commande = f'"{visionneur_chemin}" /t "{chemin_pdf}" "{nom_imprimante}"'
                else:
                    commande = f'"{visionneur_chemin}" /t "{chemin_pdf}"'
            else:
                commande = f'"{visionneur_chemin}" "{chemin_pdf}"'

            subprocess.run(
                commande,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(1)

            # Archiver si demandé
            if archiver:
                shutil.move(chemin_pdf, os.path.join(dossier_archive, fichier))

        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de l'impression de {fichier} : {e}")
            return False

    messagebox.showinfo("Succès", "Tous les PDF ont été imprimés avec succès !")
    return True

# ======================
# INTERFACE GRAPHIQUE
# ======================

class AppImpressionPDF:
    def __init__(self, root):
        self.root = root
        self.root.title("Impression PDF Automatique")
        self.root.geometry("600x400")

        # Variables
        self.dossier_pdf = tk.StringVar(value=os.path.expanduser("~\\Documents"))
        self.archiver = tk.BooleanVar(value=True)
        self.visionneur = tk.StringVar(value="SumatraPDF")
        self.imprimante = tk.StringVar()

        # Interface
        self.creer_interface()

        # Remplir les listes
        self.remplir_imprimantes()
        self.remplir_visionneurs()

    def creer_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)

        # --- Dossier ---
        ttk.Label(main_frame, text="Dossier contenant les PDF :").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable=self.dossier_pdf, width=50).grid(row=0, column=1, pady=5)
        ttk.Button(main_frame, text="Parcourir...", command=self.choisir_dossier).grid(row=0, column=2, pady=5, padx=5)

        # --- Visionneur ---
        ttk.Label(main_frame, text="Visionneur PDF :").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_visionneur = ttk.Combobox(main_frame, textvariable=self.visionneur, state="readonly")
        self.combo_visionneur.grid(row=1, column=1, pady=5, sticky="ew")

        # --- Imprimante ---
        ttk.Label(main_frame, text="Imprimante :").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_imprimante = ttk.Combobox(main_frame, textvariable=self.imprimante, state="readonly")
        self.combo_imprimante.grid(row=2, column=1, pady=5, sticky="ew")

        # --- Archivage ---
        ttk.Checkbutton(
            main_frame,
            text="Archiver les PDF après impression (évite les doublons)",
            variable=self.archiver
        ).grid(row=3, column=0, columnspan=3, pady=10, sticky="w")

        # --- Bouton d'impression ---
        ttk.Button(
            main_frame,
            text="🖨️ Lancer l'impression",
            command=self.lancer_impression
        ).grid(row=4, column=0, columnspan=3, pady=20)

        # Configure la grille
        main_frame.columnconfigure(1, weight=1)

    def remplir_imprimantes(self):
        imprimantes = lister_imprimantes()
        self.combo_imprimante["values"] = imprimantes
        if imprimantes:
            self.imprimante.set(imprimantes[0])

    def remplir_visionneurs(self):
        self.combo_visionneur["values"] = list(VISIONNEURS.keys())
        self.combo_visionneur.current(0)  # Sélectionne SumatraPDF par défaut

    def choisir_dossier(self):
        dossier = filedialog.askdirectory(title="Sélectionner le dossier contenant les PDF")
        if dossier:
            self.dossier_pdf.set(dossier)

    def lancer_impression(self):
        dossier = self.dossier_pdf.get()
        archiver = self.archiver.get()
        imprimante = self.imprimante.get()
        visionneur = self.visionneur.get()

        # Vérifie que le dossier existe
        if not os.path.isdir(dossier):
            messagebox.showerror("Erreur", f"Le dossier '{dossier}' n'existe pas.")
            return

        # Confirme avant impression
        if messagebox.askyesno(
            "Confirmation",
            f"Imprimer les PDF depuis :\n{dossier}\n\n"
            f"Visionneur : {visionneur}\n"
            f"Imprimante : {imprimante}\n"
            f"Archiver : {'Oui' if archiver else 'Non'}\n\n"
            "Voulez-vous continuer ?"
        ):
            imprimer_pdfs(dossier, archiver, imprimante, visionneur)

# ======================
# EXÉCUTION
# ======================

if __name__ == "__main__":
    root = tk.Tk()
    app = AppImpressionPDF(root)
    root.mainloop()