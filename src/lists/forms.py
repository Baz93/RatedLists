from django import forms
from .models import Vote, Item, User, List


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = [
            'first',
            'second',
            'difference',
            'weight',
        ]

    def __init__(self, list_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first'].queryset = Item.objects.filter(list__id=list_id)
        self.fields['second'].queryset = Item.objects.filter(list__id=list_id)


class RatersGroupForm(forms.Form):
    all_except = forms.BooleanField(label='All except', required=False)
    members = forms.ModelMultipleChoiceField(queryset=None, label='Raters')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].queryset = User.objects.all()


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'title',
        ]


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = [
            'title',
        ]

