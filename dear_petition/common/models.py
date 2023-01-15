from itertools import chain


class PrintableModelMixin(object):
    """
    Mixin used by Models to implement repr().  It includes all fields in the model including uneditable fields
    and many to many relationships. If desired, fields can be excluded from output.

    See discussion at:
    https://stackoverflow.com/questions/21925671/convert-django-model-object-to-dict-with-all-of-the-fields-intact
    """

    def __repr__(self, exclude_fields=[]):
        """
        Example output:
        {'id': 1, 'created': datetime.datetime(2022, 12, 18, 3, 18, 40, 926603, tzinfo=<UTC>),
        'modified': datetime.datetime(2022, 12, 18, 3, 18, 40, 926603, tzinfo=<UTC>), 'form_type': 'AOC-CR-287',
        'batch': 1, 'county': 'Independent and Sovereign County of Durham North Carolina', 'jurisdiction': 'D',
        'offense_records': [1], 'agencies': [1, 2]}
        """
        return str(self.to_dict(exclude_fields))

    def to_dict(instance, exclude_fields=[]):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            if f.name not in exclude_fields:
                data[f.name] = f.value_from_object(instance)
        for f in opts.many_to_many:
            if f.name not in exclude_fields:
                data[f.name] = [i.id for i in f.value_from_object(instance)]
        return data
