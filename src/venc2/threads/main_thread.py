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

from venc2.threads.thread import Thread
from venc2.pattern.processor import UnknownContextual
from venc2.pattern.processor import MergeBatches

class MainThread(Thread):
    def __init__(self, prompt, datastore, theme):
        super().__init__(prompt, datastore, theme)
        
        self.OrganizeEntries([
            entry for entry in datastore.GetEntries(
                datastore.blogConfiguration["reverseThreadOrder"]
            )
        ])

        self.fileName = self.datastore.blogConfiguration["path"]["indexFileName"]
        self.entryName = str()
        self.relativeOrigin = str()
        self.exportPath = "blog/"
        self.inThread = True




                
                

