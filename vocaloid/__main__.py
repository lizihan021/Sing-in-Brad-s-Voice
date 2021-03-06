import sys, os, io
# sys.path.insert(0,'../')
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPalette, QBrush, QKeyEvent, QIcon
from PyQt5.QtCore import QSize, QCoreApplication, QThreadPool, QRunnable, Qt, QUrl, QDir, QEvent
from PyQt5.QtMultimedia import QSound, QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtCore
from mido.sockets import PortServer, connect
import mido
from urllib.parse import *
from urllib.request import *
import time

from .gui.mainUI import MainUI
from vocaloid.utils import *
from vocaloid.syllablesParser import *
from vocaloid.song import *
from vocaloid.midiMonitor import *

import qdarkstyle
import pyaudio
import wave
from threading import Thread
import subprocess, traceback

import simpleaudio as sa

MAX_NUM_SYLLABLES = 36
# for audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 1
RATE = 16000 #sample rate
WAVE_OUTPUT_FILENAME = "./tmp/recorded.wav"

class MainWindow(QMainWindow, MainUI, QRunnable):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.tutorialButton.clicked.connect(self.onTutorialButtonClick)
        self.startButton.clicked.connect(self.onStartButtonClick)
        self.video = VideoWindow(self)
        self.lyricsFilePath = ""
        self.lyrics = ""
        self.syllables = []
        self.page_num = 0
        self.song = Song("", self)
        self.curr_len = 2 # It's a quarter note.
        self.threadpool = QThreadPool()
        # for recording:
        self.onRecording = False
        self.midiStart = False
        self.recordThread = 0
        if not os.path.exists("./tmp"):
            os.makedirs("./tmp")


    def onStartButtonClick(self):
        self.setupUi2(self)
        self.page_num = 1
        self.chooseButton.clicked.connect(self.openFile)
        self.nextButton.clicked.connect(self.loadFile)
        self.recordButton.clicked.connect(self.recordSound)
        self.backButton.clicked.connect(self.onBackButtonClick)


    def onTutorialButtonClick(self):
        self.video.resize(1080, 720)
        self.video.show()


    def onBackButtonClick(self):
        self.setupUi(self)
        self.page_num = 0
        self.tutorialButton.clicked.connect(self.onTutorialButtonClick)
        self.startButton.clicked.connect(self.onStartButtonClick)


    def onBack2ButtonClick(self):
        self.setupUi2(self)
        self.page_num = 1
        self.lyrics = ""
        self.syllables = []
        self.lyricsFilePath = ""
        self.song = Song("", self)
        self.curr_len = 2
        self.chooseButton.clicked.connect(self.openFile)
        self.nextButton.clicked.connect(self.loadFile)
        self.recordButton.clicked.connect(self.recordSound)
        self.backButton.clicked.connect(self.onBackButtonClick)

    def recordSound(self):
        if self.onRecording:
            # TODO enable buttons.
            self.onRecording = False
            self.recordThread.join()
            if not os.path.isfile(WAVE_OUTPUT_FILENAME):
                self.textEdit.setText("Error! Check whether the recorded audio exist.")
                return
            self.lyrics = self.ask_google_for_text(WAVE_OUTPUT_FILENAME)
            self.textEdit.setText(self.lyrics)
            self.chooseButton.setEnabled(True)
            self.nextButton.setEnabled(True)
            self.backButton.setEnabled(True)
        else:
            # TODO disable buttons
            self.chooseButton.setEnabled(False)
            self.nextButton.setEnabled(False)
            self.backButton.setEnabled(False)
            self.onRecording = True
            self.recordThread = Thread(target = self.record_and_save_to_file, args = ( ))
            self.recordThread.start()

    def record_and_save_to_file(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK) #buffer

        print("* recording")
        self.recordButton.setStyleSheet("background-color: #881111;font: 36pt 'Arial';")
        self.recordButton.setText("Recording...")
        frames = []
        while self.onRecording:
            data = stream.read(CHUNK)
            frames.append(data) # 2 bytes(16 bits) per channel
        print("* done recording")
        self.recordButton.setStyleSheet("background-color: #31363b;font: 36pt 'Arial';")
        self.recordButton.setText("Record Lyrics")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def ask_google_for_text(self, speech_file):
        """Transcribe the given audio file."""
        from google.cloud import speech
        from google.cloud.speech import enums
        from google.cloud.speech import types
        client = speech.SpeechClient()

        with io.open(speech_file, 'rb') as audio_file:
            content = audio_file.read()

        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US')
        response = client.recognize(config, audio)
        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            print('Transcript: {}'.format(result.alternatives[0].transcript))
            return result.alternatives[0].transcript

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Lyrics File Selection", "","Text files (*.txt)", options=options)
        if fileName:
            self.lyricsFilePath = fileName
            self.fileLabel.setText(fileName.split("/")[-1])
            self.lyrics = get_lyrics_from_filepath(self.lyricsFilePath)
            self.textEdit.setText(self.lyrics)


    def loadFile(self):
        self.lyrics = self.textEdit.toPlainText()
        if self.lyrics == '':
            QMessageBox.critical(self, "Error", "You must input the lyrics to generate a song!")
            return
        self.syllables = parse_syllables(self.lyrics)
        phonemes_list = parse_phonemes(get_phonemes(get_ssml(self.lyrics)))
        if phonemes_list is None or len(self.syllables) != len(phonemes_list):
            QMessageBox.critical(self, "Error", "Sorry, the lyrics you just entered cannot be parsed correctly! Please try again.")
            self.syllables = []
            self.lyrics = ""
            return
        self.song.addLyrics(self.lyrics)
        self.setupUi5(self)
        self.page_num = 2
        # print(self.page_num)
        self.back5Button.clicked.connect(self.onBack2ButtonClick)
        self.next5Button.clicked.connect(self.onNext2ButtonClick)
        self.next5Button.setEnabled(False)

        self.setNoteImg()
        self.sylLabel.setText(self.syllables[0])
        if self.midiStart == False:
            midiListener = MidiListener(self)
            self.threadpool.start(midiListener)
            midiMonitor = MidiMonitor()
            self.threadpool.start(midiMonitor)
            self.midiStart = True


    def renderSyllables(self, syllables):
        for i, syl in enumerate(syllables):
            # Sorry, the UI now can only handle 35 syllables...
            if i >= MAX_NUM_SYLLABLES:
                print("too many syllables in the lyrics")
                break
            label = getattr(self, "label_%i" % i)
            label.setText(syl)
        midiListener = MidiListener(self)
        self.threadpool.start(midiListener)
        midiMonitor = MidiMonitor()
        self.threadpool.start(midiMonitor)


    def onBack4ButtonClick(self):
        self.setupUi5(self)
        self.page_num = 2
        self.back5Button.clicked.connect(self.onBack2ButtonClick)
        self.next5Button.clicked.connect(self.onNext2ButtonClick)
        self.song.displayMusic()


    def onNext2ButtonClick(self):
        if len(self.song.notes) == 0:
            q = QMessageBox()
            q.setText("Warning: You have not entered any note!")
            # q.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            q.setStandardButtons(QMessageBox.Ok)
            q.setIcon(QMessageBox.Warning)
            button = q.exec()
            if button == QMessageBox.Ok:
                return
        self.setupUi4(self)
        self.page_num = 3
        self.listVoices()
        self.comboBox.currentIndexChanged.connect(self.voiceSelection)
        if self.generateButton.text() == "Generate Song":
            self.generateButton.clicked.connect(lambda: self.generateSong(self.comboBox.currentText()))
        elif self.generateButton.text() == "Play":
            self.generateButton.clicked.connect(self.playSong)
        self.restartButton.clicked.connect(self.restartProgram)
        self.back4Button.clicked.connect(self.onBack4ButtonClick)
        self.exitButton.clicked.connect(self.exitProgram)


    def voiceSelection(self, i):
        self.generateButton.setText("Generate Song")
        self.generateButton.clicked.connect(lambda: self.generateSong(self.comboBox.currentText()))


    def restartProgram(self):
        self.setupUi(self)
        self.page_num = 0
        print(self.page_num)
        self.tutorialButton.clicked.connect(self.onTutorialButtonClick)
        self.startButton.clicked.connect(self.onStartButtonClick)
        self.lyricsFilePath = ""
        self.lyrics = ""
        self.syllables = []
        self.song = Song("", self)
        self.curr_len = 2 # It's a quarter note.


    def exitProgram(self):
        sys.exit()


    def listVoices(self):
        get_voice = "http://localhost:59125/voices"
        with urlopen(get_voice) as response:
            html = response.read()
        html = str(html)
        html = html[2:]
        html = html[:-3]
        voices = html.split("\\n")
        for voice in voices:
            self.comboBox.addItem(voice.split()[0])


    def generateSong(self, voice):
        if self.generateButton.text() == "Play":
            return
        # print("generate")
        # traceback.print_stack()
        xml = self.song.convertToMaryXML()
        file = open("./tmp/song.xml", "w")
        file.write(xml);
        file.close();
        host_name = "http://localhost"
        port_num = ":59125"
        operation = "/process?"
        input_text = xml
        input_type = "RAWMARYXML"
        output_type = "AUDIO"
        locale = "en_US"
        audio = "WAVE_FILE"
        # voice = "brad_s_voice-hsmm"
        get_string = host_name + port_num + operation + "INPUT_TEXT=" \
                     + quote_plus(xml) + "&INPUT_TYPE=" + input_type \
                     + "&OUTPUT_TYPE=" + output_type + "&LOCALE=" + locale\
                     + "&AUDIO=" + audio + "&VOICE=" + voice
        urlopen(get_string)
        self.soundfilename = './tmp/speech.wav'
        urlretrieve(get_string, self.soundfilename)
        self.generateButton.setText("Play")
        self.generateButton.clicked.connect(self.playSong)


    def playSong(self):
        QSound.play(self.soundfilename)


    def setNoteImg(self):
        wholePm = QPixmap("library/whole.png")
        halfPm = QPixmap("library/half.png")
        quarterPm = QPixmap("library/quarter.png")
        eighthPm = QPixmap("library/eighth.png")
        try:
            if self.curr_len == 1:
                self.noteLabel.setPixmap(eighthPm)
            elif self.curr_len == 2:
                self.noteLabel.setPixmap(quarterPm)
            elif self.curr_len == 3:
                self.noteLabel.setPixmap(halfPm)
            elif self.curr_len == 4:
                self.noteLabel.setPixmap(wholePm)
            self.noteLabel.adjustSize()
            self.noteLabel.show()
        except:
            return


    def keyPressEvent(self, event):
        if self.page_num == 2 and type(event) == QKeyEvent:
            key = event.key()
            if event.key() == Qt.Key_D and self.curr_len < 4:
                self.curr_len += 1
                self.setNoteImg()
            elif event.key() == Qt.Key_H and self.curr_len > 1:
                self.curr_len -= 1
                self.setNoteImg()
            elif event.key() == Qt.Key_R:
                self.song.addRest(self.curr_len)
            elif event.key() == Qt.Key_X:
                self.song.deleteNote(self.song.curr_note - 1)
            elif event.key() == Qt.Key_Plus:
                if self.song.num_notes + self.song.num_rest > self.song.curr_note:
                    self.song.curr_note += 1
                    self.song.convertToLilyPond()
            elif event.key() == Qt.Key_Minus:
                if self.song.curr_note > 0:
                    self.song.curr_note -= 1
                    self.song.convertToLilyPond()
            elif event.key() in [Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7]:
                octave = 3
                pitch = [Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7].index(key)
                if pitch <= 2:
                    pitch *= 2
                else:
                    pitch = pitch * 2 - 1
                print(pitch)
                length = self.curr_len
                self.song.addNote(octave, pitch, length)
                notation_map = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b"]
                wave_obj = sa.WaveObject.from_wave_file("library/" + notation_map[pitch] + str(octave - 1) + ".wav")
                play_obj = wave_obj.play()
            elif event.key() in [Qt.Key_8, Qt.Key_9, Qt.Key_0, Qt.Key_U, Qt.Key_I, Qt.Key_O, Qt.Key_P]:
                octave = 4
                pitch = [Qt.Key_8, Qt.Key_9, Qt.Key_0, Qt.Key_U, Qt.Key_I, Qt.Key_O, Qt.Key_P].index(key)
                if pitch <= 2:
                    pitch *= 2
                else:
                    pitch = pitch * 2 - 1
                length = self.curr_len
                self.song.addNote(octave, pitch, length)
                notation_map = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b"]
                wave_obj = sa.WaveObject.from_wave_file("library/" + notation_map[pitch] + str(octave - 1) + ".wav")
                play_obj = wave_obj.play()
            event.accept()
        else:
            event.ignore()


class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Tutorial")
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        wid = QWidget(self)
        self.setCentralWidget(wid)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(os.getcwd() + "/tutorial/EECS498 Vocaloid Tutorial.mp4")))
        self.playButton.setEnabled(True)


    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())



class MidiListener(QRunnable):
    def __init__(self, window_in):
        super().__init__()
        self.window = window_in


    @pyqtSlot()
    def run(self):
        try:
            server = PortServer('localhost', 8080)
        except:
            print("midi listener already up!")
            return

        for message in server:
            if self.window.page_num != 2:
                return
            if message.type == 'note_on':
                C0 = 24
                octave = (message.note - C0) // 12
                pitch = (message.note - C0) % 12
                length = self.window.curr_len
                if octave == 4 or octave == 3:
                    self.window.song.addNote(octave, pitch, length)
                    notation_map = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b"]
                    wave_obj = sa.WaveObject.from_wave_file("library/" + notation_map[pitch] + str(octave - 1) + ".wav")
                    play_obj = wave_obj.play()


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()