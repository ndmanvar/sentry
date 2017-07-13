from __future__ import absolute_import

from itertools import izip
import six

from sentry.api.serializers import Serializer, register, serialize
from sentry.constants import LOG_LEVELS
from sentry.models import (
    GroupTombstone, User
)


@register(GroupTombstone)
class GroupTombstoneSerializer(Serializer):

    def get_attrs(self, item_list, user):
        project_set = set(i.project for i in item_list)
        projects = {
            p.id: d for p, d in izip(project_set, serialize(project_set, user))
        }

        user_list = list(User.objects.filter(id__in=[item.actor_id for item in item_list]))
        users = {
            u.id: d for u, d in izip(user_list, serialize(user_list, user))
        }

        attrs = {}
        for item in item_list:
            attrs[item] = {
                'project': projects.get(item.project_id, {}),
                'user': users.get(item.actor_id, {}),
            }
        return attrs

    def serialize(self, obj, attrs, user):
        return {
            'id': six.text_type(obj.id),
            'project': attrs['project'],
            'level': LOG_LEVELS.get(obj.level, 'unknown'),
            'message': obj.message,
            'culprit': obj.culprit,
            'type': obj.get_event_type(),
            'actor': attrs.get('user'),

        }