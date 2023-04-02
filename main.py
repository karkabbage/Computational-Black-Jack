"""CSC111 Winter 2023 Project Phase 2: Blackjack - A Computational Analysis
Module Description
===============================
This Python module contains the main file for our project. It launches our interactive GUI!

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the
CSC111 instructional team at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this material,
please consult the Canadian Copyright Act.
This file is Copyright (c) 2023 Alessia Ruberto, Karyna Lim, Rachel Kim, Sasha Chugani.
"""
import gui

# Instructions: Simply run this file and select from the dropdown menu what game statistics you'd like to see!
#               some graphs are made from pre-generated data, while others will generate data live based on your input.

if __name__ == '__main__':
    gui.launch_gui()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['gui'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
