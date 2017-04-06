from collections import OrderedDict

UNDERGROUND_SOURCE_TYPE = 'underground'
SURFACE_SOURCE_TYPE = 'surface'
SOURCE_TYPE_CHOICES = OrderedDict([
    ('underground', 'Underground'),
    ('surface', 'Surface'),
])

FIRST_SOURCE_CLASS = 1
SECOND_SOURCE_CLASS = 2
THIRD_SOURCE_CLASS = 3
UNFIT_SOURCE_CLASS = 4
SOURCE_CLASSIFICATION_CHOICES = OrderedDict([
    (FIRST_SOURCE_CLASS, 'Перший клас'),
    (SECOND_SOURCE_CLASS, 'Другий клас'),
    (THIRD_SOURCE_CLASS, 'Третій клас'),
    (UNFIT_SOURCE_CLASS, 'Непридатне'),
])

INTENSITY_ZERO = 0
INTENSITY_ONE = 1
INTENSITY_SECOND = 2
INTENSITY_THIRD = 3
INTENSITY_FOURTH = 4
INTENSITY_FIFTH = 5
INTENSITY_CHOICES = OrderedDict([
    (INTENSITY_ZERO, '0 - не виявляються'),
    (INTENSITY_ONE, '1 - виявляються дегустатором'),
    (INTENSITY_SECOND, '2 - виявляються споживачем'),
    (INTENSITY_THIRD, '3 - виявляються легко'),
    (INTENSITY_FOURTH, '4 - сильний запах і присмак'),
    (INTENSITY_FIFTH, '5 - непридатна для пиття'),
])

STATUS_NEW = 0
STATUS_CHECKED = 1
STATUS_CHOICES = OrderedDict([
    (STATUS_NEW, 'Знятий'),
    (STATUS_CHECKED, 'Досліджений'),
])
