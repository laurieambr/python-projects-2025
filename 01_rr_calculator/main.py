'''
Saisies des informations par l'utilisateur
'''
capital = input("Entrez votre capital ?")
risque = input("Quelle est le pourcentage de risque ?")
stop_loss_pips = input("Quel est le stop loss en pips ?")
contract_size = input("Quel est la taille de contrat ?")

'''
Retourne le montant risqué
'''
def calcul_risque():
    return capital * (risque/100)

'''
Retourne la taille de position
'''
def calcul_position_size():
    # en cours
    return None

'''
On affiche les informations à l'utilisateur
'''
print(f'Capital : ${capital} €')
print(f'Risque : ${risque} % => Perte possible : ${calcul_risque()} €')
print(f'Stop Loss : ${stop_loss_pips} pips => Taille de position : {calcul_position_size()}')