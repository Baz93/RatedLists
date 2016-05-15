from decimal import Decimal
from django.core.management.base import BaseCommand
from ...models import Item, RatersGroup, Score


def update_score(score):
    multiplier = Decimal(0.5)
    stabilizer = (1 + multiplier) / (2 * multiplier)

    votes = score.votes()
    sum_e = 0
    sum_p = 0
    for vote in votes:
        other_item = vote.second
        additive = vote.difference * stabilizer
        weight = vote.weight
        if other_item == score.item:
            other_item = vote.first
            additive = -additive
        sum_e += (Score.get_or_create(score.group, other_item).value + additive) * weight
        sum_p += weight

    score.value = sum_e / sum_p * multiplier
    score.save()


def update(raters_group):
    for score in raters_group.scores.all():
        score.delete()
    votes = raters_group.relevant_votes()
    items = (
        Item.objects.filter(votes_as_first__in=votes) |
        Item.objects.filter(votes_as_second__in=votes)
    ).distinct()
    delta = 1
    while delta > 0.00001:
        delta = 0
        for item in items.iterator():
            score = Score.get_or_create(raters_group, item)
            prev_val = score.value
            update_score(score)
            new_val = score.value
            delta = max(delta, abs(prev_val - new_val))


class Command(BaseCommand):
    help = 'Run a background process updating scores'

    def handle(self, *args, **options):
        while True:
            for group in RatersGroup.objects.iterator():
                update(group)