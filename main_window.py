from PySide6.QtWidgets import QMainWindow, QLineEdit, QCheckBox
from ui_mainwindow import Ui_MainWindow
from clue_bot import ClueBot

def func():
    print("heyyee")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect signals
        self.ui.playGameBtn.clicked.connect(self.deal_cards)
        self.ui.submitDealtCardsBtn.clicked.connect(self.play_game)
        self.ui.submitTurnBtn.clicked.connect(self.submit_turn)
        self.ui.submitClueBotTurnBtn.clicked.connect(self.submit_cluebot_turn)

        # We have both frames visible at first, hide this one for now
        self.ui.gamePlayFrame.setVisible(False)
        self.ui.dealtCardsFrame.setVisible(False)

        # TODO remove this, we aren't changing inputs right now:
#        self.play_game()

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
        self.dealtSuspects = []
        for i in range(self.ui.dealtSuspectsVbox.layout().count()):
            widget = self.ui.dealtSuspectsVbox.layout().itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.isChecked():
                self.dealtSuspects.append(widget.text())

        self.dealtWeapons = []
        for i in range(self.ui.dealtWeaponsVbox.layout().count()):
            widget = self.ui.dealtWeaponsVbox.layout().itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.isChecked():
                self.dealtWeapons.append(widget.text())

        self.dealtRooms = []
        for i in range(self.ui.dealtRoomsVbox.layout().count()):
            widget = self.ui.dealtRoomsVbox.layout().itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.isChecked():
                self.dealtRooms.append(widget.text())


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

        # Switch UI Frames to play game Frame
        self.ui.dealtCardsFrame.setVisible(False)
        self.ui.gamePlayFrame.setVisible(True)


    def submit_turn(self):
        self.clue_bot.submit_turn()


    def submit_cluebot_turn(self):
        pass
