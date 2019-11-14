# -*- coding: utf-8 -*-
import remi
import remi.gui as gui
import cv2
from threading import Timer, Thread
import traceback
import time

# noinspection PyUnresolvedReferences
class OpencvWidget(object):
    def _setup(self):
        #this must be called after the Widget super constructor
        self.on_new_image.do = self.do

    def do(self, callback, *userdata, **kwuserdata):
        #this method gets called when an event is connected, making it possible to execute the process chain directly, before the event triggers
        if hasattr(self.on_new_image.event_method_bound, '_js_code'):
            self.on_new_image.event_source_instance.attributes[self.on_new_image.event_name] = self.on_new_image.event_method_bound._js_code%{
                'emitter_identifier':self.on_new_image.event_source_instance.identifier, 'event_name':self.on_new_image.event_name}
        self.on_new_image.callback = callback
        self.on_new_image.userdata = userdata
        self.on_new_image.kwuserdata = kwuserdata
        #here the callback is called immediately to make it possible link to the plc
        if callback is not None: #protection against the callback replacements in the editor
            callback(self, *userdata, **kwuserdata)

    @gui.decorate_set_on_listener("(self, emitter)")
    @gui.decorate_event
    def on_new_image(self):
        return ()


class OpencvImRead(gui.Image, OpencvWidget):
    """ OpencvImRead widget.
        Allows to read an image from file.
        The event on_new_image can be connected to other Opencv widgets for further processing
    """
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADwAAAAuCAYAAAB04nriAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAFnQAABZ0B24EKIgAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAATOSURBVGiB5ZpdbBRVFMd/d6ZlpVCKQEF48jtEQkyMiRFNjEZe9AHUxMQHg/HBQOKjJD7ogxojwcYHIKAEP7AaYpQPQb6hQqpdqgIWRIpbChWU7W63y3a7O9vdmbk+lG637LYz087druH3tLn33HPOf+fOvWfujFi+eK7kFkKb7ATKTdXQD6HpBObcMZm5KGOgJ4y0LaBAcPWseh5cu33SklLJ6TeWk+0JA7fylHbDNHqYJ/9AExbdLCLJ/+8WcCW4GoPHWM8jcjMCG26s6+08w0HxHga3q8zRV1wIljwvV3IXzUU9C9lHnfyHRvEdNrqC9PzH8R5exO6SYoeYTxsP8aWvSanEUfBYYvM20tmmUnAUPFN2OTqZxWU/cikLjoJj3OvoJMr9viRTDhwFh8RSRych8bQvyTjRYfxES2IrphwYtw/HVbqDpzjHMhbxfcn+Tp7gLC+MOwE35KTBt92raU83kZMZ2vr38OqCrQTENM++XFVae0UDx8VqckzNt5kECLKK7eITQHgO7JaEFebTf1/mbGofOZkB4O/MKXZF3x6XP1eFh41OkFW0iteYQwgNkwgLsb0Vap7pTJ9gT+wdwtkLRX3t6aNcTLdwT80STz49ZWyjE2GhpwDjIScNjvau42RyB/1WtKRNxkrSFF/P3TWPIjzMMLWXyCWmzBLLdRHJdtBpBOnMBIlkLzqO6xo4STCxlSV1r7iO5UmwQQJDJAjI6UylDm2C5eSp5E5+T+4ikguRNHuwMT2Nt6RJa982Hq59kSlajasxjoLDop1mfQtXtTOkiGOKDDrV3CZrmSHnMVveyX3ycRZbz7r+A+LmVXZF36LTaJ3QFgMQyYbYH1vDsvp3XdmPKbhJ30Cr/hV9IlLUlxbX6RVXuMxvnGYnx/RNPGAv5UnzdaqYMqrP86kj7I+tJZrrcJWgG86lDrJk5grqq+9xtB11WzpY9SHHqjaWFHszNhZhcYEmfQMbpzxHi/5FSbtfEtvYHn3TV7EASSvK/tgaV7YlBbfpuzmhfU2OjOfg18R59la9z2fVK0gTz7cHE40cijeQsno9+3TDxXQLZ1P7HO2KBA+IFEf19WRE37iD21iEtGY2V7/EJa2V4/GPORxvIGXFnQePk6w0aI5vwZJjL3xFgg/oa4kK5y3BDd3aXzTqKzlirsOwkr74HIur2TMcv75pTJsRgrOkCWn+PtsaWgJzfgbqfHVbEiltTiV30D/GbTNC8M/658TEZf8z0YF5QK3/rm8mluviQOyDUftHCO7UTqjLpAqYT1lEn0//yJVMW8m+vGCJTVgUF+m+MiR6qpPhxEhbvRyKN5TsywvOYdAvetRmAoOiF4DqQ85LRiu/9n1T1J4XbIqs2gwKCYDqM3xLmgQTjUWla16w18J9wtQC09WGuJb9k8O9H41oKxBsqY1+MxowR32Ytv4fsAuKkRGLVtmpAWarDZEwr2HYw1VjgeBJ+hBgJsoXMFMOPxNM/uvSADBXbYjCizn5ggFmMCi8DFSGYB3lV3mIyhAMg1uU4m0KKkmwQPmKDQWCvZztKqOGwVVbIQWCK+ANvgBmqQ2hDf+okNkdQGkFJvKfHmqCVH2Z6+nRkIAJftVCNQkdcaOQHD6XtiXTuitgWiumQuZx+fgPED6yi1RbbEEAAAAASUVORK5CYII="
    @gui.decorate_constructor_parameter_types(["file"])
    def __init__(self, filename, **kwargs):
        self.app_instance = None
        super(OpencvImRead, self).__init__("", **kwargs)
        OpencvWidget._setup(self)
        self.style.update({'position':'absolute','left':'10px','top':'10px','width':'200px','height':'180px'})
        self.frame_index = 0
        self.set_image(filename)

    def _need_update(self, emitter=None):
        #overriding this method allows to correct the image url that gets updated by the editor
        gui.Image.set_image(self, '/%(id)s/get_image_data?index=%(frame_index)s'% {'id': id(self), 'frame_index':0})
        super(OpencvImRead, self)._need_update(emitter)

    def on_new_image_listener(self, emitter):
        if emitter.img is None:
            return
        self.set_image_data(emitter.img)

    def set_image(self, filename):
        self.set_image_data(cv2.imread(filename, cv2.IMREAD_COLOR)) #cv2.IMREAD_GRAYSCALE)#cv2.IMREAD_COLOR)

    def set_image_data(self, img):
        self.img = img
        self.update()
        self.on_new_image()

    def search_app_instance(self, node):
        if issubclass(node.__class__, remi.server.App):
            return node
        if not hasattr(node, "get_parent"):
            return None
        return self.search_app_instance(node.get_parent()) 

    def update(self, *args):
        if self.app_instance==None:
            self.app_instance = self.search_app_instance(self)
            if self.app_instance==None:
                return
        self.frame_index = self.frame_index + 1
        self.app_instance.execute_javascript("""
            url = '/%(id)s/get_image_data?index=%(frame_index)s';
            
            xhr = null;
            xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.responseType = 'blob'
            xhr.onload = function(e){
                urlCreator = window.URL || window.webkitURL;
                urlCreator.revokeObjectURL(document.getElementById('%(id)s').src);
                imageUrl = urlCreator.createObjectURL(this.response);
                document.getElementById('%(id)s').src = imageUrl;
            }
            xhr.send();
            """ % {'id': id(self), 'frame_index':self.frame_index})

    def get_image_data(self, index=0):
        try:
            ret, png = cv2.imencode('.png', self.img)
            if ret:
                headers = {'Content-type': 'image/png'}
                return [png.tostring(), headers]
        except:
            print(traceback.format_exc())
        return None, None


