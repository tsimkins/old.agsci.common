from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements

classifications = ['Faculty', 'Staff', 'Educator', 'District Director',
                          'Assistant Director of Programs',]

states = ['PA', ]

from counties import counties

# Directory classifications for people
class ClassificationsVocabulary(object):

    implements(IVocabularyFactory)
    
    def __call__(self, context):

        return SimpleVocabulary(
            [SimpleTerm(x ,title=x) for x in classifications]
        )


ClassificationsVocabularyFactory = ClassificationsVocabulary()


# Directory States for people
class StatesVocabulary(object):

    implements(IVocabularyFactory)
    
    def __call__(self, context):

        return SimpleVocabulary(
            [SimpleTerm(x ,title=x) for x in states]
        )


StatesVocabularyFactory = StatesVocabulary()


# Directory Counties for people
class CountiesVocabulary(object):

    implements(IVocabularyFactory)
    
    def __call__(self, context):

        return SimpleVocabulary(
            [SimpleTerm(x ,title=x) for x in counties]
        )


CountiesVocabularyFactory = CountiesVocabulary()