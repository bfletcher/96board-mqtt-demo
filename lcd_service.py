#!/usr/bin/env python
# Python widget that simulates an LCD dot-matrix display
# like those found on stereo equipment. 
# For general emulation of IoT embedded client displays
# in demo code. It has been modified to run threaded and 
# as an rpyc service.
#
# Copyright (C) 2005 Gerome Fournier <jefke(at)free.fr>
# Copyright (C) 2008 John Stowers <john.stowers@gmail.com>
# Copyright (C) 2016 Bill Fletcher <bill.fletcher@linaro.org>
#
# Also based on Simple pyGTK multithreading example
# Adapted from a post by Alif Wahid on the pyGTK mailinglist.
# Cedric Gustin, August 2003

import sys
import time
import gtk
import gtk.glade
import rpyc
import os

from threading import Thread
from Queue import Queue

Debug = False

# LCD characters definition
_CHARS_FILENAME = "lcd_chars.txt"

# Shared queue for display messages
g_message_q = Queue()

# Display size
g_rows = 4
g_cols = 40

# Service coordinates
g_service_alias = ""
g_socket_id = 0


# Drawing routines for the LCD
class LCDWidget:
        "GTK+ LCD Widget"

        def __init__(self, widget, rows, cols):
                "Instantiate a LCD widget"
                self.rows = rows
                self.cols = cols
                self._area = widget
                self._pix = None
                self._table = {}
                self._area.connect("configure-event", self._configure_cb)
                self._area.connect("expose-event", self._expose_cb)

        def set_zoom_factor(self, factor):
                "Set the zoom factor"
                self._factor = factor
                self._border = 5
                self._cborder = 3*factor
                self._cwidth = 9*factor
                self._cheight = 13*factor
                self._width = 2*self._border + \
                                (self._cwidth+self._cborder)*self.cols + self._cborder
                self._height = 2*self._border + \
                                (self._cheight+self._cborder)*self.rows + self._cborder
                self._area.set_size_request(self._width, self._height)

        def get_zoom_factor(self):
                return self._factor

        def refresh(self):
                "Refresh the LCD widget"
                self._area.queue_draw_area(0, 0, self._width, self._height)

        def draw_char(self, row, col, charindex):
                """Draw the character stored at position 'charindex' in the internal
                   character definition table, on the LCD widget
                """
                if not self._pix:
                        return
                x = col * (self._cwidth+self._cborder) + self._border + self._cborder
                y = row * (self._cheight+self._cborder) + self._border + self._cborder
                self._pix.draw_drawable(self._back, self._table[charindex], \
                                0, 0, x, y, self._cwidth, self._cheight)

        def set_brightness_percentage(self, percentage):
                fg_colors = {
                        100: "#00ff96",
                        75: "#00d980",
                        50: "#00b269",
                        25: "#008c53",
                        0: "#303030"
                }
                if percentage not in fg_colors.keys():
                        return
                if hasattr(self, "_brightness_percentage") \
                        and self._brightness_percentage == percentage:
                        return
                self._brightness_percentage = percentage
                self._set_colors(["#000000", "#303030", fg_colors[percentage]])
                self._load_font_definition()

        def get_brightness_percentage(self):
                return self._brightness_percentage

        def clear(self):
                "Clear the LCD display"
                for row in range(self.rows):
                        for col in range(self.cols):
                                self.draw_char(row, col, 32)
                self.refresh()

        def create_char(self, charindex, shape):
                """Insert a new char in the character table definition,
                   at position 'charindex', based on 'shape'
                """
                pix = gtk.gdk.Pixmap(self._area.window, self._cwidth, self._cheight)
                pix.draw_rectangle(self._back, True, 0, 0, self._cwidth, self._cheight)
                for x in range(5):
                        for y in range(7):
                                pix.draw_rectangle(self._charbg, True, \
                                        x*2*self._factor, y*2*self._factor, \
                                        self._factor, self._factor)
                for index in range(35):
                        if shape[index] == "1":
                                row = index / 5
                                col = index - row*5
                                pix.draw_rectangle(self._charfg, True, \
                                        col*2*self._factor, row*2*self._factor, \
                                        self._factor, self._factor)
                self._table[charindex] = pix

        def print_line(self, string,pos=0):
                "Print a single line on the LCD display"
                for i in range(len(string[:self.cols])):
                        self.draw_char(pos, i, ord(string[i]))

        def _configure_cb(self, widget, event):
                x, y, width, height = widget.get_allocation()
                self._pix = gtk.gdk.Pixmap(widget.window, width, height)
                self.set_brightness_percentage(100)
                self._pix.draw_rectangle(self._back, True, 0, 0, width, height)
                self._load_font_definition()
                self.clear()
                return True

        def _expose_cb(self, widget, event):
                if self._pix:
                        widget.window.draw_drawable(self._back, self._pix, 0, 0, 0, 0, \
                                        self._width, self._height)
                return False

        def _set_colors(self, colors):
                for widget, color in zip(["_back", "_charbg", "_charfg"], colors):
                        exec "self.%s = gtk.gdk.GC(self._pix)" % widget
                        exec "self.%s.set_rgb_fg_color(gtk.gdk.color_parse('%s'))" \
                                % (widget, color)

        def _load_font_definition(self):
                try:
                        file = open(_CHARS_FILENAME)
                except IOError:
                        print >>sys.stderr, "Unable to open font characters definition '%s'" \
                                        % _CHARS_FILENAME
                        sys.exit(1)
                index = 1
                shape = ""
                for line in file.readlines():
                        line = line.rstrip()
                        if not line or line[0] == "#":
                                continue
                        if index == 1:
                                char_index = int(line, 16)
                        else:
                                shape = ''.join([shape, line])
                        index += 1
                        if index == 9:
                                self.create_char(char_index, shape)
                                index = 1
                                shape = ""

