from PySide6.QtWidgets import QMainWindow, QLineEdit, QCheckBox, QLabel, QHBoxLayout, QVBoxLayout, QTableWidgetItem, QFrame
from ui_mainwindow import Ui_MainWindow
from clue_bot import ClueBot

def func():
    print("heyyee")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.resize(1500, 800)

        # Connect signals
        self.ui.playGameBtn.clicked.connect(self.deal_cards)
        self.ui.submitDealtCardsBtn.clicked.connect(self.play_game)
        self.ui.submitTurnBtn.clicked.connect(self.submit_turn)
        self.ui.submitClueBotTurnBtn.clicked.connect(self.submit_cluebot_turn)

        # We have both frames visible at first, hide this one for now
        self.ui.gamePlayFrame.setVisible(False)
        self.ui.dealtCardsFrame.setVisible(False)

        # Run a test
        self.run_test()


    def run_test(self):
        self.deal_cards()

        drawn_cards = [
        "Prof. Plum",
        "Mr. Green",
        "Lead Pipe",
        "Kitchen",
        "Library"
        ]
        for i in range(self.ui.dealtSuspectsVbox.layout().count()):
            widget = self.ui.dealtSuspectsVbox.layout().itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.text() in drawn_cards:
                widget.setChecked(True)

        for i in range(self.ui.dealtWeaponsVbox.layout().count()):
            widget = self.ui.dealtWeaponsVbox.layout().itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.text() in drawn_cards:
                widget.setChecked(True)

        for i in range(self.ui.dealtRoomsVbox.layout().count()):
            widget = self.ui.dealtRoomsVbox.layout().itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.text() in drawn_cards:
                widget.setChecked(True)

        self.play_game()


    def read_setup_inputs(self):
        # Grab all the fields from the UI setup Frame
        self.playerNames = []
        for i in range(self.ui.playerNamesVbox.layout().count()):
            widget = self.ui.playerNamesVbox.layout().itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                self.playerNames.append(widget.text())

        self.suspectNames = []
        for i in range(self.ui.suspectNamesVbox.layout().count()):
            widget = self.ui.suspectNamesVbox.layout().itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                self.suspectNames.append(widget.text())

        self.weaponNames = []
        for i in range(self.ui.weaponNamesVbox.layout().count()):
            widget = self.ui.weaponNamesVbox.layout().itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                self.weaponNames.append(widget.text())

        self.roomNames = []
        for i in range(self.ui.roomNamesVbox.layout().count()):
            widget = self.ui.roomNamesVbox.layout().itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                self.roomNames.append(widget.text())

    def populate_dealt_cards_vboxes(self):
        # Create the checkboxes in each of these Vboxes
        for suspect in self.suspectNames:
            self.ui.dealtSuspectsVbox.addWidget(QCheckBox(suspect))

        for weapon in self.weaponNames:
            self.ui.dealtWeaponsVbox.addWidget(QCheckBox(weapon))

        for rooms in self.roomNames:
            self.ui.dealtRoomsVbox.addWidget(QCheckBox(rooms))

    '''
    Switch to the deal cards state
    '''
    def deal_cards(self):
        self.read_setup_inputs()

        self.populate_dealt_cards_vboxes()

        # Switch UI Frames to dealt cards Frame
        self.ui.gameSetupFrame.setVisible(False)
        self.ui.dealtCardsFrame.setVisible(True)


    def read_dealt_inputs(self):
        # For each card, store a tuple of (index, name). We will mainly use the index
        self.dealtSuspects = []
        for i in range(self.ui.dealtSuspectsVbox.layout().count()):
            widget = self.ui.dealtSuspectsVbox.layout().itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.isChecked():
                self.dealtSuspects.append( (i, widget.text()) )

        self.dealtWeapons = []
        for i in range(self.ui.dealtWeaponsVbox.layout().count()):
            widget = self.ui.dealtWeaponsVbox.layout().itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.isChecked():
                self.dealtWeapons.append( (i, widget.text()) )

        self.dealtRooms = []
        for i in range(self.ui.dealtRoomsVbox.layout().count()):
            widget = self.ui.dealtRoomsVbox.layout().itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.isChecked():
                self.dealtRooms.append( (i, widget.text()) )


    '''
    init_game_play_frame() will populate the comboboxes, the main guess card table/grid,
    and the previous guesses vbox area
    '''
    def init_game_play_frame(self):
        # Populate the ClueBot Play Frame
        self.ui.whoShowedClueBotCmbBox.addItems(self.playerNames)
        self.ui.playerToClueBotCardCmbBox.addItems(self.suspectNames)
        self.ui.playerToClueBotCardCmbBox.addItems(self.weaponNames)
        self.ui.playerToClueBotCardCmbBox.addItems(self.roomNames)

        # Populate the Other Player Play Frame
        self.ui.playerGuessSuspectCmbBox.addItems(self.suspectNames)
        self.ui.playerGuessWeaponCmbBox.addItems(self.weaponNames)
        self.ui.playerGuessRoomCmbBox.addItems(self.roomNames)
        self.ui.whoShowedCardCmbBox.addItems(self.playerNames)

        # Populate the Guess Grid
        self.ui.guessCardTable.setColumnCount(len(self.playerNames))
        self.ui.guessCardTable.setHorizontalHeaderLabels(self.playerNames)
        verticalHeaderLabels = self.suspectNames + self.weaponNames + self.roomNames
        self.ui.guessCardTable.setRowCount(len(verticalHeaderLabels))
        self.ui.guessCardTable.setVerticalHeaderLabels(verticalHeaderLabels)

        # Populate the Guess Grid with ClueBot's data...
        for row in range(self.ui.guessCardTable.rowCount()):
            for col in range(self.ui.guessCardTable.columnCount()):
                self.ui.guessCardTable.setItem(row, col, QTableWidgetItem(self.get_cell_guess(row, col)))

        # Create the previous guesses table
        self.ui.previousGuessTable.setColumnCount(len(self.playerNames))
        self.ui.previousGuessTable.setHorizontalHeaderLabels(self.playerNames)
        self.ui.previousGuessTable.verticalHeader().hide()



    '''
    Switch to the play game State
    '''
    def play_game(self):
        self.read_dealt_inputs()

        # Create the clue object with all of our inputs
        self.clue_bot = ClueBot(
        players=self.playerNames,
        suspects=self.suspectNames,
        weapons=self.weaponNames,
        rooms=self.roomNames,
        dealtSuspects=self.dealtSuspects,
        dealtWeapons=self.dealtWeapons,
        dealtRooms=self.dealtRooms
        )

        self.init_game_play_frame()

        # Switch UI Frames to play game Frame
        self.ui.dealtCardsFrame.setVisible(False)
        self.ui.gamePlayFrame.setVisible(True)

        self.update_info_frame()


    '''
    '''
    def get_cell_guess(self, guessCardIdx, playerIdx):
        guess = ""
        if guessCardIdx < len(self.suspectNames):
            guess = self.clue_bot.get_suspect_guess(playerIdx, guessCardIdx)
        elif guessCardIdx < len(self.suspectNames) + len(self.weaponNames):
            guess = self.clue_bot.get_weapon_guess(playerIdx, guessCardIdx - len(self.suspectNames))
        elif guessCardIdx < len(self.suspectNames) + len(self.weaponNames) + len(self.roomNames):
            guess = self.clue_bot.get_room_guess(playerIdx, guessCardIdx - len(self.suspectNames) - len(self.weaponNames))
        return guess

    '''
    This will update the guess card after clue bot has made an update
    '''
    def update_guess_card(self):
        # Loop through each cell in the table and get what the clue bot has for that entry
        for row in range(self.ui.guessCardTable.rowCount()):
            for col in range(self.ui.guessCardTable.columnCount()):
                self.ui.guessCardTable.item(row, col).setText( self.get_cell_guess(row, col) )

    '''
    This will destroy and re-create the guess history tuple vbox for the players
    '''
    def update_guess_history(self):

        # Clear
        self.ui.previousGuessTable.setRowCount(0)

        # Fill in every players past guesses
        for playerIdx in range(len(self.clue_bot.playerPastGuesses)):

            # Increase the row count if we have to
            if len(self.clue_bot.playerPastGuesses[playerIdx]) > self.ui.previousGuessTable.rowCount():
                self.ui.previousGuessTable.setRowCount(len(self.clue_bot.playerPastGuesses[playerIdx]))

            for guessIdx, guess in enumerate(self.clue_bot.playerPastGuesses[playerIdx]):
                print(guess)
                guessCell = QLabel( str(guess[0]) + " " + str(guess[1]) + " " + str(guess[2]) )
                self.ui.previousGuessTable.setCellWidget(guessIdx, playerIdx, guessCell)



    def update_info_frame(self):

        self.ui.turnCounterLbl.setText("Turn " + str(self.clue_bot.turn_counter))
        self.ui.playerTurnLbl.setText("Player " + str(self.clue_bot.current_player)) #TODO convert to string
        if self.clue_bot.is_cluebot_turn():
            self.ui.otherPlayerPlayFrame.hide()
            self.ui.cluebotPlayFrame.show()
        else:
            self.ui.otherPlayerPlayFrame.show()
            self.ui.cluebotPlayFrame.hide()


    '''
    This will update everything on the UI after a guess has occured
    '''
    def update_ui(self):
        self.update_guess_card()
        self.update_guess_history()
        self.update_info_frame()


    def submit_turn(self):
        print(self.ui.whoShowedCardCmbBox.currentText() + " showed one of (" +
            self.ui.playerGuessSuspectCmbBox.currentText() + ", " +
            self.ui.playerGuessWeaponCmbBox.currentText() + ", " +
            self.ui.playerGuessRoomCmbBox.currentText() + ")")

        # Send ClueBot the index values, not the text
        self.clue_bot.submit_turn(playerIdx=self.ui.whoShowedCardCmbBox.currentIndex(),
                                suspectIdx=self.ui.playerGuessSuspectCmbBox.currentIndex(),
                                weaponIdx=self.ui.playerGuessWeaponCmbBox.currentIndex(),
                                roomIdx=self.ui.playerGuessRoomCmbBox.currentIndex())

        self.update_ui()


    def submit_cluebot_turn(self):
        print(self.ui.whoShowedClueBotCmbBox.currentText() + " showed ClueBot " +
            self.ui.playerToClueBotCardCmbBox.currentText())

        guessCardIdx = self.ui.playerToClueBotCardCmbBox.currentIndex()
        if guessCardIdx < len(self.suspectNames):
            self.clue_bot.submit_cluebot_turn(playerIdx=self.ui.whoShowedClueBotCmbBox.currentIndex(),
                                            suspectIdx=guessCardIdx)
        elif guessCardIdx < len(self.suspectNames) + len(self.weaponNames):
            self.clue_bot.submit_cluebot_turn(playerIdx=self.ui.whoShowedClueBotCmbBox.currentIndex(),
                                            weaponIdx=guessCardIdx - len(self.suspectNames))
        elif guessCardIdx < len(self.suspectNames) + len(self.weaponNames) + len(self.roomNames):
            self.clue_bot.submit_cluebot_turn(playerIdx=self.ui.whoShowedClueBotCmbBox.currentIndex(),
                                            roomIdx=guessCardIdx - len(self.suspectNames) - len(self.weaponNames))

        self.update_ui()
