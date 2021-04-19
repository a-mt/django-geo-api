from django.db import models
from unidecode import unidecode
from .validators import validate_numeric

class Region(models.Model):
    code   = models.SlugField(max_length=2, primary_key=True, validators=[validate_numeric])
    nom    = models.CharField(max_length=32)

    def __str__(self):
        return self.code + ' ' + self.nom

class Departement(models.Model):
    code   = models.SlugField(max_length=3, primary_key=True, validators=[validate_numeric])
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    nom    = models.CharField(max_length=32)

    def __str__(self):
        return self.code + ' ' + self.nom

class Commune(models.Model):
    code        = models.SlugField(max_length=5, primary_key=True, validators=[validate_numeric])
    departement = models.ForeignKey(Departement, blank=True, null=True, on_delete=models.CASCADE)
    nom         = models.CharField(max_length=255)
    nom_norm    = models.CharField(max_length=255)
    population  = models.IntegerField()

    def __str__(self):
        return self.code + ' ' + self.nom

    @staticmethod
    def normalize(text):
        """
        Normalize the given text
        To be able to search on it efficiently (in DB)
        - replace accented letter with non-accented equivalent
        - replace hyphens with space
        - remove apostrophe
        - lowercase
        - add space at the beggining (to match the beggining of any word)

        :param string text
        :return string
        """
        if not text:
            return text

        text = unidecode(text)
        text = text.replace("-", " ")
        text = text.replace("'", "")
        return " " + text.lower().strip()

    def setCodesPostaux(self, codes, checkExisting=True):
        """
        :param set<string> codes
        :param boolean checkExisting - [True]
        """
        if checkExisting:
            for item in self.codepostal_set.all():
                if item.code in codes:
                    codes.remove(item.code)
                else:
                    item.delete()

        if codes:
            insert = []

            for cp in codes:
                insert.append(CodePostal(code=cp, commune=self))
            CodePostal.objects.bulk_create(insert, ignore_conflicts=True)

    def save(self, *args, **kwargs):
        self.nom_norm = self.normalize(self.nom)
        super().save(*args, **kwargs)

class CodePostal(models.Model):
    # Can be associated with several communes (ex 01330)
    id          = models.BigAutoField(auto_created=True, primary_key=True, verbose_name='ID')
    code        = models.CharField(max_length=5, db_index=True, validators=[validate_numeric])
    commune     = models.ForeignKey(Commune, on_delete=models.CASCADE)

    def __str__(self):
        return self.code

    class Meta:
        unique_together = (("code", "commune"),)

        verbose_name_plural = "Codes Postaux"