"""
main.py - Application Streamlit pour calculer la taille de position en trading.

Ce script permet à l'utilisateur d'entrer ses paramètres de trade et retourne
la taille de lot approprié.
"""

import streamlit as st

def custom_input(prompt, default=None):
    '''
    Récupère les inputs et renvoie leur valeur ou une valeur par défaut

    Args:
        prompt (str): Prompt de l'utilisateur
        default : Valeur par défaut

    Returns:
        float: Valeur de l'utilisateur
    '''
    if default is not None:
        user_input = st.number_input(f"{prompt} (par défaut : {default}) ? ", 0, value=default)
    else:
        user_input = st.number_input(f"{prompt} ? ", 0)
    return user_input

def calcul_risque(risque_=1):
    '''
    Calcul le montant risqué

    Returns:
            float: montant risqué
    '''
    return capital * (risque_/100)

def get_digits_multiplicateur(digits_=5):
    '''
    Retourne le multiplicateur en fonction du nombre de decimal
    Exemple :   5 => 10000
                3 => 100
    
    Args:
        digits_ (float): Nombre de decimal

    Returns:
        float: Multiplicateur
    '''
    return 10 ** (digits_ - 1)

st.title('Calculateur taille de position de trading')

st.markdown('Répondez aux questions pour calculer la taille de position de votre trade.')

capital = custom_input("Entrez le montant de votre capital", None)
risque = custom_input("Quelle est le pourcentage de risque", 1)
contract_size = custom_input("Quel est la taille de contrat", 100000)
digits = custom_input("Quel est le nombre de decimal de votre actif", 5)
stop_loss_pips = custom_input("Quel est le stop loss en pips", None)


if st.button('Calculer la taille de position', type='primary'):
    if capital > 0 and risque > 0 and contract_size > 0 and digits > 0 and stop_loss_pips > 0:
        risque_price = calcul_risque(risque)
        lot = ((risque_price / stop_loss_pips) * get_digits_multiplicateur(digits)) / contract_size

        st.subheader(f'Taille de position : {lot:.2f}')
        st.write(f'**Montant risque** : {risque_price:.2f}')

    elif capital <= 0 or risque <= 0 or contract_size <= 0 or digits <= 0 or stop_loss_pips <= 0:
        st.error('Veuillez renseigner tous les champs. Certains ont une valeur inférieur ou'
                 ' égale à zéro.')
