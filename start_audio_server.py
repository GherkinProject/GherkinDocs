#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#adding path of audio player to the lib
import sys
if 'audio/' not in sys.path:
    sys.path.append('audio/')

#running server
import ghk_server
