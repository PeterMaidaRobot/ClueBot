# This Python file uses the following encoding: utf-8

# Create a fake Enum for now
class HasCard:
    NO = 'NO'
    YES = 'YES'
    MAYBE = 'MAYBE'

class CardType:
    SUSPECT = 'SUSPECT'
    WEAPON = 'WEAPON'
    ROOM = 'ROOM'


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
    Update the status of previous guesses if this person has that card or not
    '''
    def updatePreviousGuesses(self):
        updateOccured = False
        # Loop through every player and update all 3 of their cards based off the current card
        for playerIdx in range(len(self.players)):
            playerGuesses = self.playerPastGuesses[playerIdx]
            for guessIdx in range(len(playerGuesses)):
                # Grab the suspect index, and then update the hasCard status based on our guess card.
                suspectIdx = playerGuesses[guessIdx][CardType.SUSPECT][0]
                hasSuspect = self.suspectGuessCard[playerIdx][suspectIdx]

                weaponIdx = playerGuesses[guessIdx][CardType.WEAPON][0]
                hasWeapon = self.weaponGuessCard[playerIdx][weaponIdx]

                roomIdx = playerGuesses[guessIdx][CardType.ROOM][0]
                hasRoom = self.roomGuessCard[playerIdx][roomIdx]

                # If we have two NO's in our tuple, then the last one has to be a yes!
                if hasSuspect == HasCard.NO and hasWeapon == HasCard.NO and hasRoom == HasCard.MAYBE:
                    hasRoom = HasCard.YES
                    updateOccured = True
                elif hasSuspect == HasCard.NO and hasWeapon == HasCard.MAYBE and hasRoom == HasCard.NO:
                    hasWeapon = HasCard.YES
                    updateOccured = True
                elif hasSuspect == HasCard.MAYBE and hasWeapon == HasCard.NO and hasRoom == HasCard.NO:
                    hasSuspect = HasCard.YES
                    updateOccured = True

                playerGuesses[guessIdx][CardType.WEAPON] = (weaponIdx, hasWeapon)
                playerGuesses[guessIdx][CardType.SUSPECT] = (suspectIdx, hasSuspect)
                playerGuesses[guessIdx][CardType.ROOM] = (roomIdx, hasRoom)

        return updateOccured

    '''
    Processes the previous guesses and updates the cards with new findings
    '''
    def processPreviousGuesses(self):
        # Loop through every player and update all 3 of their cards based off the current card
        for playerIdx in range(len(self.players)):
            playerGuesses = self.playerPastGuesses[playerIdx]
            for guessIdx in range(len(playerGuesses)):
                # Grab the suspect index, and then update the hasCard status based on our guess card.
                suspectIdx = playerGuesses[guessIdx][CardType.SUSPECT][0]
                hasSuspect = playerGuesses[guessIdx][CardType.SUSPECT][1]

                # If our card was uncertain, but our previous guess tuple wasn't, then update the card with the tuple value
                if self.suspectGuessCard[playerIdx][suspectIdx] == HasCard.MAYBE and hasSuspect != HasCard.MAYBE:
                    self.suspectGuessCard[playerIdx][suspectIdx] = hasSuspect


                weaponIdx = playerGuesses[guessIdx][CardType.WEAPON][0]
                hasWeapon = playerGuesses[guessIdx][CardType.WEAPON][1]

                if self.weaponGuessCard[playerIdx][weaponIdx] == HasCard.MAYBE and hasWeapon != HasCard.MAYBE:
                    self.weaponGuessCard[playerIdx][weaponIdx] = hasWeapon


                roomIdx = playerGuesses[guessIdx][CardType.ROOM][0]
                hasRoom = playerGuesses[guessIdx][CardType.ROOM][1]

                if self.roomGuessCard[playerIdx][roomIdx] == HasCard.MAYBE and hasRoom != HasCard.MAYBE:
                    self.roomGuessCard[playerIdx][roomIdx] = hasRoom

    '''
    THIS IS WHERE THE MAGIC HAPPENS
    '''
    def process_results(self):
        updateOccured = True
        while updateOccured:
            self.processPreviousGuesses()
            updateOccured = self.updatePreviousGuesses() # TODO idk what the order of this and the other stuff should be

    '''
    Submit another player's turn for our history which we will process later
    '''
    def submit_turn(self, playerIdx, suspectIdx, weaponIdx, roomIdx):
        self.playerPastGuesses[playerIdx].append( { CardType.SUSPECT: (suspectIdx, HasCard.MAYBE),
                                                    CardType.WEAPON: (weaponIdx, HasCard.MAYBE),
                                                    CardType.ROOM: (roomIdx, HasCard.MAYBE) } )
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

