# 🚀 Étapes Simples pour Mettre Votre Site en Ligne

## ÉTAPE 1 : Installer Git ⬇️

1. Ouvrez votre navigateur
2. Allez sur : **https://git-scm.com/download/win**
3. Cliquez sur le bouton de téléchargement
4. Une fois téléchargé, double-cliquez sur le fichier `.exe`
5. Cliquez sur "Next" plusieurs fois (gardez les options par défaut)
6. Cliquez sur "Install" puis "Finish"

✅ **Test :** Ouvrez PowerShell et tapez `git --version`. Si vous voyez un numéro, c'est bon !

---

## ÉTAPE 2 : Créer un compte GitHub 📝

1. Allez sur : **https://github.com**
2. Cliquez sur "Sign up" (S'inscrire)
3. Créez votre compte :
   - Nom d'utilisateur : (ex: `SighanoCel` ou `CelestinSighano`)
   - Email : votre email
   - Mot de passe : créez un mot de passe
4. Confirmez votre email

---

## ÉTAPE 3 : Créer le dépôt GitHub 🆕

1. Une fois connecté sur GitHub, cliquez sur le bouton **"+"** en haut à droite
2. Cliquez sur **"New repository"**

3. Sur la page de création :
   - **Repository name** : Tapez `portfolio` (ou un autre nom simple)
   - **Description** : (optionnel) "Mon portfolio personnel"
   - Cochez **Public** (important pour l'hébergement gratuit)
   - **NE COCHEZ RIEN D'AUTRE** (pas de README, pas de .gitignore)
   
4. Cliquez sur le bouton vert **"Create repository"**

5. **IMPORTANT :** Copiez l'URL qui apparaît. Elle ressemble à :
   ```
   https://github.com/VOTRE-USERNAME/portfolio.git
   ```
   Vous en aurez besoin à l'étape 5 !

---

## ÉTAPE 4 : Configurer Git (première fois) ⚙️

Ouvrez PowerShell et tapez (remplacez avec vos vraies informations) :

```powershell
git config --global user.name "Celestin Sighano"
git config --global user.email "sighanobob@yahoo.fr"
```

---

## ÉTAPE 5 : Envoyer vos fichiers sur GitHub 📤

Dans PowerShell, exécutez ces commandes une par une :

```powershell
# 1. Aller dans le dossier de votre site
cd "C:\Users\LENOVO\Desktop\site test"

# 2. Initialiser Git
git init

# 3. Ajouter tous les fichiers
git add .

# 4. Créer un "sauvegarde" de vos fichiers
git commit -m "Première version du portfolio"

# 5. Connecter à GitHub (REMPLACEZ l'URL avec celle que vous avez copiée)
git remote add origin https://github.com/VOTRE-USERNAME/portfolio.git

# 6. Renommer la branche
git branch -M main

# 7. Envoyer sur GitHub
git push -u origin main
```

**Si GitHub demande vos identifiants :**
- Nom d'utilisateur : votre nom d'utilisateur GitHub
- Mot de passe : créez un "Personal Access Token" (voir guide complet)

---

## ÉTAPE 6 : Activer GitHub Pages 🌐

1. Sur GitHub, allez dans votre dépôt (vous devriez voir tous vos fichiers)
2. Cliquez sur **"Settings"** (en haut à droite du dépôt)
3. Dans le menu de gauche, cliquez sur **"Pages"**
4. Dans **"Source"** :
   - Sélectionnez **Branch : main**
   - Sélectionnez **Folder : / (root)**
5. Cliquez sur **"Save"** (Enregistrer)

---

## ÉTAPE 7 : Voir votre site en ligne ! 🎉

1. Attendez 1-2 minutes
2. Retournez dans **Settings → Pages**
3. Vous verrez un message vert avec votre URL :
   ```
   Your site is live at https://VOTRE-USERNAME.github.io/portfolio/
   ```
4. Cliquez sur ce lien pour voir votre site !

---

## 🔄 Pour mettre à jour votre site plus tard

Quand vous modifiez des fichiers, refaites seulement :

```powershell
cd "C:\Users\LENOVO\Desktop\site test"
git add .
git commit -m "Mise à jour du site"
git push
```

---

## 💡 Exemple concret

Si votre nom d'utilisateur GitHub est **`SighanoCel`** et vous créez un dépôt nommé **`portfolio`** :

- Dépôt GitHub : `https://github.com/SighanoCel/portfolio`
- Site en ligne : `https://SighanoCel.github.io/portfolio/`

---

## ❓ Besoin d'aide ?

Consultez le fichier `GUIDE_COMPLET_DEPLOIEMENT.md` pour plus de détails sur chaque étape.

