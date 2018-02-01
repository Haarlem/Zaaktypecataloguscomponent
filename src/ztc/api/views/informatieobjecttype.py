from rest_framework import viewsets

from ...datamodel.models import InformatieObjectType
from ..serializers import InformatieObjectTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin


class InformatieObjectTypeViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    De verzameling van ZAAKTYPEn - incl. daarvoor relevante objecttypen - voor een Domein die als één geheel beheerd
    wordt.

    list:
    Een verzameling van CATALOGUSsen.
    """
    queryset = InformatieObjectType.objects.all()
    serializer_class = InformatieObjectTypeSerializer