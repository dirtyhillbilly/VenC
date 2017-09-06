#! /usr/bin/python3

#    Copyright 2016, 2017 Denis Salem
#
#    This file is part of VenC.
#
#    VenC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    VenC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with VenC.  If not, see <http://www.gnu.org/licenses/>.

import os

from VenC.helpers import Notify
from VenC.threads.thread import Thread
from VenC.pattern.processor import UnknownContextual
from VenC.pattern.processor import MergeBatches

class DatesThread(Thread):
    def __init__(self, prompt, datastore, theme):
        super().__init__(prompt, datastore, theme)
        
        self.fileName = self.datastore.blogConfiguration["path"]["indexFileName"]
        self.entryName = str()
        self.relativeOrigin = "../"
        self.inThread = True

    def Do(self):
        
        for thread in self.datastore.entriesPerDates:
            Notify("\t"+thread.value+"...")
            self.exportPath = "blog/"+thread.value+'/'
            os.makedirs(self.exportPath)
            self.OrganizeEntries([
                entry for entry in self.datastore.GetEntriesForGivenDate(
                    thread.value,
                    self.datastore.blogConfiguration["reverseThreadOrder"]
                )
            ])

            super().Do()




                
                

