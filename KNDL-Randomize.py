# Program that randomizes Kirby: Nightmare in Dream Land for GBA
# Written by Aquova, 2017-2018
# http://github.com/Aquova/KNDL-Rando

from PyQt5 import QtWidgets
import os, random, sys, hashlib
from mainwindow import Ui_MainWindow

VERSION = '1.0.0'

# Valid byte values for Kirby's ability
ability_values = ["00","01","02","03","04","05","06","07","08","09","0A","0B","0C",
                "0D","0E","0F","10","11","12","13","14","15","16","17","18"]

# ROM locations of enemy abilities
ability_locations = ["7417C4", "7429F4", "740C38", "743344", "742A20", "7417F0", "742A4C",
                     "7418A0", "740C64", "740C90", "7418F8", "742B28", "741924", "741950",
                     "740CE8", "740D14", "741A58", "741A84", "740D6C", "740D98", "740DC4"]

# ROM locations of Kirby's palette
palette_locations = ["DC62A", "DC8AA", "DC96C", "DCB2A", "DCBAA", "DD0C4", "DD0E6", "DD23A", "DD306",
                     "E7418", "E745C", "E74A0", "E9D5C", "E9D7E", "E9ED2", "E9F9E", "F997C", "F997C",
                     "F99C0", "F9A04", "FEFFC", "FF01E", "FF172", "FF23E", "108364", "1083A8", "1083EC",
                     "10C260", "10C282", "10C3D6", "10C4A2", "123604", "123648", "12368C", "12A6DC",
                     "12A6FE", "12A852", "12A91E", "137F80", "137FC4", "138008", "13BF44", "13BF66",
                     "13C0BA", "13C186", "149734", "149778", "14D078", "14D09A", "14D1EE", "14D2BA",
                     "150320", "150364", "1503A8", "1517E4", "151806", "15197C", "151A48", "153810",
                     "153854", "153898", "1543E0", "154402", "154600", "15ECE0", "15ED24", "15ED68",
                     "162678", "16269A", "166CE4", "166D06", "166F04", "16FCF0", "16FD34", "16FD78",
                     "172448", "17246A", "1751A0", "1751C2", "175316", "1753E2", "17C3E4", "17C428",
                     "1801E4", "180206", "18035A", "180426", "183F34", "183F78", "183FBC", "1845E8",
                     "18460A", "18464E", "186C7C", "186C9E", "189714", "189736", "196E48", "196E6A",
                     "1A1890", "1A394C", "1A7818", "1A8830", "1A9D94", "1AB300", "1AC5CC", "1AD30C",
                     "1AE878", "1AF444", "1B19EC", "1B3E14", "1B66FC", "1B6E34", "1BC074", "1BE6BE",
                     "1BE8C0", "1BEFF8", "1C051C", "1C7260", "1C9890", "1CC7EC", "1CC82E", "1CF814",
                     "1D4348", "1D60B8", "1D9F20", "1E1F28", "1E1F6A", "1F0074", "1F0096", "1F1F4C",
                     "1F5A34", "1FA7E0", "1FB9D8", "1FDF58", "1FDF9A", "201374", "203BF4", "20D1E4",
                     "218CD4", "21C3D0", "21DEF0", "23F834", "23F988", "23FA54", "23FA98", "2476A0",
                     "2476E4", "24A9FC", "53F4E6", "596D22", "599922", "5BA46E", "5BD09A", "5BF426",
                     "5C220E", "5C4AAA", "5C7452", "5C9B22", "5CCC90", "5CCCD2", "5E2C22", "609D42", "7DB192"]

new_palette = ["2104F953F01BCF136D07880606068305FC055A051205", # Green
               "2104FF077F07FF06DD061606B1054C059F047C043604", # Yellow
               "2104BF563F203C18571053084E082A043F543C383718", # Red
               "2104FF7FFF7F9C731863734EEF3D6B2D5F35BB243718", # Snow
               "21043146EF3DAD356B2D29250821C6189F0A1F067A05", # Carbon
               "2104F57F927F0E7F8B7E067EA365E6408D7D2A71875C", # Ocean
               "2104577F907A2D72EB69615D0151A1402B60294C2838", # Sapphire
               "21041A7F977EF57D727D4F6CCD05AA383745B338302C", # Grape
               "2104F873EF63684FA13A2136C12D6121BF2A1C169805", # Emerald
               "2104DF07FF129F121F169F193911D10C5F05F9049104", # Orange
               "21049B4A3B36D82D7425111DCE148B10B41071082F04", # Chocolate
               "21047F7F7F721F66BF55FC3C74206D0CA432272EC621", # Cherry
               "2104FF7F9C7318639452EF3D6B2DE71C10428C312925"] # Chalk

