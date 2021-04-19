from django import forms
from django.core.exceptions import ValidationError
from .models import Commune, CodePostal

class CommuneForm(forms.ModelForm):
    codesPostaux = forms.CharField(
                        required=False,
                        label='Codes postaux',
                        help_text='Liste séparée par des virgules')

    class Meta:
        model  = Commune
        fields = ('code', 'nom', 'population', 'departement', 'codesPostaux')


    def __init__(self, *args, **kwargs):
        """
        Tweak the view if we're editing an instance
        """
        super().__init__(*args, **kwargs)

        # We're editing an instance
        instance = getattr(self, 'instance', None)
        if instance and instance.code:
            self.fields['code'].disabled = True
            self.initial['codesPostaux'] = ",".join(sorted([str(x) for x in instance.codepostal_set.all()]))

    def clean_codesPostaux(self):
        """
        :raise ValidationError
        :return list
        """
        value = self.cleaned_data['codesPostaux'].strip()

        if not value:
            return value

        # Validate the codes
        f = CodePostal._meta.get_field('code')

        data = []
        for txt in value.split(","):
            if txt != "":
                f.clean(txt, None) # Raises ValidationError if invalid
                data.append(txt)

        return data

    def as_table(self):
        """
        Return this form rendered as HTML <tr>s
        -- excluding the <table></table>."
        """
        return self._html_output(
            normal_row='<tr%(html_class_attr)s><th>%(label)s</th><td>%(field)s%(help_text)s%(errors)s</td></tr>',
            error_row='<tr><td colspan="2">%s</td></tr>',
            row_ender='</td></tr>',
            help_text_html='<br><span class="helptext">%s</span>',
            errors_on_separate_row=False,
        )