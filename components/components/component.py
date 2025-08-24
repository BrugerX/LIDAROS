from abc import ABC,abstractmethod

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from persona import Persona

class Component(Node):

    def __init__(self,persona: Persona,type = "base"):


