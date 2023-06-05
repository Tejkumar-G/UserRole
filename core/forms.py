"""
Forms for the user app.
"""
from django import forms

CATEGORIES_LIST = [
    ('view', 'View'),
    ('create', 'Create'),
    ('edit', 'Edit'),
    ('delete', 'Delete'),
]
class StrategyAccesses(forms.Form):
    strategy_access = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=CATEGORIES_LIST,
    )
    def __init__(self, *args, **kwargs):
        super(StrategyAccesses, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.initial['strategy_access'] = eval(self.initial['strategy_access'])