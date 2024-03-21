# Conq

A custom Risk game project in Python.

## Using the Code

* The adminGUI is built with custom tkinter while the clientPyGame is written on PyGame (both MVP)
* To run the game, first start the Server using "python adminGUI" which will then begin to listen for player connections
* Then from additional terminals, run one or more instances of clientPyGame which is the GUI version of the Client app
* When ending the components use care that the Python processes are all stopped to assure they release network resources.

## Potential Epics and Features

* Foundational play - Server, Board, Players, Combat, and Turns
* Gameplay metrics
* Automated turn execution
* Probabilities and AI driven execution
