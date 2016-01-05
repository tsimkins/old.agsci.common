from agsci.common import AgSciMessageFactory as _
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import provider, implementer

# Set up fields for re-use in API output

contact_fields = ['email_address', 'venue', 'office_address', 'office_city', 'office_state', 'office_zip_code', 'office_phone', 'fax_number', ]

professional_fields = ['classifications', 'counties', 'job_titles', 'biography', 'areas_expertise', 'education', ]

social_media_fields = ['twitter_url', 'facebook_url', 'linkedin_url', 'google_plus_url', ]

@provider(IFormFieldProvider)
class IPerson(model.Schema):

    # Fieldsets

    model.fieldset(
        'contact',
        label=_(u'Contact Information'),
        fields=contact_fields,
    )
    
    model.fieldset(
        'professional',
        label=_(u'Professional Information'),
        fields=professional_fields,
    )

    model.fieldset(
        'social-media',
        label=_(u'Social Media'),
        fields=social_media_fields,
    )

    # Fields

    user_id = schema.TextLine(
        title=_(u"Penn State Username"),
        description=_(u"Of format 'xyz123'"),
        required=True,
    )

    first_name = schema.TextLine(
        title=_(u"First Name"),
        required=True,
    )

    middle_name = schema.TextLine(
        title=_(u"Middle Name"),
        required=False,
    )

    last_name = schema.TextLine(
        title=_(u"Last Name"),
        required=True,
    )

    suffix = schema.TextLine(
        title=_(u"Suffix"),
        required=False,
    )

    classifications = schema.List(
        title=_(u"Classifications"),
        required=True,
        value_type=schema.Choice(vocabulary="agsci.common.person.classifications"),
    )

    email_address = schema.TextLine(
        title=_(u"Email"),
        required=True,
    )

    venue = schema.TextLine(
        title=_(u"Venue/Building Name"),
        required=False,
    )

    office_address = schema.Text(
        title=_(u"Office Address"),
        required=False,
    )

    office_city = schema.TextLine(
        title=_(u"Office City"),
        required=False,
    )

    office_state = schema.Choice(
        title=_(u"Office State"),
        vocabulary="agsci.common.person.states",
        required=False,
    )

    office_zip_code = schema.TextLine(
        title=_(u"Office ZIP Code"),
        required=False,
    )

    office_phone = schema.TextLine(
        title=_(u"Office Phone"),
        required=False,
    )

    fax_number = schema.TextLine(
        title=_(u"Fax Number"),
        required=False,
    )

    job_titles = schema.List(
        title=_(u"Job Titles"),
        value_type=schema.TextLine(required=True),
        required=True,
    )

    biography = RichText(
        title=_(u"Biography"),
        required=False,
    )

    education = schema.List(
        title=_(u"Education"),
        value_type=schema.TextLine(required=True),
        required=False,
    )

    counties = schema.List(
        title=_(u"Counties"),
        value_type=schema.Choice(vocabulary="agsci.common.person.counties"),
        required=False,
    )

    areas_expertise = schema.List(
        title=_(u"Areas of Expertise"),
        value_type=schema.TextLine(required=True),
        required=False,
    )

    twitter_url = schema.TextLine(
        title=_(u"Twitter URL"),
        required=False,
    )

    facebook_url = schema.TextLine(
        title=_(u"Facebook URL"),
        required=False,
    )

    linkedin_url = schema.TextLine(
        title=_(u"LinkedIn URL"),
        required=False,
    )

    google_plus_url = schema.TextLine(
        title=_(u"Google+ URL"),
        required=False,
    )

# Calculate "Title" as person name
# Based on http://davidjb.com/blog/2010/04/plone-and-dexterity-working-with-computed-fields/
from plone.dexterity.content import Item
from zope.interface import implements
from plone.app.content.interfaces import INameFromTitle

class Person(Item):

    @property
    def title(self):

        fields = ['first_name', 'middle_name', 'last_name']
        names = [getattr(self, x, '') for x in fields]
    
        v = " ".join([x.strip() for x in names if x])
        
        if getattr(self, 'suffix', ''):
            v = "%s, %s" % (v, self.suffix.strip())

        return v

    def setTitle(self, value):
        return


class ITitleFromPersonUserId(INameFromTitle):
    def title():
        """Return a processed title"""

class TitleFromPersonUserId(object):
    implements(ITitleFromPersonUserId)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.user_id