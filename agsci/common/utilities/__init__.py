from DateTime import DateTime
from datetime import datetime, tzinfo
import pytz
import base64

def toISO(v):
            
    if isinstance(v, DateTime):
        try:
            tz = pytz.timezone(v.timezone())
        except pytz.UnknownTimeZoneError:
            # Because that's where we are.
            tz = pytz.timezone('US/Eastern') 
    
        tmp_date = datetime(v.year(), v.month(), v.day(), v.hour(), 
                            v.minute(), int(v.second()))

        if tmp_date.year not in [2499, 1000]:
            return tz.localize(tmp_date).isoformat()

    return None

def getText(object):
    if object.portal_type in ['File', 'Image', 'Link', 'FSDFacultyStaffDirectoryTool'] or object.portal_type.startswith('Form'):
        text = ''
    elif hasattr(object, 'getRawText'):
        text = object.getRawText()
    elif hasattr(object, 'getText'):
        text = object.getText()
    else:
        text = ""
    return text

def encode_blob(f):
    data = getattr(f, 'data', None)
    if data:
        return (getContentType(f), base64.b64encode(data))
    return (None, None)

def getContentType(i):
    for j in ['getContentType', 'contentType', 'content_type']:
        v = getattr(i,j,None)
        if v:
            if hasattr(v, '__call__'):
                return v()
            else:
                return v
    return None
            
        