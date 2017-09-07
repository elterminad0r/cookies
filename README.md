# cookies
Some projects on "the cookie game" in Python. Includes an automatic opponent and some testing scripts on higher dimensions of the game. Here is a sample of `opponent.py` dealing out a thrashing (featuring a little more description of what the game is):

`$ python opponent.py -j 4 8`

    Automatically play the cookie game (in 2 dimensions, for now). Prepare not to
    win. The game works like so: There are two jars. Each has some cookies. You win
    if you take the last cookie. You can take some n cookies from any combination
    of jars - but n for each jar. (ie for the two-jar case, you must take either
    the same from both or any number you like from one.

    jars given: (4, 8)
    computer starts
    computer takes 1 cookie from jar { 8 }
    Jars are: 
    Jar 0: 4
    Jar 1: 7
    Enter two jar numbers> 0 1
    Jars are: 
    Jar 0: 4
    Jar 1: 6
    computer takes 1 cookies from both jars
    Jars are: 
    Jar 0: 3
    Jar 1: 5
    Enter two jar numbers> 2 2
    Jars are: 
    Jar 0: 1
    Jar 1: 3
    computer takes 1 cookie from jar { 3 }
    Jars are: 
    Jar 0: 1
    Jar 1: 2
    Enter two jar numbers> 1 0
    Jars are: 
    Jar 0: 0
    Jar 1: 2
    computer takes 2 cookies from jar { 2 }
    computer wins

Also features a miscellaneous utility function that greps for lines containing the letters of a word, in order.
