import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango
import subprocess
import os

class WCharacter(Gtk.Window):
    """docstring for WindowLogin"""

    def __init__(self):
        Gtk.Window.__init__(self)
        self.maximize()
        self.set_resizable(True)
        # self.fullscreen()
        self.set_title("LOGIN")
        self.init()
        self.connect("destroy", self.onDestroy)

    def init(self):
        # Reading builder
        self.builder = Gtk.Builder()
        self.builder.add_from_file("windows/character.glade")

        # LAYOUT
        self.layout_main = self.builder.get_object("layout_main")
        self.add(self.layout_main)

        # LOGO
        character = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            'sprites/morty/character.png', 300, 280, True)

        self.builder.get_object("image_character").set_size_request(100, 300)
        self.builder.get_object("image_character").set_from_pixbuf(character)

        sprites = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            'sprites/morty/sprites.png', 400, 280, True)

        self.builder.get_object("image_sprites").set_size_request(100, 300)
        self.builder.get_object("image_sprites").set_from_pixbuf(sprites)
        # BUTTONS
        self.builder.get_object("button_morty").connect("clicked", self.character_selected)
        self.builder.get_object("button_rick").connect("clicked", self.character_selected)
        self.builder.get_object("button_summer").connect("clicked", self.character_selected)
        self.builder.get_object("button_jerry").connect("clicked", self.character_selected)

    def character_selected(self, button):
        character = button.get_name()
        self.hide()
        self.close()

        # subprocess.run(['python3', 'main.py', character])
        # os.system('python3 main.py '+character)
        self.go_to_game(character)

    def onDestroy(self, *args):
        Gtk.main_quit()
    def go_to_game(self, character):
        subprocess.run(['python3', 'main.py', character])
        # os.system('python3 main.py '+character)