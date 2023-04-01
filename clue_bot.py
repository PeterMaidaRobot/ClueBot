# This Python file uses the following encoding: utf-8


class ClueBot:
    def __init__(self, players, suspects, weapons, rooms, dealtSuspects, dealtWeapons, dealtRooms):

        self.players = players
        self.suspects = suspects
        self.weapons = weapons
        self.rooms = rooms

        self.current_player = 0
        self.turn_counter = 0

        self._init_guess_card(dealtSuspects, dealtWeapons, dealtRooms)


        print(self.suspectGuessCard)
        print(self.weaponGuessCard)
        print(self.roomGuessCard)

        print("Clue Bot was dealt:")
        print(dealtSuspects)
        print(dealtWeapons)
        print(dealtRooms)


    def _init_guess_card(self, dealtSuspects, dealtWeapons, dealtRooms):
        # Guess card is a matrix of [NUM_PLAYERS][NUM_CARDS]
        self.suspectGuessCard = []
        for playerIdx in range(len(self.players)):
            self.suspectGuessCard.append([])
            for suspect in self.suspects:
                self.suspectGuessCard[playerIdx].append('?')
        self.weaponGuessCard = []
        for playerIdx in range(len(self.players)):
            self.weaponGuessCard.append([])
            for weapon in self.weapons:
                self.weaponGuessCard[playerIdx].append('?')
        self.roomGuessCard = []
        for playerIdx in range(len(self.players)):
            self.roomGuessCard.append([])
            for room in self.rooms:
                self.roomGuessCard[playerIdx].append('?')

        # Fill in the ClueBot Guesses
        for suspect in dealtSuspects:
            pass

    def get_suspect_guess(self, playerIdx, suspectIdx):
        return self.suspectGuessCard[playerIdx][suspectIdx]

    def get_weapon_guess(self, playerIdx, weaponIdx):
        return self.weaponGuessCard[playerIdx][weaponIdx]

    def get_room_guess(self, playerIdx, roomIdx):
        return self.roomGuessCard[playerIdx][roomIdx]

    def submit_turn(self):
        print("test")

    def submit_cluebot_turn(self):
        print("test")
