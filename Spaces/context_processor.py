def list_of_spaces(request):
    from .models import Space
    from ShareUser.models import ShareUser
    from django.db.models import Q
    if request.user.is_authenticated:
        s_user = ShareUser.objects.get(user=request.user)
        return {'spaces_list': Space.objects.filter(Q(owner=s_user) | Q(added_users__in=[s_user]))}
    else:
        return {}
