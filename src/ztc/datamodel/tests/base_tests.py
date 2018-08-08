from django.utils import timezone

from ztc.datamodel.choices import (
    JaNee, ObjectTypen, RolTypeOmschrijving, VertrouwelijkheidAanduiding
)

from .factories import (
    BesluitTypeFactory, CatalogusFactory, EigenschapFactory,
    InformatieObjectTypeFactory, ProductDienstFactory, ResultaatTypeFactory,
    RolTypeFactory, StatusTypeFactory, ZaakObjectTypeFactory, ZaakTypeFactory
)

# TODO: Catalogus and ResultaatTypeFacory are not used yet. Currently all other factories will indirectly create
# things that we dont want, like random Catalogus, more ZaakTypes etc etc

# TODO: for several fields the input from Haaglanden is too long. There are no To Do's on every line
# search for '[:' in this file, since I kept the original string but used string indexing to cut it of[:100]


class HaaglandenMixin(object):
    """
    Create instances for all models with realistic data.

    Use OD_Haaglanden_-Zaaktypecatalogus_v1.0-_20120210
    The case for 'Vergunningaanvraag regulier behandelen' (starting at page 95)
    """

    def setUp(self):
        #
        # kerngegevens
        #
        self.catalogus = CatalogusFactory.create(
            domein='DEMO',
            rsin='123456789',
        )

        self.product_dienst_vergunning_milieu = ProductDienstFactory.create(
            naam='Vergunning voor milieu'
        )
        self.zaaktype = ZaakTypeFactory.create(
            datum_begin_geldigheid=timezone.now().date(),
            zaaktype_omschrijving='Vergunningaanvraag regulier behandelen',
            doel='''Een besluit nemen op een aanvraag voor een vergunning, ontheffing of
                vergelijkbare beschikking op basis van een gedegen beoordeling van die
                aanvraag in een reguliere procedure.''',
            aanleiding='''De gemeente als bevoegd gezag heeft een aanvraag voor een
                omgevingsvergunning of milieuwetgeving-gerelateerde vergunning
                ontvangen.
                De gemeente heeft geconstateerd dat het een enkelvoudige aanvraag
                betreft met alleen een milieu-component of dat het een meervoudige
                aanvraag betreft met betrekking tot een milieuvergunningplichtige
                inrichting of -locatie en met een milieu-component (milieu-aspect is
                ‘zwaartepunt’) .
                De gemeente heeft de ODH gemandateerd om dergelijke aanvragen te
                behandelen. Zij draagt de ODH op om de ontvangen aanvraag te
                behandelen. De ODH heeft vastgesteld dat de aanvraag in een reguliere
                procedure behandeld kan worden.
                of:
                De provincie als bevoegd gezag heeft een aanvraag voor een
                omgevingsvergunning of milieuwetgevinggerelateerde vergunning
                ontvangen. Zij heeft de ODH gemandateerd om dergelijke aanvragen te
                behandelen. Zij draagt de ODH op om de ontvangen aanvraag te
                behandelen. De ODH heeft vastgesteld dat de aanvraag in een reguliere
                procedure behandeld kan worden.
                Ook is het mogelijk dat het bevoegd gezag of de ODH zelf (afhankelijk van
                de mandatering) het initiatief neemt voor het wijzigen of intrekken van
                een vergunning, veelal naar aanleiding van een constatering tijdens de
                uitvoering van een zaak van het type ‘Toezicht uitvoeren’.
                Zie ook bovenstaande figuren.'''[:1000],
            product_dienst=[self.product_dienst_vergunning_milieu],  # there are many more
            # TODO: is_deelzaaktype_van, Hoofdzaak (voor de ODH); deelzaak van de hoofdzaak ‘Behandelen
            # aanvraag vergunning’ bij de gemeente als bevoegd gezag
            handeling_initiator='Aanvragen',
            onderwerp='Milieu-gerelateerde vergunning',
            # TODO: behandeling door OD
            # TODO: generieke_aanduiding='',
            # TODO: bronzaaktype is FK on the model, doc has two Bronnen..
            toelichting='''Bij dit zaaktype draagt het bevoegd gezag de behandeling van de
                vergunningaanvraag op aan de ODH. De start van de zaakbehandeling
                verschilt naar gelang de aanvraag ontvangen is door de gemeente dan
                wel de provincie als bevoegd gezag. Aangezien de gemeente de front-
                office vormt (in het geval zij bevoegd gezag is), verzorgt zij haar deel van
                de intake, met name registratie van de zaak en uitdoen van de ontvangst-
                bevestiging. Daarna zet de ODH als back-office de behandeling voort. Als
                de provincie het bevoegd gezag is, verzorgt de ODH het front-office en
                voert de gehele intake uit, waaronder het uitdoen van de ontvangst-
                bevestiging, en zet daarna als back-office de behandeling voort.
                De ODH bepaalt tijdens haar intake, of zo spoedig mogelijk daarna, dat de
                aanvraag in een reguliere procedure behandeld kan worden. Als dit niet
                mogelijk is, betreft het een zaak van het type  ́Aanvraag vergunning
                uitgebreid behandelen ́.
                Het alternatief, waarbij het bevoegd gezag zelf de behandeling doet en de
                ODH om toetsing vraagt, betreft een zaak van het type ‘Toetsing
                uitvoeren’. Hiervan is sprake als het een meervoudige aanvraag betreft
                met een milieu-component die geen betrekking heeft op een milieu-
                inrichting of -locatie (‘het zwaartepunt ligt niet bij het milieu-aspect’).
                Enkel- en meervoudige aanvragen zonder milieucomponent worden
                geheel door het bevoegd gezag behandeld.
                Een uitzondering hierop vormen de aanvragen om zgn. BRIKS-
                vergunningen waarbij de provincie het bevoegd gezag is. De provincie
                draagt deze taak geheel over aan de ODH. Bij de behandeling van
                dergelijke aanvragen en ook bij de behandeling van BRIKS-onderdelen in
                meervoudige vergunningaanvragen (door de ODH) vraagt de ODH de
                gemeente om toetsing op de betreffende BRIKS-onderdelen.'''[:1000],

            #
            # Planning
            #
            doorlooptijd_behandeling=8,  # weken
            # servicenorm_behandeling=8,  # TODO 'afhankelijk van hetgeen aangevraagd is' should be an integer

            #
            # Publicatie (van indiening)
            #
            vertrouwelijkheidaanduiding=VertrouwelijkheidAanduiding.openbaar,
            publicatie_indicatie=JaNee.ja,  # Bij Wabo-aanvraag (reguliere procedure): ja
            publicatietekst='N.t.b.',

            #
            # Opschorting / aanhouding
            #
            opschorting_aanhouding_mogelijk=JaNee.ja,
            # toelichting: TODO: is in Haaglanden doc, not in the datamodel

            #
            # Verlenging
            #
            verlenging_mogelijk=JaNee.ja,
            # toelichting: TODO: is in Haaglanden doc, not in the datamodel

            maakt_deel_uit_van=self.catalogus,

            versiedatum=timezone.now().date()
        )

        #
        # kosten  # TODO
        #
        # tarief = ??
        # on-line_betalen = ??

        #
        # rollen en betrokkenen
        #
        # NOTE: Statusen are first in the Haaglanden document, but our datamodel has a reverse relation, so RolType goes first here
        # NOTE: statussen are 1, 2, 3, 4, 5, but there is no 5, only a 6
        self.rol_type_vergunnings_aanvrager = RolTypeFactory.create(
            roltypeomschrijving='Vergunningaanvrager',
            roltypeomschrijving_generiek=RolTypeOmschrijving.initiator,
            soort_betrokkene=['Aanvrager'],
            is_van=self.zaaktype,
        )
        self.rol_type_bevoegd_gezag = RolTypeFactory.create(
            roltypeomschrijving='Bevoegd gezag',
            roltypeomschrijving_generiek=RolTypeOmschrijving.belanghebbende,
            soort_betrokkene=['Bevoegd gezag'],
            is_van=self.zaaktype,
        )
        self.rol_type_zaakverantwoordelijke = RolTypeFactory.create(
            roltypeomschrijving='Zaakverantwoordelijke'[:20],  # TODO: this one has length 21, too long for AN20
            roltypeomschrijving_generiek=RolTypeOmschrijving.beslisser,  # FIXME: docs has 'verantwoordelijke' but is not an option in the specs  # FIXME: is not an option
            soort_betrokkene=['Teamleider afdeling', 'Toetsing & Vergunningen'],
            is_van=self.zaaktype,
        )
        self.rol_type_vergunningbehandelaar = RolTypeFactory.create(
            roltypeomschrijving='Vergunningbehandelaar'[:20],  # TODO: this one has length 21, too long for AN20
            roltypeomschrijving_generiek=RolTypeOmschrijving.behandelaar,  # FIXME: docs has 'uitvoerder' but is not an option in the specs
            soort_betrokkene=['Teamleider afdeling', 'Toetsing & Vergunningen'],
            is_van=self.zaaktype,
        )
        self.rol_type_juridisch_adviseur = RolTypeFactory.create(
            roltypeomschrijving='Juridisch adviseur',
            roltypeomschrijving_generiek=RolTypeOmschrijving.adviseur,  # FIXME: docs has 'uitvoerder' but is not an option in the specs
            soort_betrokkene=['Milieujurist'],
            is_van=self.zaaktype,
        )
        self.rol_type_documentair_ondersteuner = RolTypeFactory.create(
            roltypeomschrijving='Documentair ondersteuner'[:20],  # TODO: this one is longer then AN20
            roltypeomschrijving_generiek=RolTypeOmschrijving.klantcontacter,  # FIXME: docs has 'overig' but is not an option in the specs
            soort_betrokkene=['Medewerker Administratie'],
            is_van=self.zaaktype,
        )
        self.rol_type_procesondersteuner = RolTypeFactory.create(
            roltypeomschrijving='Procesondersteuner',
            roltypeomschrijving_generiek=RolTypeOmschrijving.klantcontacter,  # FIXME: docs has 'overig' but is not an option in the specs
            soort_betrokkene=['Medewerker Procedurele ondersteuning Milieu'],
            is_van=self.zaaktype,
        )

        #
        # Statusen
        #
        self.status_type_intake_afgerond = StatusTypeFactory.create(
            statustype_omschrijving='Intake afgerond',
            statustypevolgnummer=1,
            doorlooptijd_status=2,  # werkdagen
            informeren=JaNee.ja,
            toelichting='''Er wordt beoordeeld of de
                ontvangen aanvraag inderdaad in een reguliere
                procedure behandeld kan worden en of de
                aanvraag volledig is. Zo ja, dan wordt de zaak
                aangemaakt met daarbij de ontvangen
                documenten (aanvraag met bijlagen, opdracht tot
                behandeling van bevoegd gezag en eventueel
                ontvangstbevestiging) en wordt de
                zaakbehandelaar (medewerker of organisatie-
                onderdeel) bepaald (de startdatum is de datum
                van ontvangst door het bevoegd gezag, indien van
                toepassing). Als het bevoegd gezag de gemeente is,
                wordt zij geïnformeerd dat de intake heeft
                plaatsgevonden (d.m.v. een digitaal bericht). Als
                het bevoegd gezag de provincie is, wordt de
                ontvangstbevestiging aan de aanvrager gezonden,
                cc. naar provincie.
                Als de aanvraag niet in een reguliere procedure
                behandeld kan worden, wordt overgestapt naar
                een zaak van het type ‘Vergunningaanvraag
                uitgebreid behandelen’.'''[:999],
            roltypen=[
                self.rol_type_vergunnings_aanvrager,
                self.rol_type_bevoegd_gezag,
                self.rol_type_zaakverantwoordelijke,
                self.rol_type_documentair_ondersteuner,
                self.rol_type_procesondersteuner,
            ],
            is_van=self.zaaktype,
        )
        self.status_type_getoetst = StatusTypeFactory.create(
            statustype_omschrijving='Getoetst op indieningsvereisten',
            statustypevolgnummer=2,
            doorlooptijd_status=4,  # werkdagen
            informeren=JaNee.ja,
            toelichting='''De aanvraag wordt beoordeeld
                op de kwaliteit (aanvaardbaarheid) van de
                ontvangen documenten. Als de aanvraag niet
                kwalitatief voldoende wordt bevonden, wordt de
                aanvrager om aanvullende gegevens verzocht. De
                procedure wordt dan tijdelijk opgeschort. Als de
                kwaliteit onvoldoende blijft, wordt deze buiten
                behandeling gesteld cq. niet-ontvankelijk
                verklaard. Ook kan de aanvraag niet-ontvankelijk
                worden verklaard als bijvoorbeeld de aanvrager
                niet gemachtigd is.
                Tijdens de toets kan alsnog blijken dat de aanvraag
                in een uitgebreide procedure behandeld moet
                worden. Daartoe wordt overgegaan naar een zaak
                van het type ‘Aanvraag vergunning uitgebreid
                behandelen’.''',
            roltypen=[
                self.rol_type_vergunnings_aanvrager,
                self.rol_type_bevoegd_gezag,
                self.rol_type_zaakverantwoordelijke,
                self.rol_type_vergunningbehandelaar,
                self.rol_type_juridisch_adviseur,
                self.rol_type_procesondersteuner,
            ],
            is_van=self.zaaktype,
        )
        self.status_type_inhoudelijk_behandeld = StatusTypeFactory.create(
            statustype_omschrijving='Inhoudelijk behandeld',
            statustypevolgnummer=3,
            doorlooptijd_status=21,  # 3 weken
            informeren=JaNee.ja,
            toelichting='''De aanvraag wordt allereerst
                beoordeeld op de relevante wetgeving en
                informatie over de milieu-inrichting of -locatie.
                Waar nodig wordt in- en/of extern om een
                beoordeling (toetsing) gevraagd (bijvoorbeeld als
                er sprake is van BRIKS-onderdelen of van milieu-
                aspecten die binnen de provincie ondergebracht
                zijn bij één RUD). Dat kan leiden tot in- en/of
                externe deelzaken (‘Toetsing uitvoeren’). De status
                is bereikt met een eenduidig advies over het al dan
                niet verlenen van de vergunning.''',
            roltypen=[
                self.rol_type_vergunnings_aanvrager,
                self.rol_type_bevoegd_gezag,
                self.rol_type_zaakverantwoordelijke,
                self.rol_type_vergunningbehandelaar,
                self.rol_type_juridisch_adviseur,
                self.rol_type_procesondersteuner,
            ],
            is_van=self.zaaktype,
        )
        self.status_type_besluit_genomen = StatusTypeFactory.create(
            statustype_omschrijving='Besluit genomen',
            statustypevolgnummer=4,
            doorlooptijd_status=2,  # werkdagen
            informeren=JaNee.nee,
            toelichting='''Op basis van de aanvraag en het advies met betrekking tot de 
                vergunning wordt het definitieve besluit op- en vastgesteld.''',
            roltypen=[
                self.rol_type_bevoegd_gezag,
                self.rol_type_zaakverantwoordelijke,
                self.rol_type_vergunningbehandelaar,
                self.rol_type_juridisch_adviseur,
                self.rol_type_procesondersteuner,
            ],
            is_van=self.zaaktype,
        )
        self.status_type_producten_geleverd = StatusTypeFactory.create(
            statustype_omschrijving='Producten geleverd',
            statustypevolgnummer=6,  # NOTE: also refered to as '5' in de haaglanden doc
            doorlooptijd_status=3,  # werkdagen
            informeren=JaNee.nee,
            toelichting='''Het besluit wordt verzonden en gepubliceerd en het zaakdossier wordt afgesloten 
                en gearchiveerd (indien de provincie het bevoegd gezag is) dan wel ter archivering 
                overgedragen aan het bevoegd gezag (indien dat de gemeente is).''',
            roltypen=[
                self.rol_type_vergunnings_aanvrager,
                self.rol_type_bevoegd_gezag,
                self.rol_type_zaakverantwoordelijke,
                self.rol_type_documentair_ondersteuner,
                self.rol_type_procesondersteuner,
            ],
            is_van=self.zaaktype,
        )

        #
        # Objecten
        #
        # TODO: link these with StatusType.. but which one?
        self.zaakobjecttype_milieu = ZaakObjectTypeFactory.create(
            objecttype='Milieu-inrichting of -locatie',  # it's one that is not in the choices
            ander_objecttype=JaNee.ja,
            relatieomschrijving='De milieu-inrichting(en) en/of milieulocatie(s) waarop de zaak betrekking heeft.',
            # status_type=foreign key StatusType
            is_relevant_voor=self.zaaktype
        )
        self.zaakobjecttype_pand = ZaakObjectTypeFactory.create(
            objecttype=ObjectTypen.pand,
            ander_objecttype=JaNee.nee,
            relatieomschrijving='Het (de) pand(en) (in de BAG) waarin het deel van de milieu-inrichting '
                                'gevestigd is waarop de zaak betrekking heeft.'[:80],
            # status_type=foreign key StatusType
            is_relevant_voor=self.zaaktype
        )
        self.zaakobjecttype_verblijfsobject = ZaakObjectTypeFactory.create(
            objecttype=ObjectTypen.verblijfsobject,
            ander_objecttype=JaNee.nee,
            relatieomschrijving='Het (de) verblijfsobject(en) (in de BAG) met bijbehorend adres(sen) '
                                'waarin het deel van de milieu-inrichting gevestigd is waarop de zaak'
                                'betrekking heeft.'[:80],
            # status_type=foreign key StatusType
            is_relevant_voor=self.zaaktype
        )
        # NOTE: there are three more

        #
        # Eigenschappen
        #
        self.eigenschap_beoogde_producten = EigenschapFactory.create(
            eigenschapnaam='Beoogd(e) product(en)'[:20],
            # definitie='',
            toelichting='',
            # specificatie_van_eigenschap= fk EigenschapSpecificatie
            # referentie_naar_eigenschap= fk EigenschapReferentie
            # status_type=fk StatusType
            is_van=self.zaaktype,
        )
        self.eigenschap_aard_product = EigenschapFactory.create(
            eigenschapnaam='Aard product',
            toelichting='Nieuw / Verandering / Ambtshalve wijziging / Ontheffing / Intrekking',
            is_van=self.zaaktype,
        )

        #
        # Documenten
        #
        # NOTE: the haaglanden doc calls it documenten, I use this as InformatieObjectType
        self.document_vergunningaanvraag = InformatieObjectTypeFactory.create(
            informatieobjecttype_omschrijving='Vergunningsaanvraag',
            informatieobjecttype_omschrijving_generiek__informatieobjecttype_omschrijving_generiek='Aanvraag',
            informatieobjectcategorie='Aanvraag',
            informatieobjecttypetrefwoord=[],  # ArrayField
            vertrouwelijkheidaanduiding=VertrouwelijkheidAanduiding.zaakvertrouwelijk,
            model=[],  #ArrayField
            zaaktypes=[self.zaaktype],

            # TODO: following fields are in haaglanden doc but not in the datamodel
            # volgnummer=1  # is pk...
            # bron=ontvangen
            # verplicht=ja
            # TODO: link with Status 1
            maakt_deel_uit_van=self.catalogus,
        )
        self.document_ontvangstbevestiging = InformatieObjectTypeFactory.create(
            informatieobjecttype_omschrijving='Ontvangstbevestiging',
            informatieobjecttype_omschrijving_generiek__informatieobjecttype_omschrijving_generiek='Brief',
            informatieobjectcategorie='Brief',
            informatieobjecttypetrefwoord=[],  # ArrayField
            vertrouwelijkheidaanduiding=VertrouwelijkheidAanduiding.zaakvertrouwelijk,
            model=[],  #ArrayField
            zaaktypes=[self.zaaktype],

            # TODO: following fields are in haaglanden doc but not in the datamodel
            # volgnummer=1  # is pk...
            # bron=ontvangen of uitgaand
            # verplicht=ja
            # TODO: link with Status 1
            maakt_deel_uit_van=self.catalogus,
        )
        # there are 10+ more

        #
        # Resultaten en bewaartermijnen
        #
        self.resultaattype_verleend = ResultaatTypeFactory.create(
            resultaattypeomschrijving='Verleend',
            is_relevant_voor=self.zaaktype,
            bepaalt_afwijkend_archiefregime_van=None,
        )
        self.resultaattype_geweigerd = ResultaatTypeFactory.create(
            resultaattypeomschrijving='Geweigerd',
            is_relevant_voor=self.zaaktype,
            bepaalt_afwijkend_archiefregime_van=None,
        )
        self.resultaattype_niet_ontvankelijk = ResultaatTypeFactory.create(
            resultaattypeomschrijving='Niet ontvankelijk',
            is_relevant_voor=self.zaaktype,
            bepaalt_afwijkend_archiefregime_van=None,
        )
        self.resultaattype_niet_nodig = ResultaatTypeFactory.create(
            resultaattypeomschrijving='Niet nodig',
            is_relevant_voor=self.zaaktype,
            bepaalt_afwijkend_archiefregime_van=None,
        )
        self.resultaattype_ingetrokken = ResultaatTypeFactory.create(
            resultaattypeomschrijving='Ingetrokken',
            is_relevant_voor=self.zaaktype,
            bepaalt_afwijkend_archiefregime_van=None,
        )

        #
        # Besluiten
        #
        self.besluittype_niet_ontvankelijk = BesluitTypeFactory.create(
            besluittype_omschrijving='Niet-ontvankelijk-besluit',
            besluittype_omschrijving_generiek='Ontvankelijkheidsbesluit',
            # besluitcategorie='',
            reactietermijn=42,  # 6 weken
            publicatie_indicatie=JaNee.nee,  # required, but not in haaglanden
            # publicatietekst='',
            # publicatietermijn=-99
            toelichting='Besluit over het niet ontvankelijk verklaren (bijvoorbeeld omdat de aanvrager niet'
                        'gemachtigd is) van de aanvraag als ook het buiten behandeling stellen van de aanvraag',
            maakt_deel_uit_van=self.catalogus,
            # wordt_vastgelegd_in=models.ManyToManyField('datamodel.InformatieObjectType'
            is_resultaat_van=[self.resultaattype_niet_ontvankelijk, ],
            zaaktypes=[self.zaaktype],
        )
        self.besluittype_verlenging = BesluitTypeFactory.create(
            besluittype_omschrijving='Verlengingsbesluit',
            besluittype_omschrijving_generiek='Verlengingsbesluit',
            reactietermijn=42,  # 6 weken (of 15 weken)
            publicatie_indicatie=JaNee.ja,
            toelichting='De beslissing dat meer tijd genomen wordt voor de behandeling van de aanvraag.',
            maakt_deel_uit_van=self.catalogus,
            # Guess:
            is_resultaat_van=[self.resultaattype_verleend, ],
            zaaktypes=[self.zaaktype],
        )
        self.besluittype_op_aanvraag = BesluitTypeFactory.create(
            besluittype_omschrijving='Besluit op aanvraag',
            besluittype_omschrijving_generiek='Vergunning',
            reactietermijn=42,  # 6 weken (+1 dag voor Raad van State)
            publicatie_indicatie=JaNee.nee,  # required, but not in haaglanden
            maakt_deel_uit_van=self.catalogus,
            # Guess:
            is_resultaat_van=[self.resultaattype_verleend, ],
            zaaktypes=[self.zaaktype],
        )
        self.besluittype_aanhoudingsbesluit = BesluitTypeFactory.create(
            besluittype_omschrijving='Aanhoudingsbesluit',
            besluittype_omschrijving_generiek='',
            reactietermijn=42,  # 6 weken
            publicatie_indicatie=JaNee.nee,
            toelichting='',
            maakt_deel_uit_van=self.catalogus,
            # Guess:
            is_resultaat_van=[self.resultaattype_verleend, ],
            zaaktypes=[self.zaaktype],
        )

        #
        # Gerelateerde zaken
        #
        # TODO: 6 more zaaktypes

        #
        # Deelzaken
        #
        # TODO: 1 deelzaak

        #
        # Vervolgzaken
        #
        # TODO: 3 more zaaktypes


def create_haaglanden_test_data():
    """
    Just call the setUp from above test.

    Works on an empty database. If there is data already, there is a chance on duplicate key constraints
    """
    HaaglandenMixin().setUp()
