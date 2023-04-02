"""CSC111 Winter 2023 Project Phase 2: Black Jack Algorithim
Module Description
===============================

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the
CSC111 instructional team at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this material,
please consult the Canadian Copyright Act.
This file is Copyright (c) 2023 Alessia Ruberto, Karyna Lim, Rachel Kim, Sasha Chugani.
"""
from __future__ import annotations
from typing import Optional, Any
import random
import probability_tree as tree


class Card:
    """A Card Object that represents a card in the deck

    Instance Attributes:
    - name: the name-value of the card(ace, 2, 3, ... etc).
    - value:
        The numerical value of the card, corresponding to its name.
        In the initialization, the Ace is automatically given the value of 11 instead of 1.
    - suit: the suit of the card(heart, diamond, spade, club).

    Representation Invariants:
    - self.name in ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'king', 'queen', 'jack']
    - self.value in [2, 3, 4, 5, 6, 7, 8, 9, 10, (11, 1)]
    - self.suit in ['heart', 'diamond', 'spade', 'club']
    - (self.name not in ['10', 'jack', 'queen', 'king']) or (self.value == 10)
    - (self.name not 'ace') or (self.value == (1,11))
    - (self.name not in ['2', '3', '4', '5', '6', '7', '8', '9', '10']) or (self.value == str(self.name))
    """
    name: str
    value: int | tuple[int]
    suit: str

    def __init__(self, name: str, value: int, suit: str) -> None:
        """Initialize card class with with the name-value of the card, the numerical value of the card, and the suit of the card"""
        self.name = name
        self.value = value
        self.suit = suit


