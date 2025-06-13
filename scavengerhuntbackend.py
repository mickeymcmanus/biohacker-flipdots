from __future__ import absolute_import
import time
from .games.scavengerhunt import scavengerhunt

__author__ = 'boselowitz'

while True:
    scavengerhunt.compile_data()
    time.sleep(60)