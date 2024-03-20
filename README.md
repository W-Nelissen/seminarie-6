# hector
Codebase voor het seminarie "Programmeren in Python" van de zesdejaars van het Sint-Pieterscollege in Jette 
Project: schaakbot.

## Progress:
* 12 Maart: Tekenen van chessboard+pieces
* 12 Maart: Basisklassen voor klok (chess_clock.py)
* 12 Maart: Basismechanisme voor moves (chess_board.py)
* 14 Maart: Implementatie van classes voor sound en video (handle_sound.py; handle_video.py)
* 15 Maart: Implementatie van move + slaan, pion kan 2 vakjes bij start
* 16 Maart: Pion move + slaan. (nog niet en passant)
* 17 Maart: Na move switchen we van speler. (enkel speler aan zet kan stukken verzetten)
* 20 Maart: Bijhouden en tonen van historiek van zetten
* 20 Maart: Kleurenschema verbeterd
* 20 Maart: Optie om steeds wit onderaan te hebben of steeds te flippen bij zet
## TODO: (in willekeurige volgorde)
* Alle mogelijke moves implementeren (rokade, pion aan eind)(lastmoved,lastmove bijhouden)
* Slaan voor Pionnen (en passant)
* Detectie van schaak en stalemate
* Rokade: Toren mee verzetten
* Console implementeren (messages en later commands)
* klok laten switchen bij zet
* History van zetten bijhouden
* Eigen file formaat (als tussenstap)
* History area: Weergeven van historiek (chess_area_history.py)
    +bord terugzetten naar vorige toestand (multiple undo)
* Uittesten background routines
* Uittesten dialog boxes
* Evaluatie: class voor stukken + class voor positie (modifier)
* Alpha-Beta pruning routine
* PC laten spelen tegen speler
