import random

# -------------------------------
# Classes for current game, cards, and players
# -------------------------------
class GameState:
    def __init__(self):
        #scoring caregories start at zero
        self.scores = [0,0,0,0]
        self.turn = 0
        self.history = []

    def log(self, message):
        print(message)
        self.history.append(message)

class Card:
    def __init__(self, name, effect_func, desc, challenger):
        self.name = name
        self.effect = effect_func
        self.desc = desc
        self.challenger = challenger

    def play(self, game_state, players, player, team):
        game_state.log(f"\nTurn {game_state.turn}: {team} ({player}) plays '{self.name}'")
        self.effect(game_state, team, players, self)

class Player:
    def __init__(self, name, team):
        self.name = name
        self.hand = []
        self.team = team

    def draw(self, deck, n=1):
        for _ in range(n):
            if deck:
                self.hand.append(deck.pop())

    def discard(self, card):
        self.hand.remove(card)
        return card


# -------------------------------
# Card effect functions 
# -------------------------------
# Categories:
# 0: density
# 1: transit-infra
# 2: suburb-devel
# 3: urban-car-infra

def tram_derailment(game_state, team, players, card):
    if game_state.scores[3] > 10:
        game_state.scores[1] -= 3
        game_state.log(f"-3 transit-infra (now {game_state.scores[1]})")
    else:
        game_state.scores[1] += 3
        game_state.log(f"+3 transit-infra (now {game_state.scores[1]})")

#instantiation currently gives it challenge rights against yimby blunder
def strava_bro_assembly(game_state, team, players, card):
    #change choice to take user decision input
    choice = random.choice([True, False])
    if choice:
        game_state.scores[1] += 3
        game_state.log(f"+3 transit-infra (now {game_state.scores[1]})")
    else:
        game_state.scores[1] -= 3
        game_state.log(f"-3 transit-infra (now {game_state.scores[1]})")

def yimby_blunder(game_state, team, players, card):

    challenged = challenge_func(game_state, card, team, players)

    if challenged:
        game_state.scores[0] += 3
        game_state.scores[3] += 5
        game_state.log(f"Additional funding provided! +3 density (now {game_state.scores[0]}), +5 urban-car infra (now {game_state.scores[3]})")
    else:
        game_state.scores[0] += 3
        game_state.scores[3] += 2
        game_state.log(f"Standard funding. +3 density (now {game_state.scores[0]}), +2 urban-car infra (now {game_state.scores[3]})")

def motor_envy(game_state, team, players, card):

    game_state.scores[3] += 5
    game_state.log(f"+5 urban-car-infra (now {game_state.scores[3]})")

def nimby_confusion(game_state, team, players, card):

    game_state.scores[2] += 3
    game_state.scores[3] -= 3
    game_state.log(f"+3 suburb-devel (now {game_state.scores[2]}), -3 urban-car infra (now {game_state.scores[3]})")


# -------------------------------
# Universal challenge function. Effects of a challenge
# are defined in card effect functions 
# -------------------------------
def challenge_func(game_state, card, team, players):
    game_state.log(f"Card challengable. Checking for challenges.")
    for player in players:
        for other_card in player.hand:
            if other_card.name == card.challenger:
                #change challenge decision to take user input
                 while True:
                    choice = input(f"{player.name} would you like to challenge (y/n)?").strip().lower()
                    if choice == "y":
                        game_state.log(f"{player.name} Challenged! ")
                        player.discard(other_card)
                        return True
                    elif choice == "n":
                        return False
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")

# -------------------------------
# Declare constants and card objects
# -------------------------------

#Tram Derailment
desc_1 = (
    "A local light rail system has a minor derailment, injuring one passenger.\n"
    "If support for urban car infrastructure is sufficiently high, motor vehicle\n" 
    "lobbyists successfully sell the narrative that trams are dangerous.\n" 
    "Otherwise, investments are made in improving safety of transit systems.\n"
    "-3/+2 support for transit infrastructure respectively.\n"
)