# Thread to service the display
class Display (Thread):
    def __init__ (self):
        Thread.__init__(self)
        self._setup_widgets()
        self._set_zoom_factor(1)

    def run (self):
        #time.sleep(1)
        gtk.threads_enter()
        self._window.set_title(g_service_alias)
        self._window.show_all()
        self.lcd_display.clear()
        self.lcd_display.print_line("Linaro & 96Boards",0)
        self.lcd_display.print_line("Waiting for MQTT messages ...",1)
        self.lcd_display.refresh()
        gtk.threads_leave()
        while os.getppid() != 1 :
		string = g_message_q.get(block=True)
		# Slice the message to fit the display
		# does the message need to be truncated?
		if len(string) > g_rows * g_cols:
		    trunc = string[:g_rows*g_cols]
		else:
		    trunc = string

                gtk.threads_enter()
                self.lcd_display.clear()
		# Iterate through the string in line length chunks
		# We already know it will fit the number of lines
		for i in range(0,(int(len(trunc)-1)/g_cols)+1):
                	self.lcd_display.print_line(trunc[i*g_cols:(i+1)*g_cols],i)
                self.lcd_display.refresh()
                gtk.threads_leave()
        print os.path.basename(__file__),": Parent exited"
        self._quit
        sys.exit(1)


    def _setup_widgets(self):
        self._window = gtk.Window()
        self._window.hide()
        self._window.connect("destroy", self._quit)
        widget = gtk.DrawingArea()
        self._window.add(widget)
        self.lcd_display = LCDWidget(widget, g_rows, g_cols)

    def _quit(self, *args):
        gtk.main_quit()

    def _set_zoom_factor(self, factor):
        if factor < 1:
                factor = 1
        if factor > 2:
                factor = 2
        self.lcd_display.set_zoom_factor(factor)

    def _set_brightness_percentage(self, percent):
        if percent < 0:
                percent = 0
        if percent > 100:
                percent = 100
        self.lcd_display.set_brightness_percentage(percent)

# Defines a simple rpyc service to take remote requests and
# submit them to the message queue
class LCDisplayService(rpyc.Service):
        ALIASES = [g_service_alias,]
        def on_connect(self):
                pass

        def on_disconnect(self):
                pass

        def exposed_print_string(self,string):
                if Debug == True :
                	print "Server: ", string
		g_message_q.put(string)
                return

# Thread to service the rpyc Service
class Service (Thread):
    def __init__ (self):
        Thread.__init__(self)

    def run (self):
        from rpyc.utils.server import ThreadedServer
        t = ThreadedServer(LCDisplayService, port = g_socket_id)
        t.start()

def start_new_display ():
    a = Display()
    a.daemon = True
    a.start()

def start_new_service ():
    a = Service()
    a.daemon = True
    a.start()

def main():
    #
    # In order to uniquely identify the service, pass in an
    # alias name and socket id on the command line
        global g_service_alias
        global g_socket_id
        if len(sys.argv) == 3:
            g_service_alias = sys.argv[1]
            g_socket_id = int(sys.argv[2])
        elif len(sys.argv) > 2:
            print "Usage: lcd_service.py (service_alias_name socket_id)"
            sys.exit(2)
        else:
            # defaults
            g_service_alias = "LCD1"
            g_socket_id = 18861

        print "Using service alias:", g_service_alias, " and socket id", g_socket_id
        # Initialize threads
        gtk.threads_init()
        start_new_display()
        start_new_service()
        # gtk multithreaded stuff 
        gtk.threads_enter()
        gtk.main()
        gtk.threads_leave()

if __name__ == "__main__":
    main()
