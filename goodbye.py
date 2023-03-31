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
        self.move = None  # move will be determined when producing probability tree

    def record_participant(self, participant: bj.Participant):
        """Record the actions of the participant to calculate probabilities of any future moves or if they should be a move at all

        Representations Invariants:
        - participant exists
        - a card has been drawn

        """

        self.current_total = participant.sum_cards


class ProbabilityTree:
    """The tree that runs through every possibility of the game to make the best possible desicion for the player to ensure they get close
    a win.

    Instance Attributes:
    ...
    - if making probability tree, then game should exist

    """

    root: SumNode
    _subtrees: dict[str, ProbabilityTree]  # match same type as deck implementation

    def __init__(self, value: int) -> None:
        self.root = SumNode(value)
        self._subtrees = {}
        # start off with assuming 0% busting! very ideal situation

    def generate_tree(self, decky: bj.Deck) -> ProbabilityTree | None:
        """
        return the move the player should do assuming they will win
        and with respect to their bust-probability-threshold
        Representation Invariants:
        - timeout karyna

        """

        # base case
        # okay i guess self.threshold is the proportion of busting and threshold is actually
        # the thing we've been comparing since the beginning

        if self.root.current_total >= 21:
            # example, we chose 50% of busting, we'll stand, and we got a 52% chance of picking a card
            # that'll ensure we don't bust, so we WONT stand.
            # if we got a 40% chance of picking a card where we wont bust, we WILL stand, cos its lower
            # than our desired threshold to bust. ie. we got 60% chance of busting over us only being ok at 50%

            # my logic, you can't have a probabilitly sent out, it has to be predetermined
            # so even with intializing the probability at 1.0, it works for SumNodes that
            # haven't computed their fraction yet.

            self.root.move = "stand"
            return None

        # recursive step
        else:
            # the move to get here was a hit
            self.root.move = "hit"
            deck_class = decky.deck

            # underneath, calculating probability score
            # compute probability to hit or stand and need length to compute probabilities

            # hitting_proportion = 0 --> actually only need one of the proportions to make a decision anyways

            standing_proportion = 0
            total_cards = decky.__len__()

            # compute all possible subtrees,
            for card_type in deck_class:

                # each element is a string of the card
                if card_type == 'ace' and self.root.current_total + 11 > 21:
                    value_to_add = 1
                elif card_type == 'ace' and self.root.current_total + 11 <= 21:
                    value_to_add = 11
                else:
                    value_to_add = deck_class[card_type][0].value
                    # know we can always index 0 since the card is in here

                total_for_subtree_node = value_to_add + self.root.current_total

                # adding amount of cards based on if it should hit or stand after receiing it
                if total_for_subtree_node > 21:
                    standing_proportion += len(deck_class[card_type])

                # else:
                #     hitting_proportion += len(deck_class[card_type])

                # actually adding the values to our probability tree
                self._subtrees[card_type] = ProbabilityTree(total_for_subtree_node)

            stat = standing_proportion / total_cards
            for subtree_str in self._subtrees:
                # compute copy of new blackjack assuming this one card was taken out!
                deck_copy = decky.copy()
                deck_copy.manual_take_out(subtree_str)

                # same threshold as before
                self._subtrees[subtree_str].generate_tree(deck_copy)

        return self

    def _str_indented(self, indent: int) -> str:
        str_so_far = '  ' * indent + f'{str(self.root.current_total)}\n'
        for subtree in self._subtrees.values():
            str_so_far += subtree._str_indented(indent + 1)
        return str_so_far


if __name__ == '__main__':
    ...
    import python_ta

    # python_ta.check_all(config={
    #     'extra-imports': [],  # the names (strs) of imported modules
    #     'allowed-io': [],     # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })

"""
testing shit:

black_jack_intialized = bj.BlackJack()
black_jack_intialized.dealer.initial_face_up = black_jack_intialized.deck.draw_card(black_jack_intialized.dealer)
black_jack_intialized.dealer.initial_face_down = black_jack_intialized.deck.draw_card(black_jack_intialized.dealer)
black_jack_intialized.player.first_card = black_jack_intialized.deck.draw_card(black_jack_intialized.player)
black_jack_intialized.player.second_card = black_jack_intialized.deck.draw_card(black_jack_intialized.player)
pt = ProbabilityTree(black_jack_intialized.player.sum_cards)

# won't work
pt.generate_tree(black_jack_intialized, 0.5)

"""
