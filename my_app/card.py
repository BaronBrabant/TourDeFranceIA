import random  


# list of all exchange case
exchanges_places = [[13, 1, "n"], [14, 1, "n"], [18, 1, "n"], [20, 1, "n"], [20, 2, "n"], [22, 2, "n"], [26, 2, "d"], [27, 2, "d"], [30, 2, "n"], [32, 2, "n"], [36, 1, "n"], [46, 0, "n"], [46, 1, "n"], [61, 1, "n"], [62, 1, "n"], [71, 1, "n"], [72, 1, "n"], [81, 0, "n"], [81, 1, "n"], [85, 0, "n"], [85, 1, "n"], [86, 1, "n"], [89, 1, "b"], [90, 1, "b"]]
chance_places = [[9, 0, "a"], [10, 0, "a"], [11, 0, "n"], [12, 0, "n"], [15, 1, "n"], [16, 1, "n"], [19, 2, "n"], [21, 2, "n"], [24, 0, "n"], [26, 0, "A"], [28, 0, "n"], [30, 0, "n"], [32, 0, "n"], [34, 0, "n"], [48, 0, "n"], [57, 1, "n"], [66, 0, "n"], [66, 1, "n"], [74, 0, "n"], [90, 1, "c"]]

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
    
    for _ in range(card_quantity):  # Distribuer card_quantity cartes à chaque équipe        

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


    if len(equipes[indice]) < 3:
        for card in equipes[indice]:
            equipes[indice].remove(card)
        cards_distribution_to_a_team(cartes, equipes, indice , 3)

    else: 
        for card in exchanged_card_list:
            equipes[indice].remove(card)
        cards_distribution_to_a_team(cartes, equipes, indice , 3)
        
        



#Test
"""
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
"""
