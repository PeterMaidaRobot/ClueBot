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

        # Find out what index the clue bot is at since we will use that index a lot
        self.clueBotPlayerIdx = -1
        for playerIdx in range(len(players)):
            if players[playerIdx] == 'Clue Bot':
                self.clueBotPlayerIdx = playerIdx

        # Initialize our past guesses vbox history
        self.playerPastGuesses = []
        for playerIdx in range(len(players)):
            self.playerPastGuesses.append([])

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


    '''
    return the value of the suspect cell at this matrix index
    '''
    def get_suspect_guess(self, playerIdx, suspectIdx):
        return self.suspectGuessCard[playerIdx][suspectIdx]

    '''
    return the value of the weapon cell at this matrix index
    '''
    def get_weapon_guess(self, playerIdx, weaponIdx):
        return self.weaponGuessCard[playerIdx][weaponIdx]

    '''
    return the value of the room cell at this matrix index
    '''
    def get_room_guess(self, playerIdx, roomIdx):
        return self.roomGuessCard[playerIdx][roomIdx]

    '''
    Increment the turn counter, and player index (wrapping as necessary)
    '''
    def increment_turn(self):
        self.turn_counter = self.turn_counter + 1
        self.current_player = (self.current_player + 1) % len(self.players)

    '''
    THIS IS WHERE THE MAGIC HAPPENS
    '''
    def process_results(self):
        pass

    '''
    Submit another player's turn for our history which we will process later
    '''
    def submit_turn(self, playerIdx, suspectIdx, weaponIdx, roomIdx):
        self.playerPastGuesses[playerIdx].append( (suspectIdx, weaponIdx, roomIdx) )
        self.process_results()
        self.increment_turn()

    '''
    Submit a ClueBot turn where we prompted a guess and got something in return
    '''
    def submit_cluebot_turn(self, playerIdx, suspectIdx=None, weaponIdx=None, roomIdx=None):
        if suspectIdx != None:
            self.player_has_suspect(playerIdx, suspectIdx)
        if weaponIdx != None:
            self.player_has_weapon(playerIdx, weaponIdx)
        if roomIdx != None:
            self.player_has_room(playerIdx, roomIdx)
        self.process_results()
        self.increment_turn()

    '''
    Return True if it is cluebot's turn, False otherwise
    '''
    def is_cluebot_turn(self):
        return self.current_player == self.clueBotPlayerIdx

