"""
Forms for the user app.
"""
from django import forms

from core.models import User

CATEGORIES_LIST = [
    ('view', 'View'),
    ('create', 'Create'),
    ('edit', 'Edit'),
    ('delete', 'Delete'),
]
class StrategyAccessForm(forms.ModelForm):
    strategy_access = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=CATEGORIES_LIST,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.initial['strategy_access'] = eval(self.initial['strategy_access'])

    class Meta:
        model = User
        fields = '__all__'

