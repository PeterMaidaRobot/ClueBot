# This Python file uses the following encoding: utf-8

# Create a fake Enum for now
class HasCard():
    NO = 'NO'
    YES = 'YES'
    MAYBE = 'MAYBE'


class ClueBot:
    def __init__(self, players, suspects, weapons, rooms, dealtSuspects, dealtWeapons, dealtRooms):

        self.players = players
        self.suspects = suspects
        self.weapons = weapons
        self.rooms = rooms

        self.clueBotPlayerIdx = -1
        for playerIdx in range(len(players)):
            if players[playerIdx] == 'Clue Bot':
                self.clueBotPlayerIdx = playerIdx

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
                if playerIdx == self.clueBotPlayerIdx:
                    self.suspectGuessCard[playerIdx].append(HasCard.NO)
                else:
                    self.suspectGuessCard[playerIdx].append(HasCard.MAYBE)

        self.weaponGuessCard = []
        for playerIdx in range(len(self.players)):
            self.weaponGuessCard.append([])
            for weapon in self.weapons:
                if playerIdx == self.clueBotPlayerIdx:
                    self.weaponGuessCard[playerIdx].append(HasCard.NO)
                else:
                    self.weaponGuessCard[playerIdx].append(HasCard.MAYBE)

        self.roomGuessCard = []
        for playerIdx in range(len(self.players)):
            self.roomGuessCard.append([])
            for room in self.rooms:
                if playerIdx == self.clueBotPlayerIdx:
                    self.roomGuessCard[playerIdx].append(HasCard.NO)
                else:
                    self.roomGuessCard[playerIdx].append(HasCard.MAYBE)

        # Fill in the ClueBot Guesses
        for suspectTuple in dealtSuspects:
            suspectIdx = suspectTuple[0]
            self.player_has_suspect(self.clueBotPlayerIdx, suspectIdx)

        for weaponTuple in dealtWeapons:
            weaponIdx = weaponTuple[0]
            self.player_has_weapon(self.clueBotPlayerIdx, weaponIdx)

        for roomTuple in dealtSuspects:
            roomIdx = roomTuple[0]
            self.player_has_room(self.clueBotPlayerIdx, roomIdx)

    '''
    Will set the current player to YES, and all others to NO
    '''
    def player_has_suspect(self, playerHasIdx, suspectIdx):
        for playerIdx in range(len(self.players)):
            if playerIdx == playerHasIdx:
                self.suspectGuessCard[playerIdx][suspectIdx] = HasCard.YES
            else:
                self.suspectGuessCard[playerIdx][suspectIdx] = HasCard.NO

    '''
    Will set the current player to YES, and all others to NO
    '''
    def player_has_weapon(self, playerHasIdx, weaponIdx):
        for playerIdx in range(len(self.players)):
            if playerIdx == playerHasIdx:
                self.weaponGuessCard[playerIdx][weaponIdx] = HasCard.YES
            else:
                self.weaponGuessCard[playerIdx][weaponIdx] = HasCard.NO

    '''
    Will set the current player to YES, and all others to NO
    '''
    def player_has_room(self, playerHasIdx, roomIdx):
        for playerIdx in range(len(self.players)):
            if playerIdx == playerHasIdx:
                self.roomGuessCard[playerIdx][roomIdx] = HasCard.YES
            else:
                self.roomGuessCard[playerIdx][roomIdx] = HasCard.NO


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
