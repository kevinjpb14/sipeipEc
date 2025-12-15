from auditlog.models import LogEntry

def log(mensaje, request, accion, instance_object=None):
    from django.contrib.contenttypes.models import ContentType

    #from sga.commonviews import get_client_ip
    if accion == "del":
        logaction = LogEntry.Action.DELETE
    elif accion == "add":
        logaction = LogEntry.Action.CREATE
    else:
        logaction = LogEntry.Action.UPDATE
    LogEntry.objects.create(
        actor_id=request.user.pk,
        content_type_id=instance_object and ContentType.objects.get_for_model(instance_object).pk or ContentType.objects.get_for_model(User).id,
        object_id=instance_object and instance_object.pk or request.user.id,
        object_pk=instance_object and instance_object.pk or request.user.id,
        object_repr=accion,
        action=logaction,
        changes_text=(u'%s' % (mensaje)).upper(),
        remote_addr=request and get_client_ip(request) or ''
    )

def get_client_ip(request):
    x_forwarded_for = request.headers.get(
        'X-Forwarded-For-CLIENT') or request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.headers.get(
            'X-Forwarded-For-CLIENT') or request.META.get('REMOTE_ADDR')
    return ip