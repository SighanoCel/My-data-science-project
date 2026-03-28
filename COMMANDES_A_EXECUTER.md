# 📋 Commandes à Exécuter Étape par Étape

## Étape 1 : Créer un Personal Access Token sur GitHub

1. **Ouvrez votre navigateur** et allez sur :
   ```
   https://github.com/settings/tokens
   ```

2. **Cliquez sur** : "Generate new token" → "Generate new token (classic)"

3. **Remplissez** :
   - Note : `Portfolio deployment`
   - Expiration : Choisissez 90 days
   - **Cochez UNIQUEMENT `repo`** (tout en haut dans la liste)

4. **Cliquez sur** : "Generate token" (en bas)

5. **COPIEZ LE TOKEN** : Il commence par `ghp_...`
   - ⚠️ Copiez-le maintenant, vous ne le reverrez plus !

## Étape 2 : Dans PowerShell, exécutez ces commandes

### Commande 1 : Envoyer les fichiers
```powershell
git push origin main
```

### Quand Git demande :
- **Username** : `SighanoCel`
- **Password** : Collez le token (celui qui commence par `ghp_`)

### Commande 2 : Vérifier que ça a marché
```powershell
git log origin/main -1
```

---

## Alternative : Si le push ne fonctionne pas

Si après avoir entré le token, le push ne fonctionne toujours pas, essayez cette méthode :

### Méthode avec le token dans l'URL

Remplacez `VOTRE_TOKEN_ICI` par le token que vous avez copié :

```powershell
git remote set-url origin https://ghp_VOTRE_TOKEN_ICI@github.com/SighanoCel/My-data-science-project.git
git push origin main
```

**Exemple** (si votre token était `ghp_abc123xyz...`) :
```powershell
git remote set-url origin https://ghp_abc123xyz...@github.com/SighanoCel/My-data-science-project.git
git push origin main
```

---

## ✅ Comment savoir que ça a marché ?

1. Allez sur : https://github.com/SighanoCel/My-data-science-project
2. Vous devriez voir vos fichiers :
   - `index.html`
   - Dossier `css/` (cliquez pour voir `portfolio.css`)
   - Dossier `js/` (cliquez pour voir `portfolio.js`)
   - Toutes vos images (`.jpg`, `.png`)
   - `cv.pdf`
   - Les fichiers de documentation (`.md`)

---

## 🆘 Besoin d'aide ?

Si vous avez des problèmes :
1. Vérifiez que le token commence bien par `ghp_`
2. Vérifiez que vous copiez bien le token complet
3. Essayez la méthode alternative ci-dessus

**Dites-moi quand les fichiers apparaissent sur GitHub et je vous aiderai à activer GitHub Pages !**

