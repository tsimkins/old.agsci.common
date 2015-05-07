from Products.CMFCore.utils import getToolByName
from collective.elasticindex.changes import get_uid, sortable_string, get_security
import urlparse
from Acquisition import aq_base
import Missing
from BeautifulSoup import BeautifulSoup
from agsci.leadimage import hasLeadImage
from collective.elasticindex.utils import connect, DOCUMENT_MAPPING, \
    ANALYZED_STRING_MAPPING, STORED_STRING_MAPPING, STRING_MAPPING, DATE_MAPPING, INT_MAPPING

# updated create_index method
def create_index(settings):
    import pdb; pdb.set_trace()
    connection = connect(settings.server_urls)
    connection.indices.create_index_if_missing(settings.index_name)
    connection.indices.put_mapping(
        'document', {'properties' : DOCUMENT_MAPPING}, [settings.index_name])

# updated get_data method
def get_data(content, security=False, domain=None):
    """Return data to index in ES.
    """
    uid = get_uid(content)
    if not uid:
        return None, None
    title = content.Title()
    try:
        text = content.SearchableText()
    except:
        text = title
    url = content.absolute_url()
    if domain:
        parts = urlparse.urlparse(url)
        url = urlparse.urlunparse((parts[0], domain) + parts[2:])

    data = {'title': title,
            'metaType': content.portal_type,
            'sortableTitle': sortable_string(title),
            'description': content.Description(),
            'subject': content.Subject(),
            'contributors': content.Contributors(),
            'url': url,
            'author': content.Creator(),
            'content': text}

    data.update(getCatalogData(content))

    if security:
        data['authorizedUsers'] = get_security(content)

    if hasattr(aq_base(content), 'pub_date_year'):
        data['publishedYear'] = getattr(content, 'pub_date_year')

    created = content.created()
    if created is not (None, 'None'):
        data['created'] = created.strftime('%Y-%m-%dT%H:%M:%S')

    modified = content.modified()
    if modified is not (None, 'None'):
        data['modified'] = modified.strftime('%Y-%m-%dT%H:%M:%S')

    return uid, data

# Methods to grab metadata from catalog

# Duplicated or extraneous indexes
excluded_indexes = [
    'Title',
    'meta_type',
    'sortable_title',
    'Description',
    'Subject',
    'commentators',
    'author_name',
    'listCreators',
    'allowedRolesAndUsers',
    'last_comment_date',
    'cmf_uid',
    'CreationDate',
    'Creator',
    'Date',
    'EffectiveDate',
    'ExpirationDate',
    'ModificationDate',
    'SearchableText',
    'effectiveRange',
    'exclude_from_nav',
    'getObjPositionInParent',
    'getRawRelatedItems',
    'getRemoteUrl',
    'getId',
    'UID',
    'id',
    'in_reply_to',
    'in_response_to',
    'is_default_page',
    'is_folderish',
    'total_comments',
    'path',
    'portal_type',
]

def getCatalogData(context):

    # Start with getting the indexed data
    data = getIndexDataFor(context)
    
    # Metadata trumps indexed data
    data.update(getMetaDataFor(context))

    # Remove excluded indexes
    for i in excluded_indexes:
        if data.has_key(i):
            del data[i]

    # Remove empty indexes and convert dates to formated string
    del_keys = []

    for (k,v) in data.iteritems():
        if not bool(v):
            del_keys.append(k)
        elif hasattr(v, 'strftime') and hasattr(v.strftime, '__call__'):
            data[k] = v.strftime('%Y-%m-%dT%H:%M:%S')

    for k in del_keys:
        del data[k]

    data["leadImageUrl"] = ''

    if hasLeadImage(context)():
        try:
            images_view = context.restrictedTraverse('@@images')
        except AttributeError:
            pass
        else:
        
            img_tag = images_view.tag('leadimage', scale='leadimage_folder')
            
            if img_tag:
                soup = BeautifulSoup(img_tag)
            
                data["leadImageUrl"] = soup.find('img').get('src', '')

    return data

def portal_catalog(context):
    return getToolByName(context, 'portal_catalog')

def getMetaDataFor(context):
    try:
        return portal_catalog(context).getMetadataForUID("/".join(context.getPhysicalPath()))
    except KeyError:
        return {}

def getIndexDataFor(context):
    try:
        return portal_catalog(context).getIndexDataForUID("/".join(context.getPhysicalPath()))
    except KeyError:
        return {}
 