class OpencvVideo(OpencvImRead):
    """ OpencvVideo widget.
        Opens a video source and dispatches the image frame by generating on_new_image event.
        The event on_new_image can be connected to other Opencv widgets for further processing
    """
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAAAuCAYAAACoGw7VAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAKyAAACsgBvRoNowAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAXdSURBVHic7ZptTFNnFMf/z21rX1baQi0MBGojoesUJeJLNBhw6oddk5YuY2LMMjMSzLIYDCZLtsTEGbPpwvi0LQsSpgkpYRFDhpGYRVCnxCWObTi/YJ2ogKuDXspLwd7bPvsAmikKvaXlUuD3pcl9Oed//3l67rknD8ESMcXpdBqDweApIrWQ+U5xcbGM5/kMnucZsfcSQjYyDFNJKdUtGf0SWJY1MwzzPiHkHUqpiRDCUEqp2DiEEA2ARAB98ujLjF92795tk8lkVZTSXADJABhCJtbi099IWTIaQFlZmeLRo0fVAN6mlKbEIseiLx1Op9MoCEILgDUA1DFK0ye6wC8kWJbNFQThJoA8xM5kAIu4dNjt9g8opScBhFsqPJRSr5gchJDXAJgAkEVn9NGjR5mOjo5vQ6HQe4SQpDBv8wDYc/78+SticpWVlSn6+vqOE0IORaVGFxUVrQqFQvnRiBVj1AAOUUpXUUqfMAwj/P8kpZTg+fdWcPL49yMjI59fvnx5PJKkDofjzagYbbfbP5n8Gy5UgsFgcNWFCxfuRxqA4Xn+BKXUEk1VS0yF4Xm+/N69ex39/f03BUFwUEplUotaiMj9fr+/vLw8KT09PY9l2R+2bdsWGB4e/lGr1VYSQh7MJnhBTw/e6ukBAFxLS8PPmZkAgDvFdzCwZgAAkHUuC8v/XD7Lx5j/POuje3p6UF1dnVhaWppSU1PzUW9v7x+Dg4O/CYJgn3xJiCbN74eV42DlOKwYHX12fMgyBM7KgbNyGE+K6P0Sd0xp7wKBAFpbW+Wtra2JWVlZiXa7/cy6devGfD7fKZ1O9w0h5N9wg9dnZ6M+O3vK8byv8mYpO/6Yto92u92oqqoyaDQaQ0FBwadFRUUfcxz3u8FgOAngEiFE9ERrsRLWJ7jf70dLS4viwIEDxmPHju28evVqvc/nuz82NnaEUhpu07+oET3rcLvdqKysXH7w4MGMxsbGz7xeb9e+fftyYyFuIRHxJ/jg4CAaGhpUHo9HtX79elM0RS1EFvX0bi5ZMnqOWDJ6jpgXY1KLxYKSkhKkpaVBrY7u/D0QCODx48doa2vDlSuippxRRXKjLRYLKioq4HK50N3dHZMcKSkp2LlzJ6xWK6qrq2OSYyYkLx379+9HXV1dzEwGAI/HA5fLBavViuTk5JjlmQ5JjU5ISIBOp8ODB7OaXYUFpRSdnZ3IycmJea6XIanRK1eunBOTn+L1emEySdPyS146QqHQjNe0l7Sja2vXrHPxPI9ly5bNOk4kSG50OHCvc7hech1nj5wFl8pJLSci4sJoAOCVPLzpXjQfbkbbh20IqAJSSxJFxO2d2WyGw+Hwbdq0abyxsfFhNEVNx3jCONwb3eh9oxd5zXmwXbMBcTCsFWW0QqHA5s2bqcPh8JpMpod6vf5LmUx2rqmpqSJWAl8GZSj8ej9uvHsDt7ffxo6aHUjsS5xLCaIJy+jU1FSwLDtSWFjIA2jS6/XHCSF/Pz1vt9tjJnA6eBUP74qJcpLxVwby6/OhGFdIomUmXmk0wzDIycmhe/fuHUhPT/dptdpKhmHOEELG5lJgOIxrJ8uJbbKc/GKTWtIUphidlJSEXbt2jbAsO8YwzCW9Xv8FIeSWFOLEQGUT5aR9Tzs0Pg3MnWapJT2HHJjYZL127Vo4nU7OYrEMajSar5VK5WlCyOhMAeYLylElDP8YsL12O3T9OqnlTEGu0+k0tbW1AzKZrNVgMJwghHRILUoM8idyaIY02NqwFZm3MqWW80rkCoXisNForCOEDEktRgwkRKAeVmN122rkXswFCc3vPfVyQsh3UosQi3pYjdSuVOS78qEaUUktJywkn0eLQTmqhK5fh8LThfO+b36RuDCaCTLQerXId+XP6zo8HXFh9IbmDTA+NIIJxs1oZgpxYbSpO/63jcTvEokzorKiQ6HQRQDCjBe+gNlsztqyZUupzWbjo6FjJlQqlezu3bu/Ukp/EnMfwzBEEIT+2eT+D23+73+IM13aAAAAAElFTkSuQmCC"
    @gui.decorate_constructor_parameter_types([int, int])
    def __init__(self, video_source, framerate_hz, **kwargs):
        self.capture = cv2.VideoCapture(video_source)
        self.thread_stop_flag = False
        self.framerate = framerate_hz
        self.frame_index = 0
        self.last_frame = None
        super(OpencvVideo, self).__init__("", **kwargs)
        self.thread = Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()

    def set_image_data(self, image_data_as_numpy_array):
        #oveloaded to avoid update
        self.img = image_data_as_numpy_array

    def search_app_instance(self, node):
        if issubclass(node.__class__, remi.server.App):
            return node
        if not hasattr(node, "get_parent"):
            return None
        return self.search_app_instance(node.get_parent()) 

    def __del__(self):
        self.thread_stop_flag = True
        super(OpencvVideo, self).__del__()

    def update(self, *args):
        while not self.thread_stop_flag:
            time.sleep(1.0/self.framerate)
            if self.app_instance==None:
                self.app_instance = self.search_app_instance(self)
                if self.app_instance==None:
                    continue

            with self.app_instance.update_lock:
                self.frame_index = self.frame_index + 1
                self.app_instance.execute_javascript("""
                    var url = '/%(id)s/get_image_data?index=%(frame_index)s';
                    var xhr = new XMLHttpRequest();
                    xhr.open('GET', url, true);
                    xhr.responseType = 'blob'
                    xhr.onload = function(e){
                        var urlCreator = window.URL || window.webkitURL;
                        urlCreator.revokeObjectURL(document.getElementById('%(id)s').src);
                        var imageUrl = urlCreator.createObjectURL(this.response);
                        document.getElementById('%(id)s').src = imageUrl;
                    }
                    xhr.send();
                    """ % {'id': id(self), 'frame_index':self.frame_index})
                

    def get_image_data(self, index=0):
        try:
            ret, frame = self.capture.read()
            if ret:
                self.set_image_data(frame)
                self.on_new_image()
                ret, png = cv2.imencode('.png', frame)
                if ret:
                    headers = {'Content-type': 'image/png'}
                    # tostring is an alias to tobytes, which wasn't added till numpy 1.9
                    return [png.tostring(), headers]
        except:
            print(traceback.format_exc())
        return None, None


