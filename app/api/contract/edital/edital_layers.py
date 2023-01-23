from api.engine.document_interfaces import HTMLDocument, PDFDocument
from api.contract.edital.edital_templates import DTBB001, DTBB002, DTBB003, DTBB004, DTBB005, DTBB006, EditalRodapeDefault


#####################################################################################
# ------------------------------------- DTBB001 -------------------------------------#

class DTBB001Capa(DTBB001, HTMLDocument):

    document_name = "DTBB001 - CAPA"
    current_layer = "capa.html"


class DTBB001Miolo(DTBB001, PDFDocument):

    document_name = "DTBB001 - MIOLO"
    current_layer = "miolo.pdf"


class DTBB001Rodape(EditalRodapeDefault):

    document_name = "DTBB001 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB001 -------------------------------------#
#####################################################################################


#####################################################################################
# ------------------------------------- DTBB002 -------------------------------------#

class DTBB002Capa(DTBB002, HTMLDocument):

    document_name = "DTBB002 - CAPA"
    current_layer = "capa.html"


class DTBB002Miolo(DTBB001, PDFDocument):

    document_name = "DTBB002 - MIOLO"
    current_layer = "miolo.pdf"


class DTBB002Rodape(EditalRodapeDefault):

    document_name = "DTBB002 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB002 -------------------------------------#
#####################################################################################


#####################################################################################
# ------------------------------------- DTBB003 -------------------------------------#

class DTBB003Capa(DTBB003, HTMLDocument):

    document_name = "DTBB003 - CAPA"
    current_layer = "capa.html"


class DTBB003Miolo(DTBB003, PDFDocument):

    document_name = "DTBB003 - MIOLO"
    current_layer = "miolo.pdf"


class DTBB003Rodape(EditalRodapeDefault):

    document_name = "DTBB003 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB003 -------------------------------------#
#####################################################################################


#####################################################################################
# ------------------------------------- DTBB004 -------------------------------------#

class DTBB004Capa(DTBB004, HTMLDocument):

    document_name = "DTBB004 - CAPA"
    current_layer = "capa.html"


class DTBB004Miolo(DTBB004, PDFDocument):

    document_name = "DTBB004 - MIOLO"
    current_layer = "miolo.pdf"


class DTBB004Rodape(EditalRodapeDefault):

    document_name = "DTBB004 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB004 -------------------------------------#
#####################################################################################


#####################################################################################
# ------------------------------------- DTBB005 -------------------------------------#

class DTBB005Capa(DTBB005, HTMLDocument):

    document_name = "DTBB005 - CAPA"
    current_layer = "capa.html"


class DTBB005Rodape(EditalRodapeDefault):

    document_name = "DTBB005 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB005 -------------------------------------#
#####################################################################################


#####################################################################################
# ------------------------------------- DTBB006 -------------------------------------#

class DTBB006Capa(DTBB006, HTMLDocument):

    document_name = "DTBB006 - CAPA"
    current_layer = "capa.html"


class DTBB006Miolo(DTBB006, PDFDocument):

    document_name = "DTBB001 - MIOLO"
    current_layer = "miolo.pdf"


class DTBB006Rodape(EditalRodapeDefault):

    document_name = "DTBB006 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB006 -------------------------------------#
#####################################################################################
