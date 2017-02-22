def list_of_spaces(request):
    from .models import Space
    from django.db.models import Q
    if request.user.is_authenticated:
        return {'spaces_list': Space.objects.filter(Q(owner=request.user) | Q(added_users__in=[request.user]))}
    else:
        return {}
