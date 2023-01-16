# Import widgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton
from PyQt5 import uic, QtCore
import sys, json, random

# Global Vars
dictionary = {}
keyword = ""
current_word_idx = 0
alphabet_status = ["A","E","I","O","U","\n","B","C","D","F","G","H","J","K","L","M","\n","N","P","Q","R","S","T","V","W","X","Y","Z"]

# Change bgcolor
# self.word_display[0][0].setStyleSheet("background-color: green")
# Change font color
# self.word_display[0][1].setStyleSheet("color:blue")

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # UI to be loaded
        self.setFixedSize(270, 480)
        uic.loadUi("data/wordle.ui", self)
        # Define widgets here
        self.new_game_button = self.findChild(QPushButton, "pushButton")
        self.quit_game_button = self.findChild(QPushButton, "pushButton_2")
        self.send_answer_button = self.findChild(QPushButton, "pushButton_3")
        self.input_box = self.findChild(QLineEdit, "lineEdit")
        self.input_label = self.findChild(QLabel, "label_36")
        self.letters_label = self.findChild(QLabel, "label_37")
        self.wins_label = self.findChild(QLabel, "label")
        # Text Labels
        self.word_display = []
        self.row = []
        for x in range(6,36):
            self.row.append(self.findChild(QLabel, f"label_{x}"))
            if (x % 5 == 0):
                self.word_display.append(self.row.copy())
                self.row.clear()
        # Define events here
        self.new_game_button.clicked.connect(self.newGame)
        self.quit_game_button.clicked.connect(self.quitGame)
        self.send_answer_button.clicked.connect(self.sendAnswer)
        # Load Assets
        self.loadJson()
        self.newGame()
        self.wins_label.setText(f"{dictionary['wins']} WINS")
        # Show the app
        self.show()
    
    def loadJson(self):
        '''Loads json file.'''
        global dictionary
        with open('data/userdata.json') as json_file:
            dictionary = json.load(json_file)

    def updateAndDisplayWins(self):
        '''Adds 1 to win, then updates json and win label.'''
        global dictionary
        dictionary['wins'] += 1
        self.wins_label.setText(f"{dictionary['wins']} WINS")
        with open('data/userdata.json','w') as outfile:
            json.dump(dictionary, outfile)

    def newGame(self):
        '''Fetch a word from wordle dictionary.'''
        global dictionary, keyword
        keyword = random.choice(dictionary['answers'])
        print(keyword)
        self.input_label.setText("New word fetched. Take a guess!")
        # Play Sound Effect
        self.resetGame()
        return keyword
    
    def resetGame(self):
        '''Resets game, preparation for a new game.'''
        global alphabet_status, current_word_idx
        for x in self.word_display:
            for y in x:
                y.setStyleSheet("background-color: white")
                y.setText("")
        alphabet_status = ["A","E","I","O","U","\n","B","C","D","F","G","H","J","K","L","M","\n","N","P","Q","R","S","T","V","W","X","Y","Z"]
        string = ""
        for x in alphabet_status:
            string += x + " "
        self.letters_label.setText(string)
        current_word_idx = 0
        self.send_answer_button.setEnabled(True)
        self.input_box.clear()
    
    def sendAnswer(self):
        '''Checks if answer is valid. If yes, proceed to word processing.'''
        answer = str(self.input_box.text()).lower()
        if (len(answer) == 5) & (answer in dictionary['dictionary']):
            self.input_label.setText(f"Your word is: {answer}")
            self.input_box.clear()
            self.processWord(answer)
        else:
            self.input_label.setText(f"{answer} is an invalid word, try again!")
            # Play Sound Effect
    
    def processWord(self, answer):
        '''Processes the valid word: Puts word in specific row, processes correct letters and labels.'''
        global keyword, current_word_idx, alphabet_status
        answer_list = list(answer.upper().strip(" "))
        keyword_list = list(keyword.upper().strip(" "))
        #print(answer_list+keyword_list) # FOR DEBUGGING
        # Display letters
        for i in range(0,5):
            self.word_display[current_word_idx][i].setText(answer_list[i])
        # Correct Position, Correct Letter
        for i in range(0,5):
            if answer_list[i] == keyword_list[i]:
                self.word_display[current_word_idx][i].setStyleSheet("background-color: green")
                answer_list[i] = '!'
                keyword_list[i] = '!'
        # Correct Letter
        for letter in keyword_list:
            if letter.isalpha():
                if letter in answer_list:
                    idx = answer_list.index(letter)
                    self.word_display[current_word_idx][idx].setStyleSheet("background-color: yellow")
                    answer_list[idx] = '*'
        for letter in answer_list:
            if letter.isalpha() and letter in alphabet_status:
                alphabet_status.remove(letter)
        current_word_idx += 1
        # Update Remaining Letters
        string = ""
        for x in alphabet_status:
            string += x + " "
        self.letters_label.setText(string)
        # Check current player status
        self.checkWinLose(answer_list)

    def checkWinLose(self, answer_list):
        '''Checks current player status.'''
        global current_word_idx, keyword
        if answer_list == ['!','!','!','!','!']:
            self.input_label.setText(f"You win!")
            self.send_answer_button.setEnabled(False)
            self.updateAndDisplayWins()
        elif current_word_idx == 6:
            self.input_label.setText(f"Game Over! The word is {keyword}")
            self.send_answer_button.setEnabled(False)
        

    def quitGame(self):
        '''Quits the game.'''
        quit()
    
# Initialisation
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()