#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#adding path of audio player to the lib
import sys

if 'play/' not in sys.path:
    sys.path.append('play/')

#ui is calling the database
if 'db-tools/' not in sys.path:
    sys.path.append('db-tools/')

#running server
import runIG
