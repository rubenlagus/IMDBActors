# -*- coding: utf-8 -*-
'''
Copyright 2014 Ruben Bermudez Lopez

coprotagositas is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

coprotagositas is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with coprotagositas.  If not, see <http://www.gnu.org/licenses/>.
'''

from fileHandler import FileHandler
from writer import Writer

if __name__ == "__main__":
    ''' This script recieve 2 actors or actresses and print the films where they are coprotagonist '''
    option = ""
    while(option != "0"):
        print(("Please write the name of two actors/actresses to find the films they made together "
            + "(Only full names supported)"
            + " , write 0 to exit:"))
        option1 = str(input('Enter the actor/actress name: '))    
        if option1 != "" and option1 != "0":
            option2 = str(input('Enter the actor/actress name: '))    
            if option2 != "" and option2 != "0":
                db = FileHandler()
                writer = Writer()
                db.openActDB()
                resultsdata = db.searchFilms2actors(option1, option2)
                writer.printFilms2Actors(option1, option2, resultsdata)
                db.closeActDB()
            else:
                print("Exiting")
        else:
            print("Exiting")
                