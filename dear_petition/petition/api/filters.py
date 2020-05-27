from django_filters import rest_framework as filters

from dear_petition.petition.models import Contact


class ContactFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    category = filters.CharFilter(field_name="category", lookup_expr="icontains")

    class Meta:
        model = Contact
        fields = [
            "name",
            "category",
        ]
