# moku-models

Pydantic models for Moku device deployment, discovery, and configuration.

## Overview

This package provides the core data models for working with Moku devices:

- **MokuConfig**: Central deployment abstraction for multi-instrument configurations
- **SlotConfig**: Per-slot instrument configuration (CloudCompile, Oscilloscope, etc.)
- **MokuConnection**: MCC signal routing between slots and physical ports
- **MokuDeviceInfo**: Device discovery and caching models
- **Platform Models**: Moku:Go, Moku:Lab, Moku:Pro specifications

## Installation

```bash
# From PyPI (when published)
pip install moku-models

# Development installation (editable)
pip install -e .

# With uv
uv pip install -e .
```

## Usage

```python
from moku_models import MokuConfig, SlotConfig, MokuConnection, MOKU_GO_PLATFORM

# Create a deployment configuration
config = MokuConfig(
    platform=MOKU_GO_PLATFORM,
    slots={
        1: SlotConfig(
            instrument='CloudCompile',
            bitstream='path/to/bitstream.tar',
            control_registers={0: 0xE0000000}
        ),
        2: SlotConfig(
            instrument='Oscilloscope',
            settings={'sample_rate': 1e6}
        )
    },
    routing=[
        MokuConnection(source='Input1', destination='Slot1InA'),
        MokuConnection(source='Slot1OutA', destination='Output1'),
        MokuConnection(source='Slot2OutA', destination='Output2')
    ]
)

# Validate and export
errors = config.validate_routing()
if errors:
    print(f"Validation errors: {errors}")
else:
    config_dict = config.to_dict()
```

## Models

### MokuConfig

The central deployment abstraction. Specifies:
- Which platform (Go/Lab/Pro)
- Instruments in each slot (1-4 for Go)
- MCC signal routing
- Metadata (version, deployment info)

### SlotConfig

Per-slot configuration:
- `instrument`: Type name ('CloudCompile', 'Oscilloscope', etc.)
- `bitstream`: Path to .tar bitstream (CloudCompile only)
- `control_registers`: CR0-CR31 initial values (CloudCompile only)
- `settings`: Instrument-specific settings dict

### MokuConnection

Signal routing between:
- Physical ports: `Input1`, `Input2`, `Output1`, `Output2`
- Slot virtual ports: `Slot1InA`, `Slot2OutB`, etc.

### Platform Models

- `MOKU_GO_PLATFORM`: 4 slots, 2 analog in/out, 125 MHz sampling
- Additional platforms in `moku_models.platforms`

## Design Philosophy

**Single Source of Truth**: MokuConfig works for BOTH simulation (CocotB behavioral models) AND hardware deployment (real Moku devices).

**Type Safety**: Pydantic validation ensures configs are correct before deployment.

**Human-Friendly**: Name-based device discovery, slot-based organization.

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black moku_models/
ruff check moku_models/
```

## License

MIT License - see LICENSE file for details.
