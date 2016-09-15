from plone.event.interfaces import IEvent
from Products.Five import BrowserView
from zope.interface import implements, Interface
from RestrictedPython.Utilities import same_type as _same_type
from RestrictedPython.Utilities import test as _test
from zope.component import getUtility, getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from agsci.leadimage.interfaces import ILeadImageMarker as ILeadImage
from agsci.common.content.behaviors.container import ITileFolder
from plone.app.search.browser import Search as _Search
from plone.app.search.browser import  quote_chars
from plone.memoize.instance import memoize
from Products.CMFPlone.browser.navtree import getNavigationRoot

try:
    from zope.app.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite

class IFolderView(Interface):
    pass

class FolderView(BrowserView):

    implements(IFolderView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.setHeaders()

    def setHeaders(self):

        # Prevent from being cached in proxy cache
        self.request.response.setHeader('Pragma', 'no-cache')
        self.request.response.setHeader('Cache-Control', 'private, no-cache, no-store')

    @property
    def show_date(self):
        return getattr(self.context, 'show_date', False)

    @property
    def show_description(self):
        return getattr(self.context, 'show_description', False)

    @property
    def show_image(self):
        return getattr(self.context, 'show_image', False)

    @property
    def show_read_more(self):
        return getattr(self.context, 'show_read_more', False)

    @property
    def _portal_state(self):
        return getMultiAdapter((self.context, self.request),
                                name=u'plone_portal_state')

    @property
    def _context_state(self):
        return getMultiAdapter((self.context, self.request),
                                name=u'plone_context_state')

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def anonymous(self):
        return self._portal_state.anonymous()

    # Providing Restricted Python "test" method
    def test(self, *args):
        return _test(*args)

    # Providing Restricted Python "test" same_type
    def same_type(self, arg1, *args):
        return _same_type(arg1, *args)

    # Does this item have a leadimage?
    def getItemHasLeadImage(self, item):
        return getattr(item, 'hasLeadImage', False)

    def getItemLeadImage(self, item, css_class='leadimage', scale='leadimage_folder'):
        if self.getItemHasLeadImage(item):
            return ILeadImage(item.getObject()).tag(css_class=css_class, scale=scale)
        return ''

    @property
    def hasTiledContents(self):
        return ITileFolder.providedBy(self.context)

    def getLayout(self):
        if hasattr(self.context, 'getLayout') and self.context.getLayout():
            return self.context.getLayout()
        return ''

    @property
    def use_view_action(self):
        return getToolByName(self.context, 'portal_properties').get("site_properties").getProperty('typesUseViewActionInListings', ())

    def isPublication(self, item):
        return False

    def getItemURL(self, item):

        item_type = item.portal_type

        if hasattr(item, 'getURL'):
            item_url = item.getURL()
        else:
            item_url = item.absolute_url()

        # Logged out
        if self.anonymous:
            if item_type in ['Image',] or \
               (item_type in ['File',] and \
                    (self.isPublication(item) or not self.getFileType(item))):
                return item_url + '/view'
            else:
                return item_url
        # Logged in
        else:
            if item_type in self.use_view_action:
                return item_url + '/view'
            else:
                return item_url

    def getIcon(self, item):

        if hasattr(item, 'getIcon'):
            if hasattr(item.getIcon, '__call__'):
                return item.getIcon()
            else:
                return item.getIcon

        return None

    def fileExtensionIcons(self):
        ms_data = ['xls', 'doc', 'ppt']

        data = {
            'xls' : u'Microsoft Excel',
            'ppt' : u'Microsoft PowerPoint',
            'publisher' : u'Microsoft Publisher',
            'doc' : u'Microsoft Word',
            'pdf' : u'PDF',
            'pdf_icon' : u'PDF',
            'text' : u'Plain Text',
            'txt' : u'Plain Text',
            'zip' : u'ZIP Archive',
        }

        for ms in ms_data:
            ms_type = data.get(ms, '')
            if ms_type:
                data['%sx' % ms] = ms_type

        return data

    def getFileType(self, item):

        icon = self.getIcon(item)

        if icon:
            icon = icon.split('.')[0]

        return self.fileExtensionIcons().get(icon, None)

    def getLinkType(self, url):

        if '.' in url:
            icon = url.strip().lower().split('.')[-1]
            return self.fileExtensionIcons().get(icon, None)

        return None

    def getItemSize(self, item):
        if hasattr(item, 'getObjSize'):
            if hasattr(item.getObjSize, '__call__'):
                return item.getObjSize()
            else:
                return item.getObjSize
        return None

    def getRemoteUrl(self, item):
        if hasattr(item, 'getRemoteUrl'):
            if hasattr(item.getRemoteUrl, '__call__'):
                return item.getRemoteUrl()
            else:
                return item.getRemoteUrl
        return None

    def getItemInfo(self, item):
        if item.portal_type in ['File',]:
            obj_size = self.getItemSize(item)
            file_type = self.getFileType(item)

            if file_type:
                if obj_size:
                    return u'%s, %s' % (file_type, obj_size)
                else:
                    return u'%s' % file_type

        elif item.portal_type in ['Link',]:
            url = self.getRemoteUrl(item)
            return self.getLinkType(url)

        return None

    def getItemClass(self, item):

        layout = self.getLayout()

        # Default classes for all views
        item_class = ['listItem',]

        # If "Hide items excluded from navigation" is checked on the folder,
        # and this item is excluded, apply the 'excludeFromNav' class
        if getattr(self.context.aq_base, 'hide_exclude_from_nav', False) and getattr(item, 'exclude_from_nav'):
            item_class.append('excludeFromNav')

        # A class if we're showing leadimages
        if self.show_image:
            item_class.append('listItemLeadImage')

            if self.getItemHasLeadImage(item):
                item_class.append('listItemHasLeadImage')
            else:
                item_class.append('listItemMissingLeadImage')

        # Per-layout classes
        if layout == 'folder_summary_view':

            # Class for rows in summary view
            item_class.append('listItemSummary')

        elif layout == 'folder_listing':

            if 'excludeFromNav' not in item_class:
                item_class.append('contenttype-%s' % item.Type.lower())

        if self.hasTiledContents:
            item_class.append('list-item-columns-%s' % self.getTileColumns)

        return " ".join(item_class)

    def getItemDate(self, item):
        item_date = getattr(item, 'effective', getattr(item, 'created', None))
        if item_date:
            return item_date.strftime('%B %d, %Y')
        return None

    @property
    def getTileColumns(self):
        return getattr(self.context, 'tile_folder_columns', '3')

    def isEvent(self, item):

        if getattr(item, 'getObject', False):
            item = item.getObject()

        return IEvent.providedBy(item)

    @memoize
    def getUserId(self):

        user_id = getattr(self, 'user_id', self.request.form.get('user_id', None))

        if user_id:
            return user_id

        user = self.portal_membership.getAuthenticatedMember()

        if user:
            return user.getId()

        return None

    def getFolderContents(self, contentFilter={}):

        if self.context.Type() in ['Topic', 'Collection']:
            return self.context.queryCatalog(batch=False, **contentFilter)

        return self.context.getFolderContents(contentFilter, batch=False)

    def getOwner(self, item=None):

        if item:

            owners = getattr(item, 'Owners', [])

            if owners:
                return owners[0]


        return None

    def getTruncatedDescription(self, item, max_chars=200):
        el = ' ...'

        description = item.Description

        if description:
            description = " ".join(description.strip().split())

            if len(description) > max_chars:
                description = description[:max_chars]
                _d = description.split()
                _d.pop()
                description = " ".join(_d) + el
                return description

        return ''

    def getIssues(self, item):
        issues = item.ContentIssues

        levels = ['High', 'Medium', 'Low']

        if issues:
            rv = []

            data = dict(zip(levels, issues))

            for k in levels:
                v = data.get(k)

                if isinstance(v, int) and v > 0:
                    rv.append(v*('<span class="error-check-%s"></span>' % k.lower()))
            if rv:
                return "".join(rv)

            return '<span class="error-check-none"></span>'

class Search(_Search):

    def filter_query(self, query):
        request = self.request

        catalog = getToolByName(self.context, 'portal_catalog')
        valid_indexes = tuple(catalog.indexes())
        valid_keys = self.valid_keys + valid_indexes

        text = query.get('SearchableText', None)
        if text is None:
            text = request.form.get('SearchableText', '')
        if not text:
            # Without text, must provide a meaningful non-empty search
            valid = set(valid_indexes).intersection(request.form.keys()) or \
                set(valid_indexes).intersection(query.keys())
            if not valid:
                return

        for k, v in request.form.items():
            # We're passing in bracketed [] parameters so the JSON works.
            # Strip these out to make them fit the catalog indexes.
            if k.endswith('[]'):
                k = k[:-2]
            if v and ((k in valid_keys) or k.startswith('facet.')):
                query[k] = v
        if text:
            query['SearchableText'] = quote_chars(text)

        # don't filter on created at all if we want all results
        created = query.get('created')
        if created:
            try:
                if created.get('query') and created['query'][0] <= EVER:
                    del query['created']
            except AttributeError:
                # created not a mapping
                del query['created']

        # respect `types_not_searched` setting
        types = query.get('portal_type', [])
        if 'query' in types:
            types = types['query']
        query['portal_type'] = self.filter_types(types)
        # respect effective/expiration date
        query['show_inactive'] = False
        # respect navigation root
        if 'path' not in query:
            query['path'] = getNavigationRoot(self.context)

        return query
