# My-data-science-project

Dépôt personnel de **Celestin Signe Sighano** (Junior Data Scientist) : portfolio web sur GitHub Pages, notebooks de projets, documents et ressources associés.

## Contenu

- **Site portfolio** : page d’accueil `index.html` à la racine (compatible GitHub Pages sans configuration supplémentaire).
- **Projets** : notebooks Jupyter dans `notebooks/` (régression, churn, fraude, capstone, etc.).
- **Documentation** : guides Git, déploiement et authentification dans `docs/`.

## Arborescence

```
.
├── index.html          # Page principale du portfolio (GitHub Pages)
├── README.md
├── LICENSE
├── .gitignore
├── css/                # Feuilles de style (portfolio, etc.)
├── js/                 # Scripts (portfolio.js, gallery.js, …)
├── docs/               # Fichiers Markdown (guides, procédures)
├── notebooks/          # Notebooks Jupyter (.ipynb)
├── pdf/                # CV et rapports PDF
├── images/             # Photos et illustrations (jpg, png, gif, …)
└── html/               # Autres pages HTML (copie portfolio, variantes)
```

Les chemins dans `index.html` pointent vers `css/`, `js/`, `images/` et `pdf/`. Les liens GitHub vers les notebooks utilisent le chemin `notebooks/<nom>.ipynb` sur la branche `main`.

## GitHub Pages

1. **Settings** → **Pages** du dépôt.
2. **Source** : branche `main`, dossier **`/ (root)`** (car `index.html` est à la racine).

URL typique une fois activé :

`https://sighanocel.github.io/My-data-science-project/`

(Le nom d’utilisateur GitHub peut s’afficher avec une casse différente ; l’URL reste valide.)

## Cloner et pousser des changements

```bash
git clone https://github.com/SighanoCel/My-data-science-project.git
cd My-data-science-project
# … modifications …
git add .
git commit -m "Description des changements"
git push origin main
```

## Guides détaillés

Les instructions pas à pas (premier dépôt, authentification, déploiement) sont dans **`docs/`** (par exemple `INSTALLATION_GIT.md`, `GUIDE_COMPLET_DEPLOIEMENT.md`, `AUTHENTIFICATION_GITHUB.md`).

## Contact

- Email : sighanobob@yahoo.fr  
- LinkedIn : [Celestin Signe Sighano](https://www.linkedin.com/in/celestin-signe-sighano-52974a37/)  
- GitHub : [SighanoCel](https://github.com/SighanoCel)
