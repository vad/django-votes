from django.db import models
from django.db.models.base import ModelBase
from django.utils.translation import (ugettext_lazy as _, ugettext)
from django.contrib.auth.models import User

class VotesField(object):
    """
    Usage:

    class MyModel(models.Model):
        ...
        Votes = VotesField()
    """
    def __init__(self):
        pass

    def contribute_to_class(self, cls, name):
        self._name = name
        models.signals.class_prepared.connect(self.finalize, sender=cls)

    def finalize(self, sender, **kwargs):
        descriptor = self._create_Vote_model(sender)
        setattr(sender, self._name, descriptor)

    def _create_Vote_model(self, model):
        class VoteMeta(ModelBase):
            """
            Make every Vote model have their own name/table.
            """
            def __new__(c, name, bases, attrs):
                # Rename class
                name = '%sVote' % model._meta.object_name

                # This attribute is required for a model to function properly in Django.
                attrs['__module__'] = model.__module__

                return ModelBase.__new__(c, name, bases, attrs)

        rel_nm_user = '%s_votes' % model._meta.object_name.lower()

        class Vote(models.Model):
            """
            Vote model
            """
            __metaclass__ = VoteMeta

            voter = models.ForeignKey(User, verbose_name=_('voter'))
            value = models.IntegerField(default=1, verbose_name=_('value'))            
            date = models.DateField(db_index=True, verbose_name=_('voted on'))
            object = models.ForeignKey(model, verbose_name=_('object'))
            
            class Meta:
                ordering = ('date',)
                verbose_name = _('Vote')
                verbose_name_plural = _('Votes')

            def __unicode__(self):
                values = {'voter': self.voter.username,
                          'like': _('likes') if self.value > 0 else _('hates'),
                          'object': self.object}
                
                return "%(voter)s %(like)s %(object)s" % values


        class VoteFieldDescriptor(object):
            def __init__(self):
                pass

            def __get__(self, obj, objtype):
                """
                Return the related manager for the Votes.
                """
                if obj:
                    return getattr(obj, ('%svote_set' % model._meta.object_name).lower())
                else:
                    return Vote.objects

        return VoteFieldDescriptor()
        
class VoteModel(models.Model):
    """
    Every model which needs votes should inherit this abstract model.
    """
    
    votes = VotesField()
        
    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')
        abstract = True
            
    @classmethod
    def get_state_model_name(self):
        return '%s.%s' % (self._meta.app_label, self._meta.object_name)