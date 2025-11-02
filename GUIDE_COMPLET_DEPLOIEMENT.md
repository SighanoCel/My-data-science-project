# Guide Complet - Déploiement du Portfolio sur GitHub Pages

## 📋 Étape 1 : Installer Git

Voir le fichier `INSTALLATION_GIT.md` pour les instructions détaillées.

**Résumé rapide :**
- Allez sur : https://git-scm.com/download/win
- Téléchargez et installez Git
- Redémarrez PowerShell après l'installation

## 📋 Étape 2 : Créer un compte GitHub (si vous n'en avez pas)

1. Allez sur : https://github.com
2. Cliquez sur "Sign up" (S'inscrire)
3. Créez votre compte avec :
   - Votre email
   - Un nom d'utilisateur (ex: `SighanoCel` ou `CelestinSighano`)
   - Un mot de passe
4. Confirmez votre email

## 📋 Étape 3 : Choisir un nom pour votre dépôt GitHub

### Qu'est-ce qu'un nom de dépôt ?

Le nom du dépôt est simplement le nom que vous donnez à votre projet sur GitHub.

### Suggestions de noms :

Vous pouvez choisir parmi ces options (ou créer le vôtre) :

1. **`portfolio`** - Simple et clair
2. **`celestin-portfolio`** - Avec votre prénom
3. **`portfolio-data-scientist`** - Descriptif
4. **`mon-portfolio`** - En français
5. **`sighano-portfolio`** - Avec votre nom de famille

**Important :** 
- Utilisez des lettres minuscules et des tirets (-) uniquement
- Pas d'espaces, pas d'accents, pas de caractères spéciaux
- Court et facile à retenir

### Exemple avec votre nom d'utilisateur GitHub

Si votre nom d'utilisateur GitHub est `SighanoCel`, et que vous choisissez le nom de dépôt `portfolio`, alors :
- URL du dépôt : `https://github.com/SighanoCel/portfolio`
- URL du site : `https://SighanoCel.github.io/portfolio/`

## 📋 Étape 4 : Créer le dépôt sur GitHub

1. Allez sur : https://github.com/new
2. **Repository name** : Tapez le nom choisi (ex: `portfolio`)
3. **Description** (optionnel) : "Portfolio personnel - Celestin Signe Sighano"
4. Choisissez **Public** (important pour GitHub Pages gratuit)
5. **NE COCHEZ PAS** :
   - ❌ "Add a README file"
   - ❌ "Add .gitignore"
   - ❌ "Choose a license"
   
   (On va tout créer manuellement)

6. Cliquez sur le bouton vert **"Create repository"**

7. **IMPORTANT :** Sur la page suivante, GitHub vous montrera des commandes. 
   - Copiez l'URL qui ressemble à : `https://github.com/VOTRE-USERNAME/NOM-DU-DEPOT.git`
   - Vous en aurez besoin pour les étapes suivantes !

## 📋 Étape 5 : Configurer Git pour la première fois

Ouvrez PowerShell et tapez ces commandes (remplacez avec VOS informations) :

```powershell
git config --global user.name "Votre Nom"
git config --global user.email "votre-email@example.com"
```

Exemple :
```powershell
git config --global user.name "Celestin Sighano"
git config --global user.email "sighanobob@yahoo.fr"
```

## 📋 Étape 6 : Envoyer vos fichiers sur GitHub

Dans PowerShell, naviguez vers votre dossier et exécutez :

```powershell
# Aller dans le dossier du projet
cd "C:\Users\LENOVO\Desktop\site test"

# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Créer le premier commit
git commit -m "Première version du portfolio"

# Ajouter votre dépôt GitHub (REMPLACEZ avec l'URL que vous avez copiée)
git remote add origin https://github.com/VOTRE-USERNAME/NOM-DU-DEPOT.git

# Renommer la branche en 'main'
git branch -M main

# Envoyer sur GitHub (GitHub vous demandera de vous connecter)
git push -u origin main
```

**Note :** Lors de `git push`, GitHub vous demandera vos identifiants. Utilisez votre nom d'utilisateur GitHub et un "Personal Access Token" (voir étape 7).

## 📋 Étape 7 : Créer un Personal Access Token (si demandé)

Si GitHub demande un mot de passe lors de `git push` :

1. Allez sur : https://github.com/settings/tokens
2. Cliquez sur "Generate new token" → "Generate new token (classic)"
3. Donnez un nom : "Portfolio deployment"
4. Cochez la case **`repo`** (donne accès aux dépôts)
5. Cliquez sur "Generate token" en bas
6. **COPIEZ LE TOKEN** (vous ne pourrez plus le voir après !)
7. Utilisez ce token comme mot de passe lors du `git push`

## 📋 Étape 8 : Activer GitHub Pages

1. Allez sur votre dépôt : `https://github.com/VOTRE-USERNAME/NOM-DU-DEPOT`
2. Cliquez sur l'onglet **"Settings"** (tout en haut à droite)
3. Dans le menu de gauche, cliquez sur **"Pages"**
4. Dans la section **"Source"** :
   - **Branch** : Sélectionnez `main`
   - **Folder** : Sélectionnez `/ (root)`
5. Cliquez sur **"Save"** (Enregistrer)

## 📋 Étape 9 : Accéder à votre site

1. Attendez 1-2 minutes pour que GitHub déploie votre site
2. Retournez dans **Settings** → **Pages**
3. Vous verrez un message vert avec l'URL de votre site :
   ```
   Your site is live at https://VOTRE-USERNAME.github.io/NOM-DU-DEPOT/
   ```
4. Cliquez sur ce lien pour voir votre site en ligne !

## 🔄 Mettre à jour votre site

Chaque fois que vous modifiez des fichiers :

```powershell
cd "C:\Users\LENOVO\Desktop\site test"
git add .
git commit -m "Description de vos modifications"
git push
```

Le site se mettra à jour automatiquement en quelques minutes.

## ❓ Questions fréquentes

**Q : Mon site affiche une erreur 404 ?**
R : Attendez quelques minutes, vérifiez que `index.html` est bien à la racine du dépôt.

**Q : Les images ne s'affichent pas ?**
R : Vérifiez que tous les fichiers images sont bien dans le dépôt et que les noms correspondent exactement (attention aux majuscules/minuscules).

**Q : Comment changer l'URL de mon site ?**
R : L'URL dépend du nom de votre dépôt. Pour la changer, créez un nouveau dépôt avec le nom souhaité ou renommez votre dépôt dans Settings.

## 📞 Besoin d'aide ?

Vérifiez que :
- ✅ Git est installé (`git --version` dans PowerShell)
- ✅ Vous avez un compte GitHub
- ✅ Votre dépôt est **Public**
- ✅ Le fichier `index.html` est à la racine
- ✅ GitHub Pages est activé dans Settings → Pages

