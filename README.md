
# 🖨️ Folder-AutoPrint-PDF

**Outil léger d'impression automatique de PDF avec interface graphique**

Un script Python **portable et sans dépendances externes** pour imprimer automatiquement des fichiers PDF via **SumatraPDF**, **Adobe Reader** ou **Foxit Reader**.
Idéal pour automatiser des tâches d'impression répétitives en entreprise ou à la maison.

---

## ✨ Fonctionnalités

✅ **Interface graphique intuitive** (Tkinter)
✅ **Mémorisation automatique** des paramètres (dossier, visionneur, imprimante, archivage)
✅ **Lanceur Windows intégré** (`lancer_impression.bat`) – **sans fenêtre CMD**
✅ **100% portable** : 2 fichiers seulement (`pdf-print.py` + `lancer_impression.bat`)
✅ **Aucune installation requise** (si Python est déjà installé)
✅ **Logs intégrés** pour le suivi des impressions
✅ **Compatibilité** : Windows 10/11

---

## 📦 Prérequis

- **Python 3.11+** (ou [Python Portable](https://winpython.github.io/) pour une version sans installation)
- **Un visionneur PDF** (recommandé : [SumatraPDF](https://www.sumatrapdfreader.org/free-pdf-reader))

---

## 🚀 Installation et utilisation

### 1️⃣ Télécharger le projet
- **Cloner le dépôt** :
  ```bash
  git clone https://github.com/remiwbk/Folder-AutoPrint-PDF.git
  cd Folder-AutoPrint-PDF
  ```
- **Ou télécharger le ZIP** :
  [Télécharger le ZIP](https://github.com/remiwbk/Folder-AutoPrint-PDF/archive/refs/heads/main.zip)

### 2️⃣ Lancer l'outil
- **Double-cliquez sur `lancer_impression.bat`** (méthode recommandée).
- **Ou via la ligne de commande** :
  ```bash
  python pdf-print.py
  ```

---
## 📂 Structure du projet
```
Folder-AutoPrint-PDF/
├── pdf-print.py          # Script principal (interface + logique)
├── lancer_impression.bat # Lanceur Windows (sans fenêtre CMD)
├── LICENSE               # Licence MIT
└── README.md             # Documentation
```
> *Aucun autre fichier requis : tout est intégré dans ces 2 fichiers !*

---
## 🛠️ Configuration

### Premier lancement
1. Placez vos fichiers PDF dans un dossier (ex: `C:\MesPDF`).
2. Lancez `lancer_impression.bat`.
3. Sélectionnez :
   - Le **dossier** contenant les PDF.
   - Le **visionneur PDF** (SumatraPDF recommandé).
   - L'**imprimante** (par défaut : imprimante par défaut du système).
   - L'option **d'archivage** (coché par défaut).

### Paramètres mémorisés
L'outil **sauvegarde automatiquement** vos choix dans un fichier `config.ini` (créé automatiquement) pour les réutiliser lors des prochains lancements.

---
## 📜 Exemple de fichier `config.ini` (généré automatiquement)
```ini
[DEFAULT]
dossier = C:\Users\Utilisateur\Documents\MesPDF
archiver = True
visionneur = SumatraPDF
imprimante = HP LaserJet Pro M404n
```

---
## 🔧 Personnalisation

### Changer le visionneur par défaut
Modifiez la variable `VISIONNEURS` dans `pdf-print.py` pour ajouter ou modifier un visionneur :
```python
VISIONNEURS = {
    "SumatraPDF": [".\\SumatraPDF.exe"],  # Chemin relatif
    "MonVisionneur": ["C:\\Chemin\\Vers\\MonVisionneur.exe"],
    ...
}
```

### Désactiver les logs
Supprimez ou commentez les appels à `logging` dans le code.

---
## 🤝 Contribuer
Les contributions sont les bienvenues !

1. **Fork** le projet.
2. Créez une **branche** (`git checkout -b feature/ma-fonctionnalité`).
3. **Commit** vos changements (`git commit -m 'Ajout de ma fonctionnalité'`).
4. **Push** vers la branche (`git push origin feature/ma-fonctionnalité`).
5. Ouvrez une **Pull Request**.

---
## 📄 Licence
Ce projet est sous licence **MIT** – voir le fichier [LICENSE](LICENSE) pour plus de détails.
---