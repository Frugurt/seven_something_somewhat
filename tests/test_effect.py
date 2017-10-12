import yaml
from ..mlp.grid import Cell
from ..mlp.unit import UNITS
from ..mlp.loader import load

DUMMY = 'Dummy'
A = 'A'
B = 'B'

load()


class TestEffect:

    tests_path = "./tests/effect_tests.yaml"

    def setUp(self):
        self.source = Cell((0, 0))
        self.author = UNITS[DUMMY](A)
        self.author.place_in(self.source)
        self.author.switch_state()
        self.target = Cell((1, 1))
        self.victim = UNITS[DUMMY](B)
        self.victim.place_in(self.target)
        self.victim.switch_state()
        self.context = {
            'owner': self.author,
            'source': self.source,
            'victim': self.victim.stats,
        }

    def test_effects(self):
        with open(self.tests_path) as tests_file:
            tests = yaml.load(tests_file)
        for test in tests:
            yield self.check, [effect.get() for effect in test['effects']], test['check']

    def check(self, effects, expression):
        for effect in effects:
            effect.apply([self.target], self.context)
        assert expression.get(self.context)
