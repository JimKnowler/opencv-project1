import unittest

from stabiliser import Stabiliser

def helper_make_face(x, y, w, h):
    return (x,y,w,h)

class StabiliserTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_should_construct(self):
        stabiliser = Stabiliser()
        self.assertIsInstance(stabiliser, Stabiliser)

    def test_should_process_zero_faces(self):
        stabiliser = Stabiliser()
        has_face, face = stabiliser.process([])
        self.assertFalse(has_face)
        self.assertIsNone(face)

    def test_should_process_single_face(self):
        stabiliser = Stabiliser()
        test_face1 = helper_make_face(0,0,100,100)
        has_face, face = stabiliser.process([test_face1])
        self.assertTrue(has_face)
        self.assertTupleEqual(face, test_face1)
    
    def test_should_process_multiple_faces(self):
        stabiliser = Stabiliser()
        test_face_small = helper_make_face(90,90,10,10)
        test_face_large = helper_make_face(10,10,80,80)
        test_face_medium = helper_make_face(0,0,40,40)
        faces = [
            test_face_small,
            test_face_large,
            test_face_medium
        ]
        has_face, face = stabiliser.process(faces)
        self.assertTrue(has_face)
        self.assertTupleEqual(face, test_face_large)

    def test_should_persist_last_face_if_face_is_missing(self):
        stabiliser = Stabiliser()
        test_face1 = helper_make_face(0,0,100,100)
        stabiliser.process([test_face1])
        has_face, face = stabiliser.process([])
        self.assertTrue(has_face)
        self.assertTupleEqual(face, test_face1)
