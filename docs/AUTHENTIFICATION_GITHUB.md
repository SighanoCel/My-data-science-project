# 🔐 Authentification GitHub pour le Push

## Pourquoi cette étape est nécessaire ?

GitHub ne permet plus d'utiliser votre mot de passe pour Git. Il faut créer un **Personal Access Token**.

## Étape 1 : Créer un Personal Access Token

1. Allez sur : **https://github.com/settings/tokens**
2. Cliquez sur **"Generate new token"** → **"Generate new token (classic)"**
3. Donnez un nom : **"Portfolio deployment"** (ou un autre nom)
4. Sélectionnez la durée : **90 days** (ou **No expiration** si vous préférez)
5. **Cochez la case `repo`** (c'est la plus importante - donne accès aux dépôts)
   - Si vous cochez `repo`, toutes les sous-options seront cochées automatiquement
6. Faites défiler et cliquez sur **"Generate token"** (en bas de la page)
7. **⚠️ IMPORTANT : COPIEZ LE TOKEN MAINTENANT !** 
   - Il ressemble à : `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Vous ne pourrez plus le voir après !

## Étape 2 : Utiliser le token lors du push

Quand vous faites `git push`, GitHub vous demandera :
- **Username** : `SighanoCel` (votre nom d'utilisateur GitHub)
- **Password** : Collez le **token** que vous avez copié (pas votre mot de passe !)

## Étape 3 : Réessayer le push

Dans PowerShell, exécutez à nouveau :

```powershell
git push origin main
```

Quand il demande votre mot de passe, utilisez le token.

---

## Alternative : Utiliser GitHub Desktop

Si vous préférez une interface graphique, téléchargez **GitHub Desktop** :
- https://desktop.github.com/
- Il gère l'authentification automatiquement
- Vous pouvez faire glisser-déposer vos fichiers

---

## Vérifier que le push a réussi

Après le push, allez sur :
**https://github.com/SighanoCel/My-data-science-project**

Vous devriez voir tous vos fichiers du portfolio (index.html, css/, js/, images, etc.)

