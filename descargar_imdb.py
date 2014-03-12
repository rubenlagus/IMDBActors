# -*- coding: ISO-8859-1 -*-
'''
Copyright 2014 Ruben Bermudez Lopez

descargar_imdb is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

descargar_imdb is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with descargar_imdb.  If not, see <http://www.gnu.org/licenses/>.
'''

from downloadFromWeb import DownloadFromWeb
from fileHandler import FileHandler
import time

if __name__ == '__main__':
    ''' 
    This script ask if new version should be downloaded from the web (only if new version is available),
    then, it download the actor and actresses database and load them into a shelve file so it can be access
    faster.
    It may take long, depending on how big are the databases and the speed of PC, network connection
    and Harddisks.
    '''
    dw = DownloadFromWeb("ftp.fu-berlin.de","pub/misc/movies/database" )
    download = False
    option = 0
    try:
        option = int(input("Do you want to download the new version of the databases if available? (1=yes, 0= no)"))
        if option != 0 and option != 1:
            raise ValueError()
    except ValueError:
        print("Option not found, assuming default value: no")
        
    if option == 1:
        download = True
    result = dw.fetch("actresses.list.gz", download)
    print(result)
    result = dw.fetch("actors.list.gz", download)
    print(result)

    print("All fetched")
    print("Loading actors")
    actorHandler = FileHandler()
    actorHandler.open("actors.list.gz")
    actorHandler.loadData()
    print("Actors loaded, closing files")
    actorHandler.close()    
    print("Loading actresses")
    actressHandler = FileHandler()
    actressHandler.open("actresses.list.gz")
    actressHandler.loadData()
    print("Actresses loaded, closing files")
    actressHandler.close()