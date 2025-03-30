def input_with_default_value(prompt, default):
    '''
    Récupère les inputs et renvoie leur valeur ou une valeur par défaut

    Args:
        prompt (str): Prompt de l'utilisateur
        default : Valeur par défaut

    Returns:
        str: Valeur de l'utilisateur
    '''
    user_input = input(f"{prompt} (par défaut : {default}) ? ")
    return user_input if user_input.strip() != "" else default

capital = float(input("Entrez le montant de votre capital ? "))
risque = float(input_with_default_value("Quelle est le pourcentage de risque", 1))
contract_size = int(input_with_default_value("Quel est la taille de contrat", 100000))
digits = int(input_with_default_value("Quel est le nombre de decimal de votre actif", 5))
stop_loss_pips = float(input("Quel est le stop loss en pips ? "))

def calcul_risque(risque_=1):
    '''
    Calcul le montant risqué

    Returns:
            int: montant risqué
    '''
    return capital * (risque_/100)


risque_price = calcul_risque(risque)

def get_digits_multiplicateur(digits_=5):
    '''
    Retourne le multiplicateur en fonction du nombre de decimal
    Exemple :   5 => 10000
                3 => 100
    
    Args:
        digits_ (int): Nombre de decimal

    Returns:
        int: Multiplicateur
    '''
    return 10 ** (digits_ - 1)

def calcul_position_size():
    '''
    Calcul la taille de position dynamiquement

    Returns:
            float: taille de lot à utiliser
    '''
    return ((risque_price / stop_loss_pips) * get_digits_multiplicateur(digits)) / contract_size


'''
On affiche les informations à l'utilisateur
'''
print(f'Capital : {capital:.2f} €')
print(f'Risque : {risque} % => Perte possible : {risque_price:.2f} €')
print(f'Stop Loss : {stop_loss_pips} pips => Taille de position : {calcul_position_size():.2f}')