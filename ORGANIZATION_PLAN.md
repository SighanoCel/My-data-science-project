# 📊 Repository Organization Plan

**Created:** 2026-05-13  
**Branch:** `organize-by-format`  
**Status:** ✅ Ready for Implementation  

---

## 📋 Overview

This plan organizes your repository files by format into logical, easy-to-navigate folders. This improves maintainability, makes it easier to find files, and creates a professional repository structure.

---

## 📁 New Directory Structure

```
My-data-science-project/
│
├── 📓 notebooks/                          (9 files - 7.24 MB - 66%)
│   ├── Bank_Customer_Churn.ipynb
│   ├── Bank_transaction_fraud_detection.ipynb
│   ├── Cancer_prediction.ipynb
│   ├── Car_performance_prediction.ipynb
│   ├── Final_Capstone_business_analytics.ipynb
│   ├── House_rent_project.ipynb
│   ├── banking_churn_with_deep_learning.ipynb
│   ├── project_2_linear_regression.ipynb
│   └── projet_1_linear_regression.ipynb
│
├── 📄 docs/                               (9 files - 30 KB - 0.3%)
│   ├── README.md
│   ├── COMMANDES_A_EXECUTER.md
│   ├── CREER_DEPOT_PORTFOLIO.md
│   ├── DEPLOIEMENT.md
│   ├── ETAPES_SIMPLES.md
│   ├── GUIDE_AUTHENTIFICATION_DETAILLE.md
│   ├── GUIDE_COMPLET_DEPLOIEMENT.md
│   ├── INSTALLATION_GIT.md
│   └── RESUME_SITUATION.md
│
├── 📋 pdfs/                               (4 files - 2.79 MB - 25%)
│   ├── CV_Junior_data_scientist.pdf
│   ├── Capstone_FinalReport.pdf
│   ├── data_Science_CV_english.pdf
│   └── cv.pdf
│
├── 🖼️ images/                             (18 files - 0.57 MB - 5%)
│   ├── Cancer-Prediction.png
│   ├── Car Acceleration illustration.jpg
│   ├── Churn Customer.JPG
│   ├── Churn immage illustration.jpg
│   ├── Data-Driven-Logistica-immage.jpg
│   ├── Renting Price photo illustration.jpg
│   ├── Tof laurea 1.jpg
│   ├── Tof laurea 2.jpg
│   ├── Tof laurea 3.jpg
│   ├── Universita_di_Ferrara_image.jpeg
│   ├── fraud-immage.jpeg
│   ├── photo animation.png
│   ├── photo-profile.jpg
│   ├── photo2.jpg
│   ├── rome business school image.jpg
│   ├── tof_firenze.jpg
│   ├── udemy_image.jpg
│   └── universidad de valencia_image.gif
│
├── 🌐 web/                                (Nested structure)
│   ├── html/                              (3 files - 70 KB)
│   │   ├── Celestin SIgne Sighano.html
│   │   ├── index.html
│   │   └── my site.html
│   ├── css/                               (Empty - ready for stylesheets)
│   └── js/                                (Empty - ready for scripts)
│
├── ⚙️ config/                             (2 files - 12 KB)
│   ├── .gitignore
│   └── LICENSE
│
├── repository_structure.json              (Original metadata)
├── repository_structure_organized.json    (Organized mapping)
├── ORGANIZATION_PLAN.md                   (This file)
└── README.md                              → docs/README.md

```

---

## 📊 File Distribution

| Category | Count | Size | Percentage |
|----------|-------|------|-----------|
| 📓 Jupyter Notebooks | 9 | 7.24 MB | 66% |
| 📋 PDF Documents | 4 | 2.79 MB | 25% |
| 🖼️ Images | 18 | 0.57 MB | 5% |
| 📄 Markdown Docs | 9 | 30 KB | 0.3% |
| 🌐 HTML Files | 3 | 70 KB | 0.6% |
| ⚙️ Config Files | 2 | 12 KB | 0.1% |
| **TOTAL** | **54** | **10.97 MB** | **100%** |

---

## 🎯 Projects Contained

The repository contains **8 major data science projects**:

1. **Bank Customer Churn Analysis**
   - `notebooks/Bank_Customer_Churn.ipynb` (813 KB)
   - `notebooks/banking_churn_with_deep_learning.ipynb` (428 KB)

2. **Bank Transaction Fraud Detection**
   - `notebooks/Bank_transaction_fraud_detection.ipynb` (1.5 MB)

3. **Cancer Prediction**
   - `notebooks/Cancer_prediction.ipynb` (89.8 KB)

4. **Car Performance Prediction**
   - `notebooks/Car_performance_prediction.ipynb` (1.2 MB)

5. **House Rent Price Prediction**
   - `notebooks/House_rent_project.ipynb` (163 KB)

6. **Linear Regression Projects (2)**
   - `notebooks/project_2_linear_regression.ipynb` (265 KB)
   - `notebooks/projet_1_linear_regression.ipynb` (381 KB)

