from .forms import *
from .models import *

form_template_dict = {
    1: ('booking_portal/fesem.html', FESEMForm, FESEM),
    2: ('booking_portal/tcspc.html', TCSPCForm, TCSPC),
    3: ('booking_portal/ftir.html', FTIRForm, FTIR),
    4: ('booking_portal/lcms.html', LCMSForm, LCMS),
    5: ('booking_portal/rheometer.html', RheometerForm, Rheometer),
    6: ('booking_portal/aas.html', AASForm, AAS),
    7: ('booking_portal/tga.html', TGAForm, TGA),
    8: ('booking_portal/bet.html', BETForm, BET),
    9: ('booking_portal/cdspectrophotometer.html', CDSpectrophotometerForm, CDSpectrophotometer),
    10: ('booking_portal/lscm.html', LSCMForm, LSCM),
    11: ('booking_portal/dsc.html', DSCForm, DSC),
    12: ('booking_portal/gc.html', GCForm, GC),
    13: ('booking_portal/edxrf.html', EDXRFForm, EDXRF),
    14: ('booking_portal/hplc.html', HPLCForm, HPLC),
    15: ('booking_portal/nmr.html', NMRForm, HPLC),
    16: ('booking_portal/pxrd.html', PXRDForm, PXRD),
    17: ('booking_portal/scxrd.html', SCXRDForm, SCXRD),
    18: ('booking_portal/xps.html', XPSForm, XPS),
    19: ('booking_portal/uvspectrophotometer.html', UVSpectrophotometerForm, UVSpectrophotometer),
}

view_application_dict = {model: (template, form)
                         for idx, (template, form, model) in form_template_dict.items()}