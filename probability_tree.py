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

    Representation Invariants:
    - if the root of the tree represents a game state's current sum, then self.remaining is None (since self.remaining
      only represents the total avalible cards of a given type that produces its subtrees, and for the current sum
      root, remaining doesn't apply)
    - if the root is a hypothetical tree, then self.remaining is not None and is greater than 0 (since we remove
      all the cards that have no more cards to draw from the deck, and those hypothetical trees were computed by
      'knowing' which card was drawn.)
    - elf._subtrees is empty iff the root.current_total >= target value for cards (ex: if target is 21, no
      subtrees should be computed for roots of a tree that are greater, since the player wouldn't need to hit again
      since a) they got to the target number or b) their current sum is greater and lost to the dealer / busted.)
    - self.root.current_total is a valid number viable in the range of possible sums, depending on the target number.

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

    def just_objects(self) -> list[ProbabilityTree]:
        return [self._subtrees[cardtype] for cardtype in self._subtrees]

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
            self.root.move = "Stand"
            return self

        # recursive step
        else:
            self.root.move = "Hit"
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
                # how many of this card type was there for self.root to choose from?
                self._subtrees[subtree_str].remaining = len(deck_class[subtree_str])

                deck_copy = decky.copy_deck_and_draw_specific_card(subtree_str)

                # same threshold as before
                # compute copy of new blackjack assuming this one card was taken out!
                # hence why a hypothetical deck copy was computed
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
        # assert self.root.move == 'hit'

        if current_value >= target:
            # in case recursed to a tree value greater than the target, which it SHOULDN'T
            return 'Stand'

        else:

            standing_proportion = 0
            total_cards = curr_deck.__len__()

            for card_type in self._subtrees:
                if self._subtrees[card_type].root.current_total > target:
                    standing_proportion += len(curr_deck.deck[card_type])

            stat = standing_proportion / total_cards
            print(stat)

            if stat <= threshold:
                return "Hit"
            else:
                return "Stand"

    # def tree_to_graph(self, graph: nx.Graph, d: int) -> None:
    #     """nrjknf
    #     """
    #     if not self._subtrees:
    #         pass
    #
    #     else:
    #         # add node version - FAIL --> values kept in this weird thing
    #         '''sub_graph = nx.Graph()
    #         temp = []
    #         sub_graph.add_node(count, value=(self.root.current_total, d))
    #         for subtree in self._subtrees:
    #             count += 1
    #             sub_graph.add_node(count, value=(self._subtrees[subtree].root.current_total, d + 1))
    #             temp.append((0, count))
    #         sub_graph.add_edges_from(temp)
    #         graph.add_edges_from(sub_graph.edges)
    # x
    #         for subtree in self._subtrees:
    #             self._subtrees[subtree].tree_to_graph(graph, d + 1, count + 1)'''
    #
    #         # labels version - FAIL --> the enumerate labels thing resets to 0 for the subtrees b/c recursion
    #         '''temp = []
    #         for subtree in self._subtrees:
    #             tpl = (self._subtrees[subtree].root.current_total, d + 1)
    #             temp.append(tpl)
    #         labels = {i: l for i, l in enumerate(temp)}
    #         nodes = labels.keys()
    #         sub_graph = nx.Graph()
    #         sub_graph.add_nodes_from(nodes)
    #         graph.add_edges_from(sub_graph.edges)
    #         for subtree in self._subtrees:
    #             self._subtrees[subtree].tree_to_graph(graph, d + 1)'''
    #
    #         # ORIGINAL VERSION(adj_dict version) - FAIL --> later connects to existing nodes instead of making new ones
    #         # --> BUT also most reliable of these attempts for stealing code
    #         """adjacency_dict = {}
    #         temp = []
    #         for subtree in self._subtrees:
    #             tpl = (self._subtrees[subtree].root.current_total, d + 1)
    #             temp.append(tpl)
    #         adjacency_dict[(self.root.current_total, d)] = tuple(temp)
    #         sub_graph = nx.Graph(adjacency_dict)
    #         graph.add_edges_from(sub_graph.edges)
    #         for subtree in self._subtrees:
    #             self._subtrees[subtree].tree_to_graph(graph, d + 1)"""
    #
    #
    # def draw_graph(graph: nx.Graph) -> None:
    #     """slnkfjsnf
    #     """
    #     pos = {}
    #
    #     for node in graph.nodes:
    #         x = list(node)[0]
    #         y = 0 - list(node)[1]
    #         pos[node] = (x, y)
    #
    #     options = {
    #         "font_size": 10,
    #         "node_size": 2000,
    #         "node_color": "white",
    #         "edgecolors": "black",
    #         "linewidths": 5,
    #         "width": 5,
    #     }
    #
    #     nx.draw_networkx(graph, pos, **options)
    #
    #     ax = plt.gca()
    #     ax.margins(0.001)
    #     plt.axis("off")
    #     plt.show()


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
