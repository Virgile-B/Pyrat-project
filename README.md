# About

This is the software of the course [PyRat](https://formations.imt-atlantique.fr/pyrat).

Code by Vincent Gripon.

Fork revised and maintained by Bastien Pasdeloup.

Illustrations by [Lauren Lefumeur-Pasdeloup](http://neruall.deviantart.com/) and [Christina Roberts](http://neyjour.deviantart.com/).

See full credits [here](https://formations.imt-atlantique.fr/pyrat/).

# Usage

1. Open a terminal and navigate to the directory containing pyrat.py

2. Run 'python pyrat.py --help' for a complete list of options. A good start is 'python pyrat.py --rat AIs/random.py'.

You may have to use command 'python3' instead of 'python' above if Python 3 is not your default version.

You can play with the keyboard (tested on Linux and Windows) with 'python pyrat.py --rat human --python human'. The rat is controlled with arrows and the python with keypad.

3. For instance, to compare the final algorithm of Virgile with a greedy algorithm, write in a terminal: 
python pyrat.py --rat AIs/slightly_better_than_greedy.py --python AIs/greedy.py
//
or
//
python pyrat.py --rat AIs/beat_greedy.py --python AIs/greedy.py

# Install

To be able to run, one should only need Python 3 and pygame for Python 3.

Installation details on Linux, MacOS and Windows are provided [here](https://formations.imt-atlantique.fr/pyrat/installing-the-pyrat-software/).
