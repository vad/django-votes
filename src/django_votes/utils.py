from django_votes.models import _vote_models

def get_vote_model(model_name):
    vote_model = filter(lambda m: m.get_model_name() == model_name, _vote_models)

    if len(vote_model) == 0:
        raise Exception('No vote models named "%s" found' % model_name)
    else:
        return vote_model[0]