class OpencvCrop(OpencvImRead):
    """ OpencvCrop widget.
        Allows to crop an image.
        Receives an image on on_new_image_listener.
        The event on_new_image can be connected to other Opencv widgets for further processing
    """
    icon = "data:image/png;base64,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"
    @gui.decorate_constructor_parameter_types([int, int, int, int])
    def __init__(self, x, y, w, h, **kwargs):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        super(OpencvCrop, self).__init__("", **kwargs)

    def on_new_image_listener(self, emitter): #CROP
        if emitter.img is None:
            return
        self.img = emitter.img[self.x:self.x+self.w, self.y:self.y+self.h]
        self.set_image_data(self.img)


class OpencvThreshold(OpencvImRead):
    """ OpencvThreshold widget.
        Allows to threashold an image.
        Receives an image on on_new_image_listener.
        The event on_new_image can be connected to other Opencv widgets for further processing
    """
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADwAAAAuCAYAAAB04nriAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAETSURBVGhD7ZYBDsMgCEV197+zG+m60EwBHXaCvKRZslnhlT/TnFIqr2sbHu/PbdhO+BLpUnymO2fQPIhIe0ccaRwLjIW/QXekW7IA9duKqETakjQrbG2CHHFKe4cVlpzCll5YzEwYzhJ8jSISpiZ4x3RrgqPScNen4xWjSYlJ+8V7LBtpaJKb4siUlxOWiP4C7PzXSGvIcX3jGiJhrqmRB6U9RaoHXIuMNCyUNHauk6wFpOtm0BQebYq7b5asdN8phxYUrzUwS7aHqrBWY+c+rQegjaTGl7B2Y3eIYrh6UyK9Mhfhu6cxC8pj7wl7ojXlmLAnalOGb/pfhA0TkfZOCHsnhL0Twt4JYe+EsHdC2DcpPQHUiTG7/qs9SwAAAABJRU5ErkJggg=="
    @gui.decorate_constructor_parameter_types([int])
    def __init__(self, threshold_value, **kwargs):
        self.threshold_value = threshold_value
        super(OpencvThreshold, self).__init__("", **kwargs)

    def on_new_image_listener(self, emitter): #THRESHOLD
        if emitter.img is None:
            return
        img = emitter.img
        if len(img.shape)>2:
            img = cv2.cvtColor(emitter.img, cv2.COLOR_BGR2GRAY)
        res, self.img = cv2.threshold(img,self.threshold_value,255,cv2.THRESH_BINARY)
        self.set_image_data(self.img)
        

