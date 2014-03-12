# -*- coding: utf-8 -*-
'''
Copyright 2014 Ruben Bermudez Lopez

grados_separacion is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

grados_separacion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with grados_separacion.  If not, see <http://www.gnu.org/licenses/>.
'''
from fileHandler import FileHandler
from shortestPath import ShortestPath, Node
from writer import Writer

if __name__ == "__main__":
    ''' 
    This script receive 2 actors o actresses names and the maximum distance between them and 
    return the minimum number of relation (tipe "work with") between them.
    Remember that the higher distance, the longer the algorithm will last (default value is 11 
    and the minimum is 3).
    '''
    option = ""
    while(option != "0"):
        print(("Please write the name of two actors/actresses (Only full names supported)"
            + " to see if they are related , write 0 to exit:"))
        option = str(input('Enter the actor/actress name: '))    
        if option != "" or option != "0":
            option2 = str(input('Enter the actor/actress name: '))    
            if option2 != "" or option2 != "0":
                db = FileHandler()
                db.openActDB()
                db.openFilmsDB()
                try:
                    option3 = int(input('Enter maximum length of path to follow, the higher number, the longer it takes (minimum 3, default 11):'))
                except:
                    option3 = 11
                if option3 < 3:
                    option3 = 3
                shortestPath  = ShortestPath(db, limit=option3)
                result = shortestPath.findPath(origin=option, destiny=option2)
                if result is None:
                    print("One of the actor/actress names doesn't exists.")
                elif type(result) is int and result == -1:
                    print("No relation found within " + option3 + " steps")
                elif type(result) is Node:
                    writer = Writer()
                    writer.printRelation(actor1=option, actor2=option2, relation=result)
                db.closeActDB()
                db.closeFilmsDB()
            else:
                print("Exiting")
        else:
            print("Exiting")
                