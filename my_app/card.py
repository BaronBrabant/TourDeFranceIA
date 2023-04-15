import random  


#Initiate the card deck
def initiate_cards_deck():
    return [i for i in range(1, 13) for _ in range(8)]  #create a list with all cards


#distribue 5 cartes dans chaque equipe
def cards_distribution(cartes, equipes):
    
    for _ in range(5):  # Distribuer 5 cartes à chaque équipe        

        for i in range(4):             
            carte = random.choice(cartes)  # Choisir une carte au hasard en tenant compte du nombre de cartes similaires encore en jeu             
            equipes[i].append(carte)  # Ajouter la carte à l'équipe correspondante             
            cartes.remove(carte)  # Retirer la carte de la liste des cartes disponibles          
    
    

#distribue des cartes dans une equipe
def cards_distribution_to_a_team(cartes, equipes, indice, card_quantity):
    
    for _ in range(card_quantity):  # Distribuer 5 cartes à chaque équipe        

        carte = random.choice(cartes)  # Choisir une carte au hasard en tenant compte du nombre de cartes similaires encore en jeu             
        equipes[indice].append(carte)  # Ajouter la carte à l'équipe correspondante             
        cartes.remove(carte)  # Retirer la carte de la liste des cartes disponibles          
    
    

def remove_card(equipes, indice, card):
    
    if card in equipes[indice]:
        equipes[indice].remove(card)


    

#lucky case : withdraw a number beetween -3 and 3
def lucky_case():
    
    return random.randrange(-3,3)
"""
exchange case:
    - If the teams have less than 3 cards there are all taken and replaced by 3 new cards
    - If you have a least 3 cards, you choose 3 cards that you exchange

"""
def exchange_case(cartes, equipes, indice, exchanged_card_list):


    if equipes[indice].size < 3:
        for card in equipes[indice]:
            equipes[indice].remove(card)
        cards_distribution_to_a_team(cartes, equipes, indice , 3)

    else: 
        for card in exchanged_card_list:
            equipes[indice].remove(card)
        cards_distribution_to_a_team(cartes, equipes, indice , 3)
        
        



#Test

cartes = initiate_cards_deck()
equipes = [[] for _ in range(4)]


print(cartes)
print("------------------------------------------")
print(equipes)

#equipes = cards_distribution(cartes, equipes)
cards_distribution_to_a_team(cartes, equipes, 0, 5)

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print(cartes)
print("------------------------------------------")
print(equipes)

remove_card(equipes,0 , 5)

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print(cartes)
print("------------------------------------------")
print(equipes)

