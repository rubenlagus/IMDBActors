# -*- coding: utf-8 -*-
'''
Copyright 2014 Ruben Bermudez Lopez

FileHandler is free software: you can redistribute it and/or modify
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

import re
import shelve
import gzip

class FileHandler():
    ''' This class provide all the functionality needed to manage the files and the databases '''

    def __init__(self):
        ''' 
        Constructor 
        During construction, regular expresions are build. They are used to read the files from IMDB
        '''
        queries = self.queries()
        self.seriereg = re.compile(queries[0], re.UNICODE)
        self.filmreg = re.compile(queries[1], re.UNICODE)
        self.autreg = re.compile(queries[2], re.UNICODE)
        self.chapterreg = [re.compile(queries[3][0], re.UNICODE),
            re.compile(queries[3][1], re.UNICODE),
            re.compile(queries[3][2], re.UNICODE)]

    def queries(self):
        ''' 
           Regular expresions to read the IMDB files.
           
           note:
               They are based on the script: http://www.greenteapress.com/thinkpython/code/imdb.py
        '''
        queryserie = '"(?P<title>[^(]+)"'
        queryserie += '\s+'
        queryserie += '\((?P<year>\d{4})\)'
        queryserie += '\s+'
        queryserie += '(?:'
        queryserie += '\{(?P<chapterinfo>[^{}]+)\}'
        queryserie += ')?'
        queryserie += '\s+'
        queryserie += '(?:\(V\)|\(TV\)|\(uncredited\)|\(credit\sonly\)\s+)?'
        queryserie += '\[(?P<role>[^\]]+)\]'
        queryserie += '[.]*'

        queryfilm = '(?P<title>[^(]+)'
        queryfilm += '\s+'
        queryfilm += '\((?P<year>\d{4})\)'
        queryfilm += '\s+'
        queryfilm += '(?:\(V\)|\(TV\)|\(uncredited\)|\(credit\sonly\)\s+)?'
        queryfilm += '\[(?P<role>[^\]]+)\]'
        queryfilm += '[.]*'

        querychapter = ['\((?P<chapterno>[^()]+)\)',
            '(?P<chapter>[^()]+)\s*\((?P<chapterno>[^()]+)\)',
            '(?P<chapter>[^()]+)']

        queryaut = '([^\t]*)\t*(.*)'

        return queryserie, queryfilm, queryaut, querychapter

    def open(self, filename):
        '''
        This method open a file
        
        params:
         * filename: file to open (it should be in current folder)
        
        return: True if the file was open, False otherwise
        '''
        try:
            self.filename = "./" + filename
            self.file = gzip.open(self.filename, 'rb')
        except:
            return False
        return True

    def openActDB(self):
        ''' 
        Open the actors/actresses database
        
        return: True if it was open, False otherwises
        '''
        try:
            self.actdb = shelve.open('./actdb')
        except:
            return False
        return True

    def openFilmsDB(self):
        ''' 
        Open the films database
        
        return: True if it was open, False otherwises
        '''
        try:
            self.filmsdb = shelve.open('./filmsdb')
        except:
            return False
        return True

    def searchActor(self, fullname):
        ''' 
        Find films/tvseries where an actor/actress appears 
        
        params:
         * fullname: Name of the actor/actress
         
        return: Empty list if the actor is not found, a list with the info requested otherwise
        '''       
        if fullname in self.actdb["actors"]:
            return self.actdb[fullname]
        else:
            return []
        
    def broadSpectrumSearchActor(self, fullname):
        ''' 
                Split the name of an actor/actress and search all the actors/actresses in the database
            that fit with any of the parts
            
            params:
             * fullname: Name of the actor
             
            return: Empty dictionary if no actors/actresses were found, otherwise, a dictionary where
               keys are the name of the actors/actresses found and values are the films where they appear.
        '''
        names = fullname.split()
        for i in range(len(names)):
            names[i] = re.sub(r'[^a-zA-Z0-9]','', names[i]) # remove from each part all caracters that aren't numbers or letters
        posibles = []
        for name in names:
            for actor in self.actdb:
                if str(name) in str(actor):
                    posibles.append(actor)               
        results = {}
        for actor in posibles:
            print(actor)
            results[actor] = self.actdb[actor]
            
        return results

    def searchFilms2actors(self, fullname1, fullname2):
        ''' 
        Find the films where two actors/actresses are coprotagonist
        
        params: 
         * fullname1: Name of the first actor/actress
         * fullname2: Name of the second actor/actress
         
        return:
         A data structure as pairs with the info of each film, where first element belong to the first 
           actor/actress and the second element to the second actor/actress
        '''
        
        films1 = self.searchActor(fullname1) # Get films for fullname1
        films2 = self.searchActor(fullname2) # Get films for fullname2
        
        titles1 = [film['title'] for film in films1] # Titles of films for fullname1
        titles2 = [film['title'] for film in films2] # Titles of films for fullname2
        
        results = []
        for title in titles1:
            if title in titles2:
               results.append(title) # Add films that belong to both fullnames
        
        resultsdata = []
        for result in results: # Build return data structure
            res1 = []
            res2 = []
            for film in films1:
                if film['title'] == result:
                    res1 = film
            for film in films2:
                if film['title'] == result:
                    res2 = film
            resultsdata.append((res1,res2))
        
        return resultsdata
    
    def close(self):
        '''
        This method close the file opended with open method
        
        return: True if the file was closed, False otherwise
        '''
        try:
            self.file.close()
        except:
            return False
        return True

    def closeActDB(self):
        '''
        This method close the actors/actresses database opened with openActDB method
        
        return: True if the DB was closed, False otherwise
        '''
        try:
            self.actdb.close()
        except:
            return False
        return True

    def closeFilmsDB(self):
        '''
        This method close the films database opened with openFilmsDB method
        
        return: True if the DB was closed, False otherwise
        '''
        try:
            self.filmsdb.close()
        except:
            return False
        return True

    def loadData(self):
        ''' 
        This method load the information in the file opened with open method to two database (need to make following task faster):
          * actdb: Database where the keys are the actors/actresses names and values are lists with all the films/tvserie
                    where current actor/actress appear.
          * filmsdb: Database where the keys are the films/tvseries names and values are lists with the names of 
                    all the actors/actresses that appear in current film/tvserie.
                    
        note: In actdb, a new key is added with key 'actors' and value a list of all the actors that are in the database
        '''
        self.actdb = shelve.open('./actdb',writeback=True)
        self.filmsdb = shelve.open('./filmsdb',writeback=True)
        names = set()
        actor = ''
        count = 0
        for line in self.file: # Ignore line until start of desired infomation
            if line.strip() == b'----			------':
                break
        for line in self.file:
            count += 1
            if count > 1000000: # Syncronize the shelve structure with the disc periodically
                self.actdb.sync()
                self.filmsdb.sync()
            line = str(line, 'ISO-8859-1')
            line = line.rstrip()
            if line == '': # If line is empty, read next
                continue
            if line[0] == '-----': # If it is the end, finish for loop
                break
            ro = self.autreg.match(line) # Split the line in actor and information
            if not ro: # If previous regular expresion don't match the line, read next
                continue
            new_actor, info = ro.groups()
            if new_actor: # If actor exits, add it to the database
                names.add(new_actor)
                actor = new_actor
                if not actor in self.actdb:
                    self.actdb[actor] = []
            if info[0] == '"': # If info start with an " we are in a TVSerie
                re = self.seriereg.match(line) # Split line into year, role, title and chapter info
                if not re: # If previous regular expresion don't match the line, read next
                    continue
                aux = re.groupdict()
                aux["type"] = "TVSerie" # Set type of current line to TVSerie
                if aux["chapterinfo"] is not None: # If there is chapter information, read it
                    ch = self.chapterreg[0].match(aux["chapterinfo"]) # Look for only chapter number
                    if ch: # If chapter info match previous regular expresion
                        aux.update(ch.groupdict())
                        del aux["chapterinfo"]
                    else: 
                        ch = self.chapterreg[1].match(aux["chapterinfo"]) # Look for chapter name and number
                        if ch: # If chapter info match for name and number
                            aux.update(ch.groupdict())
                            del aux["chapterinfo"]
                        else:
                            ch = self.chapterreg[2].match(aux["chapterinfo"]) # Look only for chapter name
                            if ch: # If chapter info match only for name
                                aux.update(ch.groupdict())
                            del aux["chapterinfo"]
                self.actdb[actor].append(aux) # Append info read to currentt actor/actress
                if not aux["title"] in self.filmsdb: # If the TV serie is not yet in films DB, add it
                    self.filmsdb[aux["title"]] = []
                self.filmsdb[aux["title"]].append(actor) # Add current actor to current TVSerie in films DB
            else: # If we  are in a film
                re = self.filmreg.match(info) # Split info into title, year and role
                if not re: # If line doesn't match previous regular expresion, read next line
                    continue
                aux = re.groupdict()
                aux["type"] = "Film" # Set type of current line to Film
                self.actdb[actor].append(aux) # Append info read to current actor/actress
                if not aux["title"] in self.filmsdb: # If the Films is not yet in films DB, add it
                    self.filmsdb[aux["title"]] = []
                self.filmsdb[aux["title"]].append(actor) # Add current actor to current Film in films DB
        if "actors" in self.actdb: # Finally add the list of actors/actresses to actor DB
            self.actdb["actors"] = names
        else:
            self.actdb["actors"] = names.copy()
        self.actdb.close() # Close DBs
        self.filmsdb.close()    
