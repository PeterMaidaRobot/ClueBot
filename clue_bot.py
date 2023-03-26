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

    def submit_turn(self):
        print("test")

    def submit_cluebot_turn(self):
        print("test")
