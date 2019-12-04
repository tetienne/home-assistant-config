"""
Support for Somfy Smart Thermostat.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/climate.somfy/
"""
from typing import Optional, List

from ..pymfy.api.devices.category import Category
from ..pymfy.api.devices.thermostat import Thermostat

from homeassistant.components.climate import (
    ClimateDevice,
)
from homeassistant.const import (
    TEMP_CELSIUS,

)
from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    HVAC_MODE_AUTO,
    PRESET_AWAY,
    PRESET_ECO,
    PRESET_COMFORT,
    PRESET_NONE,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_OFF,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_PRESET_MODE,
)

from homeassistant.components.somfy import DOMAIN, SomfyEntity, DEVICES, API


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Somfy climate platform."""

    def get_thermostats():
        """Retrieve thermostats."""
        categories = {
            Category.THERMOSTAT.value,
        }

        devices = hass.data[DOMAIN][DEVICES]

        return [
            SomfyClimate(climate, hass.data[DOMAIN][API])
            for climate in devices
            if categories & set(climate.categories)
        ]

    async_add_entities(await hass.async_add_executor_job(get_thermostats), True)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Old way of setting up platform.

    Can only be called when a user accidentally mentions the platform in their
    config. But even in that case it would have been ignored.
    """
    pass

class SomfyClimate(SomfyEntity, ClimateDevice):
    """Representation of a Somfy smart thermostat"""

    def __init__(self, device, api):
        """Initialize the Somfy device."""
        super().__init__(device, api)
        self.climate = Thermostat(self.device, self.api)

    async def async_update(self):
        """Update the device with the latest data."""
        await super().async_update()
        self.climate = Thermostat(self.device, self.api)

    @property
    def temperature_unit(self) -> str:
        return TEMP_CELSIUS


    @property
    def hvac_mode(self) -> str:
        """Return current operation."""
        return self.climate.get_hvac_state()

    @property
    def hvac_modes(self) -> List[str]:
        return [HVAC_MODE_HEAT, HVAC_MODE_OFF, HVAC_MODE_AUTO]

    @property
    def target_temperature_high(self) -> Optional[float]:
        pass

    @property
    def target_temperature_low(self) -> Optional[float]:
        pass

    @property
    def preset_mode(self) -> Optional[str]:
        pass

    @property
    def preset_modes(self) -> Optional[List[str]]:
        pass

    @property
    def is_aux_heat(self) -> Optional[bool]:
        pass

    @property
    def fan_mode(self) -> Optional[str]:
        pass

    @property
    def fan_modes(self) -> Optional[List[str]]:
        pass

    @property
    def swing_mode(self) -> Optional[str]:
        pass

    @property
    def swing_modes(self) -> Optional[List[str]]:
        pass

    def set_temperature(self, **kwargs) -> None:
        pass

    def set_humidity(self, humidity: int) -> None:
        pass

    def set_fan_mode(self, fan_mode: str) -> None:
        pass

    def set_hvac_mode(self, hvac_mode: str) -> None:
        pass

    def set_swing_mode(self, swing_mode: str) -> None:
        pass

    def set_preset_mode(self, preset_mode: str) -> None:
        pass

    def turn_aux_heat_on(self) -> None:
        pass

    def turn_aux_heat_off(self) -> None:
        pass

    @property
    def supported_features(self) -> int:
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

# class SomfyCover(SomfyEntity, CoverDevice):
#     """Representation of a Somfy cover device."""
#
#     def __init__(self, device, api):
#         """Initialize the Somfy device."""
#         super().__init__(device, api)
#         self.cover = Blind(self.device, self.api)
#
#     async def async_update(self):
#         """Update the device with the latest data."""
#         await super().async_update()
#         self.cover = Blind(self.device, self.api)
#
#     def close_cover(self, **kwargs):
#         """Close the cover."""
#         self.cover.close()
#
#     def open_cover(self, **kwargs):
#         """Open the cover."""
#         self.cover.open()
#
#     def stop_cover(self, **kwargs):
#         """Stop the cover."""
#         self.cover.stop()
#
#     def set_cover_position(self, **kwargs):
#         """Move the cover shutter to a specific position."""
#         self.cover.set_position(100 - kwargs[ATTR_POSITION])
#
#     @property
#     def current_cover_position(self):
#         """Return the current position of cover shutter."""
#         position = None
#         if self.has_capability("position"):
#             position = 100 - self.cover.get_position()
#         return position
#
#     @property
#     def is_closed(self):
#         """Return if the cover is closed."""
#         is_closed = None
#         if self.has_capability("position"):
#             is_closed = self.cover.is_closed()
#         return is_closed
#
#     @property
#     def current_cover_tilt_position(self):
#         """Return current position of cover tilt.
#
#         None is unknown, 0 is closed, 100 is fully open.
#         """
#         orientation = None
#         if self.has_capability("rotation"):
#             orientation = 100 - self.cover.orientation
#         return orientation
#
#     def set_cover_tilt_position(self, **kwargs):
#         """Move the cover tilt to a specific position."""
#         self.cover.orientation = kwargs[ATTR_TILT_POSITION]
#
#     def open_cover_tilt(self, **kwargs):
#         """Open the cover tilt."""
#         self.cover.orientation = 100
#
#     def close_cover_tilt(self, **kwargs):
#         """Close the cover tilt."""
#         self.cover.orientation = 0
#
#     def stop_cover_tilt(self, **kwargs):
#         """Stop the cover."""
#         self.cover.stop()
