"""CSC111 Winter 2023 Project Phase 2: Black Jack Algorithim

Module Description
===============================

This Python module contains a blablabla

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
from typing import Optional
import random

ALL_STATUSES = {"Player's Turn", "Dealer's Turn", "Game_End"} # TODO ask david 🥴🥴

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
        name = name
        value = value
        suit = suit


class Deck:
    """The deck of cards
    
    Instance Attributes:
    - deck: 
        A mapping containing the cards for this deck.
        Each key in the mapping is one of the 13 possible values in a deck, and the corresponding value 
        is a list of the Card objects (one for each suit).
        
    Representation Invariants:
    - all[self.deck[card_type] != [] for card_type in self.deck]
    
    
    """
    deck: dict[str, list[Card]]
    
    def __init__(self) -> None:
        self._load_standard_deck()

                
    def _load_standard_deck(self) -> None:
        self.deck = {}
        
        card_info = {'ace': (1,11), '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'jack': 10, 'queen': 10, 'king': 10}
        suits = ['hearts', 'spades', 'clubs', 'diamonds']
        
        for card_type in card_info:
            self.deck[card_type] = []
            for suit in suits:
                self.deck[card_type].append(Card(card_type, card_info[card_type], suit))
        
    
    def draw_card(self, partcipant: Participant) -> Card:
        """ Selects a random card from the deck, then removes and returns it.
        """
        # Select card
        random_card_type = random.choice(self.deck)
        random_card = random.choice(self.deck[random_card_type])

        # Remove from deck
        self.deck[random_card_type].remove(random_card)
        
        # Remove from dictionary if all types of that card have been exhausted
        if self.deck[random_card_type] == []:
            self.deck.pop([random_card_type])  

        if random_card.name == "ace":                                                       # TODO make a helper function to determine ace value
            ...                                                          
            
        # Update card sums
        Participant.sum_cards += random_card.value
        
        return random_card
    
    # TODO have a way to determine ace value
    

class Participant:
    """
    An abstract class that represents the current game state of the participant's cards.
    Dealer and Player ojbects will inherit 

    Instance Attributes:
    - intial_face_up: The first face-up card obtained from the Deck.
    - intial_face_down: The face-down card obtained from the Deck.
    - new_cards: A list of the cards that have been given by the deck, if the Dealer chooses to hit.
    - sum_cards: The total sum of the 

    Representation Invariants:
    - self.intial_face_up is not self.intial_face_down
    - all(card not in {self.intial_face_up, self.intial_face_down} for card in self.new_cards)

    """
    first_card: Card = Optional
    second_card: Card = Optional
    new_cards: list[Card]
    sum_cards: int
    
    def __init__(self) -> None:
        """Initialize a new Dealer with the given cards"""
        
        self.first_card = None
        self.second_card = None
        self.new_cards = [self.first_card, self.second_card]
        self.sum_cards = 0

    def __repr__(self) -> str:
        """Return a string representing of this object and their current cards in hand given the game state.

        __repr__ is a special method that's called when the object is evaluated in the Python console.
        Provided to help with testing/debugging.

        """
        
        NotImplementedError
    
    def hit_or_stand(self) -> None: 
        """Decide whether the participant should hit or stand using the standard Blackjack logic to make 
        the best move to win the game."""

        NotImplementedError

    def hit(self) -> str:
        """hi david/to whom it may concern(random TA) we know how to do inheritance!
        please give us bonus marks thank you"""
        NotImplementedError


    def stand(self) -> str: 
        """"""
        NotImplementedError
        
        

class Dealer(Participant):
    """A Dealer object that represents the current game state of the dealer's cards

    Instance Attributes:
    - intial_face_up: The first face-up card obtained from the Deck.
    - intial_face_down: The face-down card obtained from the Deck.

    Representation Invariants:
    - self.intial_face_up is not self.intial_face_down
    - all(card not in {self.intial_face_up, self.intial_face_down} for card in self.new_cards)

    """
    initial_face_up: Card = Optional
    initial_face_down: Card = Optional
  
    def __init__(self) -> None:
        """Initialize a new Dealer with the given cards"""
        super().__init__()
        
        self.initial_face_up = self.first_card
        self.initial_face_down = self.first_card

    def __repr__(self) -> str:
        """Return a string representing of this dealer and their current cards in hand given the game state.

        __repr__ is a special method that's called when the object is evaluated in the Python console.
        Provided to help with testing/debugging.

        >>> dealer..._
        """
        return f'Node({self.address})'

    # def hit_or_stand(self, current_player: Player) -> str:
    #     """Decide whether the dealer should hit or stand using the standard Blackjack logic to make 
    #     the best move to win the game."""

    #     total_player_sum = current_player.sum_cards
        
    #     if total_player_sum > 21 or self.sum_cards > 17:

    #         return 'Stand'
        
    #     else:

    #         return 'Hit'
       


       # TODO, they dont hit if the player looses!
    def hit(self, deck: Deck) -> str:
        """Draw a card and see if you have to hit or stand again."""
        card = deck.draw_card()

        
        

    def stand(self) -> str: 
        """..."""
        ...
        



