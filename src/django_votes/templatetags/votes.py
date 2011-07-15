from django import template
from django.template import Variable
from django.template.loader import render_to_string

register = template.Library()

from django_votes.models import VotesField

class UpDownVoteNode(template.Node):
    def __init__(self, object):
        self.object = object

    def render(self, context):
        v = Variable(self.object)
        object = v.resolve(context)

        model_name = '%s.%sVote' % (object._meta.app_label,
                                    object._meta.object_name,)

        dictionary = {'object': object,
                      'model_name': model_name}

        return render_to_string('django_votes/updownvote.html', dictionary, context_instance=context)

@register.tag
def updown_vote(parser, token):

    args = token.split_contents()

    object = args[1]

    return UpDownVoteNode(object)
