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
            # by doing this the original destination page will be intact after mergin
            srcPage = self.__src.getPage(srcPageNum)
            srcPage.mergePage(self.__dest.getPage(destPageNum))
            self.__output.addPage(srcPage)

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
