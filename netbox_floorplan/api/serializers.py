from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from ..models import Floorplan, FloorplanImage


class FloorplanImageSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_floorplan-api:floorplanimage-detail')

    class Meta:
        model = FloorplanImage
        fields = ['id', 'url', 'display', 'name', 'file', 'external_url', 'filename', 'comments', 'tags', 'custom_fields', 'created', 'last_updated']
        brief_fields = ['id', 'url', 'display', 'name', 'file', 'filename', 'external_url']


class FloorplanSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_floorplan-api:floorplan-detail')
    assigned_image = FloorplanImageSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = Floorplan
        fields = ['id', 'url', 'display', 'site', 'location', 'assigned_image',
                  'width', 'height', 'tags', 'custom_fields', 'created',
                  'last_updated', 'canvas', 'measurement_unit']
        # Without this, ?brief=1 returns every field, including the whole canvas.
        brief_fields = ['id', 'url', 'display']
