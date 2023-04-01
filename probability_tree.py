"""CSC111 Winter 2023 Project Phase 2: Black Jack Probability Tree Algorithim

Module Description
===============================
lil shawtie the baddest and she got her ways aye bud

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
import black_jack_game as bj
import plotly.graph_objects as go


class SumNode:
    """
    The node object representing the current total of a player's cards and their
    next move based on the current value.

    Instance Attributes:
    current_total:
        - the sum of a player's current cards, including all cards in a player's new_cards list
    move:
        - the next move a player should make, given their current value and game state
          # computed later with generate game tree

    Preconditions:
    - if SumNode represents a player's game state, then the player must have already been drawn their two intial cards

    Representation Invariants:
    - self.move is None or self.move in {'hit', 'stand}
    - self.current_total > 1 # since there's always two cards
    """

    current_total: int
    move: Optional[str]

    def __init__(self, current_total: int) -> None:
        """Initialize the SumNode object."""

        self.current_total = current_total
        self.move = None  # move will be determined when producing probability tree

    def record_participant(self, participant: bj.Participant):
        """Record the actions of the participant to calculate probabilities of any future moves or if they should be a move at all

        Preconditions:
        - participant object exists in a BlackJack object game and must have already been dealt two cards

        Representation Invariants:
        - participant.current_total > 1

        """
        self.current_total = participant.sum_cards


class ProbabilityTree:
    """
    A probability tree object that stores the current SumNode and
    all its possible sums given the values of a game state's deck.

    Instance Attributes:
    root:
        - The current SumNode object that its subtrees take into account when computing the possible potential sums
          by using its current_total attribute

    ** ONLY RELATED TO THE SUBTREES OF A ROOT **
    ** where the root is the sum that we want to visualize all possible card sums / outcomes **

    remaining:
        - Given the previous ProbabilityTree's root.current_total and the current game state, register the
          total availible cards of a specific card type from the current game state's deck
        - Ex: to obtain a sum of 15, where its previous sum was 14, and a deck has 4 ace cards remaining,
          self.remaining is 4
        - remaining is used for computing the proportion of busting relative to all total cards of a game state's deck
         --> see hit_or_stand_threshold() for official usage of this attribute

    _subtrees:
        - Given a game state (deck) and root's current_sum, _subtrees is the mapping of the possible card_types
          (that can be added to current_sum) to the ProbabilityTree objects that represent the hypothetical
          scenario where that card type was drawn by the player.


    Preconditions:
    -

    Representation Invariants:
    - if the root of the tree represents a game state's current sum, then self.remaining is None (since self.remaining
      only represents the total avalible cards of a given type that produces its subtrees, and for the current sum
      root, remaining doesn't apply)
    - if the root is a hypothetical tree, then self.remianinig is not None and is greater than 0 (since we remove
      all the cards that have no more cards to draw from the deck, and those hypothetical trees were computed by
      'knowing' which card was drawn.)
    - elf._subtrees is empty iff the root.current_total >= target value for cards (ex: if target is 21, no
      subtrees should be computed for roots of a tree that are greater, since the player wouldn't need to hit again
      since a) they got to the target number or b) their current sum is greater and lost to the dealer / busted.)

    """

    root: SumNode
    remaining: Optional[int]
    _subtrees: dict[str, ProbabilityTree]  # match same type as deck implementation

    def __init__(self, value: int) -> None:
        """Intialize a new ProbabilityTree object with respect to all preconditions and representation invariants"""

        self.root = SumNode(value)
        self.remaining = None
        self._subtrees = {}

    def get_subtrees(self) -> dict[str, tuple[ProbabilityTree, int]]:
        """Return the subtrees (avalible card types, object, and remaining cards) of this probability tree.

        The returned mapping is formatted to be accessed by card_type:str, and its value is a tuple which
        returns the object associated to the card_type being added to self.root.current_total and the remaining
        cards of that type that could have been drawn from the deck. """

        return {cardtype: (self._subtrees[cardtype], self._subtrees[cardtype].remaining) for cardtype in self._subtrees}

    def _str_indented(self, indent: int) -> str:
        """ Return a str representation of all roots current_total indented by their subtree locations"""
        str_so_far = '  ' * indent + f'{str(self.root.current_total)}\n'
        for subtree in self._subtrees.values():
            str_so_far += subtree._str_indented(indent + 1)
        return str_so_far

    def __str__(self) -> str:
        """
        Return a string representation of this tree.
        """
        return self._str_indented(0)

    def __len__(self) -> int:
        """Return the number of items (ProbabilityTree objects) in this tree."""

        return 1 + sum(subtree.__len__() for subtree in self._subtrees.values())

    def find_subtree_by_sum(self, target: int) -> dict[str, ProbabilityTree]:
        """ Return dict of subtree(s) corresponding to the given move.
        the mapping is organized by card type for that sum

        Multiple subtrees possible due to jack, 10, king, queen cards since their current_total would be the same

        Return {} if no subtree corresponds to that move."""

        return {cardtype: self._subtrees[cardtype] for cardtype in self._subtrees if
                target == self._subtrees[cardtype].root.current_total}

    def generate_tree(self, decky: bj.Deck, target: int) -> ProbabilityTree:
        """
        Return all possible sums that may be computed given a deck (from a BlackJack game state) and
        the current sum of the player's cards (self.root.current_total)

        target is the target value for the BlackJack game. For the original Black Jack game, the target is 21.
        """

        if self.root.current_total >= target:
            self.root.move = "stand"
            return self

        # recursive step
        else:
            self.root.move = "hit"
            deck_class = decky.deck

            # compute all possible subtrees,
            for card_type in deck_class:

                # each element is a string of the card
                if card_type == 'ace' and self.root.current_total + 11 > target:
                    value_to_add = 1
                elif card_type == 'ace' and self.root.current_total + 11 <= target:
                    value_to_add = 11
                else:
                    value_to_add = deck_class[card_type][0].value

                total_for_subtree_node = value_to_add + self.root.current_total

                self._subtrees[card_type] = ProbabilityTree(total_for_subtree_node)

            for subtree_str in self._subtrees:
                # compute copy of new blackjack assuming this one card was taken out!
                self._subtrees[subtree_str].remaining = len(deck_class[subtree_str])

                deck_copy = decky.copy_deck_and_draw_specific_card(subtree_str)

                # same threshold as before
                self._subtrees[subtree_str].generate_tree(deck_copy, target)

        return self

    def hit_or_stand_threshold(self, threshold: float, curr_deck: bj.Deck, target: int) -> str:
        """
        Given a probability tree, the deck from a game state and the probability threshold that a user is
        OK with busting at, compute whather or not the player should hit or stand.

        If the computed standing_proportion is less than or equal to the provided threshold, then the
        algorithim will suggest the player to hit. Else, method will suggest the player to stand, since
        the computed standing_proportion (chance of them busting) is greater than what they are comfortable with.

        """

        current_value = self.root.current_total
        assert self.root.move == 'hit'

        if current_value >= target:
            # in case recursed to a tree value greater, which it SHOULDN'T
            return 'stand'

        else:

            standing_proportion = 0
            total_cards = curr_deck.__len__()

            for card_type in self._subtrees:
                if self._subtrees[card_type].root.current_total > target:
                    standing_proportion += len(curr_deck.deck[card_type])

            print(standing_proportion)
            print(total_cards)
            stat = standing_proportion / total_cards

            if stat <= threshold:
                return 'hit'
            else:
                return 'stand'

    # def generate_tree(self, decky: bj.Deck) -> ProbabilityTree:
    #     """
    #     return the move the player should do assuming they will win
    #     and with respect to their bust-probability-threshold
    #     Representation Invariants:
    #     - timeout karyna
    #
    #     """
    #
    #     # base case
    #     # okay i guess self.threshold is the proportion of busting and threshold is actually
    #     # the thing we've been comparing since the beginning
    #
    #     if self.root.current_total >= 21:
    #         # example, we chose 50% of busting, we'll stand, and we got a 52% chance of picking a card
    #         # that'll ensure we don't bust, so we WONT stand.
    #         # if we got a 40% chance of picking a card where we wont bust, we WILL stand, cos its lower
    #         # than our desired threshold to bust. ie. we got 60% chance of busting over us only being ok at 50%
    #
    #         # my logic, you can't have a probabilitly sent out, it has to be predetermined
    #         # so even with intializing the probability at 1.0, it works for SumNodes that
    #         # haven't computed their fraction yet.
    #
    #         self.root.move = "stand"
    #         return self
    #
    #     # recursive step
    #     else:
    #         # the move to get here was a hit
    #         self.root.move = "hit"
    #         deck_class = decky.deck
    #
    #         # underneath, calculating probability score
    #         # compute probability to hit or stand and need length to compute probabilities
    #
    #         # compute all possible subtrees,
    #         for card_type in deck_class:
    #
    #             # each element is a string of the card
    #             if card_type == 'ace' and self.root.current_total + 11 > 21:
    #                 value_to_add = 1
    #             elif card_type == 'ace' and self.root.current_total + 11 <= 21:
    #                 value_to_add = 11
    #             else:
    #                 value_to_add = deck_class[card_type][0].value
    #                 # know we can always index 0 since the card is in here
    #
    #             total_for_subtree_node = value_to_add + self.root.current_total
    #
    #             # else:
    #             #     hitting_proportion += len(deck_class[card_type])
    #
    #             # actually adding the values to our probability tree
    #             self._subtrees[card_type] = ProbabilityTree(total_for_subtree_node)
    #
    #         for subtree_str in self._subtrees:
    #             # compute copy of new blackjack assuming this one card was taken out!
    #             self._subtrees[subtree_str].remaining = len(deck_class[subtree_str])
    #
    #             deck_copy = decky.copy_deck_and_draw_specific_card(subtree_str)
    #
    #             # same threshold as before
    #             self._subtrees[subtree_str].generate_tree(deck_copy)
    #
    #     return self
    #
    # def hit_or_stand_threshold(self, threshold: float, curr_deck: bj.Deck) -> str:
    #     """ compute suggested moves based on acceptable loss probability (threshold)
    #
    #     suggested after the first root is random, based on the random card it bases
    #
    #     The threshold is defined as the percentage the player is alright with 'busting'
    #
    #     ex: if the threshold was 0.5, and the computed threshold (which this function will calculate
    #     based on the generated probability tree) is less than or equal to this probability, the
    #     program will suggest it to keep hitting. if the computed threshold is greater than the
    #     percentage the user input, we'll suggest them to stand, which is the last value of the output
    #     list (output_list[-1] )
    #     )
    #
    #     Preconditions:
    #     - tree must be a generated tree
    #     - 0.0 <= threshold <= 1.0
    #     """
    #
    #     current_value = self.root.current_total
    #     #assert self.root.move == 'hit'
    #
    #     if current_value >= 21:
    #         # in case recursed to a tree value greater, which it SHOULDN'T
    #         return 'stand'
    #
    #     else:
    #
    #         standing_proportion = 0
    #         total_cards = curr_deck.__len__()
    #
    #         for card_type in self._subtrees:
    #             if self._subtrees[card_type].root.current_total > 21:
    #                 standing_proportion += len(curr_deck.deck[card_type])
    #
    #         print(standing_proportion)
    #         print(total_cards)
    #         stat = standing_proportion / total_cards
    #
    #         if stat <= threshold:
    #             return 'hit'
    #
    #         else:
    #             return 'stand'


def run_example_tree() -> ProbabilityTree:
    """Return a ProbabilityTree given the methods from
    black_jack_game for intializing cards for the dealer and player"""

    black_jack_intialized = bj.BlackJack()
    black_jack_intialized.dealer.initial_face_up = black_jack_intialized.deck.draw_card(black_jack_intialized.dealer)
    black_jack_intialized.dealer.initial_face_down = black_jack_intialized.deck.draw_card(black_jack_intialized.dealer)
    black_jack_intialized.player.first_card = black_jack_intialized.deck.draw_card(black_jack_intialized.player)
    black_jack_intialized.player.second_card = black_jack_intialized.deck.draw_card(black_jack_intialized.player)
    pt = ProbabilityTree(black_jack_intialized.player.sum_cards)
    return pt.generate_tree(black_jack_intialized.deck, 21)


if __name__ == '__main__':
    ...
    import python_ta

    # python_ta.check_all(config={
    #     'extra-imports': [],  # the names (strs) of imported modules
    #     'allowed-io': [],     # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })
