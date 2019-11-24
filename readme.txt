

Instructions to run the program:

To execute the script.
In a terminal that points to the the project folder, run the following command: python mas_assignment_1.py 
The script can take the following arguments: 
-h: to show the options

-s/--scheme SCHEME: To select the voting scheme(plurality,vote2, anti_plurality, borda)

-p/--pref: The input file name of the preference matrix tobe used. Can be numerical or alphabetical. Various preferencematrix examples are included in the project folder. If thepreference matrix argument is not used, a random generatedmatrix will be used.

-v/--voter: To select the index of the voter, that strategicvoting will be calculated for. If no selection was placed, thefirst one will be chosen.

-b/--behavior: If the voter is not selected, one can choosea behavior(selfish, altruistic). The voter with the most fittingresult for this behavior will be selected.

The script outputs the original outcome, the original overall happiness, the risk of the selected voter, and a list of the strategic options that the selected voter can take. Each option contains his altered preference, the outcome by using this preference, the total happiness after applying it, and a reason why this option is preferred.