from simple_history.admin import SimpleHistoryAdmin


class BaseModelAdmin(SimpleHistoryAdmin):
    # noinspection PyUnresolvedReferences
    exclude = ['enumeration_attack_uuid']
