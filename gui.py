"""CSC111 Group Project: Turning our code into a data set using interactive features so anyone looking at our
data can be a part of the experience and put in their own spins on the work."""

from tkinter import *
import stats


def launch_gui() -> None:
    """Launches the GUI for our analysis
    """
    blackjack = Tk()
    blackjack.title("BlackJack: A Computational Analysis")
    blackjack.geometry("1100x1100")

    # creating the label widget for the game
    black_jack_label = Label(blackjack, text="BlackJack: A Computational Analysis", font='Helvetica 25 bold',
                             justify=CENTER)
    group_names = Message(blackjack, text="Group Members: Alessia Ruberto, Karyna Lim, Rachel Kim, Sasha Chugani.",
                          aspect=800, font="'Helvetica 15 bold", justify=CENTER)
    instructions_label = LabelFrame(blackjack, text="Introduction and Instruction", borderwidth=10, background="silver")
    my_message = Message(instructions_label,
                         text="In BlackJack there are a lot of different influences that come together "
                              "that bring you closer to a win. Let us go see the statistics "
                              "after running various different games and the visualizations"
                              " this data brings!", aspect=800)
    # putting the label onto the screen
    black_jack_label.grid(row=0, column=0, padx=10, ipadx=10)
    group_names.grid(row=1, column=0)
    instructions_label.grid(row=2, column=0)
    my_message.grid(row=2, column=0)

    which_game = Label(blackjack, text="Choose Which Type of Game You Want To Be Played")
    which_game.grid(row=5, column=0)

    which_version_of_tree = StringVar()
    which_version_of_tree.set("")

    drop = OptionMenu(blackjack, which_version_of_tree, "Basic Pie Chart", "Single Strategical Pie Chart",
                      "Dual Comparison Bar Graph", "Large Generated Example Data Original",
                      "Large Generated Example Data Experimental", "Line Plot Threshold", "Line Plot Target")
    drop.grid(row=5, column=1)

    def basic_pie() -> None:
        """Graph the basic pie chart based on the inputed values"""

        def basic_pie_chart() -> None:
            """Graph the Basic Pie Chart"""
            stats.gen_and_graph_basic_pie(int(target.get()), int(number_of_games.get()))

        num_game = Label(blackjack, text="Enter the Number of Games You Want to See as and Integer"
                                         " Greater Than 0")
        num_game.grid(row=7, column=0)

        number_of_games = Entry(blackjack, width=10)
        number_of_games.grid(row=7, column=1)

        num_target = Label(blackjack, text="Enter the Target Number You Want the Game to Reach That's Close to 21. "
                                           "Preferably between 19-23")
        num_target.grid(row=10, column=0)

        target = Entry(blackjack, width=10)
        target.grid(row=10, column=1)

        please = Label(blackjack, text="Please Fill in the Following Values! Hit Get Graphs To Move On.",
                       font="Helvetica 15 bold")
        please.grid(row=6)

        ready_to_play = Button(blackjack, text="Get Graphs", command=basic_pie_chart)
        ready_to_play.grid(row=17, column=0)

    def singl_strat() -> None:
        """Graph the single strategical pie chart based on the inputed values"""

        def single_strat() -> None:
            """Graph the Single Strategical Pie Chart"""
            stats.gen_and_graph_strategical_pie(int(target.get()), int(number_of_games.get()), float(threshold.get()))

        num_game = Label(blackjack, text="Enter the Number of Games You Want to See as and Integer"
                                         " Greater Than 0")
        num_game.grid(row=7, column=0)

        number_of_games = Entry(blackjack, width=10)
        number_of_games.grid(row=7, column=1)

        num_target = Label(blackjack, text="Enter the Target Number You Want the Game to Reach That's Close to 21. "
                                           "Preferably between 19-23")
        num_target.grid(row=10, column=0)

        target = Entry(blackjack, width=10)
        target.grid(row=10, column=1)

        num_threshold = Label(blackjack, text="Enter The Percentage You Want to See to Stop Hitting Between 0.0 to 1.0")
        num_threshold.grid(row=12, column=0)

        threshold = Entry(blackjack, width=10)
        threshold.grid(row=12, column=1)

        ready_to_play = Button(blackjack, text="Get Graphs", command=single_strat)
        ready_to_play.grid(row=17, column=0)

        please = Label(blackjack, text="Please Fill in the Following Values! Hit Get Graphs to Move On.",
                       font="Helvetica 15 bold")
        please.grid(row=6)

    def dual_one() -> None:
        """Graph the dual comparison bar graph using the inputed values"""

        def dual_bar() -> None:
            """Graph the Dual Comparison Bar Graph"""
            stats.gen_and_graph_dual_bar(int(target.get()), int(number_of_games.get()), float(threshold.get()))

        num_game = Label(blackjack, text="Enter the Number of Games You Want to See as and Integer"
                                         " Greater Than 0")
        num_game.grid(row=7, column=0)

        number_of_games = Entry(blackjack, width=10)
        number_of_games.grid(row=7, column=1)

        num_target = Label(blackjack, text="Enter the Target Number You Want the Game to Reach")
        num_target.grid(row=10, column=0)

        target = Entry(blackjack, width=10)
        target.grid(row=10, column=1)

        num_threshold = Label(blackjack, text="Enter The Percentage You Want to See to Stop Hitting Between 0.0 to 1.0")
        num_threshold.grid(row=12, column=0)

        threshold = Entry(blackjack, width=10)
        threshold.grid(row=12, column=1)

        ready_to_play = Button(blackjack, text="Get Graphs", command=dual_bar)
        ready_to_play.grid(row=17, column=0)

        please = Label(blackjack, text="Please Fill in the Following Values! Hit Get Graphs To Move On.",
                       font="Helvetica 15 bold")
        please.grid(row=6)

    def something_to_cover() -> None:
        """Function to cover the inputs that aren't needed for a specific function"""
        something_to_cover1 = Label(blackjack,
                                    text="                                                                   "
                                         "                                                                 "
                                         "                                                                 ")
        something_to_cover1.grid(row=12, column=0)
        something_to_cover2 = Label(blackjack, text="                               ")
        something_to_cover2.grid(row=12, column=1)

        something_to_cover3 = Label(blackjack,
                                    text="                                                                   "
                                         "                                                                  "
                                         "                                              ")
        something_to_cover3.grid(row=7, column=0)
        something_to_cover4 = Label(blackjack, text="                               ")
        something_to_cover4.grid(row=7, column=1)

        something_to_cover5 = Label(blackjack,
                                    text="                                                                   "
                                         "                                                       "
                                         "                                               ")
        something_to_cover5.grid(row=10, column=0)
        something_to_cover6 = Label(blackjack, text="                               ")
        something_to_cover6.grid(row=10, column=1)

    def get_necessary_inputs() -> None:
        """Depending on the type of tree the person using the function choose return entries that they have to add
        in.
        """
        if which_version_of_tree.get() == "Basic Pie Chart":
            something_to_cover_basic = Label(blackjack, text="                                                     "
                                                             "                                                         "
                                                             "                               ")
            something_to_cover_basic.grid(row=12, column=0)
            something_to_cover1 = Label(blackjack, text="                               ")
            something_to_cover1.grid(row=12, column=1)
            basic_pie()
        elif which_version_of_tree.get() == "Large Generated Example Data Original":
            something_to_cover()

            def large_generated() -> None:
                """Graph the large generated example data"""
                stats.graph_large_dataframe_original()

            ready_to_play = Button(blackjack, text="Get Graph", command=large_generated)
            ready_to_play.grid(row=17, column=0)
        elif which_version_of_tree.get() == "Large Generated Example Data Experimental":
            something_to_cover()

            def large_generated_experimental() -> None:
                """Graph the large generated experimental example data"""
                stats.graph_large_dataframe_exper()

            ready_to_play = Button(blackjack, text="Get Graphs", command=large_generated_experimental)
            ready_to_play.grid(row=17, column=0)
        elif which_version_of_tree.get() == "Line Plot Threshold":
            something_to_cover()

            def plot_threshold() -> None:
                """Graph a line plot comparing player wins and the threshold value."""
                stats.graph_line_plot_threshold()

            ready_to_play = Button(blackjack, text="Get Graphs", command=plot_threshold)
            ready_to_play.grid(row=17, column=0)
        elif which_version_of_tree.get() == "Line Plot Target":
            something_to_cover()

            def line_plot_target() -> None:
                """Graph the large generated example data"""
                stats.graph_line_plot_target()

            ready_to_play = Button(blackjack, text="Get Graphs", command=line_plot_target)
            ready_to_play.grid(row=17, column=0)
        elif which_version_of_tree.get() == "Single Strategical Pie Chart":
            singl_strat()
        elif which_version_of_tree.get() == "Dual Comparison Bar Graph":
            dual_one()

    get_stats = Button(blackjack, text="Enter", command=get_necessary_inputs)
    get_stats.grid(row=5, column=2)

    button_quit = Button(blackjack, text="Exit Program", command=blackjack.quit)
    button_quit.grid(row=20, column=0)

    blackjack.mainloop()


if __name__ == '__main__':
    import python_ta

    # The following we're necessary to disable
    python_ta.check_all(config={
        'extra-imports': ['stats', 'tkinter'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'disable': ['too-many-statements', 'wildcard-import'],
        'max-line-length': 120
    })
