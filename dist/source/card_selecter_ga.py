import random
from typing import List

NumberOfCardsInDeck : int = 100
NumberOfLands : int = 35
NumberOfGenerations : int = 10000
AllCards : List[tuple] = []
LimitForSolution : float = 9999.0
ReasonablePrice : float = 20.0

# Inputs: List[tuple (name, value, cost)]
# Outputs: Score (0 to 100 minus the Number of Lands) or 1 for a bad deck
def SuccessFunction(Deck: List[tuple], pricePoint : float) -> float:
    score : float = NumberOfCardsInDeck - NumberOfLands
    priceOfDeck : float = 0.0

    for card in Deck:
        score -= card[1]
        priceOfDeck += card[2]

    if priceOfDeck > pricePoint:
        return NumberOfCardsInDeck
    
    return score

# Test each of the decks and get a list that is closest to 0.0
def FitnessFunction(Deck: List[tuple], pricePoint : float):
    
    deckScore = SuccessFunction(Deck, pricePoint)
    
    if deckScore == 0:
        return LimitForSolution
    else:
        return abs(NumberOfCardsInDeck / deckScore)

def main():

    priceLimit : float
    
    try:
        priceLimit = float(input("Input a price for the deck: "))
    except ValueError:
        return

    # Safety Checks:
        # Check if it is a positive number, a reasonable price, etc.
        # Check if AllCards are Set

    if priceLimit < ReasonablePrice or len(AllCards) < NumberOfCardsInDeck - NumberOfLands:

        if priceLimit < ReasonablePrice:
            print("Budget too low!")
        else:
            print("Not enough cards in AllCards!")
        return 

    # Generate our solutions from our reduced card selection
    # Ideally the cards with the correct color and types will be passed into AllCards in the structure
    # (Name of Card, Value of Card between (0-1), Price/Cost)
    createdDecks : List[List[tuple]]
    createdDeck : List[tuple]

    # Generate Initial Solutions
    for _ in range(1000):

        # Get Number of Cards minus number of Lands
        selectedIndexes : List[int]
        for j in range(NumberOfCardsInDeck - NumberOfLands):
            k : int = random.randint(0, len(AllCards) - 1)

            # We had a duplicate, get one that is not
            while k in selectedIndexes:
                k = random.randint(0, len(AllCards) - 1)

            selectedIndexes.append(k)

        for j in selectedIndexes:
            createdDeck.append(AllCards[j])

        createdDecks.append(createdDeck)

    # Run the loop for number of generations
    for i in range(NumberOfGenerations):
        rankedDecks = []

        # Run the Fitness function on each deck
        for sol in createdDecks:
            rankedDecks.append(FitnessFunction(sol, priceLimit), sol)

        # Sort them and then put the best deck on the top
        rankedDecks.sort()
        rankedDecks.reverse()

        print(f"=== Gen {i} best solutions === ")
        print(rankedDecks[0])

        # Break if we get a good result early
        if rankedDecks[0][0] >= LimitForSolution:
            break

        bestDecks = rankedDecks[:NumberOfGenerations / 10]

        # Get all the cards in this list of "best cards"
        bestCards = []
        for _, deck in bestDecks:
            for card in deck:
             if card not in bestCards:
                bestCards.append(card)

        # Generate new decks with the best cards, without duplicates
        newDeckList = []
        for _ in range(1000):
            newDeck = []
            for i in range(NumberOfCardsInDeck - NumberOfLands):
                card = random.choice(bestCards)
                while card in newDeck:
                    card =  random.choice(bestCards)

                newDeck.append(card)
            newDeckList.append(newDeck)

        # Reassign for the next loop
        createdDecks = newDeckList

if __name__ == "__main__":
    main()