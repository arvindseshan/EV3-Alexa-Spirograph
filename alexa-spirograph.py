#!/usr/bin/env python3
# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
# 
# You may not use this file except in compliance with the terms and conditions 
# set forth in the accompanying LICENSE.TXT file.
#
# THESE MATERIALS ARE PROVIDED ON AN "AS IS" BASIS. AMAZON SPECIFICALLY DISCLAIMS, WITH 
# RESPECT TO THESE MATERIALS, ALL WARRANTIES, EXPRESS, IMPLIED, OR STATUTORY, INCLUDING 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

import os
import sys
import time
import logging
import json
import random
import threading

from enum import Enum
from agt import AlexaGadget

import spirograph

# Set the logging level to INFO to see messages from AlexaGadget
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))
logger = logging.getLogger(__name__)


class Direction(Enum):
    """
    The list of commands and their variations.
    These variations correspond to the skill slot values.
    """
    DRAW = ['draw', 'print']



class MindstormsGadget(AlexaGadget):
    """
    A Mindstorms gadget that draws patterns based on voice commands.
    """

    def __init__(self):
        """
        Performs Alexa Gadget initialization routines and ev3dev resource allocation.
        """
        super().__init__()

        # Gadget state

    def on_connected(self, device_addr):
        """
        Gadget connected to the paired Echo device.
        :param device_addr: the address of the device we connected to
        """
        logger.info("{} connected to Echo device".format(self.friendly_name))

    def on_disconnected(self, device_addr):
        """
        Gadget disconnected from the paired Echo device.
        :param device_addr: the address of the device we disconnected from
        """
        logger.info("{} disconnected from Echo device".format(self.friendly_name))

    def on_custom_mindstorms_gadget_control(self, directive):
        """
        Handles the Custom.Mindstorms.Gadget control directive.
        :param directive: the custom directive with the matching namespace and name
        """
        try:
            payload = json.loads(directive.payload.decode("utf-8"))
            print("Control payload: {}".format(payload), file=sys.stderr)
            control_type = payload["type"]
            #print(control_type)
            if control_type == "draw":
                # Expected params: [direction, duration, speed]
                self._draw(int(payload["pattern"]))

        except KeyError:
            print("Missing expected parameters: {}".format(directive), file=sys.stderr)

    def _draw(self, shape):
        """
        Handles drawing command from the directive.
        :param shape: the id of the shape to draw (int 1-5)
        """
        print("drawing shape #"+str(shape))
        # Call spirograph program from spirograph.py
        spirograph.spirograph(shape)


if __name__ == '__main__':

    gadget = MindstormsGadget()

    print("loaded Alexa code")

    # Gadget main entry point
    gadget.main()

   