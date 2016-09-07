from PyPDF2 import PdfFileWriter, PdfFileReader

# TODO: create an abstract or interface class

class PDFPagePick:
    """
    class PDFPagePick
    Select any page you want and then organize them into a new PDF file
    """
    def __init__(self, src, outputFileName):
        self.__src = PdfFileReader(src)
        self.__output = PdfFileWriter()
        self.__outputFileName = outputFileName

    def pickIndividualPages(self, pageNumList):
        for pageNum in pageNumList:
            if self.__checkPageNum(self.__src, pageNum) == True:
                self.__output.addPage(self.__src.getPage(pageNum))
            else:
                print ('pageNum %d doesn''t exist. Pass' % pageNum)

    def insertBlankPage(self):
        self.__output.addBlankPage()

    def save(self):
        outputStream = open(self.__outputFileName, 'wb')
        self.__output.write(outputStream)
        outputStream.close()

    def __checkPageNum(self, target, pageNum):
        if pageNum < 0 or pageNum > target.getNumPages()-1:
            print 'Invalid pageNum'
            return False
        return True

class PDFPageMerge:
    """
    class PDFMerge
    It merges 2 pdf files into a new one.
    """
    def __init__(self, src, dest, outputFileName):
        self.__src = PdfFileReader(src)
        self.__dest = PdfFileReader(dest)
        self.__outputFileName = outputFileName
        self.__output = PdfFileWriter()

    def mergeSrcPageToDestPage(self, srcPageNum, destPageNum):
        if self.__checkPageNum(self.__src, srcPageNum) == True and self.__checkPageNum(self.__dest, destPageNum) == True:
            destPage = self.__dest.getPage(destPageNum)
            destPage.mergePage(self.__src.getPage(srcPageNum))
            self.__output.addPage(destPage)

    def getSrcTotalPage(self):
        return self.__src.getNumPages()

    def save(self):
        outputStream = open(self.__outputFileName, 'wb')
        self.__output.write(outputStream)
        outputStream.close()

    def __checkPageNum(self, target, pageNum):
        if pageNum < 0 or pageNum > target.getNumPages()-1:
            print 'Invalid pageNum'
            return False
        return True
