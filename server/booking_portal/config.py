from .forms import *

form_template_dict = {
    1: ('booking_portal/fesem.html', FESEMForm),
    2: ('booking_portal/tcspc.html', TCSPCForm),
    3: ('booking_portal/ftir.html', FTIRForm),
    4: ('booking_portal/lcms.html', LCMSForm),
}
