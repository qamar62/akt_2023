from import_export import resources

from .models import Visa


class VisaResources(resources.ModelResource):
    class Meta:
        model = Visa