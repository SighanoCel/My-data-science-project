# Guide de déploiement rapide - GitHub Pages

## 🚀 Commandes à exécuter dans PowerShell

### 1. Vérifier que Git est installé
```powershell
git --version
```
Si Git n'est pas installé, téléchargez-le depuis : https://git-scm.com/download/win

### 2. Initialiser le dépôt Git (si pas déjà fait)
```powershell
cd "C:\Users\LENOVO\Desktop\site test"
git init
```

### 3. Créer le dépôt sur GitHub

1. Allez sur https://github.com/new
2. Nom du dépôt : `portfolio` (ou un autre nom de votre choix)
3. Choisissez **Public**
4. **NE COCHEZ PAS** "Initialize with README"
5. Cliquez sur **Create repository**

### 4. Connecter votre dossier local à GitHub

**Remplacez `VOTRE-USERNAME` et `NOM-DU-DEPOT` dans les commandes suivantes :**

```powershell
# Ajouter tous les fichiers
git add .

# Créer le premier commit
git commit -m "Première version du portfolio"

# Ajouter l'origine GitHub (REMPLACEZ les valeurs ci-dessous)
git remote add origin https://github.com/VOTRE-USERNAME/NOM-DU-DEPOT.git

# Renommer la branche en main
git branch -M main

# Envoyer sur GitHub
git push -u origin main
```

### 5. Activer GitHub Pages

1. Allez sur votre dépôt GitHub : `https://github.com/VOTRE-USERNAME/NOM-DU-DEPOT`
2. Cliquez sur **Settings** (Paramètres)
3. Menu gauche → **Pages**
4. **Source** : Sélectionnez `main` et `/ (root)`
5. Cliquez sur **Save**

### 6. Accéder à votre site

Attendez 1-2 minutes, puis votre site sera disponible à :
```
https://VOTRE-USERNAME.github.io/NOM-DU-DEPOT/
```

## 🔄 Mettre à jour le site plus tard

Quand vous modifiez des fichiers, utilisez :

```powershell
git add .
git commit -m "Description de vos modifications"
git push
```

Le site se mettra à jour automatiquement en quelques minutes !

## ⚠️ Important

- Assurez-vous que tous les fichiers (images, CSS, JS, PDF) sont bien présents dans le dossier
- Le fichier `index.html` doit être à la racine
- Vérifiez que les chemins dans le HTML correspondent aux noms de vos fichiers

