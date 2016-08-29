from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

_TEMP_FONT_NAME = 'user-sepecified-font'
_POINT = 1

class pdfgenerator:
    """
    class pdfgenerator
    It creates a temporary pdf file for merging.
    """
    def __init__(self, filename, wide, height):
        self.canvas = canvas.Canvas(filename, pagesize=(wide, height))
        self.canvas.setStrokeColorRGB(0,0,0)
        self.canvas.setFillColorRGB(0,0,0)

    def setFont(self, fontPath, fontSize):
        pdfmetrics.registerFont(TTFont(_TEMP_FONT_NAME, fontPath))
        self.canvas.setFont(_TEMP_FONT_NAME, fontSize * _POINT)

    def drawString(self, x, y, text):
        self.canvas.drawString(x, y, text)

    def endThisPage(self):
        self.canvas.showPage()

    def saveAndCloseFile(self):
        """
        Saves and close the PDF document in the file.
        After this operation the canvas must not be used further.
        """
        self.canvas.save()
