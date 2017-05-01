import yaml
from .actions.new_action import (
    actions_constructor,
    NEW_ACTION_TAG
)
from .actions.base.effect import (
    effect_constructor,
    new_effect_constructor,
    NEW_EFFECT_TAG,
    EFFECT_TAG
)
from .actions.base.status import (
    status_constructor,
    STATUS_TAG,
    new_status_constructor,
    NEW_STATUS_TAG
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
from .unit.unit import (
    unit_constructor,
    NEW_UNIT_TAG,
)

# loader = yaml.Loader()
yaml.add_constructor(NEW_ACTION_TAG, actions_constructor)

yaml.add_constructor(EFFECT_TAG, effect_constructor)
yaml.add_constructor(NEW_EFFECT_TAG, new_effect_constructor)

yaml.add_constructor(STATUS_TAG, status_constructor)
yaml.add_constructor(NEW_STATUS_TAG, new_status_constructor)

yaml.add_constructor(PROPERTY_TAG, property_constructor)
yaml.add_constructor(EXPRESSION_TAG, expression_constructor)
yaml.add_constructor(AREA_TAG, area_constructor)

yaml.add_constructor(NEW_UNIT_TAG, unit_constructor)


def load(paths=None):
    paths = paths or [
        './mlp/actions/base/effects.yaml',
        './mlp/actions/base/statuses.yaml',
        './mlp/actions/actions.yaml',
        './mlp/unit/units.yaml',
    ]
    for path in paths:
        print(path)
        with open(path) as a:
            # loader = yaml.Loader(a)
            yaml.load(a)

# if __name__ == '__main__':
#     c = load()