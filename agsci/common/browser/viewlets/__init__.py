from plone.app.layout.viewlets import ViewletBase
from plone.app.layout.viewlets.content import DocumentBylineViewlet as _DocumentBylineViewlet
from agsci.atlas.content import IAtlasProduct,  IArticleDexterityContent, IArticleDexterityContainedContent

from ..views import FolderView

class LocalSearchViewlet(ViewletBase, FolderView):

    def search_enabled(self):
        return getattr(self.context, 'enable_localsearch', False)

    def search_types(self):
        return getattr(self.context, 'search_types', [])

class DocumentBylineViewlet(_DocumentBylineViewlet):

    def show_history(self):

        is_atlas_content = False

        for i in [IAtlasProduct,  IArticleDexterityContent, IArticleDexterityContainedContent]:
            if i.providedBy(self.context):
                is_atlas_content = True
                break

        if is_atlas_content:
            return super(DocumentBylineViewlet, self).show_history()

        return False