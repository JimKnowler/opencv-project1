import math

class Porthole:
    def __init__(self):
        self._padding = 0
    
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

        return (px, py, pw, ph)
        



        
        