class OpencvSplit(OpencvImRead):
    """ OpencvSplit widget.
        Allows to get a single image channel.
        Receives an image on on_new_image_listener.
        The event on_new_image can be connected to other Opencv widgets for further processing
    """
    icon = "data:image/png;base64,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"
    @gui.decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        super(OpencvSplit, self).__init__("", **kwargs)
        self.on_new_image_first_component.do = self.do_first
        self.on_new_image_second_component.do = self.do_second
        self.on_new_image_third_component.do = self.do_third
        self.backup_img = None

    def on_new_image_listener(self, emitter):
        if emitter.img is None:
            return
        self.backup_img = emitter.img
        self.set_image_data(emitter.img)
        if not self.on_new_image_first_component.callback is None:
            self.on_new_image_first_component(emitter.img)
        if not self.on_new_image_second_component.callback is None:
            self.on_new_image_second_component(emitter.img)
        if not self.on_new_image_third_component.callback is None:
            self.on_new_image_third_component(emitter.img)

    def do_first(self, callback, *userdata, **kwuserdata):
        #this method gets called when an event is connected, making it possible to execute the process chain directly, before the event triggers
        if hasattr(self.on_new_image_first_component.event_method_bound, '_js_code'):
            self.on_new_image_first_component.event_source_instance.attributes[self.on_new_image_first_component.event_name] = self.on_new_image_first_component.event_method_bound._js_code%{
                'emitter_identifier':self.on_new_image_first_component.event_source_instance.identifier, 'event_name':self.on_new_image_first_component.event_name}
        self.on_new_image_first_component.callback = callback
        self.on_new_image_first_component.userdata = userdata
        self.on_new_image_first_component.kwuserdata = kwuserdata
        #here the callback is called immediately to make it possible link to the plc
        if callback is not None: #protection against the callback replacements in the editor
            if not self.backup_img is None:
                self.img = cv2.split(self.backup_img)[0]
            callback(self, *userdata, **kwuserdata)

    @gui.decorate_set_on_listener("(self, emitter)")
    @gui.decorate_event
    def on_new_image_first_component(self, img):
        if not self.backup_img is None:
            self.img = cv2.split(self.backup_img)[0]
        return ()

    def do_second(self, callback, *userdata, **kwuserdata):
        #this method gets called when an event is connected, making it possible to execute the process chain directly, before the event triggers
        if hasattr(self.on_new_image_second_component.event_method_bound, '_js_code'):
            self.on_new_image_second_component.event_source_instance.attributes[self.on_new_image_second_component.event_name] = self.on_new_image_second_component.event_method_bound._js_code%{
                'emitter_identifier':self.on_new_image_second_component.event_source_instance.identifier, 'event_name':self.on_new_image_second_component.event_name}
        self.on_new_image_second_component.callback = callback
        self.on_new_image_second_component.userdata = userdata
        self.on_new_image_second_component.kwuserdata = kwuserdata
        #here the callback is called immediately to make it possible link to the plc
        if callback is not None: #protection against the callback replacements in the editor
            if not self.backup_img is None:
                self.img = cv2.split(self.backup_img)[1]
            callback(self, *userdata, **kwuserdata)

    @gui.decorate_set_on_listener("(self, emitter)")
    @gui.decorate_event
    def on_new_image_second_component(self, img):
        if not self.backup_img is None:
            self.img = cv2.split(self.backup_img)[1]
        return ()

    def do_third(self, callback, *userdata, **kwuserdata):
        #this method gets called when an event is connected, making it possible to execute the process chain directly, before the event triggers
        if hasattr(self.on_new_image_third_component.event_method_bound, '_js_code'):
            self.on_new_image_third_component.event_source_instance.attributes[self.on_new_image_third_component.event_name] = self.on_new_image_third_component.event_method_bound._js_code%{
                'emitter_identifier':self.on_new_image_third_component.event_source_instance.identifier, 'event_name':self.on_new_image_third_component.event_name}
        self.on_new_image_third_component.callback = callback
        self.on_new_image_third_component.userdata = userdata
        self.on_new_image_third_component.kwuserdata = kwuserdata
        #here the callback is called immediately to make it possible link to the plc
        if callback is not None: #protection against the callback replacements in the editor
            if not self.backup_img is None:
                self.img = cv2.split(self.backup_img)[2]
            callback(self, *userdata, **kwuserdata)

    @gui.decorate_set_on_listener("(self, emitter)")
    @gui.decorate_event
    def on_new_image_third_component(self, img):
        if not self.backup_img is None:
            self.img = cv2.split(self.backup_img)[2]
        return ()


