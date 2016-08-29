from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

_DEFAULT_FONT_NAME = 'user-sepecified-font'
_DEFAULT_FONT_SIZE = 20
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
        self.fontSize = _DEFAULT_FONT_SIZE

    def setFont(self, fontPath, fontSize=_DEFAULT_FONT_SIZE):
        pdfmetrics.registerFont(TTFont(_DEFAULT_FONT_NAME, fontPath))
        self.fontSize = fontSize
        self.canvas.setFont(_DEFAULT_FONT_NAME, self.fontSize * _POINT)

    def drawString(self, x, y, text):
        self.canvas.drawString(x, y, text)

    def endThisPage(self):
        self.canvas.showPage()
        # keep the font setting
        self.canvas.setFont(_DEFAULT_FONT_NAME, self.fontSize * _POINT)

    def saveAndCloseFile(self):
        """
        Saves and close the PDF document in the file.
        After this operation the canvas must not be used further.
        """
        self.canvas.save()
