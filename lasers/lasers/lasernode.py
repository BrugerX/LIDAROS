from abc import ABC,abstractmethod
from components.component import DeviceProfile
from components.persona import Persona
from interfaces.srv import SetLaserPower


class LaserProfile(ABC,DeviceProfile):
    def __init__(self,persona: Persona):
        super().__init__(persona)

        #TODO: Add a way to get the power of each channel
        #For now we assume the power starts out as 0
        self.channel_powers = [0 for x in range(self.nr_channels)]

        #TODO: add services for getChannelPower and getTemperature

    @property
    def nr_channels(self) -> str:
        #We use persona.getID() to ensure a single source of truth
        return self._persona.getDescriptor()["nr_channels"]

    @abstractmethod
    def getChannelPower(self,channel_nr):
        pass

    @abstractmethod
    def setChannelPower(self,srv: SetLaserPower):
        pass

    def getTemperature(self):
        pass

if __name__ == "__main__":
    req = SetLaserPower.Request()
    # optionally: req.power_percent = 42.0
    print(req)

    # Or the response object:
    res = SetLaserPower.Response()
    print(res)