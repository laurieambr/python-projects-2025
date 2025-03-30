import streamlit as st

st.title('RR + Position Sizing Calculator')

st.markdown("Répondez aux questions suivantes pour calculer la taille de position de votre trade.")

def custom_input(prompt, default=None):
    '''
    Récupère les inputs et renvoie leur valeur ou une valeur par défaut

    Args:
        prompt (str): Prompt de l'utilisateur
        default : Valeur par défaut
        return_type (type): Type de retour

    Returns:
        return_type: Valeur de l'utilisateur
    '''
    while True:
        if default is not None:
            user_input = st.number_input(f"{prompt} (par défaut : {default}) ? ")
            if (user_input.strip() == ""):
                    user_input = default
        else:
            user_input = st.number_input(f"{prompt} ? ")
            
        try:
            if user_input <= 0:
                raise ValueError
            else:
                return user_input
        except ValueError:
            print(f"[ERREUR] Entrée invalide. Merci de taper un(e) {return_type.__name__}.")
        
capital = custom_input("Entrez le montant de votre capital", None)
risque = custom_input("Quelle est le pourcentage de risque", 1)
contract_size = custom_input("Quel est la taille de contrat", 100000)
digits = custom_input("Quel est le nombre de decimal de votre actif", 5)
stop_loss_pips = custom_input("Quel est le stop loss en pips", None)

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
st.write(f'Capital : {capital:.2f} €')
st.write(f'Risque : {risque} % => Perte possible : {risque_price:.2f} €')
st.write(f'Stop Loss : {stop_loss_pips} pips => Taille de position : {calcul_position_size():.2f}')