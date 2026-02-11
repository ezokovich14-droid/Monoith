# MOT – Gestion des commandes de clients

## Application 2 : Gestion des commandes de clients

---

## Tableau du Modèle Organisationnel des Traitements (MOT)

| N° OP | Événement déclencheur | Opération (OP) | Acteur responsable | Actions réalisées | Événement résultat | Règle d’émission / Synchronisation |
|------|----------------------|----------------|--------------------|-------------------|--------------------|------------------------------------|
| OP1 | Commandes clients saisies aux comptoirs régionaux | Traitement des commandes clients | Service magasin (Siège) | - Réception des commandes<br>- Sélection des commandes retenues<br>- Édition des bons de réquisition | Bons de réquisition édités | Chaque matin, le service magasin traite les commandes reçues la veille |
| OP2 | Bons de réquisition transmis | Sortie des articles du stock | Magasiniers | - Sortie des articles du stock<br>- Pointage manuel des bons<br>- Acheminement des articles vers le service emballage | Articles sortis du stock et transmis à l’emballage | Après réception des bons de réquisition |
| OP3 | Articles reçus au service emballage | Emballage et expédition des colis | Service emballage | - Emballage des articles (le jour même)<br>- Expédition des colis aux clients<br>- Transmission d’une copie du bon de livraison au CTI | Colis livrés aux clients<br>Copie du bon de livraison envoyée au CTI | Expédition effectuée le lendemain de l’emballage |
| OP4 | Bons de livraison reçus durant la semaine | Facturation des clients | Centre de traitement informatique (CTI) | - Regroupement des commandes de la semaine<br>- Édition des factures<br>- Envoi des factures aux clients | Factures envoyées aux clients | Synchronisation hebdomadaire : traitement en fin de semaine |

---

## Remarques
- Chaque opération est déclenchée par un événement précis.
- Les règles d’émission définissent le moment du traitement.
- Les événements résultats correspondent aux documents produits ou transmis.

---

**Méthode MERISE – IAI TOGO**  
Année académique 2025 – 2026
