#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
A PDF presentation tool for Mac OS X

Copyright (c) 2011--2014, IIHM/LIG - Renaud Blanch <http://iihm.imag.fr/blanch/>
Licence: GPLv3 or higher <http://www.gnu.org/licenses/gpl.html>
"""


# imports ####################################################################

import sys
import os
import re
import time
import select
import getopt
import textwrap
import mimetypes

from math import exp, hypot
from collections import defaultdict


# constants and helpers ######################################################

NAME = "Présentation"
MAJOR, MINOR = 1, 2
VERSION = "%s.%s" % (MAJOR, MINOR)
HOME = "http://iihm.imag.fr/blanch/software/osx-presentation/"
CREDITS = """
Home: <a href='%s'>osx-presentation</a> <br/>
Source: <a href='https://bitbucket.org/rndblnch/osx-presentation/src/tip/presentation.py'>presentation.py</a> <br/>
Licence: <a href='http://www.gnu.org/licenses/gpl-3.0.txt'>GPLv3</a>+ <br/>
Icon courtesy of <a href="http://www.dlanham.com/">David Lanham</a>
""" % HOME
COPYRIGHT = """Copyright © 2011-2014 Renaud Blanch
Copyright © 2014-2017 Dave Mason"""

ICON = "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"

PRESENTER_FRAME   = ((100., 100.), (1024., 768.))
MIN_POSTER_HEIGHT = 20.

HELP = [
	("?",         "show/hide this help"),
	("h/q",       "hide/quit"),
	("b/w/m/s/p", "toggle black/web/movie/slide/poll view"),
	("F5/f/F",     "toggle fullscreen"),
#	("⎋",         "leave fullscreen"),
]
HELP_CLOCK = [
	("t",         "start timer"),
]
HELP_TIMER = [
	("t",         "stop timer"),
	("z",         "set origin for timer"),
	("[/]",       "sub/add  1 minute to planned time"),
	("{/}",       "sub/add 10 minutes"),
]
HELP_POLL = [
]
HELP_SLIDES = [
	("←/↑/⇞",     "previous slide/frame/section"),
	("→/↓/⇟",     "next slide/frame/section"),
	("backspace/remote ←","previous slide"),
	("space/remote →","next slide"),
	("./remote ↓","toggle black"),
#	("⌘←",        "back"),
#	("⌘→",        "forward"),
	("↖",         "first page"),
	("↘",         "last page"),
]
HELP_ANNOTATIONS = [
	("e",         "erase on-screen annotations"),
]
#HELP_MOVIE = [
#	("space",     "play/pause video (while in movie mode)"),
#	("&lt;/&gt;", "step video backward/forward"),
#]
HELP_WEB = [
	("+/-/0",     "zoom in/out/reset web view"),
]

def nop(): pass


# handling args ##############################################################

name, args = sys.argv[0], sys.argv[1:]

# ignore "-psn" arg if we have been launched by the finder
launched_from_finder = args and args[0].startswith("-psn")
if launched_from_finder:
	args = args[1:]


def exit_usage(message=None, code=0):
	usage = textwrap.dedent("""\
	Usage: %s [-hvid:f] <doc.pdf>
		-h --help          print this help message then exit
		-v --version       print version then exit
		-i --icon          print icon then exit
		-d --duration <t>  duration of the talk in minutes
		-f --feed          enable reading feed on stdin
		<doc.pdf>          file to present
	""" % name)
	if message:
		sys.stderr.write("%s\n" % message)
	sys.stderr.write(usage)
	sys.exit(code)

def exit_version():
	sys.stdout.write("%s %s\n" % (os.path.basename(name), VERSION))
	sys.exit()

def exit_icon():
	import base64
	sys.stdout.write(base64.b64decode(ICON))
	sys.exit()


# options

try:
	options, args = getopt.getopt(args, "hvid:f", ["help", "version", "icon",
	                                               "duration=", "feed"])
except getopt.GetoptError as message:
	exit_usage(message, 1)

show_feed = False
presentation_duration = 0

for opt, value in options:
	if opt in ["-h", "--help"]:
		exit_usage()
	elif opt in ["-v", "--version"]:
		exit_version()
	elif opt in ["-i", "--icon"]:
		exit_icon()
	elif opt in ["-d", "--duration"]:
		presentation_duration = int(value)
	elif opt in ["-f", "--feed"]:
		show_feed = True

if len(args) > 1:
	exit_usage("no more than one argument is expected", 1)


# application init ###########################################################

#from objc import setVerbose
#setVerbose(1)

#from objc import nil, NO, YES
nil = None
YES = True
NO = False
from Foundation import (
	NSLog, NSNotificationCenter,
	NSObject, NSTimer, NSError, NSString, NSData,
	NSAttributedString, NSUnicodeStringEncoding,
	NSURL, NSURLRequest, NSURLConnection,
	NSAffineTransform,
)

from AppKit import (
	NSApplication, NSEvent,
	NSBundle,
	NSApplicationDidFinishLaunchingNotification,
	NSOpenPanel, NSFileHandlingPanelOKButton,
	NSAlert, NSAlertDefaultReturn,
	NSView,
	NSViewWidthSizable, NSViewHeightSizable,
	NSWindow,
	NSMiniaturizableWindowMask, NSResizableWindowMask, NSTitledWindowMask,
	NSBackingStoreBuffered,
	NSCommandKeyMask, NSAlternateKeyMask,
	NSMenu, NSMenuItem,
	NSGraphicsContext,
	NSCompositingOperationClear, NSCompositingOperationSourceAtop, NSCompositingOperationCopy,
	NSRectFillUsingOperation, NSFrameRectWithWidth, NSFrameRect, NSEraseRect,
	NSZeroRect,
	NSColor, NSCursor, NSFont,
	NSFontAttributeName,	NSForegroundColorAttributeName,
	NSStrokeColorAttributeName, NSStrokeWidthAttributeName,
	NSUpArrowFunctionKey, NSLeftArrowFunctionKey,
	NSDownArrowFunctionKey, NSRightArrowFunctionKey,
	NSHomeFunctionKey, NSEndFunctionKey,
	NSPageUpFunctionKey, NSPageDownFunctionKey,
	NSPrevFunctionKey, NSNextFunctionKey,
	NSF5FunctionKey,
	NSScreen, NSWorkspace, NSImage,
	NSBezierPath, NSRoundLineCapStyle,
)

from Quartz import (
	PDFDocument, PDFAnnotationText, PDFAnnotationLink,
	PDFActionNamed,
	kPDFActionNamedNextPage, kPDFActionNamedPreviousPage,
	kPDFActionNamedFirstPage, kPDFActionNamedLastPage,
	kPDFActionNamedGoBack, kPDFActionNamedGoForward,
	kPDFDisplayBoxCropBox,
)

from WebKit import (
	WebView,
)

import AVFoundation
#from AVFoundation import (
#	AVMovie, AVMovieView,
#)
#from QTKit import (
#	QTMovie, QTMovieView,
#)

# QTKit is deprecated in 10.9 but AVFoundation will only be in PyObjC-3.0+
# so wait and see, and remember for future reference:
# https://developer.apple.com/library/mac/technotes/tn2300/_index.html


if sys.version_info[0] == 3:
	_s = NSString.stringWithString_
	sys.stdin = sys.stdin.detach() # so that sys.stdin.readline returns bytes
else:
	_s = NSString.alloc().initWithUTF8String_

def _h(s):
	h, _ = NSAttributedString.alloc().initWithHTML_documentAttributes_(
		_s(s).dataUsingEncoding_(NSUnicodeStringEncoding), None)
	return h

ICON = NSImage.alloc().initWithData_(NSData.alloc().initWithBase64Encoding_(ICON))

NSBundle.mainBundle().infoDictionary()['NSAppTransportSecurity'] = dict(NSAllowsArbitraryLoads = True)

app = NSApplication.sharedApplication()
app.activateIgnoringOtherApps_(True)

restarted = False # has the application been restarted before actual launch

if launched_from_finder:
	# HACK: run application to get dropped filename if any and then stop it
	class DropApplicationDelegate(NSObject):
		def application_openFile_(self, app, filename):
			filename = filename.encode("utf-8")
			if filename != os.path.abspath(__file__):
				args.append(filename)
		def applicationDidFinishLaunching_(self, notification):
			app.stop_(self)
	application_delegate = DropApplicationDelegate.alloc().init()
	app.setDelegate_(application_delegate)
	app.run()
	restarted = True


if args:
	url = NSURL.fileURLWithPath_(args[0])
else:
	class Opener(NSObject):
		def getURL(self):
			dialog = NSOpenPanel.openPanel()
			dialog.setAllowedFileTypes_(["pdf"])
			if dialog.runModal() == NSFileHandlingPanelOKButton:
				global url
				url, = dialog.URLs()
			else:
				exit_usage("please select a pdf file", 1)
			app.stop_(self)
	opener = Opener.alloc().init()
	opener.performSelectorOnMainThread_withObject_waitUntilDone_("getURL", None, False)
	app.run()
	restarted = True


# opening presentation

file_name = url.lastPathComponent()
pdf = PDFDocument.alloc().initWithURL_(url)
if not pdf:
	exit_usage("'%s' does not seem to be a pdf." % url.path(), 1)


# page navigation

page_count = pdf.pageCount()
first_page, last_page = 0, page_count-1
last_frame = -1
curr_section_start_page, next_section_start_page = first_page, last_page

past_pages = []
current_page = first_page
future_pages = []

def _goto(page):
	global current_page
	current_page = page
	presentation_show(slide_view)

def _pop_push_page(pop_pages, push_pages):
	def action():
		try:
			page = pop_pages.pop()
		except IndexError:
			return
		push_pages.append(current_page)
		_goto(page)
	return action


back    = _pop_push_page(past_pages, future_pages)
forward = _pop_push_page(future_pages, past_pages)

def goto_page(page):
	page = min(max(first_page, page), last_page)
	if page == current_page:
		return
	
	if future_pages and page == future_pages[-1]:
		forward()
	elif past_pages and page == past_pages[-1]:
		back()
	else:
		del future_pages[:]
		past_pages.append(current_page)
		_goto(page)


def next_page(): goto_page(current_page+1)
def prev_page(): goto_page(current_page-1)
def home_page(): goto_page(first_page)
def end_page():  goto_page(last_page)
def next_section(): goto_page(next_section_start_page)
def prev_section():
	if curr_section_start_page < current_page:
		goto_page(curr_section_start_page)
	else:
		temp,_ = extract_annotations(get_page(curr_section_start_page-1))
		goto_page(temp)
		
def next_frame():
	page = get_page(current_page)
	current_label = page.label()
	next_frame_page = current_page
	while page and page.label()==current_label:
		next_frame_page += 1
		page=get_page(next_frame_page)
	goto_page(next_frame_page)
def prev_frame():
	page = get_page(current_page-1)
	if page:
		current_label = page.label()
		prev_frame_page = current_page-1
		while page and page.label()==current_label:
			prev_frame_page -= 1
			page=get_page(prev_frame_page)
		goto_page(prev_frame_page+1)

def get_page(page_number):
	if page_number == min(max(first_page, page_number), last_page):
		return pdf.pageAtIndex_(page_number)
	return


# annotations

#def get_movie(url):
#	"""return a QTMovie object from an url if possible/desirable"""
#	if not (url and url.scheme() == "file"):
#		return
#	mimetype, _ = mimetypes.guess_type(url.absoluteString())
#	if not (mimetype and mimetype.startswith("video")):
#		return
#	if not QTMovie.canInitWithURL_(url):
#		return
#	movie, error = QTMovie.movieWithURL_error_(url, None)
#	if error:
#		return
#	return movie

notes  = defaultdict(list)
questions  = defaultdict(list)
answers  = defaultdict(list)
movies = {}
for page_number in range(page_count):
	page = pdf.pageAtIndex_(page_number)
	page.setDisplaysAnnotations_(False)
	last_frame = page.label()
	question = 'none'
	for annotation in page.annotations():
		annotation_type = type(annotation)
		if annotation_type == PDFAnnotationText:
			contents = annotation.contents()
			if contents.startswith('Q:'):
				question = contents[2:]
				questions[page_number].append(question)
#			elif annotation.contents()[1].startswith('A:'):
#				answers[question].append(contents[2:])
			else:
				notes[page_number].append(contents)
#		elif annotation_type == PDFAnnotationLink:
#			movie = get_movie(annotation.URL())
#			if movie:
#				movies[annotation] = (movie, movie.posterImage())


# interaction state

IDLE, BBOX, CLIC, DRAW = list(range(4))
state = IDLE
window_present = False

drawings = defaultdict(list)


# page drawing ###############################################################

bbox = NSAffineTransform.transform()

def draw_page(page):
	bbox.concat()
	
	NSEraseRect(page.boundsForBox_(kPDFDisplayBoxCropBox))
	page.drawWithBox_(kPDFDisplayBoxCropBox)

	NSColor.blackColor().setFill()
	for annotation in page.annotations():
		if not annotation in movies:
			continue
		bounds = annotation.bounds()
		
		_, poster = movies[annotation]
		if poster is None:
			continue
		
		bounds_size = bounds.size
		if bounds_size.height < MIN_POSTER_HEIGHT:
			continue
		
		NSRectFillUsingOperation(bounds, NSCompositingOperationCopy)
		
		poster_size = poster.size()
		aspect_ratio = ((poster_size.width*bounds_size.height)/
		                (bounds_size.width*poster_size.height))
		if aspect_ratio < 1:
			dw = bounds.size.width * (1.-aspect_ratio)
			bounds.origin.x += dw/2.
			bounds.size.width -= dw
		else:
			dh = bounds.size.height * (1.-1./aspect_ratio)
			bounds.origin.y += dh/2.
			bounds.size.height -= dh
		
		poster.drawInRect_fromRect_operation_fraction_(
			bounds, NSZeroRect, NSCompositingOperationCopy, 1.
		)
	
	for path in drawings[current_page]:
		NSColor.whiteColor().setStroke()
		path.setLineWidth_(2)
		path.stroke()
		NSColor.blackColor().setStroke()
		path.setLineWidth_(1)
		path.stroke()


# presentation ###############################################################

class SlideView(NSView):
	def drawRect_(self, rect):
		bounds = self.bounds()
		width, height = bounds.size
		
		NSRectFillUsingOperation(bounds, NSCompositingOperationClear)
		
		# current page
		page = pdf.pageAtIndex_(current_page)
		page_rect = page.boundsForBox_(kPDFDisplayBoxCropBox)
		_, (w, h) = page_rect
		r = min(width/w, height/h)
		
		NSGraphicsContext.saveGraphicsState()
		transform = NSAffineTransform.transform()
		transform.translateXBy_yBy_(width/2., height/2.)
		transform.scaleXBy_yBy_(r, r)
		transform.translateXBy_yBy_(-w/2., -h/2.)
		transform.concat()
		draw_page(page)
		NSGraphicsContext.restoreGraphicsState()


class MessageView(NSView):
	fps = 20. # frame per seconds for animation
	pps = 40. # pixels per seconds for scrolling
	
	input_lines = ["…"]
	should_check = True
	
	def initWithFrame_(self, frame):
		assert NSView.initWithFrame_(self, frame) == self
		self.redisplay_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
			1./self.fps,
			self, "redisplay:", nil,
			True
		)
		return self
	
	def redisplay_(self, timer):
		self.setNeedsDisplay_(True)
	
	def check_input(self):
		while True:
			ready, _, _ = select.select([sys.stdin], [], [], 0)
			if not ready:
				break
			line = sys.stdin.readline().decode('utf-8')
			self.input_lines.append(line.rstrip())
	
	def drawRect_(self, rect):
		if self.should_check:
			self.check_input()
			try:
				self.text = self.input_lines.pop(0)
			except IndexError:
				pass
			else:
				self.start = time.time()
				self.should_check = False
		text = NSString.stringWithString_(self.text)
		x = rect.size.width - self.pps*(time.time()-self.start)
		for attr in [{
			NSFontAttributeName:            NSFont.labelFontOfSize_(30),
			NSStrokeColorAttributeName:     NSColor.colorWithDeviceWhite_alpha_(0., .75),
			NSStrokeWidthAttributeName:     20.,
		}, {
			NSFontAttributeName:            NSFont.labelFontOfSize_(30),
			NSForegroundColorAttributeName: NSColor.colorWithDeviceWhite_alpha_(1., .75),
		}]:
			text.drawAtPoint_withAttributes_((x, 4.), attr)
		tw, _ = text.sizeWithAttributes_(attr)
		if x < -tw:
			self.should_check = True


# presenter view #############################################################

def extract_annotations(page,box=None):
	temp1, temp2 = None, None
	for annotation in page.annotations():
		if type(annotation) == PDFAnnotationLink:
			width, _ = annotation.bounds().size
			if width < 2:
				destination = annotation.destination()
				if destination:
					temp1 = temp2
					temp2 = pdf.indexForPage_(destination.page())
			elif box is not None:
				box(annotation)
	return temp1,temp2

class PresenterView(NSView):
	transform = NSAffineTransform.transform()
	duration = presentation_duration * 60.
	absolute_time = True
	elapsed_duration = 0
	start_time = time.time()
	duration_change_time = 0
	show_help = True
	annotation_state = None
	
	def drawRect_(self, rect):
		global curr_section_start_page, next_section_start_page
		bounds = self.bounds()
		width, height = bounds.size
		
		margin = width / 40.
		if window_present:
			current_width = width-2*margin
		else:
			current_width = (width-3*margin)*2/3.
		font_size = margin
		
		NSRectFillUsingOperation(bounds, NSCompositingOperationCopy)
		
		# current 
		self.page = pdf.pageAtIndex_(current_page)
		page_rect = self.page.boundsForBox_(kPDFDisplayBoxCropBox)
		_, (w, h) = page_rect
		r = current_width/w
		
		NSGraphicsContext.saveGraphicsState()
		transform = NSAffineTransform.transform()
		transform.translateXBy_yBy_(margin, height-margin)
		transform.scaleXBy_yBy_(r, r)
		transform.translateXBy_yBy_(0., -h)
		transform.concat()
		
		NSGraphicsContext.saveGraphicsState()
		
		draw_page(self.page)
		if state == DRAW:
			return
		
		# links
		NSColor.blueColor().setFill()
		curr_section_start_page, next_section_start_page = extract_annotations(self.page,lambda annotation : NSFrameRectWithWidth(annotation.bounds(), .5))
		self.transform = transform
		self.transform.prependTransform_(bbox)
		self.resetCursorRects()
		self.transform.invert()
		
		NSGraphicsContext.restoreGraphicsState()

		if window_present:
			return

		# screen border
		NSColor.grayColor().setFill()
		NSFrameRect(page_rect)
		NSGraphicsContext.restoreGraphicsState()
		
		
		# time
		now = time.time()
		if now - self.duration_change_time <= 1: # duration changed, display it
			clock = time.gmtime(self.duration)
		elif self.absolute_time:
			clock = time.localtime(now)
		else:
			running_duration = now - self.start_time + self.elapsed_duration
			clock = time.gmtime(abs(self.duration - running_duration))
		clock = NSString.stringWithString_(time.strftime("%H:%M:%S", clock))
		attr = {
			NSFontAttributeName:            NSFont.labelFontOfSize_(margin*1.5),
			NSForegroundColorAttributeName: NSColor.whiteColor(),
		}
		tw, _ = clock.sizeWithAttributes_(attr)
		clock.drawAtPoint_withAttributes_((width-margin-tw, height-2.*margin), attr)
		app.dockTile().setBadgeLabel_(clock)
	
		# page number
		page_number = NSString.stringWithString_("%s/%s (%s/%s)" % (
			self.page.label(), last_frame, current_page+1, page_count))
		attr = {
			NSFontAttributeName:            NSFont.labelFontOfSize_(font_size),
			NSForegroundColorAttributeName: NSColor.whiteColor(),
		}
		tw, _ = page_number.sizeWithAttributes_(attr)
		page_number.drawAtPoint_withAttributes_((margin*1.5+current_width,
		                                         height-1.4*margin), attr)
		
		# notes
		note = NSString.stringWithString_("\n".join(notes[current_page]))
		note.drawAtPoint_withAttributes_((margin, 0), {
			NSFontAttributeName:            NSFont.labelFontOfSize_(font_size*0.6),
			NSForegroundColorAttributeName: NSColor.whiteColor(),
		})
		
		# help
		if self.show_help:
			help_text = _h("".join([
				"<table style='color: white; font-family: LucidaGrande; font-size: 8pt;'>"
			] + [
				"<tr><th style='padding: 0 1em;' align='right'>%s</th><td>%s</td></tr>" % h for h in self.genHelp()
			] + [
				"</table>"
			]))
			help_text.drawAtPoint_((2*margin+current_width, 0))
		
		# next page
		try:
			page = pdf.pageAtIndex_(current_page+1)
			page_rect = page.boundsForBox_(kPDFDisplayBoxCropBox)
		except:
			return
		_, (w, h) = page_rect
		r = current_width/2./w
		
		NSGraphicsContext.saveGraphicsState()
		transform = NSAffineTransform.transform()
		transform.translateXBy_yBy_(2*margin+current_width, height-2.5*margin)
		transform.scaleXBy_yBy_(r, r)
		transform.translateXBy_yBy_(0., -h)
		transform.concat()
		bbox.concat()
		
		NSEraseRect(page_rect)
		page.drawWithBox_(kPDFDisplayBoxCropBox)
		NSColor.colorWithCalibratedWhite_alpha_(.25, .25).setFill()
		NSRectFillUsingOperation(page_rect, NSCompositingOperationSourceAtop)
		NSGraphicsContext.restoreGraphicsState()
	
	def genHelp(self):
		help = HELP
		if self.absolute_time:
			help = help + HELP_CLOCK
		else:
			help = help + HELP_TIMER
#		if not movie_view.isHidden():
#			help = help + HELP_MOVIE
		if not web_view.isHidden():
			help = help + HELP_WEB
		if not poll_view.isHidden():
			help = help + HELP_POLL
		if not slide_view.isHidden():
			help = help + HELP_SLIDES
			if drawings[current_page]:
				help = help + HELP_ANNOTATIONS

		return help
		
	def resetCursorRects(self):
		# updates rectangles only if needed (so that tooltip timeouts work)
		annotation_state = (self.transform.transformStruct(), current_page)
		if self.annotation_state == annotation_state:
			return
		self.annotation_state = annotation_state
		
		# reset cursor rects and tooltips
		self.discardCursorRects()
		self.removeAllToolTips()
		
		for i, annotation in enumerate(self.page.annotations()):
			if type(annotation) != PDFAnnotationLink:
				continue
			
			origin, size = annotation.bounds()
			rect = (self.transform.transformPoint_(origin),
			        self.transform.transformSize_(size))
			self.addCursorRect_cursor_(rect, NSCursor.pointingHandCursor())
			
			self.addToolTipRect_owner_userData_(rect, self, i)
	
	
	def view_stringForToolTip_point_userData_(self, view, tag, point, data):
		annotation = self.page.annotations()[data]
		return annotation.toolTip() or ""
	
	
	def keyDown_(self, event):
		c = event.characters()
		
		if event.modifierFlags() & NSAlternateKeyMask:
			c = event.charactersIgnoringModifiers()
			if c == "i": # reset bbox to identity
				global bbox
				bbox = NSAffineTransform.transform()
		elif event.modifierFlags() & NSCommandKeyMask:
			if c == NSLeftArrowFunctionKey:
				c = NSPrevFunctionKey
			elif c == NSRightArrowFunctionKey:
				c = NSNextFunctionKey
		
		if c == "q": # quit
			app.terminate_(self)
		
		elif c ==  "\uf72c": # remote pointer - back
			prev_page()
		elif c ==  "\uf72d": # remote pointer - forward
			next_page()

		elif c == chr(27): # esc
			toggle_fullscreen(fullscreen=False)
		
		elif c == "h":
			app.hide_(app)
		
		elif c == "?":
			self.show_help = not self.show_help
		
		elif c == chr(127) or c == chr(8): # delete-back or backspace
			prev_page()
		
#		elif c == " " and movie_view.isHidden(): # next page
#			next_page()
			
#		elif c == " " and not movie_view.isHidden(): # play/pause video
#			playing = movie_view.movie().rate() > 0.
#			if playing:
#				movie_view.pause_(self)
#			else:
#				movie_view.play_(self)
		
#		elif c in "<>" and not movie_view.isHidden(): # movie navigation
#			movie_view.pause_(self)
#			if c == "<":
#				movie_view.stepBackward_(self)
#			else:
#				movie_view.stepForward_(self)
		
		elif c == "t": # toggle clock/timer
			self.absolute_time = not self.absolute_time
			now = time.time()
			if self.absolute_time:
				self.elapsed_duration += (now - self.start_time)
			else:
				self.start_time = now
		
		elif c in "z[]{}" and self.absolute_time: # timer management
			self.start_time = time.time()
			self.elapsed_duration = 0
			
			self.duration += {
				"{": -600,
				"[":  -60,
				"z":    0,
				"]":   60,
				"}":  600,
			}[c]
			self.duration = max(0, self.duration)
			self.duration_change_time = time.time()
		
		elif c in "+=-_0"and not web_view.isHidden(): # web view scale
			if c == "=": c = "+"
			if c == "_": c = "-"
			
			document = web_view.mainFrame().frameView().documentView()
			clip = document.superview()
			if c == "+":
				scale = (1.1, 1.1)
			elif c == "-":
				scale = (1./1.1, 1./1.1)
			else:
				scale = clip.convertSize_fromView_((1., 1.), None)
			clip.scaleUnitSquareToSize_(scale)
			document.setNeedsLayout_(True)
		
		elif c == 'e': # erase annotation
			del drawings[current_page]
		
		else:
			action = {
				"F":                     toggle_windowed_fullscreen,
				"f":                     toggle_fullscreen,
				NSF5FunctionKey:         toggle_fullscreen,
				".":                     toggle_black_view,
				"b":                     toggle_black_view,
				"w":                     toggle_web_view,
#				"m":                     toggle_movie_view,
				"s":                     presentation_show,
				"p":                     toggle_poll_view,
				NSUpArrowFunctionKey:    prev_frame,
				NSLeftArrowFunctionKey:  prev_page,
				NSPageUpFunctionKey:     prev_section,
				NSDownArrowFunctionKey:  next_frame,
				NSRightArrowFunctionKey: next_page,
				NSPageDownFunctionKey:   next_section,
				NSHomeFunctionKey:       home_page,
				NSEndFunctionKey:        end_page,
				NSPrevFunctionKey:       back,
				NSNextFunctionKey:       forward,
			}.get(c, nop)
			action()
		
		refresher.refresh_()
	
	def scrollWheel_(self, event):
		if not (event.modifierFlags() & NSAlternateKeyMask):
			return
		p = event.locationInWindow()
		p = self.transform.transformPoint_(p)
		bbox.translateXBy_yBy_(p.x, p.y)
		bbox.scaleBy_(exp(event.deltaY()*0.01))
		bbox.translateXBy_yBy_(-p.x, -p.y)
		refresher.refresh_()
	
	def mouseDown_(self, event):
		global state
		assert state == IDLE
		if event.modifierFlags() & NSAlternateKeyMask:
			state = BBOX
		else:
			self.press_location = event.locationInWindow()
			state = CLIC
	
	def mouseDragged_(self, event):
		global state
		if state == CLIC:
			location = event.locationInWindow()
			if hypot(location.x-self.press_location.x, location.y-self.press_location.y) < 5:
				return
			self.path = NSBezierPath.bezierPath()
			self.path.setLineCapStyle_(NSRoundLineCapStyle)
			self.path.moveToPoint_(self.transform.transformPoint_(self.press_location))
			self.path.lineToPoint_(self.transform.transformPoint_(location))
			drawings[current_page].append(self.path)
			state = DRAW
		elif state == DRAW:
			self.path.lineToPoint_(self.transform.transformPoint_(event.locationInWindow()))
		elif state == BBOX:
			delta = self.transform.transformSize_((event.deltaX(), -event.deltaY()))
			bbox.translateXBy_yBy_(delta.width, delta.height)
		refresher.refresh_()
	
	def mouseUp_(self, event):
		global state
		if state == CLIC:
			self.click_(event)
		state = IDLE
		refresher.refresh_()
	
	def click_(self, event):
		point = self.transform.transformPoint_(event.locationInWindow())
		annotation = self.page.annotationAtPoint_(point)
		if annotation is None:
			return
		
		if type(annotation) != PDFAnnotationLink:
			return
		
		if annotation in movies:
			movie, _ = movies[annotation]
			movie_view.setMovie_(movie)
			presentation_show(movie_view)
			movie_view.play_(self)
			return
		
		action = annotation.mouseUpAction()
		destination = annotation.destination()
		url = annotation.URL()
		
		if type(action) == PDFActionNamed:
			action_name = action.name()
			action = {
				kPDFActionNamedNextPage:     next_page,
				kPDFActionNamedPreviousPage: prev_page,
				kPDFActionNamedFirstPage:    home_page,
				kPDFActionNamedLastPage:     end_page,
				kPDFActionNamedGoBack:       back,
				kPDFActionNamedGoForward:    forward,
#				kPDFActionNamedGoToPage:     nop,
#				kPDFActionNamedFind:         nop,
#				kPDFActionNamedPrint:        nop,
			}.get(action_name, nop)
			action()
		
		elif destination:
			goto_page(pdf.indexForPage_(destination.page()))
		
		elif url:
			args=('%s'%url).split('%20')
			if url.scheme() == 'http' or url.scheme() == 'https':
				nsurl = NSURLRequest.requestWithURL_(url)
				host = re.match(r'https?://([^/]*).*','%s'%url)
				if host :
					NSURLRequest.setAllowsAnyHTTPSCertificate_forHost_(YES, host.group(1))
				web_view.mainFrame().loadRequest_(nsurl)
			elif re.match(r'file:.*\.sh$',args[0]) :
				args[0]=args[0][7:]
				args.insert(0,"runTerminal")
				os.spawnvp(os.P_NOWAIT,args[0],args)
			else:
				NSWorkspace.sharedWorkspace().openURL_(url)

# window utils ###############################################################

def create_window(title, Window=NSWindow):
	window = Window.alloc().initWithContentRect_styleMask_backing_defer_screen_(
		PRESENTER_FRAME,
		NSMiniaturizableWindowMask|NSResizableWindowMask|NSTitledWindowMask,
		NSBackingStoreBuffered,
		NO,
		None,
	)
	window.setTitle_(title)
	window.makeKeyAndOrderFront_(nil)
	return window

def create_view(window, View=NSView):
	view = View.alloc().initWithFrame_(window.frame())
	window.setContentView_(view)
	window.setInitialFirstResponder_(view)
	return view

def add_subview(view, subview, autoresizing_mask=NSViewWidthSizable|NSViewHeightSizable):
#	sys.stderr.write("view %s " % view)
#	sys.stderr.write("subview %s\n" % subview)
	subview.setAutoresizingMask_(autoresizing_mask)
	subview.setFrameOrigin_((0, 0))
	view.addSubview_(subview)


# presentation window ########################################################

presentation_window = create_window(file_name)
presentation_view   = presentation_window.contentView()
presentation_frame = presentation_view.frame()

# slides

slide_view = SlideView.alloc().initWithFrame_(presentation_frame)
add_subview(presentation_view, slide_view)

# black view

class BlackView(NSView):
	def drawRect_(self, rect):
		bounds = self.bounds()
		NSRectFillUsingOperation(bounds, NSCompositingOperationClear)

black_view = BlackView.alloc().initWithFrame_(presentation_frame)
add_subview(presentation_view, black_view)

# poll view

class PollView(NSView):
	def drawRect_(self, rect):
		bounds = self.bounds()
		NSRectFillUsingOperation(bounds, NSCompositingOperationCopy)

poll_view = PollView.alloc().initWithFrame_(presentation_frame)
add_subview(presentation_view, poll_view)

# web view

web_view = WebView.alloc().initWithFrame_frameName_groupName_(presentation_frame, nil, nil)

class WebFrameLoadDelegate(NSObject):
	def webView_didCommitLoadForFrame_(self, view, frame):
		presentation_show(web_view)
web_frame_load_delegate = WebFrameLoadDelegate.alloc().init()
web_view.setFrameLoadDelegate_(web_frame_load_delegate)

add_subview(presentation_view, web_view)

# movie view

#class MovieView(AVMovieView):
#	def setHidden_(self, hidden):
#		QTMovieView.setHidden_(self, hidden)
#		if self.isHidden():
#			self.pause_(self)
#
#movie_view = MovieView.alloc().initWithFrame_(presentation_frame)
#movie_view.setPreservesAspectRatio_(True)

#add_subview(presentation_view, movie_view)

# message view

if show_feed:
	presentation_frame.size.height = 40
	message_view = MessageView.alloc().initWithFrame_(presentation_frame)
	add_subview(presentation_view, message_view, NSViewWidthSizable)


# views visibility

def presentation_show(visible_view=slide_view):
	for view in [slide_view, black_view, web_view, poll_view]: #, movie_view
		view.setHidden_(view != visible_view)

def toggle_view(view):
	presentation_show(view if view.isHidden() else slide_view)

def toggle_poll_view(): toggle_view(poll_view)
def toggle_black_view(): toggle_view(black_view)
def toggle_web_view():   toggle_view(web_view)
#def toggle_movie_view(): toggle_view(movie_view)
def toggle_slide_view(): toggle_view(slide_view)

presentation_show()


# presenter window ###########################################################

presenter_window = create_window(file_name)
presenter_view   = create_view(presenter_window, PresenterView)

presenter_window.center()
presenter_window.makeFirstResponder_(presenter_view)


# handling full screens ######################################################
def toggle_windowed_fullscreen():
	global window_present
	if window_present:
		window_present=False
	else:
		toggle_fullscreen(False)
		window_present=True

def toggle_fullscreen(fullscreen=None):
	global window_present
	window_present=False
	_fullscreen = presenter_view.isInFullScreenMode()
	if fullscreen is None:
		fullscreen = not _fullscreen
	
	if fullscreen != _fullscreen:
		for window, screen in reversed(list(zip([presenter_window, presentation_window],
		                                        NSScreen.screens()))):
			view = window.contentView()
			if fullscreen:
				view.enterFullScreenMode_withOptions_(screen, {})
			else:
				view.exitFullScreenModeWithOptions_({})
		presenter_window.makeFirstResponder_(presenter_view)
	
	return _fullscreen


# application delegate #######################################################

def add_item(menu, title, action, key="", modifiers=NSCommandKeyMask, target=app):
	menu_item = menu.addItemWithTitle_action_keyEquivalent_(
		NSString.localizedStringWithFormat_(" ".join(("%@",) * len(title)), *(_s(s) for s in title)),
		action, key)
	menu_item.setKeyEquivalentModifierMask_(modifiers)
	menu_item.setTarget_(target)
	return menu_item


class ApplicationDelegate(NSObject):
	def about_(self, sender):
		app.orderFrontStandardAboutPanelWithOptions_({
			"ApplicationName":    _s(NAME),
			"Version":            _s(VERSION),
			"Copyright":          _s(COPYRIGHT),
			"ApplicationVersion": _s("%s %s" % (NAME, VERSION)),
			"Credits":            _h(CREDITS),
			"ApplicationIcon":    ICON,
		})
	
	def update_(self, sender):
		nsurl = NSURLRequest.requestWithURL_(NSURL.URLWithString_(HOME + "releases/version.txt"))
		NSURLRequest.setAllowsAnyHTTPSCertificate_forHost_(YES, nsurl.host())
		try:
			data, response, _ = NSURLConnection.sendSynchronousRequest_returningResponse_error_(
				nsurl, None, None
			)
			assert response.statusCode() == 200 # found
		except:
			NSAlert.alertWithError_(
				NSError.errorWithDomain_code_userInfo_("unable to connect to internet,", 1, {})
			).runModal()
			return
		
		version = bytearray(data).decode("utf-8").strip()
		if version == VERSION:
			title   = "No update available"
			message = "Your version (%@) of %@ is up to date."
		else:
			title =   "Update available"
			message = "A new version (%@) of %@ is available."
		
		if NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
			title,
			"Go to website", "Cancel", None,
			message, version, _s(NAME),
		).runModal() != NSAlertDefaultReturn:
			return
		
		NSWorkspace.sharedWorkspace().openURL_(NSURL.URLWithString_(HOME))
	
	
	def applicationDidFinishLaunching_(self, notification):
		main_menu = NSMenu.alloc().initWithTitle_("MainMenu")
		
		application_menuitem = main_menu.addItemWithTitle_action_keyEquivalent_("Application", None, " ")
		application_menu = NSMenu.alloc().initWithTitle_("Application")
#		app.setAppleMenu_(application_menu)
		
		add_item(application_menu, ["About", NAME], "about:", target=self)
		add_item(application_menu, ["Check for updates…"], "update:", target=self)
		application_menu.addItem_(NSMenuItem.separatorItem())
		add_item(application_menu, ["Hide", NAME], "hide:", "h")
		add_item(application_menu, ["Hide Others"], "hideOtherApplications:", "h", NSCommandKeyMask | NSAlternateKeyMask)
		add_item(application_menu, ["Show All"], "unhideAllApplications:")
		application_menu.addItem_(NSMenuItem.separatorItem())
		add_item(application_menu, ["Quit", NAME], "terminate:", "q")
		main_menu.setSubmenu_forItem_(application_menu, application_menuitem)
		
		app.setMainMenu_(main_menu)
		
		app.setApplicationIconImage_(ICON)
	
	
	def applicationWillHide_(self, notification):
		self.fullscreen = toggle_fullscreen(fullscreen=False)
	
	def applicationDidUnhide_(self, notification):
		toggle_fullscreen(fullscreen=self.fullscreen)
	
	def applicationWillTerminate_(self, notification):
		presentation_show()

application_delegate = ApplicationDelegate.alloc().init()
app.setDelegate_(application_delegate)


# HACK: ensure ApplicationDelegate.applicationDidFinishLaunching_ is called
if restarted:
	NSNotificationCenter.defaultCenter().postNotificationName_object_(
		NSApplicationDidFinishLaunchingNotification, app)


# main loop ##################################################################

class Refresher(NSObject):
	def refresh_(self, timer=None):
		for window in app.windows():
			window.contentView().setNeedsDisplay_(True)
refresher = Refresher.alloc().init()

refresher_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
	1.,
	refresher, "refresh:",
	nil, YES)

sys.exit(app.run())