class OpencvBGRtoHSV(OpencvImRead):
    """ OpencvBGRtoHSV widget.
        Convert image colorspace from BGR to HSV.
        Receives an image on on_new_image_listener.
        The event on_new_image can be connected to other Opencv widgets for further processing
    """
    icon = "data:image/png;base64,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"
    @gui.decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        super(OpencvBGRtoHSV, self).__init__("", **kwargs)

    def on_new_image_listener(self, emitter):
        if emitter.img is None:
            return
        self.set_image_data(cv2.cvtColor(emitter.img,cv2.COLOR_BGR2HSV))


class OpencvBitwiseNot(OpencvImRead):
    """ OpencvBitwiseNot widget.
        Allows to invert an image mask.
        Receives an image on on_new_image_listener.
        The event on_new_image can be connected to other Opencv widgets for further processing
    """
    icon = "data:image/png;base64,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"
    @gui.decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        super(OpencvBitwiseNot, self).__init__("", **kwargs)

    def on_new_image_listener(self, emitter):
        try:
            self.set_image_data(cv2.bitwise_not(emitter.img))
        except:
            print(traceback.format_exc())


class BinaryOperator(object):
    def __init__(self, **kwargs):
        self.img1 = None
        self.img2 = None

    def process(self):
        #overload this method to perform different operations
        if not self.img1 is None:
            if not self.img2 is None:
                pass

    def on_new_image_1_listener(self, emitter):
        try:
            self.img1 = emitter.img
            self.process()
        except:
            print(traceback.format_exc())

    def on_new_image_2_listener(self, emitter):
        try:
            self.img2 = emitter.img
            self.process()
        except:
            print(traceback.format_exc())


