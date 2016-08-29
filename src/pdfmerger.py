from PyPDF2 import PdfFileWriter, PdfFileReader

class PDFmerger:
    """
    class PDFmerger
    It merges 2 pdf files into a new one.
    """
    def __init__(self, src, dest, outputFileName):
        self.__src = PdfFileReader(open(src, 'rb'))
        self.__dest = PdfFileReader(open(dest, 'rb'))
        self.__outputFileName = outputFileName
        self.__output = PdfFileWriter()

    def mergeSrcPageToDestPageThenAdd(self, srcPageNum, destPageNum):
        if self.__checkPageNum(self.__src, srcPageNum) == True and self.__checkPageNum(self.__dest, destPageNum) == True:
            destPage = self.__dest.getPage(destPageNum)
            destPage.mergePage(self.__src.getPage(srcPageNum))
            self.__output.addPage(destPage)

    def addSrcPageToDest(self, srcPageNum):
        if self.__checkPageNum(self.__src, srcPageNum) == True:
            self.__output.addPage(self.__src.getPage(srcPageNum))

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
