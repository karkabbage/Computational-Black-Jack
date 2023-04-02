"""CSC111 Winter 2023 Project Phase 2: Black Jack Algorithim Module Description =============================== This
file contains functions for the statisics and graphing portion of our assignment. It also contains many of the
functions that are directly called in our GUI.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the
CSC111 instructional team at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this material,
please consult the Canadian Copyright Act.
This file is Copyright (c) 2023 Alessia Ruberto, Karyna Lim, Rachel Kim, Sasha Chugani.
"""
from typing import Optional
import plotly.express as px
import plotly.io as pio
import pandas as pd
import black_jack_game as bj


pio.renderers.default = "browser"


# ====================================================================================================================
# Back-end GUI Functions
# ====================================================================================================================
def gen_and_graph_basic_pie(target: int, num_games: int) -> None:
    """Create a pie chart with results for the specified number of games played using the basic strategy.

    IMPORTANT: the basic strategy runs very fast, around 10,000 games works well.

    Preconditions:
        - 0.0 <= threshold <= 1.0
        - target >= 4
        - num_games > 0
    """
    df = create_dataframe_basic(target, num_games)
    graph_pie_chart(df, title=str(num_games) + ' Black Jack Basic Strategy Games with Target=' + str(target))


def gen_and_graph_strategical_pie(target: int, num_games: int, threshold: float) -> None:
    """Create a pie chart with results for the specified number of games played using the probability tree strategy.

    IMPORTANT: this strategy runs a lot slower due to the tree, more than 50 games becomes take 1 min +

    Preconditions:
        - 0.0 <= threshold <= 1.0
        - target >= 4
        - num_games > 0
    """
    df = create_dataframe_strategic(target, threshold, num_games)
    graph_pie_chart(df, title=str(num_games) + ' Black Jack Tree Strategy Games with Target=' + str(target)
                    + ' and Threshold=' + str(threshold))


def gen_and_graph_dual_bar(target: int, num_games: int, threshold: float) -> None:
    """Create a grouped bar graph with results for the specified number of games played using both the basic and
    probability tree strategy with the same overlap settings.

    IMPORTANT: this strategy runs a lot slower due to the tree, more than 50 games becomes take 1 min +

    Preconditions:
        - 0.0 <= threshold <= 1.0
        - target >= 4
        - num_games > 0
    """
    df = create_dataframe_compare_two(target, threshold, num_games)
    graph_grouped_bar(df, title=str(num_games) + ' Black Jack Games with Target=' + str(target)
                      + ' and Threshold=' + str(threshold))


def graph_large_dataframe_original() -> None:
    """Loads the large datafrae with 1000 original (target=21) Black Jack games with various configurations and
    graphs it using a grouped bar plot.
    """
    df = load_csv('data/large_dataframe_original_1000_games.csv')
    graph_grouped_bar(df, title='1000 Original (Target=21) Black Jack Games with Various Configurations')


def graph_line_plot_threshold() -> None:
    """Graph a line plot comparing player wins and the threshold value.
    """
    df = load_csv('data/large_dataframe_original_1000_games.csv')
    df.drop(0)  # Remove Basic game from this data, which does not have a threshold value
    fig = px.line(df, x='Threshold', y='Player Wins', title='Correlation Between Threshold and Number of Player Wins')
    fig.show()


# TODO generate and make for varied.
# ====================================================================================================================
# Generating, Loading, and Exporting CSV data
# ====================================================================================================================
def gen_large_dataframe_original(num_games: int) -> None:
    """This function generates and saves a large dataset csv to this file's location. We decided on a few different
    game configurations to get a large scope of data to ultimately find the best performing strategy. This function
    only follows the ORIGINAL RULES (i.e. having the target set to 21) to reflect the actual rules of the game.

    Preconditions:
        - num_games > 0
    """
    # Basic game strategy data
    df_basic = create_dataframe_basic(21, num_games, True)

    # Probability tree game strategy using different threshold values
    df_stategic_0_0 = create_dataframe_strategic(21, 0.0, num_games, True)
    df_stategic_0_2 = create_dataframe_strategic(21, 0.2, num_games, True)
    df_stategic_0_5 = create_dataframe_strategic(21, 0.5, num_games, True)
    df_stategic_0_7 = create_dataframe_strategic(21, 0.7, num_games, True)
    df_stategic_1_0 = create_dataframe_strategic(21, 1.0, num_games, True)

    df_all = pd.concat([df_basic, df_stategic_0_0, df_stategic_0_2, df_stategic_0_5, df_stategic_0_7,
                        df_stategic_1_0], axis=0)

    df_all.to_csv('large_dataframe_original_' + str(num_games) + '_games.csv', index=False)


