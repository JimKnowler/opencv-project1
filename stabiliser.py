class Stabiliser:
    def __init__(self):
        self._has_last_face = False
        self._last_face = None
    
    def process(self, faces):
        if len(faces) == 0:
            if self._has_last_face:
                return (True, self._last_face)
            else:
                return (False, None)
        
        face = self._get_largest_face(faces)

        self._has_last_face = True
        self._last_face = face

        return (True, face)

    def _get_largest_face(self, faces):
        max_area = 0
        largest_face = faces[0]
        
        for i, face in enumerate(faces):
            (_, _, w, h) = face
            area = w * h
            if area > max_area:
                largest_face = face
                max_area = area
        
        return largest_face