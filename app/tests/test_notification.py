from notification import NotificationManager, BoundingBox
import pytest

@pytest.fixture(scope='module')
def boxes():
    overlap_boxes = [
        BoundingBox(0, 10, 0, 10),
        BoundingBox(5, 15, 5, 15)
    ]

    no_overlap_boxes = [
        BoundingBox(0, 10, 0, 10),
        BoundingBox(11, 21, 0, 10)
    ]

    return overlap_boxes, no_overlap_boxes

def test_overlap(boxes):
    overlap_boxes, _ = boxes
    assert overlap_boxes[0].overlap(overlap_boxes[1])
    
def test_no_overlap(boxes):
    _, no_overlap_boxes = boxes
    assert not no_overlap_boxes[0].overlap(no_overlap_boxes[1])

def test_notify_overlap(boxes):
    overlap_boxes, _ = boxes
    noti_manager = NotificationManager()

    for bx in overlap_boxes:
        noti_manager.notify('label', bx, None)
    
    assert len(noti_manager.prev['label']) == 2

def test_notify_no_overlap(boxes):
    _, no_overlap_boxes = boxes
    noti_manager = NotificationManager()

    for bx in no_overlap_boxes:
        noti_manager.notify('label', bx, None)
    
    assert len(noti_manager.prev['label']) == 1