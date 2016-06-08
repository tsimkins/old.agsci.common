from agsci.common import AgSciMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import provider
from plone.autoform import directives as form
from zope import schema
from zope.schema.interfaces import IContextAwareDefaultFactory
from ..vocabulary import getTypes

@provider(IContextAwareDefaultFactory)
def defaultSearchTypes(context):
    types = ["Article", "Webinar Recording"]

    return list(set(types) & set(getTypes(context)))

@provider(IFormFieldProvider)
class ILocalSearch(model.Schema):

    model.fieldset(
        'search_settings',
        label=_(u'Search Settings'),
        fields=['enable_localsearch', 'search_types'],
    )

    enable_localsearch = schema.Bool(
        title=_(u"Enable Local Search"),
        description=_(u""),
        default=False,
    )
    
    search_types = schema.List(
        title=_(u"Search Types"),
        description=_(u""),
        value_type=schema.Choice(vocabulary="agsci.common.SearchTypes"),
        defaultFactory=defaultSearchTypes,
    )