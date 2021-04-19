from django.core.management.base import BaseCommand
import requests
import json
from ...models import Region, Departement, Commune, CodePostal
import time

URL_REGIONS  = 'https://geo.api.gouv.fr/regions'
URL_DPTS     = 'https://geo.api.gouv.fr/departements'
URL_COMMUNES = 'https://geo.api.gouv.fr/communes?fields=nom,code,codesPostaux,codeDepartement,population'

class Command(BaseCommand):
    help = "Importe les villes/départements/régions depuis le site du gouvernement dans la BDD."

    def handle(self, *args, **options):
        self.importRegions()
        self.importDepartement()
        self.importCommune()

    def importRegions(self):
        """
        Request the list of regions from the government API
        And insert it in the Region table
        """
        self.stdout.write("Import regions")

        # Fetch list
        data = self._fetchJSON(URL_REGIONS)
        self.stdout.write("- %d items" % len(data))

        # Insert in db (in bulk)
        insert = []
        for item in data:
            insert.append(Region(code=item['code'], nom=item['nom']))

        Region.objects.bulk_create(insert, ignore_conflicts=True)

    def importDepartement(self):
        """
        Request the list of departments from the government API
        And insert it in the Departement table
        """
        self.stdout.write("Import departements")

        # Fetch list
        data = self._fetchJSON(URL_DPTS)
        self.stdout.write("- %d items" % len(data))

        # Insert in db (in bulk)
        insert = []
        for item in data:
            insert.append(Departement(code=item['code'], nom=item['nom'], region_id=item['codeRegion']))

        Departement.objects.bulk_create(insert, ignore_conflicts=True)

    def importCommune(self):
        """
        Request the list of communes from the government API
        And insert it in the Commune and CodePostal tables
        """
        self.stdout.write("Import communes")

        # Fetch list
        data = self._fetchJSON(URL_COMMUNES)
        n    = len(data)
        self.stdout.write("- %d items" % n)

        # Insert in db (in bulk)
        insert_com = []
        insert_cp  = []
        c          = 0
        total      = 0

        self.stdout.write("")
        for item in data:
            c     += 1
            total += 1

            insert_com.append(
                Commune(
                    code=item['code'],
                    nom=item['nom'],
                    nom_norm=Commune.normalize(item['nom']),
                    departement_id=item.get('codeDepartement', None),
                    population=item.get('population', 0)))

            for cp in item['codesPostaux']:
                insert_cp.append(CodePostal(code=cp, commune_id=item['code']))

            # Flush insert every 5000 items
            if c == 5000 or total == n:
                self.stdout.write("\r\x1b[A %d/%d" % (total, n))

                Commune.objects.bulk_create(insert_com, ignore_conflicts=True)
                CodePostal.objects.bulk_create(insert_cp, ignore_conflicts=True)

                insert_com = []
                insert_cp  = []
                c = 0

    @staticmethod
    def _fetchJSON(url):
        """
        :param string url
        :return mixed - Parsed JSON
        :raises requests.exceptions.HTTPError | requests.exceptions.ConnectionError | json.decoder.JSONDecodeError
        """
        response = requests.get(url)
        response.raise_for_status()

        txt = response.text.encode('utf-8').strip()
        return json.loads(txt)