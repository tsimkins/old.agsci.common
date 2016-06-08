from plone.app.layout.viewlets import ViewletBase 
from ..views import FolderView

class LocalSearchViewlet(ViewletBase, FolderView):

    def search_enabled(self):
        return getattr(self.context, 'enable_localsearch', False)

    def search_types(self):
        return getattr(self.context, 'search_types', [])