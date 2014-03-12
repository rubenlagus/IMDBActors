# -*- coding: utf-8 -*-
'''
Copyright 2014 Ruben Bermudez Lopez

DownloadFromWeb is free software: you can redistribute it and/or modify
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

from ftplib import FTP
from datetime import datetime
import os

class DownloadFromWeb():
    '''
    This class provide all the functionality needed to download a file from the web using ftp.
    After downloading
    '''

    def __init__(self, server, directory):
        '''
        Constructor
        
        Params:
        * server: URL of the ftp server where the file is allocated
        * directory: Path inside the server to find the file
        '''
        self.server = server
        self.directory = directory

    def fetch(self, filename, download):
        '''
            Fetch the file requested from  the server if a newer version is found.
            
            param:
            * filename: Name of the file to download
            * download: True if you want to download the file, False if not
            
            note:
              Parameter download is ignored if the version in the server is the same or older than the local one. 
                 It is also ignored if there is still no local file.
            
            return: 
              Strig explaining the action performed.
        '''
        ftp = FTP(self.server) #Set server address
        ftp.login()  # Connect to server
        ftp.cwd(self.directory) # Move to the desired folder in server
        modifiedTime = ftp.sendcmd('MDTM ' + filename) # Get modification date of the file requested
        lastmodifieddate = datetime.strptime(modifiedTime[4:], "%Y%m%d%H%M%S") # Format modification date

        if os.path.exists("./" + filename):
            localfile = datetime.fromtimestamp(os.path.getmtime("./" + filename)) # Get modification date of local file
            if localfile >= lastmodifieddate:
                ftp.close()
                return "No download needed for file " + filename
            else:
                if download:
                    print("Downloading...")
                    ftp.retrbinary('RETR ' + filename,
                        open(filename, 'wb').write) # Download file from server
                    ftp.close() # Close connection
                    return "File " + filename + " downloaded"
                else:
                    ftp.close()
                    return "A new version is available, but no download requested"
        else:
            print("Downloading...")
            ftp.retrbinary('RETR ' + filename, open(filename, 'wb').write) # Download file from server
            ftp.close()
            return "File " + filename + " downloaded"

