# Main game loop for Clue
import random
from cards import BaseCard, Weapon, Location, Character
import copy
from time import sleep

class McClue:
    done = False
    murderer = None
    num_players = 4
    locations = []
    characters = []
    weapons = []
    deck = []
    player_hands = {}
    options = ['Stay', 'Move', 'Hide']

    def load_cards(self):
        def find_location_by_number(loc_id):
            return next((x for x in self.locations if int(x.get_id()) == int(loc_id)), None)

        def process_connection(line):
            parts = [x.strip() for x in line.split(',')]
            find_location_by_number(parts[0]).add_neighbor(find_location_by_number(parts[1]))
            find_location_by_number(parts[1]).add_neighbor(find_location_by_number(parts[0]))


        # Load character cards
        with open('characters.txt') as f:
            char_names = f.read().splitlines()
            self.characters = [Character(i) for i in char_names]
            self.character_cards = copy.deepcopy(self.characters)
            random.shuffle(self.characters)
            random.shuffle(self.character_cards)

        # Load location cards
        with open('locations.txt') as f:
            temp = f.read().splitlines()
            self.locations = [Location(i) for i in temp]
            random.shuffle(self.locations)

        # Load weapon cards
        with open('weapons.txt') as f:
            temp = f.read().splitlines()
            self.weapons = [Weapon(i) for i in temp]
            random.shuffle(self.weapons)

        with open('connections.txt') as f:
            temp = f.read().splitlines()
            for line in temp:
                process_connection(line)

    def create_solution(self):
        # Build solution (Character, Location, Weapon)
        solution = []
        self.murderer = self.character_cards.pop(0)
        for ch in self.characters:
            if ch.get_name() == self.murderer.get_name():
                ch.set_killer(True)

        solution.append(self.murderer)
        solution.append(self.locations.pop(0))
        solution.append(self.weapons.pop(0))
        print("{} in the {} with the {}".format(solution[0].get_name(), solution[1].get_name(), solution[2].get_name()))

        # Build remaining deck and shuffle it
        self.deck = self.character_cards + self.weapons + self.locations
        random.shuffle(self.deck)

    def setup_characters(self):
        # Populate character card folders
        # and position characters in locations
        for ch in self.characters:
            ch.set_knows_about(self.deck.pop(0))
            loc = random.choice(self.locations)
            ch.set_location(loc)
            loc.add_something(ch)

    def stash_weapons(self):
        # Stash weapons
        for wep in self.weapons:
            loc = random.choice(self.locations)
            wep.set_location(loc)
            loc.add_something(wep)

    def deal_cards(self):
        # Deal out remaining cards
        for p in range(0,4):
            self.player_hands['Player {}'.format(p+1)] = []

        while len(self.deck) > 0:
            for p in range(0,4):
                if len(self.deck) > 0:
                    self.player_hands['Player {}'.format(p+1)].append(self.deck.pop(0))

    def move_characters(self):
        # for each character
        for ch in self.characters:
            # if alive
            if ch.is_alive():
                # if murderer
                    # if in room with unused weapon and alive NPC
                    # commit another murder
                    # hide card from NPC
                # else
                    # determine: stay, move, hide
                    action = random.choice(self.options)
                    killer = ''
                    if ch.is_murderer():
                        killer = '*'
                    if action == 'Hide':
                        print("{}{} hides".format(ch.get_name(), killer))
                        ch.hide()
                    elif action == 'Stay':
                        pass
                    else:
                        ch.get_location().remove_something(ch)
                        dest = random.choice(ch.get_location().get_neighbors())
                        ch.set_location(dest)
                        dest.add_something(ch)
                        if ch.is_hidden():
                            print("{}{} moves".format(ch.get_name(), killer))
                        else:
                            print("{}{} moves to {}".format(ch.get_name(), killer, dest.get_name()))



    def main_game_loop(self):
        # Loop until game over
        round = 1
        while not self.done:
            # See if Inspector arrives
            # each player (random order):
            for p in range(0,self.num_players):
                print("Round {}: Player - {}".format(round, (p+1)))
                # get move, process guesses, search, etc.
                # move characters (and Inspector, if present)
                self.move_characters()
                sleep(5)
            round += 1


def main():
    game = McClue()
    game.load_cards()
    game.create_solution()
    game.setup_characters()
    game.stash_weapons()
    game.deal_cards()
    game.main_game_loop()

if __name__ == "__main__":
    main()

