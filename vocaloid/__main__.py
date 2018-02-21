import sys, os
# sys.path.insert(0,'../')
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPalette, QBrush, QKeyEvent
from PyQt5.QtCore import QSize, QCoreApplication, QThreadPool, QRunnable
from PyQt5.QtMultimedia import QSound
from mido.sockets import PortServer, connect
import mido
from urllib.parse import *
from urllib.request import *
import time

# from .gui.mainwindow_ui import Ui_MainWindow as mainWindow
from .gui.mainUI import MainUI
from vocaloid.utils import *
from vocaloid.syllablesParser import *
# from midiLoader import *
from vocaloid.song import *
# from midiListener import *
from vocaloid.midiMonitor import *


class MainWindow(QMainWindow, MainUI, QRunnable):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.tutorialButton.clicked.connect(self.onTutorialButtonClick)
        self.startButton.clicked.connect(self.onStartButtonClick)
        self.lyricsFilePath = ""
        self.lyrics = ""
        self.syllables = []
        self.song = Song("")
        self.threadpool = QThreadPool()


    def onStartButtonClick(self):
        self.setupUi2(self)
        self.chooseButton.clicked.connect(self.openFile)
        self.nextButton.clicked.connect(self.loadFile)
        self.backButton.clicked.connect(self.onBackButtonClick)


    def onTutorialButtonClick(self):
        print("Try tutorial!")


    def onBackButtonClick(self):
        self.setupUi(self)
        self.tutorialButton.clicked.connect(self.onTutorialButtonClick)
        self.startButton.clicked.connect(self.onStartButtonClick)


    def onBack2ButtonClick(self):
        self.setupUi2(self)
        self.chooseButton.clicked.connect(self.openFile)
        self.nextButton.clicked.connect(self.loadFile)
        self.backButton.clicked.connect(self.onBackButtonClick)


    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)
        if fileName:
            self.lyricsFilePath = fileName
            self.fileLabel.setText(fileName.split("/")[-1])
            self.lyrics = get_lyrics_from_filepath(self.lyricsFilePath)
            self.textEdit.setText(self.lyrics)


    def loadFile(self):
        if self.lyricsFilePath:
            self.lyrics = get_lyrics_from_filepath(self.lyricsFilePath)
        else:
            self.lyrics = self.textEdit.toPlainText()
        self.song.addLyrics(self.lyrics)
        self.syllables = parse_syllables(self.lyrics)
        self.setupUi3(self)
        self.back2Button.clicked.connect(self.onBack2ButtonClick)
        self.next2Button.clicked.connect(self.onNext2ButtonClick)
        self.renderSyllables(self.syllables)


    def renderSyllables(self, syllables):
        for i, syl in enumerate(syllables):
            # Sorry, the UI now can only handle 35 syllables...
            if i > 35:
                print("too many syllables in the lyrics")
                break
            label = getattr(self, "label_%i" % i)
            label.setText(syl)
        midiListener = MidiListener(self)
        self.threadpool.start(midiListener)
        midiMonitor = MidiMonitor()
        self.threadpool.start(midiMonitor)


    def onNext2ButtonClick(self):
        self.setupUi4(self)
        self.generateButton.clicked.connect(self.generateSong)
        self.playButton.clicked.connect(self.playSong)
        self.playButton.setDisabled(True)


    def generateSong(self):
        self.song.convertToMaryXML()
        xml_file = open("song.xml")
        xml = xml_file.read()
        host_name = "http://localhost"
        port_num = ":59125"
        operation = "/process?"
        input_text = xml
        input_type = "RAWMARYXML"
        output_type = "AUDIO"
        locale = "en_US"
        audio = "WAVE_FILE"
        get_string = host_name + port_num + operation + "INPUT_TEXT=" \
                     + quote_plus(xml) + "&INPUT_TYPE=" + input_type \
                     + "&OUTPUT_TYPE=" + output_type + "&LOCALE=" + locale\
                     + "&AUDIO=" + audio
        urlopen(get_string)
        self.soundfilename = 'speech.wav'
        urlretrieve(get_string, self.soundfilename)
        self.playButton.setDisabled(False)


    def playSong(self):
        QSound.play(self.soundfilename)


class MidiListener(QRunnable):
    def __init__(self, window_in):
        super().__init__()
        self.window = window_in
        self.num = 0

    @pyqtSlot()
    def run(self):
        for message in PortServer('localhost', 8080):
            if message.type == 'note_on':
                if self.num > 35:
                    continue
                label = getattr(self.window, "label_" + str(self.num))
                C0 = 24
                octave = (message.note - C0) // 12
                pitch = (message.note - C0) % 12
                length = 1
                self.window.song.addNote(octave, pitch, length)
                notation = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
                syllable = label.text()
                note_info = syllable + "\n" + notation[pitch] + " " + str(octave) + "\n" + "whole"
                label.setText(note_info)
                self.num += 1



def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()