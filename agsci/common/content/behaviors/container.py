from agsci.common import AgSciMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import provider
from plone.autoform import directives as form
from zope import schema
from z3c.form.interfaces import IEditForm, IAddForm

@provider(IFormFieldProvider)
class IFolderFields(model.Schema):

    model.fieldset(
        'settings',
        label=_(u'Settings'),
        fields=['show_date', 'show_image', 'show_read_more', 'show_description', 'listing_after_text', 'two_column'],
    )

    show_image = schema.Bool(
        title=_(u"Show Lead Image in folder listing"),
        description=_(u"This will show the lead image for each item in the folder listing."),
        default=False,
    )
    
    show_date = schema.Bool(
        title=_(u"Show date"),
        description=_(u"This will show the publication date (or, creation date) for each item in the folder listing."),
        default=False,
    )
    
    show_description = schema.Bool(
        title=_(u"Show description for contents"),
        description=_(u"This will show the description for the items in the folder listing"),
        default=True,
    )
    
    show_read_more = schema.Bool(
        title=_(u"Show \"Read More...\""),
        description=_(u"This will show the \"Read More...\" for each item in the folder listing."),
        default=False,
    )
    
    listing_after_text = schema.Bool(
        title=_(u"Show text after folder contents"),
        description=_(u"This will show the Body Text field after the folder contents instead of before."),
        default=False,
    )

    two_column = schema.Bool(
        title=_(u"Two column display"),
        description=_(u"This will automatically display the contents of the folder in two columns.  This is best for short titles/descriptions."),
        default=False,
    )

@provider(IFormFieldProvider)
class ITileFolder(model.Schema):

    model.fieldset(
        'settings',
        label=_(u'Settings'),
        fields=['tile_folder_columns'],
    )

    tile_folder_columns = schema.Choice(
        title=_(u"Tile Folder Columns"),
        description=_(u""),
        vocabulary="agsci.common.TileFolderColumns",
        default='3',
    )