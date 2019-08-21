"""Support for Tahoma lock."""
from datetime import timedelta
import logging

from homeassistant.components.lock import LockDevice
from homeassistant.const import ATTR_BATTERY_LEVEL, STATE_LOCKED, STATE_UNLOCKED

from . import DOMAIN as TAHOMA_DOMAIN, TahomaDevice

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=120)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Tahoma covers."""
    controller = hass.data[TAHOMA_DOMAIN]['controller']
    devices = []
    for device in hass.data[TAHOMA_DOMAIN]['devices']['cover']:
        devices.append(TahomaLock(device, controller))
    add_entities(devices, True)


class TahomaLock(TahomaDevice, LockDevice):

    def __init__(self, tahoma_device, controller):
        """Initialize the device."""
        super().__init__(tahoma_device, controller)
        self._state = STATE_LOCKED
        self._available = False

    def update(self):
        """Update method."""
        self.controller.get_states([self.tahoma_device])
        if self.tahoma_device.active_states.get('core:LockedUnlockedState') == 'locked':
            self._state = STATE_LOCKED
        else:
            self._state = STATE_UNLOCKED
        self._available = self.tahoma_device.active_states.get('core:AvailabilityState') == 'available'

    def open(self, **kwargs):
        pass

    def unlock(self, **kwargs):
        pass

    def lock(self, **kwargs):
        pass

    # @property
    # def is_locked(self):

    @property
    def device_state_attributes(self):
        """Return the device state attributes."""
        attr = {}
        super_attr = super().device_state_attributes
        if super_attr is not None:
            attr.update(super_attr)
        for x in self.tahoma_device.active_states:
            print(x)
            for y in self.tahoma_device.active_states[x]:
                print(y,':',self.tahoma_device.active_states[x][y])
        # attr[ATTR_BATTERY_LEVEL] = self.tahoma_device.active_states['core:BatteryState']
        return attr

