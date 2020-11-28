from appcore.models import db
import jsonschema
from jsonschema import validate


def normalize_query_param(value):
    return value if len(value) > 1 else value[0]


def normalize_query(params):
    params_non_flat = params.to_dict(flat=False)
    return {k: normalize_query_param(v) for k, v in params_non_flat.items()}


def get_class_by_tablename(tablename):
    for c in db.Model._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c


def get_filter_by_args(model_class,dic_args: dict):
    filters = []
    for key, value in dic_args.items():  # type: str, any
        if key.endswith('___min'):
            key = key[:-6]
            filters.append(getattr(model_class, key) > value)
        elif key.endswith('___max'):
            key = key[:-6]
            filters.append(getattr(model_class, key) < value)
        elif key.endswith('__min'):
            key = key[:-5]
            filters.append(getattr(model_class, key) >= value)
        elif key.endswith('__max'):
            key = key[:-5]
            filters.append(getattr(model_class, key) <= value)
        else:
            filters.append(getattr(model_class, key) == value)
    return filters


def validateJson(jsonData,dataSchema):
    try:
        validate(instance=jsonData, schema=dataSchema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True