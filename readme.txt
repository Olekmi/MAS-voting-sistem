Python 3 and numpy was used to develop this script.

Instructions to run the program:
 
In a terminal that points to the the project folder, run the following command: python mas_assignment_1.py 
The script can take the following arguments: 

-h/--help: 		To show the options

-s/--scheme SCHEME: 	To select the voting scheme(plurality, vote2, anti_plurality, borda)

-p/--pref PATH:		The input file name of the preference matrix tobe used. Can be numerical or alphabetical. 
			Various preferencematrix examples are included in the project folder.
			If the preference matrix argument is not used, a random generated matrix will be used.

-v/--voter NUM: 	To select the index of the voter, that strategic voting will be calculated for. 
			If no selection was placed, the first one will be chosen.

-b/--behavior B: 	If the voter is not selected, one can choose a behavior(selfish, altruistic). 
			The voter with the most fitting result for this behavior will be selected.

The script will output the original outcome of the votes, the original overall happiness of the voters, 
the risk of the selected voter, and a list of the strategic options that the selected voter has.
 Each option contains the voter's  altered preference, the outcome by using this preference, 
the total happiness after applying it, and a reason why this option is preferred. 