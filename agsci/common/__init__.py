from zope.i18nmessageid import MessageFactory
import re

AgSciMessageFactory = MessageFactory('agsci.common')

def initialize(context):
    pass

#Ploneify
def ploneify(toPlone):
    ploneString = re.sub("[^A-Za-z0-9]+", "-", toPlone).lower()
    ploneString = re.sub("-$", "", ploneString)
    ploneString = re.sub("^-", "", ploneString)
    return ploneString