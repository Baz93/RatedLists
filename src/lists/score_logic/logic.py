def update(raters_group, score_cls):
    for vote in raters_group.relevant_votes().all():
        instance = score_cls.get_or_create(raters_group, vote.first)
        instance.value = 0
        instance.save()
        instance = score_cls.get_or_create(raters_group, vote.second)
        instance.value = 0
        instance.save()
    for vote in raters_group.relevant_votes().all():
        instance = score_cls.get_or_create(raters_group, vote.first)
        instance.value += vote.difference * vote.weight
        instance.save()
        instance = score_cls.get_or_create(raters_group, vote.second)
        instance.value -= vote.difference * vote.weight
        instance.save()