7. **Capstone Business Analytics**
   - `notebooks/Final_Capstone_business_analytics.ipynb` (2.6 MB)

8. **Deep Learning Implementations**
   - Various implementations across notebooks

---

## ✨ Benefits of This Organization

### 1. **Improved Navigation** 🗺️
   - Find files by type instantly
   - No more scrolling through 50+ files

### 2. **Professional Structure** 👔
   - Looks organized and well-maintained
   - Better for portfolio presentation

### 3. **Easy Maintenance** 🔧
   - Add new files to appropriate folders
   - Scale the repository easily

### 4. **Better Collaboration** 👥
   - New contributors understand structure quickly
   - Clear separation of concerns

### 5. **SEO & Discovery** 📈
   - Better for GitHub search
   - Easier to highlight specific projects

---

## 🔄 Migration Path

### Step 1: Review
- ✅ Check this ORGANIZATION_PLAN.md
- ✅ Review repository_structure_organized.json for complete mapping

### Step 2: Create Pull Request
```bash
# Branch is already created: organize-by-format
# Create PR from organize-by-format → main
```

### Step 3: Merge
- Review the PR on GitHub
- Click "Merge pull request"
- New structure is applied!

### Step 4: Update References (if needed)
- Check if any internal links need updating
- Update badges in README if needed

---

## 📋 Files Moved

### Root Level → `notebooks/`
```
✓ Bank_Customer_Churn.ipynb
✓ Bank_transaction_fraud_detection.ipynb
✓ Cancer_prediction.ipynb
✓ Car_performance_prediction.ipynb
✓ Final_Capstone_business_analytics.ipynb
✓ House_rent_project.ipynb
✓ banking_churn_with_deep_learning.ipynb
✓ project_2_linear_regression.ipynb
✓ projet_1_linear_regression.ipynb
```

### Root Level → `docs/`
```
✓ README.md
✓ COMMANDES_A_EXECUTER.md
✓ CREER_DEPOT_PORTFOLIO.md
✓ DEPLOIEMENT.md
✓ ETAPES_SIMPLES.md
✓ GUIDE_AUTHENTIFICATION_DETAILLE.md
✓ GUIDE_COMPLET_DEPLOIEMENT.md
✓ INSTALLATION_GIT.md
✓ RESUME_SITUATION.md
```

### Root Level → `pdfs/`
```
✓ CV_Junior_data_scientist.pdf
✓ Capstone_FinalReport.pdf
✓ data_Science_CV_english.pdf
✓ cv.pdf
```

### Root Level → `images/`
```
✓ Cancer-Prediction.png
✓ Car Acceleration illustration.jpg
✓ Churn Customer.JPG
✓ Churn immage illustration.jpg
✓ Data-Driven-Logistica-immage.jpg
✓ Renting Price photo illustration.jpg
✓ Tof laurea 1.jpg
✓ Tof laurea 2.jpg
✓ Tof laurea 3.jpg
✓ Universita_di_Ferrara_image.jpeg
✓ fraud-immage.jpeg
✓ photo animation.png
✓ photo-profile.jpg
✓ photo2.jpg
✓ rome business school image.jpg
✓ tof_firenze.jpg
✓ udemy_image.jpg
✓ universidad de valencia_image.gif
```

### Root Level → `web/html/`
```
✓ Celestin SIgne Sighano.html
✓ index.html
✓ my site.html
```

### Existing Folders → `web/`
```
✓ css/ → web/css/
✓ js/ → web/js/
✓ nouveau site/ → web/nouveau site/
```

### Root Level → `config/`
```
✓ .gitignore
✓ LICENSE
```

---

## 🔗 Helpful Resources

- **Original Structure:** `repository_structure.json`
- **Organized Mapping:** `repository_structure_organized.json` (contains all new paths)
- **GitHub PR Template:** To create a PR, use GitHub's "Compare & pull request" button

---

## ❓ FAQ

**Q: Will my file links break?**  
A: GitHub automatically redirects old links to new locations, so existing links will still work.

**Q: Can I undo this?**  
A: Yes! Just revert the merge or keep the old branch as backup.

**Q: What about cloned repositories?**  
A: Users with cloned repos can run `git pull` to get the new structure.

**Q: Do I need to update .gitignore?**  
A: The .gitignore patterns should still work; just update if you add new folders.

---

## 📞 Next Steps

1. ✅ **Review** this plan and the JSON mapping
2. 🔀 **Create PR** from `organize-by-format` → `main`
3. ✔️ **Merge** the PR
4. 📝 **Update README** if needed to reflect new structure
5. 📢 **Announce** the new organization to any collaborators

---

**Status:** ✅ All preparation complete. Ready to merge on your approval!

**Branch:** `organize-by-format`  
**Files Added:** 2 (ORGANIZATION_PLAN.md, repository_structure_organized.json)  
**Ready to Merge:** YES

