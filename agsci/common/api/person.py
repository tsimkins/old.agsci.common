from . import BaseView
from ..content.person import IPerson, contact_fields, professional_fields, social_media_fields


class PersonView(BaseView):

    def getData(self):
        data = super(PersonView, self).getData()

        # Configure data nested data (easier to read this way!)
        structures = {
            'name' : ['first_name', 'middle_name', 'last_name', 'suffix'],   
            'social_media' : social_media_fields,
            'contact' : contact_fields,
            'professional' : professional_fields,
        }

        # Reverse lookup for all fields used in structures
        structured_fields = {}
        
        for (k,v) in structures.iteritems():
            for i in v:
                structured_fields[i] = k

        # Attach all custom fields from IPerson
        for i in IPerson.names():
        
            v = getattr(self.context, i, None)
            
            # Present biography as raw text
            if i in ('bio', ):
                v = v.raw

            # Handle values, if they exist
            if v:

                # Filter out blank list items
                if isinstance(v, (list, tuple,)):
                    v = [x for x in v if x]

                # Group some fields into data structures for XML readability
                if structured_fields.has_key(i):
                    s = structured_fields.get(i)
                    if not data.has_key(s):
                        data[s] = {}
                    if s == 'name':
                        data[s][i.replace('_name', '')] = v
                    else:
                        data[s][i] = v
                # If we're not structuring the datas
                else:
                    data[i] = v

        return data
