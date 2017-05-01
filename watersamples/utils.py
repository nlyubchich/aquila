from collections import OrderedDict

UNDERGROUND_SOURCE_TYPE = 'underground'
SURFACE_SOURCE_TYPE = 'surface'

FIRST_SOURCE_CLASS = 1
SECOND_SOURCE_CLASS = 2
THIRD_SOURCE_CLASS = 3
UNFIT_SOURCE_CLASS = 4
SOURCE_CLASSIFICATION_CHOICES = OrderedDict([
    (FIRST_SOURCE_CLASS, 'First class source'),
    (SECOND_SOURCE_CLASS, 'Second class source'),
    (THIRD_SOURCE_CLASS, 'Third class source'),
    (UNFIT_SOURCE_CLASS, 'Unfit source'),
])

INTENSITY_ZERO = 0
INTENSITY_ONE = 1
INTENSITY_SECOND = 2
INTENSITY_THIRD = 3
INTENSITY_FOURTH = 4
INTENSITY_FIFTH = 5
INTENSITY_CHOICES = OrderedDict([
    (INTENSITY_ZERO, '0 - Not found'),
    (INTENSITY_ONE, '1 - Detected by taster'),
    (INTENSITY_SECOND, '2 - Detected by consumer'),
    (INTENSITY_THIRD, '3 - Easily detected'),
    (INTENSITY_FOURTH, '4 - Strong smell and taste'),
    (INTENSITY_FIFTH, '5 - Undrinkable'),
])

STATUS_NEW = 0
STATUS_CHECKED = 1
STATUS_CHOICES = OrderedDict([
    (STATUS_NEW, 'New intake'),
    (STATUS_CHECKED, 'Investigated intake'),
])
