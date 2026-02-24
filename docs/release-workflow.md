# Release Workflow — ZymDeploy

Ce document explique comment déclencher les différents scénarios du workflow CI/CD
(`build-release.yml`).

---

## Scénarios

### 1. Tests seulement (pas de build)

Déclenché automatiquement sur tout **push ou PR vers `master`/`main`**.

```bash
git push origin master
```

**Ce qui s'exécute :**
- Installation des dépendances système et Python
- Lancement de `pytest tests/` avec rapport de couverture
- Upload du rapport sur Codecov

---

### 2. Build complet + Release stable

Déclenché par un **tag `v*`**.

```bash
git tag v1.2.0
git push origin v1.2.0
```

**Ce qui s'exécute :**
- Tests (obligatoires, le build est bloqué si les tests échouent)
- Mise à jour automatique de la version dans `constants.py`
- Build PyInstaller → `ZymDeploy.exe`
- Création de l'archive `ZymDeploy-1.2.0-Windows.zip`
- Publication d'une **GitHub Release stable**

---

### 3. Build de test + Pre-release

Déclenché par un **tag `test-*`**.

```bash
git tag test-1.2.0
git push origin test-1.2.0
```

**Ce qui s'exécute :** identique au scénario 2, mais la Release GitHub est marquée
**Pre-release** (non visible comme version stable).

---

### 4. Build manuel (sans tag)

Via l'interface GitHub :
**Actions → Build and Release ZymDeploy → Run workflow**

Saisir une version dans le champ (ex: `test-1.2.0`).

**Ce qui s'exécute :**
- Tests + build + exe + zip
- **Pas de GitHub Release créée** (artifacts disponibles dans l'onglet Actions)

---

## Convention de versioning

| Format | Type |
|---|---|
| `v1.0.0` | Release stable |
| `test-1.0.0` | Pre-release / validation |

---

## Synchronisation automatique de la version

Lors d'un build (scénarios 2, 3, 4), le workflow met à jour automatiquement
le champ `version` dans `zymosoft_assistant/utils/constants.py` avant de compiler
l'exécutable. La version affichée dans l'interface correspond donc toujours au tag utilisé.

---

## Supprimer un tag (si erreur)

```bash
# Supprimer en local
git tag -d v1.2.0

# Supprimer sur GitHub
git push origin --delete v1.2.0
```
