# -*- coding: utf-8 -*-
# bulkrename/views.py

from collections import deque
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QWidget
from .ui.window import Ui_MainWindow
from PyQt5.QtCore import QThread
from .rename import Renamer

FILTERS = ";;".join(
    (
        "All files (*)",
        "PNG Files (*.png)",
        "JPEG Files (*.jpeg)",
        "JPG Files (*.jpg)",
        "GIF Files (*.gif)",
        "Text Files (*.txt)",
        "Python Files (*.py)",
        "Icon Files (*.ico)",
        "ISO Files (*.iso)",
        "Floppy Disk Images (*.img)",
    )
)

class Window(QWidget, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self._files = deque()
        self._filesCount = len(self._files)
        self._setupUI()
        self._connectSignalsSlots()

    def _setupUI(self):
        self.setupUi(self)
    def renameFiles(self):
        self._runRenamerThread()
    def _updateProgressBar(self, fileNumber):
        progressPercent = int(fileNumber / self._filesCount * 100)
        self.progressBar.setValue(progressPercent)
    def _runRenamerThread(self):
        prefix = self.FilenamePrefix.toPlainText()
        self._thread = QThread()
        self._renamer = Renamer(
            files=tuple(self._files),
            prefix=prefix,
        )
        self._renamer.moveToThread(self._thread)
        self._thread.started.connect(self._renamer.renameFiles)
        self._renamer.renamedFile.connect(self._updateStateWhenFileRenamed)
        self._renamer.progressed.connect(self._updateProgressBar)
        self._renamer.finished.connect(self._thread.quit)
        self._renamer.finished.connect(self._renamer.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()
    def _updateStateWhenFileRenamed(self, newFile):
        self._files.popleft()
        self.listWidget.takeItem(0)
        self.listWidget_2.addItem(str(newFile))
    def _connectSignalsSlots(self):
        self.LoadBTN.clicked.connect(self.loadFiles)
        self.RenameBTN.clicked.connect(self.renameFiles)

    def loadFiles(self):
        self.listWidget_2.clear()
        if self.LastSourceDirectory.toPlainText() is not None:
            initDir = self.LastSourceDirectory.toPlainText()
        else:
            initDir = str(Path.home())
        files, filter = QFileDialog.getOpenFileNames(
            self, "Choose Files to Rename", initDir, filter=FILTERS
        )
        if len(files) > 0:
            fileExtension = filter[filter.index("*") : -1]
            self.ExtensionLBL.setText(fileExtension)
            srcDirName = str(Path(files[0]).parent)
            self.LastSourceDirectory.setText(srcDirName)
            for file in files:
                self._files.append(Path(file))
                self.listWidget.addItem(file)
            self._filesCount = len(self._files)