# Creating a custom exception, how fancy
class HashError(Exception):
    pass

class KirbyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(KirbyApp, self).__init__(parent)
        self.setupUi(self)
        self.findROMButton.clicked.connect(self.open_file)
        self.randomizeButton.clicked.connect(self.runRandomizer)
        self.title.setText(self.title.text() + VERSION)

        # Fades out starRodCheck if not clicked
        self.starRodCheck.setEnabled(False)
        self.enemyCheck.toggled.connect(self.starRodCheck.setEnabled)
        self.enemyCheck.toggled.connect(
            lambda checked: not checked and self.starRodCheck.setChecked(False))

    # Opens ROM selector window, clears the previous path text
    def open_file(self):
        self.romDisplay.clear()
        self.rom_file = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", os.path.dirname(__file__), "GBA ROMs (*.gba)")[0]
        if self.rom_file:
            self.romDisplay.setText(self.rom_file)

    def selectedColor(self):
        if self.greenColor.isChecked():
            return 0
        elif self.yellowColor.isChecked():
            return 1
        elif self.redColor.isChecked():
            return 2
        elif self.snowColor.isChecked():
            return 3
        elif self.carbonColor.isChecked():
            return 4
        elif self.oceanColor.isChecked():
            return 5
        elif self.sapphireColor.isChecked():
            return 6
        elif self.grapeColor.isChecked():
            return 7
        elif self.emeraldColor.isChecked():
            return 8
        elif self.orangeColor.isChecked():
            return 9
        elif self.chocolateColor.isChecked():
            return 10
        elif self.cherryColor.isChecked():
            return 11
        elif self.chalkColor.isChecked():
            return 12
        elif self.randomColor.isChecked():
            return random.randint(0,12)

    def runRandomizer(self):
        try:
            rom = open(self.rom_file, 'rb').read()
            test_hash = hashlib.md5(rom).hexdigest()
            # Checks for the correct ROM
            if test_hash != "35ae64b0f27e60107c14ab956f6cdf70":
                raise HashError("Invalid checksum")
            rom_list = list(rom)

            # Uses given input as seed, else randomly picks a new seed to use
            # AFAIK you can't get what the default seed is, so it needs to be changed to one we know
            KNDL_seed = self.seedValue.text()
            if KNDL_seed == "":
                KNDL_seed = random.randint(0, 999999999)
            random.seed(KNDL_seed)

            if self.enemyCheck.isChecked():
                if self.starRodCheck.isChecked():
                    ability_values.append("19")

                # Gives enemies new abilities based on random selection from file
                for item in ability_locations:
                    address = int(item, 16)
                    new_enemy = random.choice(ability_values)
                    new_enemy = int(new_enemy,16)
                    rom_list[address] = new_enemy

            if self.defaultColor.isChecked() == False:
                new_color = self.selectedColor()
                row = new_palette[new_color]
                new_colors = []
                for i in range(0, len(row) - 2, 2):
                    new_colors.append(int(row[i:i+2],16))

                # Replaces old color palettes with the new
                for item in palette_locations:
                    color_address = int(item, 16)
                    for i in range(0, len(new_colors)):
                        rom_list[color_address + i] = new_colors[i]

            rom = bytes(rom_list)
            new_rom = open('.'.join(self.rom_file.split(".")[:-1]) + "_" + str(KNDL_seed) + ".gba", 'wb')
            new_rom.write(rom)
            new_rom.close()

            QtWidgets.QMessageBox.about(self, "Success", "Your copy of Nightmare in Dream Land has been randomized. Enjoy!")
        except AttributeError:
            QtWidgets.QMessageBox.about(self, "Error", "Error: Specify a ROM location")
        except FileNotFoundError:
            QtWidgets.QMessageBox.about(self, "Error", "Error: File not found")
        except HashError:
            QtWidgets.QMessageBox.about(self, "Error", "The given file is invalid. Please use a US GBA Kirby: Nightmare in Dream Land ROM.")
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "Error", "Some mysterious error has occurred. Please contact the developers with information about what happened. {}".format(e))

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = KirbyApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()