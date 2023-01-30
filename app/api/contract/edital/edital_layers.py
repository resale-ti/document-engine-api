from api.engine.document_interfaces import HTMLDocument, PDFDocument
import api.contract.edital.edital_templates as tp


#####################################################################################
# ------------------------------------- DTBB001 -------------------------------------#

class DTBB001Capa(tp.DTBB001, HTMLDocument):

    document_name = "DTBB001 - CAPA"
    current_layer = "capa.html"


class DTBB001Miolo(tp.DTBB001, PDFDocument):

    document_name = "DTBB001 - MIOLO"
    current_layer = "miolo.pdf"


class DTBB001Rodape(tp.EditalDTBB001RodapeDefault):

    document_name = "DTBB001 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB001 -------------------------------------#
#####################################################################################


#####################################################################################
# ------------------------------------- DTBB002 -------------------------------------#

class DTBB002Capa(tp.DTBB002, HTMLDocument):

    document_name = "DTBB002 - CAPA"
    current_layer = "capa.html"


class DTBB002Miolo(tp.DTBB002, PDFDocument):

    document_name = "DTBB002 - MIOLO"
    current_layer = "miolo.pdf"


class DTBB002Rodape(tp.EditalDTBB002RodapeDefault):

    document_name = "DTBB002 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB002 -------------------------------------#
#####################################################################################


#####################################################################################
# ------------------------------------- DTBB003 -------------------------------------#

class DTBB003Capa(tp.DTBB003, HTMLDocument):

    document_name = "DTBB003 - CAPA"
    current_layer = "capa.html"


class DTBB003Miolo(tp.DTBB003, PDFDocument):

    document_name = "DTBB003 - MIOLO"
    current_layer = "miolo.pdf"


class DTBB003Rodape(tp.EditalDTBB003RodapeDefault):

    document_name = "DTBB003 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB003 -------------------------------------#
#####################################################################################


#####################################################################################
# ------------------------------------- DTBB004 -------------------------------------#

class DTBB004Capa(tp.DTBB004, HTMLDocument):

    document_name = "DTBB004 - CAPA"
    current_layer = "capa.html"


class DTBB004Miolo(tp.DTBB004, PDFDocument):

    document_name = "DTBB004 - MIOLO"
    current_layer = "miolo.pdf"


class DTBB004Rodape(tp.EditalDTBB004RodapeDefault):

    document_name = "DTBB004 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB004 -------------------------------------#
#####################################################################################


#####################################################################################
# ------------------------------------- DTBB005 -------------------------------------#

class DTBB005Capa(tp.DTBB005, HTMLDocument):

    document_name = "DTBB005 - CAPA"
    current_layer = "capa.html"


class DTBB005Rodape(tp.EditalDTBB005RodapeDefault):

    document_name = "DTBB005 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB005 -------------------------------------#
#####################################################################################


#####################################################################################
# ------------------------------------- DTBB006 -------------------------------------#

class DTBB006Capa(tp.DTBB006, HTMLDocument):

    document_name = "DTBB006 - CAPA"
    current_layer = "capa.html"


class DTBB006Miolo(tp.DTBB006, PDFDocument):

    document_name = "DTBB001 - MIOLO"
    current_layer = "miolo.pdf"


class DTBB006Rodape(tp.EditalDTBB006RodapeDefault):

    document_name = "DTBB006 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB006 -------------------------------------#
#####################################################################################
