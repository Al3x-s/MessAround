import random
from collections import Counter

class PokerGame:
    def __init__(self, num_players=5, starting_chips=100):
        self.num_players = num_players
        self.deck = self.generate_deck()
        self.players = [Player(f"Player {i+1}", starting_chips) for i in range(num_players)]
        self.current_player = 0
        self.pot = 0
        self.small_blind = 5
        self.big_blind = 10

    def generate_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_hole_cards(self, num_cards=2):
        for player in self.players:
            for _ in range(num_cards):
                card = self.deck.pop()
                player.add_card(card)

    def collect_blinds(self):
        small_blind_player = self.players[self.current_player]
        big_blind_player = self.players[(self.current_player + 1) % self.num_players]

        small_blind_player.bet(self.small_blind)
        big_blind_player.bet(self.big_blind)

        self.pot += self.small_blind + self.big_blind

        print(f"\n{small_blind_player.name} posts small blind: {self.small_blind}")
        print(f"{big_blind_player.name} posts big blind: {self.big_blind}")

    def show_table(self, community_cards=None):
        print("\n----- Table -----")
        print(f"Pot: {self.pot}")
        for player in self.players:
            print(f"{player.name} (Chips: {player.chips}): {player.show_hand()}")
        if community_cards:
            print(f"Community Cards: {', '.join(community_cards)}")

    def take_user_action(self, player, min_bet):
        while True:
            action = input(f"{player.name}, choose your action (fold/check/bet): ").lower()

            if action == 'fold':
                print(f"{player.name} folds.")
                player.fold()
                return 'fold'

            if action == 'check':
                print(f"{player.name} checks.")
                return 'check'

            if action == 'bet':
                bet_amount = int(input(f"Enter your bet (minimum bet: {min_bet}): "))
                if bet_amount < min_bet or bet_amount > player.chips:
                    print("Invalid bet amount. Please bet a valid amount.")
                else:
                    print(f"{player.name} bets: {bet_amount}")
                    player.bet(bet_amount)
                    self.pot += bet_amount
                    return 'bet'

            print("Invalid action. Please choose 'fold', 'check', or 'bet'.")

    def play_betting_round(self):
        min_bet = self.big_blind
        for player in self.players:
            if not player.is_folded():
                action = self.take_user_action(player, min_bet) if player == self.players[0] else self.computer_player_action(player, min_bet)
                
                if action == 'bet':
                    min_bet = max(min_bet, player.current_bet)

        return min_bet

    def computer_player_action(self, player, min_bet):
        # For simplicity, computer players always choose 'check' or 'bet'
        if player.chips > min_bet:
            bet_amount = random.randint(min_bet, min(player.chips, min_bet + 20))
            print(f"{player.name} bets: {bet_amount}")
            player.bet(bet_amount)
            self.pot += bet_amount
            return 'bet'
        else:
            print(f"{player.name} checks.")
            return 'check'

    def play_hand(self):
        self.shuffle_deck()
        self.collect_blinds()

        # Deal hole cards
        self.deal_hole_cards()

        # Betting round before the flop
        min_bet = self.play_betting_round()

        # Deal flop
        community_cards = []
        for _ in range(3):
            card = self.deck.pop()
            community_cards.append(f"{card['rank']} of {card['suit']}")
        self.show_table(community_cards)

        # Betting round after the flop
        min_bet = self.play_betting_round()

        # Deal turn
        card = self.deck.pop()
        community_cards.append(f"{card['rank']} of {card['suit']}")
        self.show_table(community_cards)

        # Betting round after the turn
        min_bet = self.play_betting_round()

        # Deal river
        card = self.deck.pop()
        community_cards.append(f"{card['rank']} of {card['suit']}")
        self.show_table(community_cards)

        # Final betting round after the river
        min_bet = self.play_betting_round()

        # Showdown
        self.showdown(community_cards)

    def showdown(self, community_cards):
        print("\n----- Showdown -----")
        self.show_table(community_cards)

        # Determine the winner and distribute the pot
        winning_player = max(self.players, key=lambda player: player.evaluate_hand(community_cards))
        print(f"\n{winning_player.name} wins the pot: {self.pot}")
        winning_player.chips += self.pot

    def play_game(self):
        print("Welcome to Texas Hold'em Poker Game!")
        while True:
            self.play_hand()

            play_again = input("Do you want to play another hand? (yes/no): ").lower()
            if play_again != 'yes':
                print("Thanks for playing!")
                break
    def play_betting_round(self):
        min_bet = self.big_blind
        for player in self.players:
            if not player.is_folded():
                action = self.take_user_action(player, min_bet) if player == self.players[0] else self.computer_player_action(player, min_bet)

                if action == 'bet':
                    min_bet = max(min_bet, player.current_bet)

        return min_bet

    def take_user_action(self, player, min_bet):
        while True:
            action = input(f"{player.name}, choose your action (fold/check/bet): ").lower()

            if action == 'fold':
                print(f"{player.name} folds.")
                player.fold()
                return 'fold'

            if action == 'check':
                if player == self.players[0] and min_bet == 0:
                    print(f"{player.name} checks.")
                    return 'check'
                else:
                    print("Invalid action. You can only check when it's your turn and the current bet is zero.")

            if action == 'bet':
                bet_amount = int(input(f"Enter your bet (minimum bet: {min_bet}): "))
                if bet_amount < min_bet or bet_amount > player.chips:
                    print("Invalid bet amount. Please bet a valid amount.")
                else:
                    print(f"{player.name} bets: {bet_amount}")
                    player.bet(bet_amount)
                    self.pot += bet_amount
                    return 'bet'

            print("Invalid action. Please choose 'fold', 'check', or 'bet'.")


