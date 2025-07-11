from source import *

def simulate_game():

    game = GameState()
    random.shuffle(deck)

    players = [
        Player("Alice", Team_1),
        Player("Bob", Team_2),
        Player("Carol", Team_1),
        Player("Dave", Team_2),
    ]

    discard_pile = []

    for player in players:
        player.draw(deck, 5)

    player_index = 0

    while deck:

        game.turn += 1
        player = players[player_index]
        print("\n----------------------------------------")
        print("Current scores:")
        for i in range(4):
            print(f"{categories[i]}: {game.scores[i]}")
        print("----------------------------------------")
        print(f"\n{player.name} ({player.team}) turn {game.turn}")
        player_turn(player, game, deck, discard_pile, players)
        winner = check_win(game)
        if winner:
            game.log(f"\n{winner.upper()} WINS!")
            break
        player_index = (player_index + 1) % len(players)
        print("\n----------------------------------------")
        print("Discard pile:")
        for card in discard_pile:
            print(card.name)
        print("----------------------------------------")


    print("\nFinal shared scores:")
    for i in range(4):
        print(f"{categories[i]}: {game.scores[i]}")

if __name__ == "__main__":
    simulate_game()