#! /usr/bin/env python3

import store
import cards
import locale as lc

result = lc.setlocale(lc.LC_ALL, "")
if result == "C":
    lc.setlocal(lc.LC_ALL, "en_US")

def buy_more_chips(money):
    while True:
        try:
            amount = float(input("Amount: "))
        except ValueError:
            print("Invalid amount. Try again.")
            continue

        if 0 < amount <= 10000:
            money += amount
            return money
        else:
            print("Invalid amount, must be from 0 to 10,000.")


def displayTitle():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    print("Enter 'x' for bet to exit")
    print()


def play(deck, player_hand):
    while True:
        choice = input("Hit or Stand? (h/s): ")
        print()

        if choice == "h":
            cards.add_card(player_hand, cards.deal_card(deck))
            displayCards(player_hand, "YOUR CARDS: ")
            if cards.get_points(player_hand) > 21:
                break

        elif choice == "s":
            break
        else:
            print("Not a valid choice, try again.")
    return player_hand



def getStart():
    try:
        money = store.read_money()
    except FileNotFoundError:
        money = 0

    if money < 5:
        print("You were out of money")
        print("We gave you $100 so you can continue")
        store.write_money(100)
        return 100
    else:
        return money

def getBet(money):
    while True:
        try:
            bet = float(input("Bet amount:     "))
        except ValueError:
            print("Invalid amount. Try again.")
            continue

        if bet < 5:
            print("The minimum bet is 5.")
        elif bet > 1000:
            print("The maximum bet is 1000.")
        elif bet > money:
            print("You don't have enough money to make that bet!")
        else:
            return bet

def displayCards(hand, title):
    print(title.upper())
    for card in hand:
        print(card[0], "of", card[1])
    print()


def main():
    displayTitle()

    blackjackMultiplier = 1.5

    money = getStart()
    print("Money:", lc.currency(money, grouping=True))
    print()

    #start loop
    while True:
        if money < 5:
            print("You are out of money.")
            buy_more = input("Would you like to buy more chips? (y/n): ").lower()
            if buy_more == "y":
                money = buy_more_chips(money)
                print("Money:", lc.currency(money, grouping=True))
                store.write_money(money)
            else:
                break

        bet = getBet(money)
        if bet == "x":
            break

        deck = cards.get_deck()
        cards.shuffle(deck)

        dealer_hand = cards.get_empty_hand()
        player_hand = cards.get_empty_hand()

        cards.add_card(player_hand, cards.deal_card(deck))
        cards.add_card(player_hand, cards.deal_card(deck))
        cards.add_card(dealer_hand, cards.deal_card(deck))

        displayCards(dealer_hand, "DEALER'S SHOW CARD")
        displayCards(player_hand, "YOUR CARDS: ")

        player_hand = play(deck, player_hand)

        while cards.get_points(dealer_hand) < 17:
            cards.add_card(dealer_hand, cards.deal_card(deck))
        displayCards(dealer_hand, "DEALER'S CARDS:")

        print("YOUR POINTS:     " + str(cards.get_points(player_hand)))
        print("DEALER'S POINTS:     " + str(cards.get_points(dealer_hand)))

        playerPoints = cards.get_points(player_hand)
        dealerPoints = cards.get_points(dealer_hand)

        if playerPoints > 21:
            print("Sorry, you busted. :( ")
            money -= bet
        elif dealerPoints > 21:
            print("Yay! Dealer busted. You win!")
            money += bet
        else:
            if playerPoints == 21 and len(player_hand) == 2:
                if dealerPoints == 21 and len(dealer_hand) == 2:
                    print("Dealer has blackjack too... You push")
                else:
                    print("Blackjack! You win!")
                    money += bet * 1.5
                    money = round(money, 2)
            elif playerPoints > dealerPoints:
                print("Hooray! You win!")
                money += bet
            elif dealerPoints > playerPoints:
                print("Sorry, you lose")
                money -= bet
            elif playerPoints == dealerPoints:
                print("You push.")
            else:
                print("Huh? What happened")

        print("Money:", lc.currency(money, grouping=True))

        store.write_money(money)


        again = input("Play again? (y/n): ")
        print()
        if again.lower() != "y":
            print("Come again soon!")
            break



        print()



    print("Bye")

if __name__ == "__main__":
    main()