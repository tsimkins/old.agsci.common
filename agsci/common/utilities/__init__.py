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

def encode_blob(f, show_data=True):
    data = getattr(f, 'data', None)
    if data:
        if show_data:
            return (getContentType(f), base64.b64encode(data))
        return (getContentType(f), '')
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
            
def increaseHeadingLevel(text):
    if '<h2' in text:
        for i in reversed(range(1,6)):
            from_header = "h%d" % i
            to_header = "h%d" % (i+1)
            text = text.replace("<%s" % from_header, "<%s" % to_header)
            text = text.replace("</%s" % from_header, "</%s" % to_header)
    return text
