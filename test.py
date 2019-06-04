import Windows
import gi
import requests
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
# Applying css styles

def Gtk_style():
    cssProvider = Gtk.CssProvider()
    cssProvider.load_from_path('windows/style.css')
    screen = Gdk.Screen.get_default()
    styleContext = Gtk.StyleContext()
    styleContext.add_provider_for_screen(
        screen, cssProvider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER)

win = Windows.WCharacter()

Gtk_style()
# Init window
win.present()
# Init gtk bucle
Gtk.main()