import json
from django.http import HttpResponse
from django.db.models.fields.related import ManyToManyField
from django.db.models.fields import DateField
from django.db.models import ImageField

def api_response(data):
	return HttpResponse(json.dumps(data), content_type="application/json")


def model2dict(instance, fields=None, exclude=None):
    opts = instance._meta
    data = {}
    for f in opts.fields + opts.many_to_many:

        if not f.editable and not isinstance(f, DateField):
            continue
        if fields and not f.name in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if isinstance(f, ManyToManyField):
            # If the object doesn't have a primry key yet, just use an empty
            # list for its m2m fields. Calling f.value_from_object will raise
            # an exception.
            if instance.pk is None:
                data[f.name] = []
            else:
                # MultipleChoiceWidget needs a list of pks, not object instances.
                data[f.name] = [obj.pk for obj in f.value_from_object(instance)]
        elif isinstance(f, DateField):
            data[f.name] = str(getattr(instance, f.name))
        elif isinstance(f, ImageField):
        	data[f.name] = str(getattr(instance, f.name))
        else:
            data[f.name] = f.value_from_object(instance)
    return data
