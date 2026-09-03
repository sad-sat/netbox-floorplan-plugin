import django_tables2 as tables

from netbox.tables import NetBoxTable
from .models import Floorplan, FloorplanImage
from functools import cached_property

from dcim.models import Rack, Device


class FloorplanImageTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = FloorplanImage
        fields = (
            'pk',
            'id',
            'name',
            'file'
        )


class FloorplanTable(NetBoxTable):

    class Meta(NetBoxTable.Meta):
        model = Floorplan
        fields = ('pk', 'site', 'location',
                  'assigned_image', 'width', 'height')
        default_columns = ('pk', 'site', 'location',
                           'assigned_image', 'width', 'height')


class FloorplanRackTable(NetBoxTable):
    name = tables.LinkColumn()
    embedded = True

    role = tables.TemplateColumn(
        template_code="""
        {% if record.role %}
            <span class="badge" style="background-color: #{{ record.role.color }}; color: #fff;">{{ record.role.name }}</span>
        {% else %}
            <span class="text-muted">None</span>
        {% endif %}
        """,
        verbose_name="Role"
    )

    actions = tables.TemplateColumn(template_code="""
    <div class="btn-group" role="group">
        <button type="button" class="btn btn-sm btn-primary" onclick="add_custom_floorplan_rack('{{ record.id }}', '{{ record.name|escapejs }}', '{{ record.status }}', {% if record.outer_width %}{{ record.outer_width }}{% else %}600{% endif %}, {% if record.outer_depth %}{{ record.outer_depth }}{% else %}800{% endif %}, '{{ record.outer_unit|default:'mm' }}', '{{ record.role.name|default:''|escapejs }}', '{{ record.role.color|default:'2563eb' }}', '{{ record.u_height }}U')">
            <span class="mdi mdi-plus-box"></span> افزودن رک به نقشه
        </button>
    </div>
    """, orderable=False)

    @cached_property
    def htmx_url(self):
        return "/plugins/floorplan/floorplans/racks/"

    class Meta(NetBoxTable.Meta):
        model = Rack
        fields = ('pk', 'name', 'role', 'u_height')
        default_columns = ('pk', 'name', 'role', 'u_height')
        row_attrs = {
            'id': lambda record: 'object_rack_{}'.format(record.pk),
        }


class FloorplanDeviceTable(NetBoxTable):
    name = tables.LinkColumn()
    embedded = True

    role = tables.TemplateColumn(
        template_code="""
        {% if record.role %}
            <span class="badge" style="background-color: #{{ record.role.color }}; color: #fff;">{{ record.role.name }}</span>
        {% else %}
            <span class="text-muted">None</span>
        {% endif %}
        """,
        verbose_name="Role"
    )

    actions = tables.TemplateColumn(template_code="""
    <div class="btn-group" role="group">
        <button type="button" class="btn btn-sm btn-outline-primary" onclick="add_custom_floorplan_device('{{ record.id }}', '{{ record.name|escapejs }}', '{{ record.role.slug|default:'' }}', '{{ record.status }}', '{{ record.device_type.model|escapejs }}')">
            <span class="mdi mdi-plus-box"></span> افزودن به نقشه
        </button>
    </div>
    """, orderable=False)

    @cached_property
    def htmx_url(self):
        return "/plugins/floorplan/floorplans/devices/"

    class Meta(NetBoxTable.Meta):
        model = Device
        fields = ('pk', 'name', 'role', 'device_type')
        default_columns = ('pk', 'name', 'role', 'device_type')
        row_attrs = {
            'id': lambda record: 'object_device_{}'.format(record.pk),
        }
