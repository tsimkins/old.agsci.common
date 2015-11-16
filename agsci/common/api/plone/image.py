from .. import BaseView
from agsci.common.utilities import encode_blob

class ImageView(BaseView):

    def getData(self, recursive=True):
        data = self.getBaseData()

        img_field = self.context.getFile()

        (img_mimetype, img_data) = encode_blob(img_field)

        if img_data:
            data['data'] = img_data
            data['mimetype'] = img_mimetype
        
        return data