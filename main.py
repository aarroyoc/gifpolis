import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk

from gifpolis.library import Library

class App:
    def __init__(self):
        self.library = Library()

        self.builder = Gtk.Builder()
        self.builder.add_from_file("gifpolis.glade")

        # Register IDs
        self.window = self.builder.get_object("window")
        self.search_input = self.builder.get_object("search_input")
        self.import_button = self.builder.get_object("import_button")
        self.import_dialog = self.builder.get_object("import_dialog")
        self.gif_preview = self.builder.get_object("gif_preview")
        self.description = self.builder.get_object("description")
        self.import_discard = self.builder.get_object("import_discard")
        self.import_save = self.builder.get_object("import_save")
        self.gif_grid = self.builder.get_object("gif_grid")

        # Connect Events
        self.window.connect("destroy", Gtk.main_quit)
        self.import_button.connect("clicked", self.import_file)
        self.search_input.connect("changed", lambda x: self.search())
        self.gif_grid.connect("selected-children-changed", self.copy_clipboard)

        # Initialize app
        self.current_rows = 0
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.search_results = list()
        self.window.show_all()

    def copy_clipboard(self, widget):
        n = widget.get_children().index(widget.get_selected_children()[0])
        # TODO GTK 4 para usar clipboard

    def get_data(self, clipboard, selection, info):
        breakpoint()
        self.selection.set(selection.target, 8, )
        

    def import_file(self, evt):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", 
            parent=self.window,
            action=Gtk.FileChooserAction.OPEN)

        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        filter_gif = Gtk.FileFilter()
        filter_gif.set_name("GIF files")
        filter_gif.add_mime_type("image/gif")
        dialog.add_filter(filter_gif)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
           filename = dialog.get_filename()
        else:
            return

        dialog.destroy()

        ### SECOND STEP
        def save_file(evt):
            self.library.save_file(self.description.get_text(), filename)
        self.import_discard.connect("clicked", lambda x: self.import_dialog.hide())
        self.import_save.connect("clicked", save_file)
        self.import_dialog.show_all()
        self.gif_preview.set_from_file(filename)


    def search(self):
        query = self.search_input.get_text()
        self.search_results = self.library.search(query)
        for result in self.gif_grid.get_children():
            result.destroy()
        for i,gif in enumerate(self.search_results):
            # ADD IMAGE TO EACH GRID
            img = Gtk.Image()
            img.set_from_file(gif.path)
            self.gif_grid.add(img)
        
            # CLIPBOARD EVENT
            # REMOVE EVENT
        
        self.gif_grid.show_all()

    def scale_animation(self, animation, width, height):
        iter = animation.get_iter()
        new = GdkPixbuf.PixbufSimpleAnim(width, height, iter.get_delay_time())
        while True:
            pbuf = iter.get_pixbuf()
            pbuf.scale_simple(width, height)
            new.add_frame(pbuf)




app = App()
Gtk.main()