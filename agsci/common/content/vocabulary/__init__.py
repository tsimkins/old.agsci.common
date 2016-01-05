from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.CMFCore.utils import getToolByName
from zope.interface import directlyProvides
from zope.interface import implements
from agsci.atlas.content import metadata_content_types

# Number of columns in tile folder view

class TileFolderColumnsVocabulary(object):

    implements(IVocabularyFactory)
    
    def __call__(self, context):

        return SimpleVocabulary(
            [SimpleTerm('%d'% x ,title='%d'% x) for x in range(1,6)]
        )


TileFolderColumnsVocabularyFactory = TileFolderColumnsVocabulary()


# Restrict search by object type

def getTypes(context):

    portal_catalog = getToolByName(context, 'portal_catalog')

    return portal_catalog.uniqueValuesFor('Type')

class SearchTypesVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context):

        return SimpleVocabulary(
            [SimpleTerm(x, title=x) for x in getTypes(context)]
        )
    

SearchTypesVocabularyFactory = SearchTypesVocabulary()


# Attributes to match on local search
class MatchAttributesVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context):

        return SimpleVocabulary(
            [SimpleTerm(x, title=x) for x in metadata_content_types]
        )

MatchAttributesVocabularyFactory = MatchAttributesVocabulary()