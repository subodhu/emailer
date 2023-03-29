from django_filters import rest_framework as filters

from apps.emails.models import Email


class EmailFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(field_name="created_at")
    email = filters.CharFilter(method="filter_email")
    q = filters.CharFilter(method="filter_q")

    class Meta:
        model = Email
        fields = ["q", "date", "email"]

    def filter_q(self, qs, name, value):
        return qs.filter(subject__icontains=value)

    def filter_email(self, qs, name, value):
        if value:
            return qs.filter(
                email_recipients__recipient_email__icontains=value
            ).distinct()
        return qs
