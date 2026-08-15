from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from .models import Floorplan


class FloorplanFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Floorplan
        fields = ['id', 'site', 'location']

    def search(self, queryset, name, value):
        # Floorplan extends NetBoxModel, which provides no description field, so the
        # search matches the name of whichever object the floorplan is assigned to.
        return queryset.filter(
            Q(site__name__icontains=value) | Q(location__name__icontains=value)
        )
