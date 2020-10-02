import requests
from . import config
from datetime import datetime
from pprint import pprint

class BoundingBox:
    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        
        # Size
        self.w = xmax - xmin
        self.h = ymax - ymin

        # Center
        self.x0 = xmin + 0.5 * (self.w)
        self.y0 = ymin + 0.5 * (self.h)
    
    def overlap(self, other):
        """
        Check if self overlaps other, assuming no rotations
        """
        w_diff = abs(self.x0 - other.x0)
        h_diff = abs(self.y0 - other.y0)

        return w_diff < 0.5 * (self.w + other.w) and h_diff < 0.5 * (self.h + other.h)
    
    def __str__(self):
        return 'BoundingBox(xmin={}, xmax={}, ymin={}, ymax={}, w={}, h={})'.format(self.xmin, self.xmax, self.ymin, self.ymax, self.w, self.h)
    
    def __repr__(self):
        return self.__str__()

class NotificationManager:
    def __init__(self, server, camera_id=0):
        self.prev = dict()
        self.server = server
        self.camera_id = camera_id

    def send_notification(self, label, bnd_box, msg, img):
        """
        Send a request to the notification server
        """
        files = {'image': img}
        data = {
            'time': datetime.today(),
            'camera_id': self.camera_id,
            'label': label,
            'rect_x': bnd_box.x0,
            'rect_y': bnd_box.y0,
            'rect_h': bnd_box.h,
            'rect_w': bnd_box.w,
            'msg': msg
        }

        resp = requests.post(self.server, files=files, data=data)
        print(resp.status_code)

    def notify(self, label, bnd_box, img):
        """
        Notify if the previous bounding boxes of the same classes don't overlap
        """
        prev_boxes = self.prev.get(label, [])

        is_overlap = False
        exists = False

        for bx in prev_boxes:
            if bx.overlap(bnd_box):
                is_overlap = True
            
            if str(bx) == str(bnd_box):
                exists = True
        
        if not is_overlap:
            # Send notification
            print('Detected: {}\nBox: {}, {}, {}, {}'.format(label, bnd_box.xmin, bnd_box.xmax, bnd_box.ymin, bnd_box.ymax))
            self.send_notification(label=label, bnd_box=bnd_box, msg='Detected: {}\nBox: {}, {}, {}, {}'.format(label, bnd_box.xmin, bnd_box.xmax, bnd_box.ymin, bnd_box.ymax), img=img)
            self.prev[label] = [bnd_box]
        elif not exists:
            self.prev[label].append(bnd_box)