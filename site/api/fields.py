from rest_framework import serializers

class InputCommaSeparatedField(serializers.ManyRelatedField):
    def __init__(self, *args, **kwargs):
        self.separator = kwargs.pop('separator', ',')

        # We're concatenating in the HTML only, not JSON
        if 'style' not in kwargs:
            kwargs['style'] = {
                'base_template': 'input_many.html',
                'template_pack': 'api'
            }
        kwargs['style']['separator'] = self.separator

        super().__init__(*args, **kwargs)

    def to_internal_value(self, values):

        # Expand comma-separated values
        data = []
        for txt in values:
            if txt:
                data.extend([x.strip() for x in txt.strip().split(self.separator)])

        print(data)
        if not self.allow_empty and len(data) == 0:
            self.fail('empty')

        return [
            self.child_relation.to_internal_value(item)
            for item in data
        ]