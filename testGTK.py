#coding: utf8 
from gi.repository import Gtk, GdkPixbuf, Gdk
from PIL import Image
import os,sys,urllib

TARGET_TYPE_URI_LIST = 80
MAX_SIZE=1440

class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="PyResizer by CiaccoDavide", application=app)
        self.set_default_size(300, 80)
        self.set_border_width(5)

        # a label
        self.label = Gtk.Label()
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_text("Set the max size for your images.\n")


        ad = Gtk.Adjustment(1440, 1, 10000, 1, 0, 0)
        # a spin button for integers (digits=0)
        self.spin = Gtk.SpinButton(adjustment=ad, climb_rate=1, digits=0)
        # as wide as possible
        self.spin.set_hexpand(True)
        # we connect the signal "value-changed" emitted by the spinbutton with the callback
        # function spin_selected
        self.spin.connect("value-changed", self.spin_selected)

        self.dnd = Gtk.Label()
        self.dnd.set_justify(Gtk.Justification.CENTER)
        self.dnd.set_lines(3)
        self.dnd.set_text("\n\n\nDrop Some Images Here!\n\n\n")

        self.dnd.connect('drag_data_received', on_drag_data_received)
        self.dnd.drag_dest_set( Gtk.DestDefaults.MOTION|
								Gtk.DestDefaults.HIGHLIGHT | Gtk.DestDefaults.DROP,
								[Gtk.TargetEntry.new("text/uri-list", 0, 80)], Gdk.DragAction.COPY)



        # a grid to attach the widgets
        grid = Gtk.Grid()
        grid.attach(self.label, 0, 0, 1, 1)
        grid.attach(self.spin, 0, 1, 1, 1)
        grid.attach(self.dnd, 0, 2, 1, 1)

        self.add(grid)

    # callback function: the signal of the spinbutton is used to change the
    # text of the label
    def spin_selected(self, event):
        global MAX_SIZE
        MAX_SIZE = self.spin.get_value_as_int()
        self.label.set_text("Max-size = " + str(self.spin.get_value_as_int())+"\n")


    #DRAG&DROPPER

def get_file_path_from_dnd_dropped_uri(uri):
    # get the path to file
    path = ""
    if uri.startswith('file:\\\\\\'): # windows
        path = uri[8:] # 8 is len('file:///')
    elif uri.startswith('file://'): # nautilus, rox
        path = uri[7:] # 7 is len('file://')
    elif uri.startswith('file:'): # xffm
        path = uri[5:] # 5 is len('file:')

    path = urllib.url2pathname(path) # escape special chars
    path = path.strip('\r\n\x00') # remove \r\n and NULL

    return path

def resize(max_size,inputImage):
    maxsize = (max_size,max_size)
    outputFormat = "jpg" 	#or "PNG", etc...

    img = Image.open(inputImage)										#loads the image file into img
    img.thumbnail(maxsize, Image.ANTIALIAS) 							#resizes the image using maxsize var for both the width and the height
    outputImageName=os.path.splitext(inputImage)[0]+"."+outputFormat 	#nome del file in output (si potrebbe aggiungere una stringa all'inizio o alla fine a piacere)
    img.save(outputImageName)											#il formato è definito all'inizio, se si vuole mantenere il formato originale di ciascuna foto basta usare img.save(outputImageName)

def on_drag_data_received(widget, context, x, y, selection, target_type, timestamp):
    if target_type == TARGET_TYPE_URI_LIST:
        uri = selection.get_data().strip('\r\n\x00')
        #print 'uri', uri
        uri_splitted = uri.split() # we may have more than one file dropped
        i=0
     	j=len(uri_splitted)
        for uri in uri_splitted:
            path = get_file_path_from_dnd_dropped_uri(uri)
            #widget.set_text("\n\n\n"+str(i)+"/"+str(j)+"\n\n\n") #progress
            resize(MAX_SIZE,path)
            print i,'/',j
            i+=1
        #widget.set_text("\n\nDone!\n"+str(i)+"/"+str(j)+"\n\n\n") #progress
        print 'Done! ',i,'/',j





class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)



