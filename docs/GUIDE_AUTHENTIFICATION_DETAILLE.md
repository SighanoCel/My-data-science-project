# 🔐 Guide Détaillé : Authentification GitHub et Envoi des Fichiers

## Pourquoi avez-vous besoin d'un token ?

GitHub ne permet plus d'utiliser votre mot de passe pour Git depuis 2021. Il faut créer un **Personal Access Token**.

## Étape 1 : Créer un Personal Access Token

### Méthode détaillée :

1. **Allez sur** : https://github.com/settings/tokens
   - Connectez-vous si ce n'est pas déjà fait

2. **Cliquez sur** : 
   - "Generate new token" (générer un nouveau token)
   - Puis "Generate new token (classic)"

3. **Configurez le token** :
   - **Note** : Donnez un nom descriptif comme "Portfolio deployment" ou "Git push"
   - **Expiration** : Choisissez "90 days" ou "No expiration" selon votre préférence

4. **Permissions** : 
   - **Cochez UNIQUEMENT la case `repo`**
   - Cette case coche automatiquement toutes les sous-permissions nécessaires
   - ⚠️ N'allez pas dans les détails, cochez juste `repo` en haut

5. **Générer** :
   - Faites défiler jusqu'en bas
   - Cliquez sur le bouton vert **"Generate token"**

6. **⚠️ IMPORTANT : Copiez le token IMMÉDIATEMENT !**
   - Il ressemble à : `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Il commence par `ghp_`
   - **Vous ne pourrez plus le voir après avoir quitté la page !**
   - Sauvegardez-le quelque part de sûr

## Étape 2 : Utiliser le token pour envoyer les fichiers

### Dans PowerShell, exécutez :

```powershell
git push origin main
```

### Quand Git vous demande :

1. **Username** : Tapez `SighanoCel` (votre nom d'utilisateur GitHub)
   - Appuyez sur Entrée

2. **Password** : 
   - **NE TAPEZ PAS votre mot de passe GitHub**
   - **Collez le token** que vous avez copié (celui qui commence par `ghp_`)
   - ⚠️ Quand vous collez le token, vous ne verrez rien s'afficher (c'est normal pour la sécurité)
   - Appuyez sur Entrée

3. **Attendez** : Le push devrait maintenant fonctionner !

## Étape 3 : Vérifier que ça a marché

1. Allez sur : https://github.com/SighanoCel/My-data-science-project
2. Rafraîchissez la page (F5)
3. Vous devriez maintenant voir :
   - `index.html`
   - Dossier `css/`
   - Dossier `js/`
   - Toutes vos images
   - Votre CV (cv.pdf)
   - ET vos notebooks Jupyter existants

## 🆘 Si ça ne fonctionne toujours pas

### Vérifiez que vous utilisez bien le token :
- Le token commence par `ghp_`
- C'est bien le token que vous copiez, pas votre mot de passe
- Il n'y a pas d'espaces avant/après quand vous le collez

### Essayez une autre méthode :
Utilisez l'URL avec le token dans la commande :

```powershell
git remote set-url origin https://ghp_VOTRE_TOKEN@github.com/SighanoCel/My-data-science-project.git
git push origin main
```

(Remplacez `VOTRE_TOKEN` par le token que vous avez copié)

## 📝 Alternative : GitHub Desktop

Si vous préférez une interface graphique :
1. Téléchargez : https://desktop.github.com/
2. Installez GitHub Desktop
3. Connectez-vous avec votre compte GitHub
4. Ajoutez votre dépôt local
5. Faites "Publish repository" ou "Push origin"

---

**Une fois que les fichiers sont sur GitHub, dites-moi et je vous aiderai à activer GitHub Pages !**

