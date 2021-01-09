from django_filters import FilterSet, DateFilter, OrderingFilter, DateRangeFilter, DateFromToRangeFilter

from ... import models
from ... import forms


class BasePortalFilter(FilterSet):
    """Filters on user requests portal"""

    from_date = DateFilter(
        field_name='slot__date',
        lookup_expr=('gt'),
        label='From',
        widget=forms.DateInput(
            attrs={
                'class': 'datepicker'
            }
        ),
    )
    to_date = DateFilter(
        field_name='slot__date',
        lookup_expr=('lt'),
        label='To',
        widget=forms.DateInput(
            attrs={
                'class': 'datepicker'
            }
        ),
    )

    order = OrderingFilter(
        fields=(
            ('slot', 'slot__date'),
        )
    )

    class Meta:
        model = models.Request
        fields = {
            'status': ['exact'],
            'instrument': ['exact'],
        }
