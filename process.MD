# Application de gestion des formation VCF

1 - Categories de formation (crud complet)
    * Libelle

2 - Tag du cours
    * Libelle

3 - Entreprise
    * Libelle
    * Reference
    * Responsable
    * Mail du responsable
    * Telephone du responsable

4 - Agent Entreprise
    * Id entreprise
    * Nom
    * Prenom
    * Telephone
    * Mail

5 - Cours
    * Titre
    * Id categorie
    * Id tag du cours
    * La description
    * L'image du cours
    * Status

6 - Prof
    * Nom
    * Prenom
    * Tel
    * Email

7 - Session
    * Titre
    * Date debut
    * Date de fin
    * Type de validite (jour, mois, annee)
    * Delai de validite
    * Date de validite
    * Status
    * Nombre de cours
    * Id du prof
    * Nombre max de d'etudiant
    * Total montant des cours

8 - Cours par session
    * Id de session
    * Id du cours
    * Le prix groupe
    * Nombre de personne par groupe
    * Le prix perso
    * La reduction (booleen)
    * Le pourcentage
    * La valeur de reduction

9 - 