class Deck:
    """ The deck class of Card objects

    Instance Attributes:
    - deck:
        A mapping containing the cards for this deck.
        Each key in the mapping is one of the 13 possible values in a deck, and the corresponding value
        is a list of the Card objects (one for each suit).

    Representation Invariants:
    - all[self.deck[card_type] != [] for card_type in self.deck]
    - all[1 <= len(self.deck[card_type]) <= 4 for card_type in self.deck]

    """
    deck: dict[str, list[Card]]

    def __init__(self) -> None:
        """Intialize a new deck card object"""
        self._load_standard_deck()

    def _load_standard_deck(self) -> None:
        """Private method only called by the intializer"""
        self.deck = {}

        card_info = {'ace': (1, 11), '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                     'jack': 10, 'queen': 10, 'king': 10}
        suits = ['hearts', 'spades', 'clubs', 'diamonds']

        for card_type in card_info:
            self.deck[card_type] = []
            for suit in suits:
                self.deck[card_type].append(Card(card_type, card_info[card_type], suit))

    def __len__(self) -> int:
        """Return the total amount of cards in this deck object"""
        sum_so_far = 0

        for card_type in self.deck:
            sum_so_far += len(self.deck[card_type])

        return sum_so_far

    def draw_card(self, participant: Participant) -> Card:
        """ Selects a random card from the deck, then removes and returns it."""
        # Select card
        random_card_type = random.choice(list(self.deck))
        random_card = random.choice(self.deck[random_card_type])

        # Remove from deck
        self.deck[random_card_type].remove(random_card)

        # Remove from dictionary if all types of that card have been exhausted
        if not self.deck[random_card_type]:
            self.deck.pop(random_card_type)

        if random_card.name == "ace":
            random_card.value = self.determine_ace_value(participant)

        # Update card sums
        participant.sum_cards += random_card.value

        # Update card
        participant.new_cards.append(random_card)

        return random_card

    def determine_ace_value(self, participant: Participant) -> int:
        """ Returns which ace value should be used based on the state of the game, either 1 or 11
        """
        # this is only called when an ace is received in the participant's deck
        # need participant's current cards

        if participant.sum_cards + 11 <= 21:
            return 11
        else:
            return 1

    def _copy(self) -> Deck:
        """return a copy of the current deck state"""
        copy_deck = Deck()
        copy_deck.deck = {}
        for card_type in self.deck:
            copy_deck.deck[card_type] = self.deck[card_type].copy()

        return copy_deck

    def copy_deck_and_draw_specific_card(self, card_type: str) -> Deck:
        """Make a copy of a deck object, remove a specific card from that deck, and return the new copied deck"""

        copied_deck = self._copy()

        if card_type not in copied_deck.deck:  # this case should never happen
            copied_deck.deck.pop(card_type)
            raise ValueError

        else:
            copied_deck.deck[card_type].pop(0)

            if not copied_deck.deck[card_type]:  # copied_deck.deck[card_type] == []
                copied_deck.deck.pop(card_type)

        return copied_deck


class Participant:
    """
    An abstract class that represents the current state of the participant's cards.

    Dealer and Player objects will inherit from this parent class as they are both participants.

    Instance Attributes:
    - intial_face_up: The first face-up card obtained from the Deck.
    - intial_face_down: The face-down card obtained from the Deck.
    - new_cards: A list of the cards that have been given by the deck, useful to calculate total sum
    - sum_cards: The total sum of the

    Representation Invariants:
    - self.first_card is not self.second_card
    - self.first_card in self.new_cards
    - self.second_card in self.new_cards
    - all(card not in {self.first_card, self.second_card} for card in self.new_cards)
    - self.sum_cards == sum([card.value for card in self.new_cards])
    - self.sum_cards >= 0

    """
    first_card: Optional[Card]
    second_card: Optional[Card]
    new_cards: list[Card]  # new_cards list is actually the list of all cards received
    sum_cards: int

    def __init__(self) -> None:
        """Initialize a new participant with the given cards"""

        self.first_card = None
        self.second_card = None
        self.new_cards = []
        self.sum_cards = 0

    def __repr__(self) -> str:
        """Return a string representing of this object and their current cards in hand given the game state.
        __repr__ is a special method that's called when the object is evaluated in the Python console.
        Provided to help with testing/debugging.
        """
        raise NotImplementedError

    def hit(self, deck: Deck) -> None:
        """The participant draws another card which is added to self.new_cards and the card value is added
        in self.sum_cards. This method also mutates the current game state's deck

        Preconditions: (for all methods of the instances of this class)
        - deck.deck != {} # the deck is not empty
        """
        raise NotImplementedError

    def stand(self) -> None:
        """The participant will stop their turn of play and move on to the other participant or, if both
        participants turn has already ended, go end of the game"""
        raise NotImplementedError


class Dealer(Participant):
    """A Dealer object that represents the current game state of the dealer's cards.

    Instance Attributes:
    - intial_face_up:
        The first face-up card obtained from the Deck. The Player may use this card during the game to reference
        and guide their logic of moves.

    - intial_face_down:
        The face-down card obtained from the Deck. The Player may not use this card to decide / reference on which
        moves they should make.

    Representation Invariants:
    - self.intial_face_up is not self.intial_face_down
    - self.intial_face_up in self.new_cards
    - self.intial_face_down in self.new_cards
    - all(card not in {self.intial_face_up, self.intial_face_down} for card in self.new_cards)
    """
    initial_face_up: Card = Optional
    initial_face_down: Card = Optional

    def __init__(self) -> None:
        """Initialize a new Dealer with the given cards. Attributing the cards to face_up and face_down variable
        names for easier comprehension since the card attribution for the Dealer matters."""
        super().__init__()

        self.initial_face_up = self.first_card
        self.initial_face_down = self.first_card

    def __repr__(self) -> str:
        """Return a string representing of this dealer and their current card's values in hand given the game state.
        __repr__ is a special method that's called when the object is evaluated in the Python console.
        Provided to help with testing/debugging._
        """
        return f'Dealer({[card.value for card in self.new_cards]}) ' \
               f'Face-up -> {self.initial_face_up.value}, ' \
               f'Face-down -> {self.initial_face_down.value} '

    def hit_or_stand(self, current_player: Player, target: int) -> str:
        """Decide whether the dealer should hit or stand using the standard Blackjack logic to make
        the best move to win the game.

        Preconditions:
        - target >= 1
        - current_player is a valid Player object who has already made their moves and is now standing (not their turn)
        - current_player and this dealer object have the same target values

        """

        total_player_sum = current_player.sum_cards

        # assuming that target is 21, the standard target, then it is being compared to 17
        if total_player_sum > target and self.sum_cards > target - 4:
            # doesn't hit if player is greater than target, automatic win for dealer.
            return 'Stand'
        else:
            return 'Hit'

    def hit(self, deck: Deck) -> None:
        """The participant calls for another card to be added to their cards and for the current round of play.
        This reassigns self.sum_cards and mutates (appends) to self.new_cards. This also mutates the Deck of the game.

        """
        deck.draw_card(self)

    def stand(self) -> str:
        """The participant will stop their turn of play and move on to the other participant or, if both
        participants turn has already ended, go end of the game

        The goal of this funciton is to:
        a) ease comprehension for the logic when the game is running
        b) allow potential modifications to the game when stand() is called (potentially change difficulty levels)

        """
        pass


class Player(Participant):
    """
    A Player object that represents the current state of the player's cards from a given BlackJack game / deck state.

    Instance Attributes:
    - Identical as their parent class

    Representation Invariants:
    - Identical as their parent class
    """

    def __init__(self) -> None:
        """Initialize a new Player object"""
        super().__init__()

    def __repr__(self) -> str:
        """Return a string representing of this player and their current cards in hand given the game state.
        __repr__ is a special method that's called when the object is evaluated in the Python console.
        Provided to help with testing/debugging.
        """

        return f'Player({[card.value for card in self.new_cards]}) ' \
               f'First-card -> {self.first_card.value}, ' \
               f'Second-card -> {self.second_card.value} '

    def hit_or_stand(self, current_dealer: Dealer, target: int) -> str:
        """Decide whether the player should hit or stand given the standard Blackjack logic to make
        the best move to win the game.

        Preconditions:
        - target >= 1
        - current_dealer is a valid Dealer object who has already drawn their intial cards
        - current_player and this dealer object have the same target values

        """

        """lmao idk why this was the logic cos its only comparing the first sum???"""
        # intial_sum = self.first_card.value + self.second_card.value
        # dealer_card = current_dealer.initial_face_up
        #
        # # Blackjack logic, assume that dealer's second card (dealer.intial_face_down) is 10
        # if intial_sum < dealer_card.value + 10 and intial_sum != target:
        #
        #     return "Hit"
        #
        # else:
        #     return "Stand"

        if self.sum_cards < current_dealer.initial_face_up.value + 10 and self.sum_cards < target:
            return 'Hit'
        else:
            'Stand'

    def hit(self, deck: Deck) -> None:
        """The participant calls for another card to be added to their cards and for the current round of play"""
        deck.draw_card(self)

    def stand(self) -> str:
        """The participant will stop their turn of play and move on to the other participant or, if both
        participants turn has already ended, go end of the game"""
        pass


class BlackJack:
    """
    A class representing a Black Jack game (one round of play)

     Instance Attributes:
     - deck: the deck for this game
     - dealer: the dealer for this game
     - player: the player for this game
     - current_turn: whose turn it currently is in the game

    Representation Invariants:
    - self.current_turn in {"Player's turn", "Dealer's turn", "Game End"}
    - deck, dealer, and player objects follow the same logic and invariants from their own classes

    """
    deck: Deck
    dealer: Dealer
    player: Player
    current_turn: str

    def __init__(self) -> None:
        """"Intialize the game"""

        self.deck = Deck()
        self.dealer = Dealer()
        self.player = Player()
        self.current_turn = "Player's turn"

    def run_game(self, target: int) -> str:
        """Run a BlackJack game with respect to the target number being the goal for the players.

        For all possible end game cases, please refer to self.handle_end_game()

        Preconditions:
        - target >= 1 # in original game it's 21
        - self.current_turn == "Player's turn", (ie the game just started)
        - the player and dealer's first/second or face-up/face-down cards are None,
        their sum_cards are 0 and their new_cards lists are empty
        - self.deck is a full, unmutated deck, as intialized
        - when current_turn == "Game End", then the returned
        output str is in {"Player Wins", "Dealer Wins","Push (tie)"}
        """

        # Give out initial cards for dealer
        self.dealer.initial_face_up = self.deck.draw_card(self.dealer)
        self.dealer.initial_face_down = self.deck.draw_card(self.dealer)

        # Give out initial cards for player
        self.player.first_card = self.deck.draw_card(self.player)
        self.player.second_card = self.deck.draw_card(self.player)

        while self.current_turn != "Game End":  # TODO loop might be redundant (atleast for original version)

            self.handle_player_turn(target)
            self.handle_dealer_turn(target)
            # TODO

        return self.handle_end_game(target)

    def run_probability_game(self, threshold: float, target: int) -> str:
        """run a game, but the player's make_moves are determined by the probability tree moves and the busting
        threshold that the user is okay with busting equal to or less than.

        Same implementation as run_game, except for how the player handles their turn

        Preconditions:
        - same as run_game
        - target >= 1
        - 0.0 <= threshold <= 1.0
        # 0.0 implies we stand, even if there's a small chance of busting.
        # 1.0 implies we always hit, regardless of how close we are to busting.

        """
        # make random game
        # Give out initial cards for dealer
        self.dealer.initial_face_up = self.deck.draw_card(self.dealer)
        self.dealer.initial_face_down = self.deck.draw_card(self.dealer)

        # Give out initial cards for player
        self.player.first_card = self.deck.draw_card(self.player)
        self.player.second_card = self.deck.draw_card(self.player)

        # make tree of all possibilities
        # ** NEW ** different than run_game()
        pt = tree.ProbabilityTree(self.player.sum_cards)
        generated_tree = pt.generate_tree(self.deck, target)

        assert self.current_turn == "Player's turn"  # comment after testing TODO

        while self.current_turn != "Game End":
            # ** NEW ** different than run_game()
            self.handle_player_turn_v2(generated_tree, threshold, target)
            self.handle_dealer_turn(target)

        print([card.value for card in self.player.new_cards])  # TODO
        print([card.value for card in self.dealer.new_cards])  # TODO

        return self.handle_end_game(target)

    def handle_player_turn(self, target) -> None:
        """ How the player makes their turn in the game.

        This implementation is equivalent to the basic Black Jack logical strategy.

        Preconditions:
        - target is the same value used throughout the running game functions

        # preconditions for player
        - self.current_turn == "Player's turn"
        - self.player.first_card != None
        - self.player.second_card != None
        - self.player.sum_cards != 0
        - self.player.new_cards != []

        # preconditions for the deck
        - self.deck.__len__() == 48 # since the first four cards have been drawn

        # preconditions for the dealer, as hit_or_stand functions require a dealer
        - self.dealer.initial_face_up != None
        - self.dealer.initial_face_down != None
        - self.dealer.sum_cards != 0
        - self.dealer.new_cards != []

        """
        while self.current_turn == "Player's turn":

            current_move = self.player.hit_or_stand(self.dealer, target)

            if current_move == "Hit":
                self.player.hit(self.deck)  # hit will update the new cards chosen, reclaulctae sum,

            else:
                self.player.stand()  # keep this to visualize the action and in case another player child class
                # inherits a different method
                self.current_turn = "Dealer's turn"

        assert self.current_turn == "Dealer's turn"  # TODO remove after testing

    def handle_player_turn_v2(self, probability_tree: tree.ProbabilityTree, threshold: float,
                              target: int) -> None:
        """
        How the Player makes a turn in a probability tree game.

        Preconditions:
        - same as self.handle_player_turn()
        - threshold and target are the same value as the one chosen in self.run_probability_game()

        """

        # variable to store which tree branch's root we are recursing down
        curr_tree_depth = probability_tree

        while self.current_turn == "Player's turn":
            # given the probability tree, threshold and target, suggest a move for the player
            suggested_move = curr_tree_depth.hit_or_stand_threshold(threshold=threshold, curr_deck=self.deck,
                                                                    target=target)
            # only follow through with the suggestion if it is less than the target
            # since when its equal to the target, it wouldn't make sense to hit again regardless.
            if suggested_move == "Hit" and self.player.sum_cards < target:
                self.player.hit(self.deck)

                # reassign the tree holder variable by finding the subtree that equals the new sum
                # taht was just pulled from deck
                curr_tree_depth = curr_tree_depth.find_subtree_by_sum(self.player.sum_cards)[
                    self.player.new_cards[-1].name]  # the most recent card pulled, cos list.append for new cards to lst

            # condition --> self.player.sum_cards >= target or suggested_move == "Stand":
            else:
                self.player.stand()  # keep this to visualize the action and allow for future updates
                self.current_turn = "Dealer's turn"  # reassign to stop the loop for handle turn

        assert self.current_turn == "Dealer's turn"  # TODo remove after testing

    def handle_dealer_turn(self, target: int) -> None:
        """The dealer's turn to make a move that follows the rules the dealer
        can complete with the given blackjack state to try and win the game.

        Preconditions:
        - all dealer attributes of cards are non-empty.
        - method is only called after the player's turn was handled.
        - follow same target as the given game was running previously.
        """

        # if self.player.sum_cards <= target:
        while self.player.sum_cards <= target and self.dealer.sum_cards <= target - 4:  # 21-4=17 for og BJ game
            self.dealer.hit(self.deck)

        self.current_turn = 'Game End'
        assert self.current_turn == "Game End"  # TODO, remove after

    def handle_end_game(self, target: int) -> str:
        """ Take the sum of the players cards and the sum of the dealers cards and
        compare them to see who won the game and return the winner

        Preconditions:
        - self.current_turn == "Game End"
        - dealer and player card attributes are NON-EMPTY & NON-ZERO
        - self.deck.deck.__len__() <= 48

        """
        if self.player.sum_cards == target and self.dealer.sum_cards == target:
            return 'Push (Tie)'

        elif self.player.sum_cards == self.dealer.sum_cards:
            return 'Push (Tie)'

        elif self.player.sum_cards > target:  # TODO do we need to add this condition? "and self.dealer.sum_cards > 21"?
            return 'Dealer Wins'

        elif self.dealer.sum_cards > target:
            return 'Player Wins'

        elif self.dealer.sum_cards == target or (
                self.player.sum_cards < self.dealer.sum_cards):
            return 'Dealer Wins'

        elif self.player.sum_cards == target or (
                self.dealer.sum_cards < self.player.sum_cards):
            return 'Player Wins'

        else:
            raise InterruptedError


if __name__ == '__main__':
    ...
    import python_ta

    # python_ta.check_all(config={
    #     'extra-imports': [],  # the names (strs) of imported modules
    #     'allowed-io': [],     # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })
