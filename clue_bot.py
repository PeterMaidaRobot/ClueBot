# This Python file uses the following encoding: utf-8


class ClueBot:
    def __init__(self, players, suspects, weapons, rooms, dealtSuspects, dealtWeapons, dealtRooms):

        self.players = players
        self.suspects = suspects
        self.weapons = weapons
        self.rooms = rooms

        self.dealtSuspects=dealtSuspects
        self.dealtWeapons=dealtWeapons
        self.dealtRooms=dealtRooms

        self.current_player = 0
        self.turn_counter = 0

        self.init_guess_card()

        print("Clue Bot was dealt:")
        print(dealtSuspects)
        print(dealtWeapons)
        print(dealtRooms)

    def init_guess_card(self):
        self.guess_card = []
        for player_idx in range(len(self.players)):
            self.guess_card.append([])
            cards = self.suspects + self.weapons + self.rooms
            for card in cards:
                self.guess_card[player_idx].append('?')

        print(self.guess_card)

        # Fill in the ClueBot Guesses


    def submit_turn(self):
        print("test")

    def submit_cluebot_turn(self):
        print("test")
