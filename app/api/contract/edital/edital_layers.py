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

    document_name = "DTBB006 - MIOLO"
    current_layer = "miolo.pdf"


class DTBB006Rodape(tp.EditalDTBB006RodapeDefault):

    document_name = "DTBB006 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB006 -------------------------------------#
#####################################################################################

#####################################################################################
# ------------------------------------- DT003_002 -------------------------------------#

class DT003_002Capa(tp.DT003_002, HTMLDocument):

    document_name = "DT003_002 - CAPA"
    current_layer = "capa.html"


class DT003_002Miolo(tp.DT003_002, PDFDocument):

    document_name = "DT003_002 - MIOLO"
    current_layer = "miolo.pdf"


class DT003_002Rodape(tp.EditalDT003_002RodapeDefault):

    document_name = "DT003_002 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DT003_002 -------------------------------------#
#####################################################################################

#####################################################################################
# ------------------------------------- DTBNC001_001 -------------------------------------#

class DTBNC001_001Capa(tp.DTBNC001_001, HTMLDocument):

    document_name = "DTBNC001_001 - CAPA"
    current_layer = "capa.html"


class DTBNC001_001Miolo(tp.DTBNC001_001, PDFDocument):

    document_name = "DTBNC001_001 - MIOLO"
    current_layer = "miolo.pdf"


class DTBNC001_001Rodape(tp.EditalDTBNC001_001RodapeDefault):

    document_name = "DTBNC001_001 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBNC001_001 -------------------------------------#
#####################################################################################

#####################################################################################
# ------------------------------------- DTDV001_001 -------------------------------------#

class DTDV001_001Capa(tp.DTDV001_001, HTMLDocument):

    document_name = "DTDV001_001 - CAPA"
    current_layer = "capa.html"


class DTDV001_001Miolo(tp.DTBB006, PDFDocument):

    document_name = "DTDV001_001 - MIOLO"
    current_layer = "miolo.pdf"


class DTDV001_001Rodape(tp.EditalDTDV001_001RodapeDefault):

    document_name = "DTDV001_001 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTDV001_001 -------------------------------------#
#####################################################################################

#####################################################################################
# ------------------------------------- DTEM_001 -------------------------------------#

class DTEM_001Capa(tp.DTEM_001, HTMLDocument):

    document_name = "DTEM_001 - CAPA"
    current_layer = "capa.html"


class DTEM_001Miolo(tp.DTEM_001, PDFDocument):

    document_name = "DTEM_001 - MIOLO"
    current_layer = "miolo.pdf"


class DTEM_001Rodape(tp.EditalDTEM_001RodapeDefault):

    document_name = "DTEM_001 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTEM_001 -------------------------------------#
#####################################################################################

#####################################################################################
# ------------------------------------- DTEMG001 -------------------------------------#

class DTEMG001Capa(tp.DTEMG001, HTMLDocument):

    document_name = "DTEMG001 - CAPA"
    current_layer = "capa.html"


class DTEMG001Miolo(tp.DTEMG001, PDFDocument):

    document_name = "DTEMG001 - MIOLO"
    current_layer = "miolo.pdf"


class DTEMG001Rodape(tp.EditalDTEMG001RodapeDefault):

    document_name = "DTEMG001 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTEMG001 -------------------------------------#
#####################################################################################

#####################################################################################
# ------------------------------------- DTENF_NPL_001_004 -------------------------------------#

class DTENF_NPL_001_004Capa(tp.DTENF_NPL_001_004, HTMLDocument):

    document_name = "DTENF_NPL_001_004 - CAPA"
    current_layer = "capa.html"


class DTENF_NPL_001_004Miolo(tp.DTENF_NPL_001_004, PDFDocument):

    document_name = "DTENF_NPL_001_004 - MIOLO"
    current_layer = "miolo.pdf"


class DTENF_NPL_001_004Rodape(tp.EditalDTENF_NPL_001_004RodapeDefault):

    document_name = "DTENF_NPL_001_004 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTENF_NPL_001_004 -------------------------------------#
#####################################################################################

#####################################################################################
# ------------------------------------- DTITPV001_001 -------------------------------------#

class DTITPV001_001Capa(tp.DTITPV001_001, HTMLDocument):

    document_name = "DTITPV001_001 - CAPA"
    current_layer = "capa.html"


class DTITPV001_001Miolo(tp.DTITPV001_001, PDFDocument):

    document_name = "DTITPV001_001 - MIOLO"
    current_layer = "miolo.pdf"


class DTITPV001_001Rodape(tp.EditalDTITPV001_001RodapeDefault):

    document_name = "DTITPV001_001 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTITPV001_001 -------------------------------------#
#####################################################################################

#####################################################################################
# ------------------------------------- DTRD001_001 -------------------------------------#

class DTRD001_001Capa(tp.DTRD001_001, HTMLDocument):

    document_name = "DTRD001_001 - CAPA"
    current_layer = "capa.html"


class DTRD001_001Miolo(tp.DTRD001_001, PDFDocument):

    document_name = "DTRD001_001 - MIOLO"
    current_layer = "miolo.pdf"


class DTRD001_001Rodape(tp.EditalDTRD001_001RodapeDefault):

    document_name = "DTRD001_001 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTRD001_001 -------------------------------------#
#####################################################################################

#####################################################################################
# ------------------------------------- DTTRI001_001 -------------------------------------#

class DTTRI001_001Capa(tp.DTTRI001_001, HTMLDocument):

    document_name = "DTTRI001_001 - CAPA"
    current_layer = "capa.html"


class DTTRI001_001Miolo(tp.DTTRI001_001, PDFDocument):

    document_name = "DTTRI001_001 - MIOLO"
    current_layer = "miolo.pdf"


class DTTRI001_001Rodape(tp.EditalDTTRI001_001RodapeDefault):

    document_name = "DTTRI001_001 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTTRI001_001 -------------------------------------#
#####################################################################################
