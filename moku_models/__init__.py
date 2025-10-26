"""
Moku Platform Models

Physical hardware models and routing abstractions for Moku devices.
Aligns with the 1st-party moku library conventions.

Core Abstraction:
    MokuConfig - THE central deployment model for this project
"""

from moku_models.platforms.moku_go import MokuGoPlatform, MOKU_GO_PLATFORM
from moku_models.routing import MokuConnection, MokuConnectionList
from moku_models.platform_config import MokuConfig, SlotConfig, MokuPlatformConfig
from moku_models.discovery import MokuDeviceInfo, MokuDeviceCache

__all__ = [
    # Core abstraction (use this!)
    'MokuConfig',
    'SlotConfig',

    # Platform specifications
    'MokuGoPlatform',
    'MOKU_GO_PLATFORM',

    # Routing
    'MokuConnection',
    'MokuConnectionList',

    # Device discovery
    'MokuDeviceInfo',
    'MokuDeviceCache',

    # Backward compatibility (deprecated)
    'MokuPlatformConfig',
]
