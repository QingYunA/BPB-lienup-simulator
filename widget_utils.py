from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem, QLabel
from pathlib import Path
from PyQt5.QtGui import QTransform
import time


class ItemBasic(QListWidget):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        mouse_track: bool = True,
    ):
        super().__init__(parent)

        self.setViewMode(QListWidget.IconMode)
        # self.setResizeMode(QListWidget.Adjust)
        # self.setMovement(QListWidget.Static)
        # self.setDragEnabled(True)
        # self.setDragDropMode(QListWidget.InternalMove)
        self.setMouseTracking(mouse_track)


class ItemList(ItemBasic):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        path: str = None,
        icon_size: list = [50, 50],
        mouse_track: bool = True,
    ):
        super().__init__(parent, mouse_track=mouse_track)
        # *  attributes
        self.icon_w, self.icon_h = icon_size
        self.transform = QTransform().rotate(90)
        self.have_released = True
        self.left_button = False
        self.left_right_button = False
        self.clicked_item = False
        self.copy_widget = None
        self.icon_size = icon_size
        if path:
            self.img_list = sorted(Path(path).glob("*.png"))
            self.add_img()
        # * set icon size
        self.setIconSize(QtCore.QSize(self.icon_w, self.icon_h))
        # * connect signal
        self.itemPressed.connect(self.pressed_event)

    def pressed_event(self, item: QListWidgetItem):
        # * new plabel
        if not self.left_button:
            self.pixmap = (
                item.icon().pixmap(self.icon_h, self.icon_w).scaled(int(self.icon_h * 1.75), int(self.icon_w * 1.75))
            )
            self.clicked_item = True

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)
        if e.buttons() == QtCore.Qt.RightButton | QtCore.Qt.LeftButton and self.clicked_item and self.left_button:
            self.left_right_button = True
            self.pixmap = self.pixmap.transformed(self.transform)
            self.copy_widget.setPixmap(self.pixmap)
            self.left_right_button = False
            self.copy_widget.show()
        if e.buttons() == QtCore.Qt.LeftButton and self.clicked_item:
            self.left_button = True
            self.copy_widget = QLabel(self)
            self.copy_widget.setPixmap(self.pixmap)
            self.copy_widget.setScaledContents(True)

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        if self.left_button and self.clicked_item:
            x = e.x() - int(self.copy_widget.width() / 2)
            y = e.y() - int(self.copy_widget.height() / 2)
            cor = QPoint(x, y)
            self.copy_widget.move(self.mapToParent(cor))
            self.copy_widget.show()

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        if e.button() == QtCore.Qt.LeftButton:
            self.left_button = False

    def add_img(self):
        for i in self.img_list:
            item = QListWidgetItem()
            pixmap = QtGui.QPixmap(str(i)).scaled(self.icon_w, self.icon_h)
            icon = QtGui.QIcon(pixmap)
            item.setToolTip(f"{i.stem}")
            item.setIcon(icon)
            self.addItem(item)


class BagList(ItemBasic):
    def __init__(self, parent: QtWidgets.QWidget | None = None, mouse_track: bool = True):
        super().__init__(parent, mouse_track)
