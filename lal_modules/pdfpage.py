from PyPDF2 import PdfWriter, PdfReader

# TODO: create an abstract or interface class

class PDFPagePick:
    """
    class PDFPagePick
    Select any page you want and then organize them into a new PDF file
    """
    def __init__(self, src, output_filename):
        self.__src = PdfReader(src)
        self.__output = PdfWriter()
        self.__output_filename = output_filename

    def pick_individual_pages(self, page_num_list):
        for page_num in page_num_list:
            if self.__check_page_num(self.__src, page_num) is True:
                self.__output.add_page(self.__src.pages[page_num])
            else:
                print('pageNum %d doesn''t exist. Pass' % page_num)

    def insert_blank_page(self):
        self.__output.addBlankPage()

    def save(self):
        outputstream = open(self.__output_filename, 'wb')
        self.__output.write(outputstream)
        outputstream.close()

    def __check_page_num(self, target, page_num):
        if page_num < 0 or page_num > len(target.pages)-1:
            print('Invalid pageNum')
            return False
        return True

class PDFPageMerge:
    """
    class PDFMerge
    It merges 2 pdf files into a new one.
    """
    def __init__(self, src, dest, output_filename):
        self.__src = PdfReader(src)
        self.__dest = PdfReader(dest)
        self.__output_filename = output_filename
        self.__output = PdfWriter()

    def merge_src_page_to_dest_page(self, src_page_num, dest_page_num):
        if (self.__check_page_num(self.__src, src_page_num) is True
                and self.__check_page_num(self.__dest, dest_page_num) is True):
            dest_page = self.__dest.pages[dest_page_num]
            dest_page.merge_page(self.__src.pages[src_page_num])
            self.__output.add_page(dest_page)

    def get_src_total_page(self):
        return len(self.__src.pages)

    def save(self):
        outputstream = open(self.__output_filename, 'wb')
        self.__output.write(outputstream)
        outputstream.close()

    def __check_page_num(self, target, page_num):
        if page_num < 0 or page_num > len(target.pages)-1:
            print('Invalid pageNum')
            return False
        return True
