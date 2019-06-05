from Windows import WCharacter
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository.Gdk import Screen

def gtk_style():
    css_provider = Gtk.CssProvider()
    try:
        css_provider.load_from_path("windows/style.css")
    except Exception as e:
        print(e)


    screen = Screen.get_default()
    style_context = Gtk.StyleContext()
    style_context.add_provider_for_screen(
        screen, css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER)


main = WCharacter() 
main.present()

gtk_style()
Gtk.main()
