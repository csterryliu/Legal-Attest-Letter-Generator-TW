from PyPDF2 import PdfFileWriter, PdfFileReader

class PDFmerger:
    """
    class PDFmerger
    It merge 2 pdf files into a new one.
    Merge direction: src -> dest
    """
    def __init__(self, src, dest, outputFileName):
        self.__dest = PdfFileReader(open(src, 'rb'))
        self.__src = PdfFileReader(open(dest, 'rb'))
        self.__outputFileName = outputFileName
        self.__output = PdfFileWriter()

    def mergeThenAdd(self, srcPageNum, destPageNum):
        if self.__checkPageNum(self.__src, srcPageNum) == True and self.__checkPageNum(self.__dest, destPageNum) == True:
            destPage= self.__dest.getPage(destPageNum)
            destPage.mergePage(self.__src.getPage(srcPageNum))
            self.__output.addPage(destPage)

    def save(self):
        outputStream = open(self.__outputFileName, 'wb')
        self.__output.write(outputStream)
        outputStream.close()

    def __checkPageNum(self, target, pageNum):
        if pageNum < 0 or pageNum > target.getNumPages()-1:
            print 'Invalid pageNum'
            return False
        return True
