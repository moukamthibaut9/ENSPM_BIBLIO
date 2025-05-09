"""from django.test import TestCase

# Create your tests here.

def employee_ifc_compute(convention,salaire,anciennete,anc_base,taux_base,statut,age_emp,age_retraite,ecart_anc,ajout_taux,ajout_anc):
    if convention == 'C-SA':
        # Anciennete minimal que doit avoir l'employe pour beneficier de l'IFC
        base_seniority = anc_base
        # Taux d'indemnité sur les premieres annees definies par `base_seniority`
        base_compensation_rate = taux_base
        # Aciennete a prendre en compte pour le calcul de l'IFC selon le statut du dossier de l'employe
        if statut == 'SIM':
            # Ici, on considere l'anciennete qu'aura l'employe s'il atteint l'age de la retraite au sein de la societe
            seniority = anciennete + (age_retraite - age_emp)
        else:
            # Dans les autres cas, on considere l'anciennete reelle de l'employe
            seniority = anciennete 
        if statut in ['VAL','SIM']:
            if statut == 'VAL' and anciennete < anc_base:
                return 0
            else:
                ifc_result = base_compensation_rate*base_seniority*salaire
                for i in range(anc_base,seniority,ecart_anc):
                    base_seniority += ecart_anc
                    # Aumentation du taux d'indemnité d'un certain pourcentage defini par 
                    # `ajout_taux` apres un certain nombre d'annees 
                    # defini par `ecart_anc`
                    base_compensation_rate += ajout_taux
                    if seniority >= base_seniority:
                        ifc_result += ecart_anc*base_compensation_rate*salaire
                    else:
                        print(f"Age:{base_seniority} | IFC:{ifc_result}")
                        ifc_result += (anciennete-i)*base_compensation_rate*salaire
                return ifc_result
        else:
            # Si le dossier est juste créé, abandonné ou supprimé, on ne calcule rien
            return None
employee_ifc_compute('C-SA',500000,5,5,0.2,'SIM',22,60,5,0.05,5)"""
