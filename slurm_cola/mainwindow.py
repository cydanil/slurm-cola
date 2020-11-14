from typing import Dict, List, Tuple
import sys

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton

from .handler import handler, USERNAME


class MainWindow(QObject):
    """MainWindow is the entry point of slurm-cola.
    It contains a list of jobs for this user.
    """
    display_request = pyqtSignal(int, object)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        parent.setObjectName('mainWindow')
        parent.setWindowTitle(f'Slurm-Cola Job Administation for {USERNAME}')
        parent.resize(800, 600)

        lwJobs = QListWidget(parent)
        lwJobs.setObjectName('jobList')
        lwJobs.setGeometry(QRect(20, 30, 760, 470))
        lwJobs.setFont(QFont('monospace'))
        lwJobs.itemDoubleClicked.connect(self.open_properties)
        self.lwJobs = lwJobs

        pbLog = QPushButton(parent)
        pbLog.setObjectName('pbLog')
        pbLog.setGeometry(QRect(260, 540, 100, 40))
        pbLog.setText('View Logs')
        self.pbLog = pbLog

        pbProperties = QPushButton(parent)
        pbProperties.setObjectName('pbProperties')
        pbProperties.setGeometry(QRect(400, 540, 100, 40))
        pbProperties.setText('Properties')
        pbProperties.setToolTip("The selected job's properties")
        pbProperties.clicked.connect(self.on_pbProperties_clicked)

        pbRefresh = QPushButton(parent)
        pbRefresh.setObjectName('pbRefresh')
        pbRefresh.setGeometry(QRect(540, 540, 100, 40))
        pbRefresh.setText('Refresh')
        pbRefresh.setToolTip(f"Rescan {USERNAME} jobs")
        pbRefresh.clicked.connect(self.list_jobs)

        pbQuit = QPushButton(parent)
        pbQuit.setObjectName('pbQuit')
        pbQuit.setGeometry(QRect(680, 540, 100, 40))
        pbQuit.setText('Quit')
        pbQuit.clicked.connect(sys.exit)

        # self.jobs is set in self.list_jobs()
        self.jobs: Dict[int: Dict[str, str]] = None

    def list_jobs(self):
        self.lwJobs.clear()
        self.jobs = handler.list_jobs()

        if self.jobs is None:
            self.lwJobs.addItem(f'Nothing running for {USERNAME} now')
            return

        # Group jobs by their name
        groups: List[List[Tuple[int, Dict[str, str]]]] = []
        previous = None
        group = []
        for job_id, properties in self.jobs.items():
            if properties['JobName'] != previous:
                groups.append(group)
                group = []
                previous = properties['JobName']
            group.append((job_id, properties))
        groups.append(group)

        groups = groups[1:]  # FIXME: hack to work around the initial None

        for group in groups:
            for job_id, properties in group:
                line = (str(job_id) + '    '
                        + properties['JobState'] + '    '
                        + properties['StartTime'] + '    '
                        + properties['NodeList'] + '    '
                        + properties['JobName'])
                self.lwJobs.addItem(line)
            self.lwJobs.addItem('')

    @pyqtSlot(QListWidgetItem)
    def open_properties(self, item):
        if item is None or not item.text() or 'Nothing running' in item.text():
            return

        job = int(item.text().split()[0])
        properties = self.jobs[job]

        self.display_request.emit(job, properties)

    def on_pbProperties_clicked(self):
        item = self.lwJobs.currentItem()
        if item is None:
            item = self.lwJobs.item(0)
        self.open_properties(item)
