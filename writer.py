# -*- coding: utf-8 -*-
'''
Copyright 2014 Ruben Bermudez Lopez

Writer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

utilidades is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with utilidades.  If not, see <http://www.gnu.org/licenses/>.
'''

class Writer():
    ''' Provide methods to print information in a readable way '''
    
    def printFilmData(self, film, actor1 = "", actor2 = "", role2 = ""):
        '''
        Print information of a film associated to one or two actors/actresses
        
        params:
         * film: Films information
         * actor1: Name of first actor/actress 
         * actor2: Name of second actor/actress
         * role2: Role of actor2
         
        note:
         Role of actor1 is extracted from film info
        '''
        if film['type'] == "TVSerie": # If we are printing a TVserie
            if 'title' in film: # If there is title, print it
                print(("%s Title: %s") % (" |--", film['title']))
            if 'role' in film:
                if actor1 != "": # If there is role for actor1 and it is not empty, print its name and role
                    print(("%s%s %s as: %s") % (" ", " |--", actor1, film['role']))
                    if actor2 != "": # If second actor,print also its role
                        print(("%s%s %s as: %s") % (" ", " |--", actor2, role2))
                else: # If not actor1 name provided, print just role
                    print(("%s%s Role: %s") % (" "," |--", film['role']))
            if 'year' in film: # If there is year, print it
                print(("%s%s Year: %s") % (" "," |--", film['year']))
            if 'chapter' in film: # If there is chapter name, print it
                print(("%s%s Chapter title: %s") % (" "," |--", film['chapter']))
            if 'chapterno' in film: # If there is chapter number, print it
                print(("%s%s Chapter Number: %s") % (" "," |--", film['chapterno']))
        elif film['type'] == "Film": # If we are printing a film
            if 'title' in film: # If there is title, print it
                print(("%s Title: %s") % (" |--", film['title']))
            if 'role' in film:
                if actor1 != "": # If there is role for actor1 and it is not empty, print its name and role
                    print(("%s%s %s as: %s") % (" ", " |--", actor1, film['role']))
                    if actor2 != "": # If second actor,print also its role
                        print(("%s%s %s as: %s") % (" ", " |--", actor2, role2))
                else:
                    print(("%s%s Role: %s") % (" "," |--", film['role']))
            if 'year' in film: # If there is year, print it
                print(("%s%s Year: %s") % (" ", " |--", film['year']))
        else: # If type of film is not TVSerie or Film, raise an exception
            raise Exception("Unknown error when printing.")
            
    def printFilmsDataFromActor(self, actor, films):
        ''' 
        Print the info of all the films where an actor/actress appears
        
        params:
         * actor: Actor/actress name
         * films: Films information
        '''
        print(("Films where %s appear:") % (actor))
        for film in films:
            self.printFilmData(film)
    
    def printFilms2Actors(self, actor1, actor2, films):
        ''' 
        Print the info of all the films where two actors/actresses appear together
        
        params:
         * actor1: First Actor/actress name
         * actor2: Second Actor/actress name
         * films: Films information
        '''
        print(("Films where %s and %s are coprotagonist:") % (actor1, actor2))
        for film in films:
            film1, film2 = film
            self.printFilmData(film1, actor1, actor2, film2['role'])
            
    def printRelation(self, actor1, actor2, relation):
        ''' 
        Print the path that join two actors/actress
        
        params:
         * actor1: First Actor/actress name
         * actor2: Second Actor/actress name
         * relation: Node with the path between actor1 and actor2
        '''
        print(("Actors/Actresses %s and %s are related in %d steps:") % (actor1, actor2, relation.length))
        
        elements = relation.names
        types = relation.types
        i = 0
        for name,eltype in zip(elements, types):
            if eltype == "a":
                print(("%s|-> Actor/Actress: %s") % (" "*i, name))
            elif eltype == "f":
                print(("%s|-> Film: %s ") % (" "*i,name))
            i += 1