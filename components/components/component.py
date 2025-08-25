from abc import ABC,abstractmethod

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from persona import Persona

from persona import Persona



class ComponentProfile(Node,ABC):

    def __init__(self,persona: Persona):
        self.persona = persona


        #TODO: Implement positions

        #The Node parent class needs to be given a name

        super.__init__(self.id)

    @property
    def id(self) -> str:
        #We use persona.getID() to ensure a single source of truth
        return self._persona.getID()

    def getID(self):
        return self.persona.getID()

    def getPersona(self):
        return self.persona

class DeviceProfile(ComponentProfile,ABC):
    def __init__(self,persona:Persona):
        super.__init__(persona)

    @abstractmethod
    def isConnected(self) -> bool:
        """
        Check if the device is properly connected

        :return: True if the device is properly connected, false otherwise
        """
        pass

    @abstractmethod
    def turnOn(self) -> bool:
        """
        Turn on the connected device

        :return: True if device is turned on and properly connected
        """

        if not (self.isConnected()):
            raise RuntimeWarning(f"Device {self.id} is not connected!")

        pass


