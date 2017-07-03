class Command:

    name = ""

    def execute(self):
        pass

    def dump(self):
        pass


class Place(Command):

    name = "place"

    def __init__(self, unit=None, place=None, old_place=None):
        self.unit = unit
        self.place = place
        self.old_place = old_place

    def execute(self):
        unit = self.unit
        uw = unit.make_widget()
        if self.old_place:
            self.old_place.make_widget().remove_widget(uw)
        self.place.make_widget().add_widget(uw)

    def dump(self):
        return {
            "name": self.name,
            "unit": self.unit,
            "old_place": self.old_place,
            "place": self.place,
        }