class Player(Participant):
    """ 
    
    A Player object that represents the current game state of the player's cards
    

    Instance Attributes:
    - intial_card_1: The first card obtained from the game, from the Deck.
    - intial_card_2: The second card obtained from the game, from the Deck.
   
    Representation Invariants:
    - intial_card_1 is not intial_card_2
    - all(card not in {self.intial_card_1, self.intial_card_2} for card in self.new_cards) 
    
    """
    
    def __init__(self) -> None:
        """Initialize a new Player with the given cards"""
        super().__init__()
        
    def __repr__(self) -> str:
        """Return a string representing of this player and their current cards in hand given the game state.

        __repr__ is a special method that's called when the object is evaluated in the Python console.
        Provided to help with testing/debugging.

        >>> player_david = Player()
        >>> player_david
        Player(card 1 -> None, card 2 -> None, new_cards -> [])
        >>> # make game tree that assigns card to david
        >>> player_david
        Player(card 1 -> 4 of hearts, card 2 -> 7 of spades, new_cards -> [])
        """

        return f'Player(card 1 -> None, card 2 -> None, new_cards -> [])' # do something else 
    
    def hit_or_stand(self, current_dealer: Dealer, current_deck: Deck) -> str:
        """Decide whether the dealer should hit or stand using the standard Blackjack logic to make 
        the best move to win the game."""

        intial_sum = self.first_card + self.second_card
        dealer_card = current_dealer.initial_face_up

        # Blackjack logic, assume that dealer's second card (dealer.intial_face_down) is 10

        if intial_sum < dealer_card + 10 and intial_sum != 21 :
            
            return "Hit"

        else:    
            return "Stand"
         


class BlackJack:
    """
    
    A class representing the game
    
     Instance Attributes:
     - deck: the deck for this game
     - dealer: the dealer for this game
     - player: the player for this game
     - current_turn: whose turn it currently is in the game

    
    Representation Invariants:
    - self.current_turn in {"Player's Turn", "Dealer's Turn", "Game End"}

    
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

    def run_game(self) -> None:
        """Start game, send deck"""

        # Give out initial cards for dealer
        self.dealer.initial_face_up = self.deck.draw_card()
        self.dealer.initial_face_down = self.deck.draw_card()

        # Give out initial cards for player
        self.player.first_card = self.deck.draw_card() 
        self.player.second_card = self.deck.draw_card()

        while self.current_turn != "Game_End":                      # TODO loop might be redundant (atleast for original version)

            self.handle_player_turn()
            self.handle_dealer_turn()
            # TODO
        
        return self.handle_end_game()

    def handle_player_turn(self) -> None:
    
        while self.current_turn == "Player's Turn" or self.player.sum_cards < 21: # FIXME hit_or_stand for player also checks this, so <21 might be redundant
    
            
            current_move = self.player.hit_or_stand(self.dealer, self.deck)
            
            if current_move == "hit":
                self.player.hit() # hit will update the new cards chosen, reclaulctae sum, 
            
            else:
                self.player.stand() # keep this to visualize the action and in case another player child class inherits a different method
                self.current_turn = "Dealer's Turn"
        
        assert self.current_turn == "Dealer's Turn"                           # TODO remove after testing

    def handle_dealer_turn(self) -> None:
        ...
        
    def handle_end_game(self) -> str:
        
        if self.player.sum_cards == 21 and self.dealer.sum_cards == 21:
            return 'Tie'

        elif self.player.sum_cards > 21:  # TODO do we need to add this condition? "and self.dealer.sum_cards > 21"?
            return 'Bust'
        
        elif self.dealer.sum_cards == 21 or (self.player.sum_cards < self.dealer.sum_cards and self.dealer.sum_cards < 21):
            return 'Dealer wins'
        
        elif self.player.sum_cards == 21 or (self.dealer.sum_cards < self.player.sum_cards and self.player.sum_cards < 21):
            return 'Player Wins'
         
        else:
            return 'U fucked up and forgot a case'        # TODO remove after testing
  
  
    
class ProbabilityTree:
    """fghfh"""

    move: str | tuple[str, ...]  
    guesser_win_probability: float
    _subtrees: dict[str | tuple[str, ...], ProbabilityTree]

    def __init__(self) -> None:
        ...

    

if __name__ == '__main__':
    ...
    import python_ta
    
    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],     # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })