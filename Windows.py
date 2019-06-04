import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango


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


    def onDestroy(self, *args):
        Gtk.main_quit()