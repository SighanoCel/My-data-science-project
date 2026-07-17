# My-data-science-project

Dépôt personnel de **Celestin Signe Sighano** — Junior Data Scientist.

Il regroupe un **portfolio web** (GitHub Pages), des **notebooks Jupyter** de projets data science, des **CV / rapports PDF** et les **assets** du site (images, styles, scripts).

## Aperçu

| Élément | Emplacement |
|--------|-------------|
| Site portfolio (page d’accueil) | [`index.html`](index.html) à la racine |
| Notebooks de projets | [`notebooks/`](notebooks/) |
| CV et rapports | [`pdf/`](pdf/) |
| Photos et illustrations | [`images/`](images/) |
| Pages HTML secondaires | [`html/`](html/) |
| Feuilles de style | [`css/`](css/) |
| Scripts JavaScript | [`js/`](js/) |

## Structure du dépôt

```
.
├── index.html              # Page principale du portfolio (GitHub Pages)
├── README.md
├── LICENSE
├── .gitignore
├── css/                    # portfolio.css, style.css
├── js/                     # portfolio.js, gallery.js
├── notebooks/              # Projets Jupyter (.ipynb)
├── pdf/                    # CV et rapports (.pdf)
├── images/                 # Photos et visuels (.jpg, .png, .gif, …)
└── html/                   # Variantes / copies HTML du portfolio
```

`index.html` reste à la **racine** pour que GitHub Pages fonctionne sans changer la source dans les paramètres du dépôt.

## Notebooks

| Fichier | Thème |
|---------|--------|
| `Bank_transaction_fraud_detection.ipynb` | Détection de fraude bancaire |
| `banking_churn_with_deep_learning.ipynb` | Churn bancaire (deep learning) |
| `Bank_Customer_Churn.ipynb` | Churn client bancaire |
| `House_rent_project.ipynb` | Prédiction des loyers |
| `Cancer_prediction.ipynb` | Prédiction / classification (cancer) |
| `Car_performance_prediction.ipynb` | Performance automobile |
| `Final_Capstone_business_analytics.ipynb` | Capstone business analytics |
| `projet_1_linear_regression.ipynb` | Régression linéaire (projet 1) |
| `project_2_linear_regression.ipynb` | Régression linéaire (projet 2) |

Liens depuis le portfolio : `https://github.com/SighanoCel/My-data-science-project/blob/main/notebooks/<fichier>.ipynb`

## GitHub Pages

1. Ouvrir **Settings** → **Pages** du dépôt.
2. **Source** : branche `main`, dossier **`/ (root)`**.

URL une fois le site publié :

**https://sighanocel.github.io/My-data-science-project/**

## Travailler en local

```bash
git clone https://github.com/SighanoCel/My-data-science-project.git
cd My-data-science-project
```

Pour prévisualiser le portfolio, ouvrir `index.html` dans un navigateur ou utiliser un serveur local :

```bash
# Exemple avec Python
python -m http.server 8000
# Puis : http://localhost:8000
```

## Chemins importants dans le site

- Images : `images/…`
- CV / PDF : `pdf/…`
- CSS / JS : `css/…`, `js/…`
- Copie du portfolio dans `html/` : chemins relatifs avec préfixe `../` (ex. `../images/…`, `../pdf/…`)

## Contact

- **Email** : sighanobob@yahoo.fr
- **LinkedIn** : [Celestin Signe Sighano](https://www.linkedin.com/in/celestin-signe-sighano-52974a37/)
- **GitHub** : [SighanoCel](https://github.com/SighanoCel)
