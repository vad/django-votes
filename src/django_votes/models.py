from django.db import models
from django.db.models.base import ModelBase
from django.utils.translation import (ugettext_lazy as _, ugettext)

# Global list of all state models (mapping from name -> model class }
        
class VoteModel(models.Model):
    """
    Every model which needs votes should inherit this abstract model.
    """
    
    up_votes = models.IntegerField(default=0, verbose_name=_('up votes'))
    down_votes = models.IntegerField(default=0, verbose_name=_('down votes'))
        
    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')
        abstract = True
        
    def __unicode__(self):
        return 'Up votes: %s | Down votes: %s' % (self.up_votes, self.down_votes,)
    
    @classmethod
    def get_state_model_name(self):
        return '%s.%s' % (self._meta.app_label, self._meta.object_name)