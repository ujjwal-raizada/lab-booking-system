from .forms import *
from .models.instrument.form_models import *

form_template_dict = {
    1: (FESEMForm, FESEM),
    2: (TCSPCForm, TCSPC),
    3: (FTIRForm, FTIR),
    4: (LCMSForm, LCMS),
    5: (RheometerForm, Rheometer),
    6: (AASForm, AAS),
    7: (TGAForm, TGA),
    8: (BETForm, BET),
    9: (CDSpectrophotometerForm, CDSpectrophotometer),
    10: (LSCMForm, LSCM),
    11: (DSCForm, DSC),
    12: (GCForm, GC),
    13: (EDXRFForm, EDXRF),
    14: (HPLCForm, HPLC),
    15: (NMRForm, NMR),
    16: (PXRDForm, PXRD),
    17: (SCXRDForm, SCXRD),
    18: (XPSForm, XPS),
    19: (UVSpectrophotometerForm, UVSpectrophotometer),
}

view_application_dict = {model: form
                         for idx, (form, model) in form_template_dict.items()}
