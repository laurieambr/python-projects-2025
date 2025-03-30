
capital = float(input("Entrez le montant de votre capital ? "))
risque = int(input("Quelle est le pourcentage de risque ? "))
contract_size = int(input("Quel est la taille de contrat ? "))
digits = int(input("Quel est le nombre de decimal de votre actif ? "))
stop_loss_pips = float(input("Quel est le stop loss en pips ? "))

'''
Calcul le montant risqué

Returns:
        int: montant risqué
'''
def calcul_risque():
    return capital * (risque/100)


risque_price = calcul_risque()

def get_digits_multiplicateur(digits):
    '''
    Retourne le multiplicateur en fonction du nombre de decimal
    Exemple :   5 => 10000
                3 => 100
    
    Args:
        digits (int): Nombre de decimal

    Returns:
        int: Multiplicateur
    '''
    return 10 ** (digits - 1)

'''
Calcul la taille de position dynamiquement

Returns:
        float: taille de lot à utiliser
'''
def calcul_position_size():
    return ((risque_price / stop_loss_pips) * get_digits_multiplicateur(digits)) / contract_size


'''
On affiche les informations à l'utilisateur
'''
print(f'Capital : {capital:.2f} €')
print(f'Risque : {risque} % => Perte possible : {risque_price:.2f} €')
print(f'Stop Loss : {stop_loss_pips} pips => Taille de position : {calcul_position_size():.2f}')