class OpencvBitwiseAnd(OpencvImRead, BinaryOperator):
    """ OpencvBitwiseAnd widget.
        Allows to do the AND of two images.
            - Receives the image on on_new_image_1_listener.
            - Receives the mask on on_new_image_2_listener.
        The event on_new_image can be connected to other Opencv widgets for further processing
    """
    icon = "data:image/png;base64,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"
    @gui.decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        BinaryOperator.__init__(self)
        super(OpencvBitwiseAnd, self).__init__("", **kwargs)

    def process(self):
        if not self.img1 is None:
            if not self.img2 is None:
                self.set_image_data(cv2.bitwise_and(self.img1, self.img1, mask=self.img2))


class OpencvBitwiseOr(OpencvImRead, BinaryOperator):
    """ OpencvBitwiseOr widget.
        Allows to do the OR of two images.
            - Receives the image on on_new_image_1_listener.
            - Receives the mask on on_new_image_2_listener.
        The event on_new_image can be connected to other Opencv widgets for further processing
    """
    icon = "data:image/png;base64,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"
    @gui.decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        BinaryOperator.__init__(self)
        super(OpencvBitwiseOr, self).__init__("", **kwargs)

    def process(self):
        if not self.img1 is None:
            if not self.img2 is None:
                self.set_image_data(cv2.bitwise_or(self.img1, self.img1, mask=self.img2))


class OpencvAddWeighted(OpencvImRead, BinaryOperator):
    """ OpencvAddWeighted widget.
        Allows to do the add_weighted of two images.
            - Receives first image on on_new_image_1_listener.
            - Receives second mask on on_new_image_2_listener.
        The event on_new_image can be connected to other Opencv widgets for further processing
    """
    icon = "data:image/png;base64,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"
    @gui.decorate_constructor_parameter_types([float, float, float])
    def __init__(self, alpha, beta, gamma, **kwargs):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        BinaryOperator.__init__(self)
        super(OpencvAddWeighted, self).__init__("", **kwargs)

    def process(self):
        if not self.img1 is None:
            if not self.img2 is None:
                self.set_image_data(cv2.addWeighted(self.img1, self.alpha, self.img1, self.beta, self.gamma))