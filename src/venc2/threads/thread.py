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

import codecs

from math import ceil

from VenC.helpers import Notify
from VenC.helpers import Die
from VenC.l10n import Messages
from VenC.pattern.processor import Processor
from VenC.pattern.processor import MergeBatches

class Thread:
    def __init__(self, prompt, datastore, theme):
        # Notify wich thread is processed
        Notify(prompt)
        
        # Setup useful data
        self.theme = theme
        self.currentPage = 0
        self.datastore = datastore
        
        # Setup pattern processor
        self.processor = Processor()
        self.processor.SetFunction("GetRelativeOrigin", self.GetRelativeOrigin)
        self.processor.SetFunction("GetRelativeLocation", self.GetRelativeLocation)
        self.processor.SetFunction("GetNextPage", self.GetNextPage)
        self.processor.SetFunction("GetPreviousPage", self.GetPreviousPage)
        self.processor.SetFunction("ForPages", self.ForPages)
        self.processor.SetFunction("GetRelativeLocation", self.GetRelativeLocation)
        self.processor.SetFunction("IfInThread", self.IfInThread)

    def ReturnPageAround(self, string, destinationPageNumber, fileName):
        return string.format({
            "destinationPage":destinationPageNumber,
            "destinationPageUrl":fileName,
            "entryName" : self.entryName
        })


    # Must be called in child class
    def GetRelativeLocation():
        return self.exportPath[5:]

    # Must be called in child class
    def OrganizeEntries(self, entries):
        self.pages = list()
        entriesPerPage = int(self.datastore.blogConfiguration["entriesPerPages"])
        for i in range(0, ceil(len(entries)/entriesPerPage)):
            self.pages.append(
                entries[i*entriesPerPage:(i+1)*entriesPerPage]
            )

        self.pagesCount = len(self.pages)

    # Must be called in child class
    def GetRelativeOrigin(self, argv=list()):
        return self.relativeOrigin

    # Must be called in child class
    def GetNextPage(self,argv=list()):
        if self.currentPage < len(self.pages) - 1:
            destinationPageNumber = str(self.currentPage + 1)
            ''' Must catch KeyError exception '''
            fileName = self.fileName.format({"pageNumber":destinationPageNumber})
            return self.ReturnPageAround(argv[0], destinationPageNumber, fileName)

        else:
            return str()

    # Must be called in child class
    def GetPreviousPage(self, argv=list()):
        if self.currentPage > 0:
            destinationPageNumber = str(self.currentPage - 1)
            if self.currentPage == 1:
                ''' Must catch KeyError exception '''
                fileName = self.fileName.format(page_number="")

            else:
                ''' Must catch KeyError exception '''
                fileName = self.fileName.format(page_number=destinationPageNumber)
            
            return self.ReturnPageAround(argv[0], destinationPageNumber, fileName)
        
        else:
            return str()

    # Must be called in child class
    def ForPages(self, argv):
        listLenght = int(argv[0])
        string = argv[1]
        separator = argv[2]
            
        if self.pagesCount == 1 or not self.inThread:
            return str()

        output = str()
        pageNumber = 0
        for page in self.pages:
            if (not pageNumber < self.currentPage - self.pagesCount) and (not pageNumber > self.currentPage + self.pagesCount):
                output += string.format(
                    {
                        "pageNumber":str(pageNumber),
                        "pageUrl": self.fileName.format({"pageNumber": (str() if pageNumber == 0 else pageNumber) })
                    }
                ) + separator

            pageNumber +=1
        
        return output[:-len(separator)]


    def IfInThread(self, argv):
        if self.inThread:
            return argv[0]

        else:
            return argv[1]

    def FormatFileName(self, pageNumber):
        try:
            if pageNumber == 0:
                return self.fileName.format({
                    'entryId':'',
                    'pageNumber':''
                })
        
            else:
                return self.fileName.format({
                    'entryId':pageNumber,
                    'pageNumber':pageNumber
                })

        except KeyError as e:
            Die(Messages.variableErrorInFileName.format(str(e)))

    # Must be called in child class
    def Do(self):
        pageNumber = 0
        for page in self.pages:
            output = MergeBatches(self.processor.BatchProcess(self.theme.header))

            columnsNumber = self.datastore.blogConfiguration["columns"]
            columnsCounter = 0
            columns = [ '' for i in range(0, columnsNumber) ]
            for entry in page:
                columns[columnsCounter] += MergeBatches(self.processor.BatchProcess(entry.htmlWrapper.above, not entry.doNotUseMarkdown))
                columns[columnsCounter] += MergeBatches(self.processor.BatchProcess(entry.content, not entry.doNotUseMarkdown))
                columns[columnsCounter] += MergeBatches(self.processor.BatchProcess(entry.htmlWrapper.below, not entry.doNotUseMarkdown))

                columnsCounter +=1
                if columnsCounter >= columnsNumber:
                    columnsCounter = 0

            columnsCounter = 0
            for column in columns:
                output += '<div id="__VENC_COLUMN_'+str(columnsCounter)+'__" class="__VENC_COLUMN__">'+column+'</div>'
            
            output += MergeBatches(self.processor.BatchProcess(self.theme.footer))
        
            stream = codecs.open(
                self.exportPath + self.FormatFileName(pageNumber),
                'w',
                encoding="utf-8"
            )
            stream.write(output)
            stream.close()

            pageNumber += 1