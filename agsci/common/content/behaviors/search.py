from agsci.common import AgSciMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import provider
from plone.autoform import directives as form
from zope import schema
from zope.schema.interfaces import IContextAwareDefaultFactory
from ..vocabulary import getTypes
from agsci.atlas.content import metadata_content_types

@provider(IContextAwareDefaultFactory)
def defaultSearchTypes(context):
    types = ["Article", "Webinar Recording"]

    return list(set(types) & set(getTypes(context)))

@provider(IContextAwareDefaultFactory)
def defaultMatchAttributes(context):

    if context.Type() in metadata_content_types:
        return context.Type()
    else:
        return None

@provider(IFormFieldProvider)
class ILocalSearch(model.Schema):

    model.fieldset(
        'search_settings',
        label=_(u'Search Settings'),
        fields=['enable_localsearch', 'search_types', 'match_attributes'],
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

    match_attributes = schema.Choice(
        title=_(u"Match Attributes"),
        description=_(u""),
        vocabulary="agsci.common.MatchAttributes",
        defaultFactory=defaultMatchAttributes,
        required=False,
    )
