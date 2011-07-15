from django import template
from django.template import Variable
from django.template.loader import render_to_string

register = template.Library()

from django_votes.models import VotesField
from django_votes.utils import get_vote_model

class UpDownVoteNode(template.Node):
    def __init__(self, object):
        self.object = object

    def render(self, context):
        v = Variable(self.object)
        object = v.resolve(context)

        model_name = '%s.%sVote' % (object._meta.app_label,
                                    object._meta.object_name,)

        model = get_vote_model(model_name)

        total_votes = model.objects.filter(object__id=object.id).count()

        up_votes = model.objects.filter(object__id=object.id,
                                        value=1).count()
        down_votes = model.objects.filter(object__id=object.id,
                                        value= -1).count()

        up_pct = (float(up_votes) / float(total_votes) if total_votes else 0) * 98
        down_pct = (float(down_votes) / float(total_votes) if total_votes else 0) * 98

        dictionary = {'object': object,
                      'model_name': model_name,
                      'up_pct': up_pct,
                      'down_pct': down_pct,
                      'up_votes': up_votes,
                      'down_votes': down_votes,
                      'total_votes': total_votes}

        result = render_to_string('django_votes/updownvote.html', dictionary, context_instance=context)
        print result
        return result

@register.tag
def updown_vote(parser, token):

    args = token.split_contents()

    object = args[1]

    return UpDownVoteNode(object)
