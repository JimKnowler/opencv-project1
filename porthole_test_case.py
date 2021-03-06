import unittest

from porthole import Porthole

def helper_make_face(x, y, w, h):
    return (x,y,w,h)

def helper_make_rect(x, y, w, h):
    return (x,y,w,h)

class PortholeTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_should_construct(self):
        porthole = Porthole()
        self.assertIsInstance(porthole, Porthole)
    
    def test_should_construct_with_max_image_size(self):
        porthole = Porthole(1000,500)
        self.assertIsInstance(porthole, Porthole)
    
    def test_should_set_face(self):
        porthole = Porthole()
        test_face = helper_make_face(0,0,100,100)
        porthole.set_face(test_face)

    def test_should_set_padding(self):
        porthole = Porthole()
        porthole.set_padding(10)

    def test_should_get_bounding_box(self):
        porthole = Porthole()
        test_face = helper_make_face(100,100,6,8)
        porthole.set_face(test_face)
        rect = porthole.get_bounding_box()
        self.assertTupleEqual(rect, helper_make_rect(98,99,10,10))

    def test_should_get_bounding_box_with_padding(self):
        porthole = Porthole()
        test_face = helper_make_face(100,100,6,8)
        porthole.set_face(test_face)
        porthole.set_padding(10)
        rect = porthole.get_bounding_box()
        self.assertTupleEqual(rect, helper_make_rect(88,89,30,30))
    
    def test_should_clip_to_top_left_edges_of_image(self):
        porthole = Porthole()
        test_face = helper_make_face(-100,-100,6,8)
        porthole.set_face(test_face)
        rect = porthole.get_bounding_box()
        self.assertTupleEqual(rect, helper_make_rect(0,0,10,10))

    def test_should_clip_to_bottom_right_edges_of_image(self):
        porthole = Porthole(200, 100)
        test_face = helper_make_face(200,100,6,8)
        porthole.set_face(test_face)
        rect = porthole.get_bounding_box()
        self.assertTupleEqual(rect, helper_make_rect(190,90,10,10))