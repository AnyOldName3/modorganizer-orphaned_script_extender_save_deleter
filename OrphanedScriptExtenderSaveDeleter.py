import sys

from glob import glob

from PyQt5.QtCore import QCoreApplication, qDebug
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

if "mobase" not in sys.modules:
    import mock_mobase as mobase

class OrphanedScriptExtenderSaveDeleter(mobase.IPluginTool):
    
    def __init__(self):
        super(OrphanedScriptExtenderSaveDeleter, self).__init__()
        self.__organizer = None
        self.__parentWidget = None

    def init(self, organizer):
        self.__organizer = organizer
        return True

    def name(self):
        return "Orphaned Script Extender Save Deleter"

    def author(self):
        return "AnyOldName3"

    def description(self):
        return self.__tr("Deletes script extender saves which don't have a corresponding base game save.")

    def version(self):
        return mobase.VersionInfo(1, 0, 0, mobase.ReleaseType.final)

    def isActive(self):
        return True

    def settings(self):
        return []

    def displayName(self):
        return self.__tr("Orphaned Script Extender Save Deleter")

    def tooltip(self):
        return self.__tr("Deletes script extender saves which don't have a corresponding base game save.")

    def icon(self):
        return QIcon()

    def setParentWidget(self, widget):
        self.__parentWidget = widget
    
    def display(self):
        # Give the user the opportunity to abort
        confirmationButton = QMessageBox.question(self.__parentWidget, self.__tr("Before starting deletion..."), self.__tr("Please double check that you want your orphaned script extender saves deleted. If you proceed, you won't be able to get them back, even if you find you've copied the corresponding base game save somewhere else so still have a copy."), QMessageBox.StandardButtons(QMessageBox.Ok | QMessageBox.Cancel))
        if confirmationButton != QMessageBox.Ok:
            return
        managedGame = self.__organizer.managedGame()
        gameSaveExtension = managedGame.savegameExtension()
        skseSaveExtension = managedGame.savegameSEExtension()
        gameSavesDirectory = managedGame.savesDirectory().absolutePath()
        if self.__organizer.profile().localSavesEnabled():
            gameSavesDirectory = os.path.join(self.__organizer.profile().absolutePath(), "saves")
        count = 0
        for cosave in glob(os.path.join(gameSavesDirectory, "*." + skseSaveExtension)):
            saveName = os.path.splitext(cosave)[0]
            if not os.path.isfile(saveName + "." + gameSaveExtension):
                os.remove(cosave)
                count += 1
        if count == 0:
            QMessageBox.information(self.__parentWidget, self.__tr("No orphaned script extender saves found"), self.__tr("No orphaned script extender co-saves were found, so none were removed."))
        else:
            QMessageBox.information(self.__parentWidget, self.__tr("Orphaned script extender saves removed"), self.__tr("{0} orphaned script extender co-save(s) removed successfully.").format(count))
    
    def __tr(self, str):
        return QCoreApplication.translate("OrphanedScriptExtenderSaveDeleter", str)
    
def createPlugin():
    return OrphanedScriptExtenderSaveDeleter()