class Player:
    def __init__(self, name, chips):
        self.name = name
        self.hand = []
        self.chips = chips
        self.current_bet = 0
        self.folded = False
    
    def add_card(self, card):
        self.hand.append(card)

    def show_hand(self):
        return ', '.join(f"{card['rank']} of {card['suit']}" for card in self.hand)

    def bet(self, amount):
        self.chips -= amount
        self.current_bet = amount

    def fold(self):
        self.folded = True

    def is_folded(self):
        return self.folded

    def evaluate_hand(self, community_cards):
        all_cards = self.hand + community_cards

        # Count the occurrences of each rank
        rank_counts = Counter(card['rank'] for card in all_cards)

        # Check for a straight flush
        if self.has_straight_flush(all_cards):
            return 9  # Straight Flush

        # Check for four of a kind
        if self.has_four_of_a_kind(rank_counts):
            return 8  # Four of a Kind

        # Check for a full house
        if self.has_full_house(rank_counts):
            return 7  # Full House

        # Check for a flush
        if self.has_flush(all_cards):
            return 6  # Flush

        # Check for a straight
        if self.has_straight(rank_counts):
            return 5  # Straight

        # Check for three of a kind
        if self.has_three_of_a_kind(rank_counts):
            return 4  # Three of a Kind

        # Check for two pairs
        if self.has_two_pairs(rank_counts):
            return 3  # Two Pairs

        # Check for a pair
        if self.has_pair(rank_counts):
            return 2  # One Pair

        # If none of the above, return the highest card value
        return 1  # High Card

    def has_straight_flush(self, all_cards):
        # Implement logic for a straight flush
        # For simplicity, this example does not implement the logic.

        return False

    def has_four_of_a_kind(self, rank_counts):
        return any(count == 4 for count in rank_counts.values())

    def has_full_house(self, rank_counts):
        return any(count == 3 for count in rank_counts.values()) and any(count == 2 for count in rank_counts.values())

    def has_flush(self, all_cards):
        # Implement logic for a flush
        # For simplicity, this example does not implement the logic.

        return False

    def has_straight(self, rank_counts):
        # Implement logic for a straight
        # For simplicity, this example does not implement the logic.

        return False

    def has_three_of_a_kind(self, rank_counts):
        return any(count == 3 for count in rank_counts.values())

    def has_two_pairs(self, rank_counts):
        return sum(count == 2 for count in rank_counts.values()) == 2

    def has_pair(self, rank_counts):
        return any(count == 2 for count in rank_counts.values())

if __name__ == "__main__":
    poker_game = PokerGame()
    poker_game.play_game()
