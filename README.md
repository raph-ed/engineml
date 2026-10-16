# QUANTITATIVE REGIME & PORTFOLIO ENGINE
**Dynamic Asset Allocation, Machine Learning Regime Switching & Black-Scholes Tail-Risk Hedging**

![Python](https://img.shields.io/badge/Python-3.10%2B-10B981?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-06B6D4?style=flat-square&logo=streamlit&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-4%20Fichiers%20Unifi%C3%A9s-F59E0B?style=flat-square)
![Statut](https://img.shields.io/badge/Protection-Zero%20Look--Ahead%20Bias-EF4444?style=flat-square)

---

## 1. Utilités du Site (À quoi sert la plateforme ?)

**Quantitative Regime & Portfolio Engine** est un terminal d'analyse quantitative et d'allocation dynamique de portefeuille conçu pour les investisseurs particuliers avertis comme pour les profils institutionnels (*Quant, Asset Management, Risk Management*).

###Ses 4 utilités principales :
1. **Détecter automatiquement le régime de marché actuel :** Au lieu de chercher à deviner le prix exact de demain, l'algorithme de Machine Learning classe le marché en 3 états statistiques :
   * **Régime 0 — Bullish Trend (`#10B981`) :** Tendance haussière saine et volatilité maîtrisée.
   * **Régime 1 — Ranging / Neutral (`#06B6D4`) :** Marché sans tendance, compression de volatilité.
   * **Régime 2 — High-Risk / Sell-Off (`#EF4444`) :** Risque de krach ou de correction sévère.
2. **Optimiser la répartition du portefeuille (Markowitz Robuste) :** Calcule les poids idéaux entre actions américaines (`SPY`, `QQQ`), actions européennes (`EZU`, `VGK`), or (`GLD`) et obligations (`TLT`, `SHY`) en basculant automatiquement vers les actifs refuges dès qu'un risque de baisse (Régime 2) est détecté.
3. **Simuler une couverture par options (Put Black-Scholes) :** Évalue en temps réel le prix et les Grecques (`Delta`, `Gamma`, `Thêta`, `Vega`) d'une option de vente protectrice (*Put OTM 5%*) activée uniquement pendant les phases de crise pour protéger le capital sans détruire le rendement annuel.
4. **Tester la résistance de la stratégie (Backtest Institutionnel) :** Compare la performance nette de frais (courtage + slippage) face au S&P 500 (*Buy & Hold*) et à un portefeuille classique *60/40*.

---

## 2. Prérequis & Structure du Dossier

### Prérequis Techniques
* **Système d'exploitation :** Windows, macOS ou Linux.
* **Python :** Version **3.10 ou supérieure** (aucun besoin de Docker, ce qui économise plus de 4 Go de RAM).
* **Connexion Internet :** Utilisée pour récupérer les cours en direct via l'API *Yahoo Finance* (le site fonctionne également **100 % hors-ligne** grâce à son simulateur stochastique de Markov intégré).

### Les fichiers nécessaires dans votre dossier
L'architecture a été condensée en **4 fichiers de code à plat** pour garantir un emboîtement parfait et zéro bug d'importation :

```text
quant_regime_engine/
├── app.py                 # Interface Streamlit (Globe 3D WebGL + Terminal Bento Grid + Auto-config sombre)
├── backend.py             # Cerveau mathématique (Data, ML Walk-Forward, Markowitz, Black-Scholes, Backtest)
├── i18n.py                # Dictionnaire de traduction bilingue (Français / Anglais)
├── requirements.txt       # Liste des librairies Python à installer
└── README.md              # Ce fichier de documentation