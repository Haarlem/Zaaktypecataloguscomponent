from datetime import date

import factory

from ...models import (
    InformatieObjectType, InformatieObjectTypeOmschrijvingGeneriek
)
from .catalogus import CatalogusFactory
from .relatieklassen import ZaakInformatieobjectTypeFactory


class InformatieObjectTypeOmschrijvingGeneriekFactory(factory.django.DjangoModelFactory):
    datum_begin_geldigheid = date(2018, 1, 1)

    class Meta:
        model = InformatieObjectTypeOmschrijvingGeneriek


class InformatieObjectTypeFactory(factory.django.DjangoModelFactory):
    informatieobjecttype_omschrijving = factory.Sequence(lambda n: 'Informatie object type {}'.format(n))
    informatieobjecttype_omschrijving_generiek = factory.SubFactory(
        InformatieObjectTypeOmschrijvingGeneriekFactory,
        # datum_begin_geldigheid=factory.SelfAttribute('.datum_begin_geldigheid')
    )
    informatieobjecttypetrefwoord = []  # ArrayField has blank=True but not null=True
    model = []  # ArrayField has blank=True but not null=True
    informatieobjectcategorie = 'informatieobjectcategorie'
    maakt_deel_uit_van = factory.SubFactory(CatalogusFactory)
    zaaktypes = factory.RelatedFactory(ZaakInformatieobjectTypeFactory, 'informatie_object_type')
    datum_begin_geldigheid = date(2018, 1, 1)

    class Meta:
        model = InformatieObjectType
