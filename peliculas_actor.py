# -*- coding: utf-8 -*-
'''
Copyright 2014 Ruben Bermudez Lopez

peliculas_actor is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

peliculas_actor is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with peliculas_actor.  If not, see <http://www.gnu.org/licenses/>.
'''

from fileHandler import FileHandler
from writer import Writer

if __name__ == "__main__":
    '''
    This script receive a name of an actor or actress and print the information of all the films where
    he/she has appear.
    Only full names are supported as they appear in the IMDB database, but if the name is not found, a 
    broad spectrum search is performed. In this search, the name is splitted in all the parts it have 
    and print the info of all the actors that fit to any of those partial names.
    '''
    option = ""
    while(option != "0"):
        print(("Please write the name of an actor or actress to know all the films where he/she appear "
            + "(Only full names supported)"
            + " , write 0 to exit:"))

        option = str(input('Enter the actor name option: '))
        db = FileHandler()
        writer = Writer()
        db.openActDB()
        if option != "0" and option != "":
            films = db.searchActor(option)
            if len(films) > 0:
                writer.printFilmsDataFromActor(option, films)
            else:
                print(("%s not found") % (option))
                print(("A broad spectrum search will take place, wait a moment"))
                
                result = db.broadSpectrumSearchActor(option)
                print(("All the actors whose name contains any of the words provided will be listed now"))
                for key in result.keys():
                    writer.printFilmsDataFromActor(key, result[key])
            
        else:
            print("Exiting")
            db.closeActDB()
