class Effect:

    info_message = ""

    def __init__(self, **kwargs):
        # self.owner = owner
        # self.source = source
        self.info_message = self.info_message

    def configure(self, **kwargs):
        pass

    def apply(self, source, target):
        source.owner.action_log.append(self.info_message)

    def copy(self):
        return self.__class__(**vars(self))


class Move(Effect):

    info_message = "{} move to {}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_coord = None

    def configure(self, target_coord):
        self.target_coord = target_coord

    def apply(self, source, target):
        print(self.info_message.format(target, self.target_coord))
        print(target.object)
        target.object.move(self.target_coord)
        self.info_message = self.info_message.format(target, self.target_coord)
        super().apply(source, target)


class Damage(Effect):
    pass


EFFECTS = {
    'Move': Move
}