def gen_large_dataframe_varied(num_games: int) -> None:
    """This function generates and saves a large dataset csv to this file's location. We decided on a few different
    game configurations to get a large scope of data to ultimately find the best performing strategy. This function
    only tests MANY TARGETS to see the full range of possibilities and outcomes of different Black Jack rules.

    Preconditions:
        - num_games > 0
    """
    # Basic game strategy data at different targets
    # df_basic_19 = create_dataframe_basic(19, num_games, True) #TODO remove??
    df_basic_21 = create_dataframe_basic(21, num_games, True)
    df_basic_23 = create_dataframe_basic(23, num_games, True)

    # Probability tree game strategy using different threshold and target values # TODO remove??
    # df_stategic_19_0_0 = create_dataframe_strategic(19, 0.0, num_games, True)
    # df_stategic_19_0_5 = create_dataframe_strategic(19, 0.5, num_games, True)
    # df_stategic_19_0_7 = create_dataframe_strategic(19, 0.7, num_games, True)

    df_stategic_21_0_0 = create_dataframe_strategic(21, 0.0, num_games, True)
    df_stategic_21_0_5 = create_dataframe_strategic(21, 0.5, num_games, True)
    df_stategic_21_0_7 = create_dataframe_strategic(21, 0.7, num_games, True)

    df_stategic_23_0_0 = create_dataframe_strategic(23, 0.0, num_games, True)
    df_stategic_23_0_5 = create_dataframe_strategic(23, 0.5, num_games, True)
    df_stategic_23_0_7 = create_dataframe_strategic(23, 0.7, num_games, True)

    df_all = pd.concat([df_basic_21, df_basic_23, df_stategic_21_0_0, df_stategic_21_0_5, df_stategic_21_0_7,
                        df_stategic_23_0_0, df_stategic_23_0_5, df_stategic_23_0_7], axis=0)

    df_all.to_csv('large_dataframe_experimental_' + str(num_games) + '_games.csv', index=False)


def load_csv(file_name: str) -> pd.DataFrame:
    """Loads a csv with the file format used throughout this file.
    """
    return pd.read_csv(file_name)


# ====================================================================================================================
# Data Frame Generation Functions
# ====================================================================================================================
def create_dataframe_basic(target: int, num_games: int, specify_type: Optional[bool] = False) -> pd.DataFrame:
    """Creates a dataframe of win/loss data using the possibility tree game runner and the parameters listed. Returns a
    DataFrame

    Implementation note:
        - When specify_type == True, it adds a new collumn specifying the game mode.

    Preconditions:
        - target >= 4
        - num_games > 0
    """

    if specify_type:
        results = {'Game Mode': ['Basic (tar=' + str(target) + ')'], 'Player Wins': [0], 'Dealer Wins': [0],
                   'Push (Tie)': [0], 'Target': [target]}
    else:
        results = {'Player Wins': [0], 'Dealer Wins': [0], 'Push (Tie)': [0]}

    for _ in range(0, num_games):
        black_jack = bj.BlackJack()
        result = black_jack.run_game(target)
        results[result][0] += 1

    return pd.DataFrame(results)


def create_dataframe_strategic(target: int, threshold: float, num_games: int,
                               specify_type: Optional[bool] = False) -> pd.DataFrame:
    """Creates a dataframe of win/loss data using the possibility tree game runner and the parameters listed. Returns a
    DataFrame

    Implementation note:
    - When specify_type == True, it adds a new collumn specifying the game mode.

    Preconditions:
        - 0.0 <= threshold <= 1.0
        - target >= 4
        - num_games > 0
    """

    if specify_type:
        results = {'Game Mode': ['Strategical (tar=' + str(target) + ', thr=' + str(threshold) + ')'],
                   'Player Wins': [0], 'Dealer Wins': [0],
                   'Push (Tie)': [0], 'Target': [target], 'Threshold': [threshold]}
    else:
        results = {'Player Wins': [0], 'Dealer Wins': [0], 'Push (Tie)': [0]}

    for _ in range(0, num_games):
        black_jack = bj.BlackJack()
        result = black_jack.run_probability_game(threshold, target)
        results[result][0] += 1

    return pd.DataFrame(results)


def create_dataframe_compare_two(target: int, threshold: float, num_games: int) -> pd.DataFrame:
    """ This function compares creates a dataset comparing the basic game strategy vs. the possibility tree game
    strategy under the conditions listed as import vairables (target, threshold and number of games). Returns a
    DataFrame.

    Preconditions:
        - 0.0 <= threshold <= 1.0
        - target >= 4
        - num_games > 0
    """
    df_basic = create_dataframe_basic(target, num_games, True)
    df_strategic = create_dataframe_strategic(target, threshold, num_games, True)

    return pd.concat([df_strategic, df_basic], axis=0)


# ====================================================================================================================
# Graphing Functions
# ====================================================================================================================
def graph_pie_chart(df: pd.DataFrame, title: Optional[str] = None) -> None:
    """Creates and displays a pie chart comparing the number of occurences for player/dealer wins and ties.

    Preconditions
        - title must be a string
    """
    val = [df['Player Wins'][0], df['Dealer Wins'][0], df['Push (Tie)'][0]]
    fig = px.pie(df, names=['Player Wins', 'Dealer Wins', 'Push (Tie)'], values=val, title=title)
    fig.show()


def graph_grouped_bar(df: pd.DataFrame, title: Optional[str] = None) -> None:
    """Creates and displays a grouped comparing the game mode with the number of occurences for player/dealer wins
    and ties.

    Preconditions
        - title must be a string
    """
    fig = px.bar(
        data_frame=df,
        x='Game Mode',
        y=['Player Wins', 'Dealer Wins', 'Push (Tie)'],
        barmode='group',
        title=title
    )

    fig.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['plotly.express', 'pandas', 'black_jack_game', 'plotly.io', 'Optional'],
        'disable': [],
        'allowed-io': []
    })
