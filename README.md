# Portfolio - Celestin Signe Sighano

Site portfolio personnel de Celestin Signe Sighano, Junior Data Scientist.

## 🌐 Hébergement sur GitHub Pages

Ce site est hébergé gratuitement sur GitHub Pages.

### URL du site

Une fois déployé, votre site sera accessible à l'adresse :
- `https://[votre-username].github.io/[nom-du-depot]/`

## 📋 Instructions pour déployer sur GitHub Pages

### Étape 1 : Créer un dépôt sur GitHub

1. Allez sur [GitHub.com](https://github.com) et connectez-vous
2. Cliquez sur le bouton "+" en haut à droite et sélectionnez "New repository"
3. Donnez un nom à votre dépôt (par exemple : `portfolio` ou `celestin-portfolio`)
4. Choisissez "Public" (GitHub Pages est gratuit pour les dépôts publics)
5. **NE COCHEZ PAS** "Initialize this repository with a README" (car vous avez déjà les fichiers)
6. Cliquez sur "Create repository"

### Étape 2 : Initialiser Git et envoyer les fichiers

Ouvrez votre terminal PowerShell dans le dossier du projet et exécutez les commandes suivantes :

```bash
# Initialiser Git (si ce n'est pas déjà fait)
git init

# Ajouter tous les fichiers
git add .

# Créer un commit
git commit -m "Initial commit - Portfolio site"

# Ajouter le dépôt GitHub comme origine (remplacez [votre-username] et [nom-du-depot])
git remote add origin https://github.com/[votre-username]/[nom-du-depot].git

# Renommer la branche principale en 'main' (si nécessaire)
git branch -M main

# Envoyer les fichiers sur GitHub
git push -u origin main
```

### Étape 3 : Activer GitHub Pages

1. Allez sur votre dépôt GitHub
2. Cliquez sur "Settings" (Paramètres) dans le menu en haut
3. Dans le menu de gauche, cliquez sur "Pages"
4. Dans la section "Source", sélectionnez :
   - Branch : `main`
   - Folder : `/ (root)` ou `/docs` si vos fichiers sont dans un dossier docs
5. Cliquez sur "Save" (Enregistrer)

### Étape 4 : Attendre le déploiement

- GitHub va construire et déployer votre site (cela peut prendre quelques minutes)
- Une fois terminé, vous verrez un message vert avec l'URL de votre site
- Votre site sera accessible à l'adresse : `https://[votre-username].github.io/[nom-du-depot]/`

## 📁 Structure du projet

```
.
├── index.html              # Page principale (requis pour GitHub Pages)
├── css/
│   └── portfolio.css      # Feuille de style principale
├── js/
│   └── portfolio.js       # Scripts JavaScript
├── cv.pdf                 # CV téléchargeable
├── *.jpg                  # Images du portfolio
└── README.md              # Ce fichier
```

## 🔄 Mettre à jour le site

Pour mettre à jour votre site après avoir modifié des fichiers :

```bash
# Ajouter les fichiers modifiés
git add .

# Créer un commit avec un message descriptif
git commit -m "Description des modifications"

# Envoyer les modifications sur GitHub
git push
```

GitHub Pages mettra automatiquement à jour le site en quelques minutes.

## 📝 Notes importantes

- Le fichier `index.html` doit être à la racine du dépôt (ou dans le dossier spécifié dans les paramètres GitHub Pages)
- Tous les chemins relatifs (CSS, JS, images) doivent être corrects
- Les images doivent être incluses dans le dépôt pour être accessibles
- GitHub Pages met à jour automatiquement le site à chaque push sur la branche `main`

## 🆘 Dépannage

- **Le site ne s'affiche pas** : Vérifiez que le fichier `index.html` existe à la racine
- **Les images ne s'affichent pas** : Vérifiez les noms de fichiers (sensible à la casse sur certains systèmes)
- **Le CSS ne fonctionne pas** : Vérifiez le chemin dans `index.html` : `href="css/portfolio.css"`
- **Erreur 404** : Attendez quelques minutes après le premier déploiement

## 📧 Contact

- Email : sighanobob@yahoo.fr
- LinkedIn : [Celestin Signe Sighano](https://www.linkedin.com/in/celestin-signe-sighano-52974a37/)
- GitHub : [SighanoCel](https://github.com/SighanoCel)