#Strava Bro Assembly
desc_2 = (
    "A suburbanite cycling club is frustrated with all other road users slowing down their strava times.\n"
    "Decide if they lobby for bike lanes or against local bus routes. If challenged, they do the opposite.\n"
    "+3/-4 support for transit infrastructure respectively."
)

#YIMBY Blunder
desc_3 = ("Several mixed-use complexes with limited parking are approved. Supporters were unaware that the\n"    
    "developer made a deal with the developer of a large parking complex nearby.\n" 
    "+3 support for densification. +2 support for urban car infrastructure by default, +5 with additional funding."
)

#Motor Envy
desc_4 = ("General Motors runs a hugely successful advertising campaign in the city.\n" 
    "The fancy, seemingly affordable symbols of freedom fly off the lots.\n"
    "+5 support for urban car infrastructure."
)

#NIMBY Confusion
desc_5 = ("A big proponent of urban car infrastructure finds out the new highway connector\n" 
    "will pass right over their home. They feel betrayed, move further into the suburbs,\n "
    "and oppose future developments.\n" 
    "+3 support for suburban development, -3 support for urban car infrastructure."

)

#will need to tune individual card counts
deck = (
    [Card("Tram Derailment", tram_derailment, desc_1, None) for _ in range(10)] +
    [Card("Strava Bro Assembly", strava_bro_assembly, desc_2, None) for _ in range(12)] +
    [Card("YIMBY Blunder", yimby_blunder, desc_3, "Strava Bro Assembly") for _ in range(6)] +
    [Card("Motor Envy", motor_envy, desc_4, None) for _ in range(13)] +
    [Card("NIMBY Confusion", nimby_confusion, desc_5, None) for _ in range(7)]
) 

Team_1 = 'Amsterdam'
Team_2 = 'Houston'

categories = ["density", "transit-infra", "suburb-devel", "urban-car-infra"]

# -------------------------------
# Win conditions (different for each team)
# -------------------------------
# 0: density
# 1: transit-infra
# 2: suburb-devel
# 3: urban-car-infra
def check_win(game_state):
    #need to determine appropriate criteria here
    s = game_state.scores
    #if density and transit-infra have individual scores each greater than 20, and
    #urban-car infra support 5 or below, win
    if s[0] >= 20 and s[1] >= 20 and s[3] <= 5:
        return Team_1
    #if suburb-devel and urban-car-infra have a combined score greater than 25, win
    if s[2] + s[3] >= 25:
        return Team_2
    return None

# -------------------------------
# Functionality for a player's turn
# -------------------------------
def player_turn(player, game_state, deck, discard_pile, players, max_hand=5):

    player.draw(deck, 1) #adjust how many card players draw at start of turn

    game_state.log(f"\n{player.name} ({player.team})'s hand:")
    for idx, card in enumerate(player.hand):
        print(f"{idx + 1}: {card.name}")

    while True:
        #wait for user input
        choice = input(f"\n{player.name}, choose a card to play (1-{len(player.hand)}) or d[number] for description: ")
        if choice.startswith("d"):
            try:
                desc_idx = int(choice[1:]) - 1
                if 0 <= desc_idx < len(player.hand):
                    print(f"\n{player.hand[desc_idx].name}: {player.hand[desc_idx].desc}")
                else:
                    print("Invalid card number for description.")
            except ValueError:
                print("Type 'd' followed by the card number, e.g., d2 for card 2.")
            continue
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(player.hand):
                card = player.hand.pop(idx)
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number or 'd' followed by a card number.")

    card.play(game_state, players, player.team, player.name)
    discard_pile.append(card)

    while len(player.hand) > max_hand:
        print(f"\n{player.name}'s hand (too many cards):")
        for idx, card in enumerate(player.hand):
            print(f"{idx + 1}: {card.name}")
        while True:
            try:
                discard_idx = int(input(f"\n{player.name}, choose a card to discard (1-{len(player.hand)}): ")) - 1
                if 0 <= discard_idx < len(player.hand):
                    discard = player.hand.pop(discard_idx)
                    discard_pile.append(discard)
                    game_state.log(f"{player.name} discards '{discard.name}'")
                    break
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")
