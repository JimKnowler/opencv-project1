import math

class Porthole:
    def __init__(self, max_width=640, max_height=480):
        self._padding = 0
        self._max_width = max_width
        self._max_height = max_height
    
    def set_face(self, face):
        self._face = face

    def set_padding(self, padding):
        self._padding = padding

    def get_bounding_box(self):
        x,y,w,h = self._face
        
        hw = w/2
        hh = h/2

        cx = x + hw
        cy = y + hh

        r = math.sqrt( (hw ** 2) + (hh ** 2) )

        r += self._padding

        px = int(cx - r)
        py = int(cy - r)
        pw = int(r * 2)
        ph = pw

        # clip top/left edges of porthole
        px = max(px, 0)
        py = max(py, 0)

        # clip size of porthole
        pw = min(pw, self._max_width)
        ph = min(ph, self._max_height)

        # clip bottom/right edges of porthole
        px = min(px, self._max_width - pw)
        py = min(py, self._max_height - ph)
        
        return (px, py, pw, ph)
        



        
        

