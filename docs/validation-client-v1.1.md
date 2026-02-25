# Document de validation client — ZymDeploy v1.1.0

**Projet :** ZymDeploy
**Version :** 1.1.0
**Date :** 25 février 2026
**Préparé par :** Zymoptiq
**À valider par :** ___________________________

---

## Objet

Ce document présente la nouvelle fonctionnalité développée suite à votre demande :
**le mode "Validation de plaque" autonome**, disponible dans ZymDeploy v1.1.0.

---

## Contexte et besoin exprimé

> *"Pouvoir utiliser le module de validation de plaques de manière indépendante,
> sans passer par toutes les étapes de l'installation complète."*

---

## Ce qui a été développé

### 1. Dialogue de sélection du mode au démarrage

Au lancement de l'application, une fenêtre s'affiche et propose deux modes :

| Mode | Description |
|---|---|
| **Installation complète** | Comportement existant — les 4 étapes de déploiement |
| **Validation de plaque** | Accès direct à l'étape de validation, sans les autres étapes |

L'utilisateur choisit son mode avant d'entrer dans l'application.
Si la fenêtre est fermée sans sélection, l'application se ferme proprement.

---

### 2. Mode "Validation de plaque"

Lorsque ce mode est sélectionné :

- L'interface est simplifiée : seule l'étape de validation des acquisitions est affichée
- La barre de navigation latérale est masquée
- Le titre de la fenêtre affiche **"ZymDeploy — Validation de plaque"**
- Les fonctions de session (sauvegarder / charger) ne sont pas disponibles dans ce mode
- L'éditeur de configuration (Step 2) n'est pas accessible

---

### 3. Changement de mode en cours d'utilisation

Il est possible de changer de mode sans relancer l'application via le menu **Actions** :

- **"Validation de plaque seule"** — bascule vers le mode validation
- **"Mode installation complète"** — revient au mode complet

Un message de confirmation s'affiche avant le changement. La session en cours est réinitialisée.

---

## Critères de validation

Merci de tester les points ci-dessous et d'indiquer le résultat.

| # | Test | Résultat attendu | Validé ? | Commentaire |
|---|---|---|---|---|
| 1 | Lancer l'application | La fenêtre de sélection de mode s'affiche | ☐ | |
| 2 | Fermer la fenêtre sans sélectionner | L'application se ferme sans erreur | ☐ | |
| 3 | Sélectionner "Installation complète" | Les 4 étapes s'affichent normalement | ☐ | |
| 4 | Sélectionner "Validation de plaque" | Seule l'étape de validation s'affiche | ☐ | |
| 5 | Vérifier le titre en mode validation | Le titre contient "Validation de plaque" | ☐ | |
| 6 | Tenter une action de session en mode validation | Un message indique que ce n'est pas disponible | ☐ | |
| 7 | Basculer vers le mode complet via le menu Actions | L'interface passe aux 4 étapes | ☐ | |
| 8 | Basculer vers le mode validation via le menu Actions | L'interface revient à la validation seule | ☐ | |

---

## Décision

☐ **Validé** — la fonctionnalité correspond au besoin exprimé

☐ **Validé avec réserves** — voir commentaires ci-dessous

☐ **Non validé** — des corrections sont nécessaires

---

**Commentaires :**

```
___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________
```

---

**Signature client :** ___________________________  **Date :** _______________
