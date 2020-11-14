from typing import Dict

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QRect, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QDialog, QGroupBox, QLineEdit,
                             QMessageBox, QPushButton, QTextEdit)

from .handler import handler


class JobWindow(QObject):
    """JobWindow lists all the information found in a job dictionary."""
    done = pyqtSignal()
    log = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        if parent is None:
            parent = QDialog()
        parent.setObjectName('jobProperties')
        parent.setWindowTitle('Job Properties')
        parent.setModal(False)
        parent.resize(630, 430)
        self.parent = parent

        # job id display
        gbJobId = QGroupBox(parent)
        gbJobId.setObjectName('gbJobId')
        gbJobId.setTitle('Job ID')
        gbJobId.setGeometry(QRect(190, 5, 250, 60))

        leJobId = QLineEdit(gbJobId)
        leJobId.setObjectName('leJobId')
        leJobId.setGeometry(QRect(10, 25, 230, 30))
        leJobId.setAlignment(Qt.AlignHCenter)
        leJobId.setReadOnly(True)
        self.leJobId = leJobId

        teProperties = QTextEdit(parent)
        teProperties.setObjectName('teProperties')
        teProperties.setGeometry(QRect(10, 70, 605, 290))
        teProperties.setFont(QFont('monospace'))
        teProperties.setReadOnly(True)
        self.teProperties = teProperties

        pbCancelJob = QPushButton(parent)
        pbCancelJob.setObjectName('pbCancelJob')
        pbCancelJob.setText('Cancel Job')
        pbCancelJob.setGeometry(QRect(354, 370, 116, 40))
        pbCancelJob.clicked.connect(self.cancel_job)
        pbCancelJob.setToolTip('scancel the slurm job')

        pbClose = QPushButton(parent)
        pbClose.setObjectName('pbClose')
        pbClose.setText('Close Window')
        pbClose.setGeometry(QRect(490, 370, 116, 40))
        pbClose.clicked.connect(parent.close)

    @pyqtSlot(int, object)
    def show(self, job_id: int, properties: Dict[str, str]):
        self.parent.setWindowTitle(f'Job {job_id} Properties')
        self.leJobId.setText(str(job_id))
        props = '\n'.join(f'{key}: {val}' for key, val in properties.items())
        self.teProperties.setText(props)
        self.parent.show()

    def cancel_job(self):
        job = int(self.leJobId.text())
        self.log.emit(f'Requesting cancellation for {job}.')
        ret = handler.cancel_job([job])

        if ret.returncode != 0:
            error = ret.stderr.decode()
            msg = f'There was an issue cancelling <b>{job}</b>:\n {error}'
            self.log.emit(msg)
            QMessageBox.warning(self.parent, 'Oops', msg)