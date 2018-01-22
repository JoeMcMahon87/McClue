# Definition of the cards

class BaseCard:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class Weapon(BaseCard):
    def __init__(self, name):
        BaseCard.__init__(self, name)
        self.used = False
        self.location = None

    def used(self):
        self.used = True

    def set_location(self, loc):
        self.location = loc

    def get_location(self):
        return self.location

    def show(self):
        pass


class Location(BaseCard):
    def __init__(self, name):
        parts = [x.strip() for x in name.split(',')]
        BaseCard.__init__(self, parts[1])
        self.location_id = parts[0]
        self.present = []
        self.neighbors = []

    def get_id(self):
        return self.location_id

    def add_something(self, obj):
        self.present.append(obj)

    def remove_something(self, obj):
        self.present.remove(obj)

    def get_things_in_location(self):
        return self.present

    def add_neighbor(self, loc):
        self.neighbors.append(loc)

    def get_neighbors(self):
        return self.neighbors

    def show(self):
        print("({}) {}: [{}]".format(self.location_id, self.name, ",".join([item.name for item in self.present])))
        print("Neighbors: [{}]".format(", ".join([item.name for item in self.neighbors])))

class Character(BaseCard):
    def __init__(self, name):
        BaseCard.__init__(self, name)
        self.location = None
        self.knows_about = None
        self.alive = True
        self.hidden = False
        self.killer = False

    def kill(self):
        self.alive = False

    def set_killer(self, flag):
        self.killer = flag

    def is_hidden(self):
        return self.hidden

    def hide(self):
        self.hidden = True

    def discovered(self):
        self.hidden = False

    def set_location(self, loc):
        self.location = loc

    def get_location(self):
        return self.location

    def set_knows_about(self, ka):
        self.knows_about = ka

    def get_knows_about(self):
        return self.knows_about

    def is_alive(self):
        return self.alive

    def is_murderer(self):
        return self.killer

    def show(self):
        if self.knows_about is not None:
            if isinstance(self.knows_about, Character):
                knows = "{} is innocent".format(self.knows_about.get_name())
            elif isinstance(self.knows_about, Weapon):
                knows = "the {} hasn't been used".format(self.knows_about.get_name())
            elif isinstance(self.knows_about, Location):
                knows = "the {} is not the murder scene".format(self.knows_about.get_name())
        else:
            knows = "nothing"

        killer = ''
        if self.killer:
            killer = '*'

        location = 'not set'
        if self.location is not None:
            location = self.location.get_name()
        print("{}{} is in the {} and knows {}".format(self.name, killer, location, knows))
