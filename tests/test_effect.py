from ..mlp.grid import Cell
from ..mlp.unit import UNITS
from ..mlp.actions.base import *
from ..mlp.loader import load
import nose
from nose.tools import assert_raises

DUMMY = 'Dummy'
A = 'A'
B = 'B'

load()

class TestEffect:

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
            'source': self.source
        }

    def test_damage(self):
        e = Damage(10)
        e.apply([self.target], self.context)
        assert self.victim.stats.health == 90

