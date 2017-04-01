import yaml
# import ruamel.yaml as yaml
from .actions.new_action import (
    actions_constructor,
    NEW_ACTION_TAG
)
from .actions.base.effect import (
    effect_constructor,
    EFFECT_TAG
)
from .actions.base.status import (
    status_constructor,
    STATUS_TAG,
)
from .actions.property.property import (
    property_constructor,
    PROPERTY_TAG,
)
from .actions.property.expression import (
    expression_constructor,
    EXPRESSION_TAG
)
from .actions.property.area import (
    area_constructor,
    AREA_TAG,
)
# loader = yaml.Loader()
yaml.add_constructor(NEW_ACTION_TAG, actions_constructor)
yaml.add_constructor(EFFECT_TAG, effect_constructor)
yaml.add_constructor(STATUS_TAG, status_constructor)
yaml.add_constructor(PROPERTY_TAG, property_constructor)
yaml.add_constructor(EXPRESSION_TAG, expression_constructor)
yaml.add_constructor(AREA_TAG, area_constructor)


def load(path=None):
    path = path or './mlp/actions/actions.yaml'
    with open(path) as a:
        # loader = yaml.Loader(a)
        return yaml.load(a)

if __name__ == '__main__':
    c = load()