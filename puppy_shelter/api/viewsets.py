from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from api.permissions import Public
from copy import deepcopy
from django.core.exceptions import FieldError
from rest_framework.exceptions import ValidationError


class ViewSet(ModelViewSet):
    default_filter_type_map = {
        'id': int
    }
    filter_type_map = dict()  # ! <- nadpisuje klasa dziedziczaca :)
    default_permissions = [Public]
    action_permissions = {    # ! <- nadpisuje klasa dziedziczaca :)
        'list': [IsAuthenticated],
        'create': list(),     # ! klasa dziedziczaca nie moze zostawiac pustych permissionow !!!
        'retrieve': [IsAuthenticated],
        'update': list(),
        'partial_update': list(),
        'destroy': list(),
        'metadata': [Public],
    }

    def get_queryset(self):
        # ! custom filtrowanie po query params
        query_params = deepcopy(self.request.query_params)
        for qparam in ['page', 'format']:
            try: query_params.pop(qparam)
            except Exception: pass

        filters = dict()
        type_map = self.default_filter_type_map | self.filter_type_map  # ! zlacz slowniki
        for field_name, field_value in query_params.items():
            if not field_value:  # ! jestli param= to null / None
                filters[field_name] = None
            elif '__in' in field_name:  # ! jesli mamy field_id__in=1,2  ect
                filters[field_name] = field_value.split(',')
            else:
                filters[field_name] = type_map.get(field_name, str)(field_value)
                # ! ^ castujemy str / int ect. <- z mapowania
        try:
            return self.serializer_class.Meta.model.objects.filter(**filters)
            # !  ^ self.serializer_class.Meta.model < klasa z modelem orm
        except FieldError as e:
            raise ValidationError(detail={"msg": f"Field error -> {repr(e)}"})  # ! jesli cos nie tak to 400 -> err

    def get_permissions(self):
        action = self.action or 'list'
        # print('ACTION', action)
        all_permissions = deepcopy(self.default_permissions)
        for action_permission in self.action_permissions.get(action, list()):
            if action_permission not in all_permissions: all_permissions.append(action_permission)

        permissions = [p() for p in all_permissions]
        if not permissions:
            raise EnvironmentError(f'No permissions provied for "{self.__class__.__name__} action: {action}"')
        return permissions
