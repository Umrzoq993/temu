from django.contrib.admin import SimpleListFilter
import django_filters
from django.db.models import Count
from .models import Product, Courier

class CourierFilter(django_filters.FilterSet):
    # The assigned filter will check whether a courier has any covered cities.
    assigned = django_filters.CharFilter(method='filter_assigned')
    region = django_filters.NumberFilter(method='filter_region')
    city = django_filters.NumberFilter(method='filter_city')

    class Meta:
        model = Courier
        fields = []  # We are using custom methods

    def filter_assigned(self, queryset, name, value):
        """
        If the query parameter 'assigned' equals "assigned", return couriers with one or more
        covered cities. If it equals "unassigned", return couriers with zero covered cities.
        """
        if value.lower() == "assigned":
            return queryset.annotate(num_cities=Count('covered_cities')).filter(num_cities__gt=0)
        elif value.lower() == "unassigned":
            return queryset.annotate(num_cities=Count('covered_cities')).filter(num_cities=0)
        return queryset

    def filter_region(self, queryset, name, value):
        """
        Filter couriers whose covered cities belong to the given region.
        """
        return queryset.filter(covered_cities__region_id=value).distinct()

    def filter_city(self, queryset, name, value):
        """
        Filter couriers that cover a particular city.
        """
        return queryset.filter(covered_cities__id=value).distinct()


class ProductFilter(django_filters.FilterSet):
    assigned = django_filters.CharFilter(method='filter_assigned')
    # Here we filter by region and city using the foreign key ID fields
    region = django_filters.NumberFilter(field_name="region_id")
    city = django_filters.NumberFilter(field_name="city_id")

    class Meta:
        model = Product
        fields = ['order_status', 'region', 'city']

    def filter_assigned(self, queryset, name, value):
        """
        Filter products by assigned courier:
          - 'assigned' returns products with an assigned courier (assigned_to is not null)
          - 'unassigned' returns products with no courier assigned (assigned_to is null)
        """
        if value.lower() == "assigned":
            return queryset.filter(assigned_to__isnull=False)
        elif value.lower() == "unassigned":
            return queryset.filter(assigned_to__isnull=True)
        return queryset


class AssignedFilter(SimpleListFilter):
    title = "Kuryerga biriktirilganlik"  # Display title in the admin sidebar
    parameter_name = "assigned"  # URL query parameter

    def lookups(self, request, model_admin):
        return (
            ('assigned', 'Biriktirilgan'),
            ('unassigned', 'Biriktirilmagan'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'assigned':
            return queryset.filter(assigned_to__isnull=False)
        if self.value() == 'unassigned':
            return queryset.filter(assigned_to__isnull=True)
        return queryset
