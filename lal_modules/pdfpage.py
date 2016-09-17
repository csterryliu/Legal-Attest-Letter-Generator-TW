from PyPDF2 import PdfFileWriter, PdfFileReader

# TODO: create an abstract or interface class

class PDFPagePick:
    """
    class PDFPagePick
    Select any page you want and then organize them into a new PDF file
    """
    def __init__(self, src, output_filename):
        self.__src = PdfFileReader(src)
        self.__output = PdfFileWriter()
        self.__output_filename = output_filename

    def pickIndividualPages(self, page_num_list):
        for page_num in page_num_list:
            if self.__checkPageNum(self.__src, page_num) == True:
                self.__output.addPage(self.__src.getPage(page_num))
            else:
                print('pageNum %d doesn''t exist. Pass' % page_num)

    def insertBlankPage(self):
        self.__output.addBlankPage()

    def save(self):
        outputstream = open(self.__output_filename, 'wb')
        self.__output.write(outputstream)
        outputstream.close()

    def __checkPageNum(self, target, page_num):
        if page_num < 0 or page_num > target.getNumPages()-1:
            print('Invalid pageNum')
            return False
        return True

class PDFPageMerge:
    """
    class PDFMerge
    It merges 2 pdf files into a new one.
    """
    def __init__(self, src, dest, output_filename):
        self.__src = PdfFileReader(src)
        self.__dest = PdfFileReader(dest)
        self.__output_filename = output_filename
        self.__output = PdfFileWriter()

    def mergeSrcPageToDestPage(self, src_page_num, dest_page_num):
        if (self.__checkPageNum(self.__src, src_page_num) == True
                and self.__checkPageNum(self.__dest, dest_page_num) == True):
            dest_page = self.__dest.getPage(dest_page_num)
            dest_page.mergePage(self.__src.getPage(src_page_num))
            self.__output.addPage(dest_page)

    def getSrcTotalPage(self):
        return self.__src.getNumPages()

    def save(self):
        outputstream = open(self.__output_filename, 'wb')
        self.__output.write(outputstream)
        outputstream.close()

    def __checkPageNum(self, target, page_num):
        if page_num < 0 or page_num > target.getNumPages()-1:
            print('Invalid pageNum')
            return False
        return True
