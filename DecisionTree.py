"""CSC111 Winter 2023 Project Phase 2: Black Jack Algorithim
Module Description
===============================
This Python module contains a baddie ehhhhhh               TODO remove profanities 😼
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
import BlackJack_Game as bj

class SumNode:
    """The node representing a subtree in the Tree."""

    current_total: int
    move: Optional[str]

    def __init__(self, current_total: int) -> None:
        """Initialize the class SumNode."""
        
        self.current_total = current_total
        self.move = None # move will be determined when producing probability tree

    def record_participant(self, participant: bj.Participant):
        """Record the actions of the participant to calculate probabilities of any future moves or if they should be a move at all
        
        Representations Invariants:
        - participant exists
        - a card has been drawn 
        
        """
    # FIXME to delete later, but to remind of which attributes are in participant
    # first_card: Optional[Card]
    # second_card: Optional[Card]
    # new_cards: list[Card]
    # sum_cards: 

        self.current_total = participant.sum_cards 
        
    

class ProbabilityTree:
    """The tree that runs through every possibility of the game to make the best possible desicion for the player to ensure they get close 
    a win. 
    
    Instance Attributes:
    ...
    - if making probability tree, then game should exist
    
    """

    root: SumNode
    _subtrees: dict[int, ProbabilityTree]
    threshold: float

    def __init__(self, value: int) -> None:
        self.root = SumNode(value)
        self.threshold = 0.0

    def generate_tree(self, root_value: int, game_state: bj.BlackJack, threshold: float) -> ProbabilityTree:
        """
        return the move the player should do assuming they will win 
        and with respect to their bust-probability-threshold

        Representation Invariants:
        - timeout karyna
    
        """
        self.threshold = threshold

        # base case
        if root_value >= 21: # TODO add "or probability >= threshold"
            #self.root.move = "stand"
            return

        #recursive step
        else:
            #self.root.move = "hit"
            
            deck_class = game_state.deck.deck
            total_cards = deck_class.deck.__len__

            # compute all possible subtrees, 
            for card_type in deck_class:
                value_to_add = 0

                # each element is a string of the card
                if card_type == 'ace' and self.root.current_total + 11 > 21:
                    value_to_add = 1
                elif card_type == 'ace' and self.root.current_total + 11 <= 21:
                    value_to_add = 11
                else:
                    value_to_add = deck_class[card_type][0].value

                total_for_subtree_node = value_to_add + self.root.current_total
                if value_to_add in self._subtrees:
                    self._subtrees[value_to_add] +=  ProbabilityTree(SumNode(total_for_subtree_node))
                else:
                    self._subtrees[value_to_add] =  ProbabilityTree(SumNode(total_for_subtree_node))

            for subtree in self._subtrees:
                new_deck = xyzdeck_function_to_edit() # updated game state to access a copy of a hypothetical deck
                
                subtree.generate_tree(curr_deck=new_deck, )

        return self
    


    def generate_tree_alessia_v(self, root_value: int, game_state: bj.BlackJack): 
        # Base Case
        if root_value >= 21: # TODO add "or probability >= threshold"
            return ProbabilityTree(root_value, self.threshold)
        else:
            probability_tree = ProbabilityTree(root_value, self.threshold)

            for card_type in game_state.deck.deck:
                if card_type == 'ace':
                    new_sum = root_value + ... # TODO continue here
                new_sum = game_state.deck.deck[card_type]
                tree = self.generate_tree_alessia_v(new_sum, game_state.update_deck_and_return_game_state(card_type))

                

        """
            # Base Case?
            if d == 0 or game_state.get_winner() == 'Guesser':
                if game_state.get_winner() == 'Guesser':
                    game_tree = a2_game_tree.GameTree(root_move, 1.0)
                else:
                    game_tree = a2_game_tree.GameTree(root_move)
                return game_tree
            # elif game_state.get_winner() == 'Guesser':  # NEW: this way it will edit leaf appropriately
            #     print('in elif')
            #     return a2_game_tree.GameTree(root_move, 1.0)
            else:
                game_tree = a2_game_tree.GameTree(root_move)
                possible_answers = game_state.get_possible_answers()

                # If word or GAME_START_MOVE
                if isinstance(root_move, tuple) or root_move == '*':
                    for answer in possible_answers:
                        tree = generate_complete_game_tree(answer, game_state.copy_and_record_guesser_move(answer), d - 1)
                        game_tree.add_subtree(tree)

                # Othewise it's a status
                else:
                    for answer in possible_answers:
                        status = game_state.get_status_for_answer(answer)
                        tree = generate_complete_game_tree(status, game_state.copy_and_record_adversary_move(status), d - 1)
                        game_tree.add_subtree(tree)
                return game_tree
        """










if __name__ == '__main__':
    ...
    import python_ta

    # python_ta.check_all(config={
    #     'extra-imports': [],  # the names (strs) of imported modules
    #     'allowed-io': [],     # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })
