import os
import sys
from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication, QDesktopWidget, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt

class App(QWidget):
	def __init__(self):
		super().__init__()
		self.title = 'File Rename'
		self.left = 0
		self.top = 0 
		self.width = 300
		self.height = 150
		self.dir = ''
		self.files = []
		self.filescopy = []
		self.log = []
		self.count = 0

	def initUI(self):
		self.makeMain()
		self.makeButton()
		self.show()

	def makeMain(self):
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setWindowTitle(self.title)
		self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		win = self.frameGeometry()
		center = QDesktopWidget().availableGeometry().center()
		win.moveCenter(center)
		self.move(win.topLeft())

	def makeButton(self):
		self.button1 = QPushButton("Folder: ", self)
		self.button1.setGeometry(30, 20, 90, 30)
		self.button1.clicked.connect(self.getDir)

		self.button2 = QPushButton("Start", self)
		self.button2.setGeometry(200, 110, 90, 30)
		self.button2.clicked.connect(self.start)

		self.label1 = QLabel("Choose Directory", self)
		self.label1.setGeometry(140, 20, 300, 20)
		self.label1.setWordWrap(True)

	def getDir(self):
		self.dialog1 = QFileDialog()
		self.dialog1.setFileMode(QFileDialog.Directory)
		if self.dialog1.exec_():
			self.dir = self.dialog1.selectedFiles()[0]
		self.label1.setText(self.dir)

	def writeLog(self):
		log = open('history.txt', 'a+')
		for file in self.filescopy:
			log.write(file + '\n')
		log.close()

	def getLog(self):
		if os.path.exists('history.txt'):
			log = open('history.txt', 'r')
			files = log.readlines()
			array = [file.strip() for file in files]
			log.close()
			return array
		else:
			return []

	def disableButton(self):
		self.button1.setEnabled(False)
		self.button2.setEnabled(False)

	def enableButton(self):
		self.button1.setEnabled(True)
		self.button2.setEnabled(True)
		self.label1.setText('Choose Directory')
		self.dir = ''
		self.files = []
		self.filescopy = []
		self.log = []
		self.count = 0

	def popWarning1(self):
		self.popup1 = QMessageBox()
		self.popup1.setWindowTitle("Warning")
		self.popup1.setText("Choose Folder")
		self.popup1.exec_()

	def popWarning2(self):
		self.popup2 = QMessageBox()
		self.popup2.setWindowTitle("Finished")
		self.popup2.setText("Completed")
		self.popup2.exec_()

	def start(self):
		if not self.dir:
			self.popWarning1()
		else:
			self.disableButton()
			self.files = [files for root, directory, files in os.walk(self.dir)][0]
			self.filescopy = self.files.copy()
			self.log = self.getLog()
			for files in self.files:
				if files not in self.log:
					exe = os.path.splitext(files)[1]
					os.rename(os.path.join(self.dir, files), os.path.join(self.dir, str(self.count) + exe))
					self.count+=1
				elif files in self.log:
					self.filescopy.remove(files)
		self.writeLog()
		self.popWarning2()
		self.enableButton()	

def main():
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
	QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
	app = QApplication(sys.argv)
	software = App()
	software.initUI()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
