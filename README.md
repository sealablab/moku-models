# moku-models

Pydantic models for Moku device deployment, discovery, and configuration.

**For detailed usage and development guidelines, see [CLAUDE.md](CLAUDE.md)**

## Overview

This package provides the core data models for working with Moku devices:

- **MokuConfig**: Central deployment abstraction for multi-instrument configurations
- **SlotConfig**: Per-slot instrument configuration (CloudCompile, Oscilloscope, etc.)
- **MokuConnection**: MCC signal routing between slots and physical ports
- **MokuDeviceInfo**: Device discovery and caching models
- **Platform Models**: Moku:Go, Moku:Lab, Moku:Pro, Moku:Delta specifications

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
from moku_models import MokuConfig, SlotConfig, MokuConnection
from moku_models import MOKU_GO_PLATFORM, MOKU_LAB_PLATFORM, MOKU_PRO_PLATFORM, MOKU_DELTA_PLATFORM

# Create a deployment configuration for Moku:Go
config = MokuConfig(
    platform=MOKU_GO_PLATFORM,  # 2 slots, 125 MHz
    slots={
        1: SlotConfig(
            instrument='CloudCompile',
            bitstream='path/to/bitstream.tar',
            control_registers={0: 0xE0000000}
        ),
        2: SlotConfig(
            instrument='Oscilloscope',
            settings={'sample_rate': 125e6}
        )
    },
    routing=[
        MokuConnection(source='IN1', destination='Slot1InA'),
        MokuConnection(source='Slot1OutA', destination='OUT1'),
        MokuConnection(source='Slot1OutA', destination='Slot2InA')
    ]
)

# For Moku:Pro (4 slots, 1.25 GHz)
pro_config = MokuConfig(
    platform=MOKU_PRO_PLATFORM,
    slots={
        1: SlotConfig(instrument='WaveformGenerator'),
        2: SlotConfig(instrument='CloudCompile', bitstream='custom.tar'),
        3: SlotConfig(instrument='Oscilloscope'),
        4: SlotConfig(instrument='SpectrumAnalyzer')
    },
    routing=[
        MokuConnection(source='Slot1OutA', destination='Slot2InA'),
        MokuConnection(source='Slot2OutA', destination='OUT1')
    ]
)

# For Moku:Delta (3 slots, 5 GHz, 8 I/O channels)
delta_config = MokuConfig(
    platform=MOKU_DELTA_PLATFORM,
    slots={
        1: SlotConfig(instrument='CloudCompile', bitstream='emfi.tar'),
        2: SlotConfig(instrument='Oscilloscope', settings={'sample_rate': 5e9}),
        3: SlotConfig(instrument='WaveformGenerator')
    },
    routing=[
        MokuConnection(source='IN1', destination='Slot1InA'),
        MokuConnection(source='Slot1OutA', destination='OUT1'),
        MokuConnection(source='Slot3OutA', destination='IN8')  # 8 channels available
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
- Which platform (Go/Lab/Pro/Delta)
- Instruments in each slot (2-4 slots depending on platform)
- MCC signal routing
- Metadata (version, deployment info)

See [docs/MOKU_PLATFORM_SPECIFICATIONS.md](docs/MOKU_PLATFORM_SPECIFICATIONS.md) for detailed hardware specs.

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

| Platform | Slots | Analog I/O | Clock | DIO | Constant |
|----------|-------|------------|-------|-----|----------|
| Moku:Go | 2 | 2 IN / 2 OUT | 125 MHz | 16 pins | `MOKU_GO_PLATFORM` |
| Moku:Lab | 2 | 2 IN / 2 OUT | 500 MHz | None | `MOKU_LAB_PLATFORM` |
| Moku:Pro | 4 | 4 IN / 4 OUT | 1.25 GHz | None | `MOKU_PRO_PLATFORM` |
| Moku:Delta | 3 | 8 IN / 8 OUT | 5 GHz | 32 pins | `MOKU_DELTA_PLATFORM` |

**Notes**:
- Lab/Pro have no DIO headers (only Go and Delta)
- Delta has 2×16-pin headers (32 total)
- Delta uses 3-slot mode (better performance than 8-slot mode)
- Official datasheets available in `datasheets/` directory

For complete platform specifications and datasheet references, see [docs/MOKU_PLATFORM_SPECIFICATIONS.md](docs/MOKU_PLATFORM_SPECIFICATIONS.md).

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

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Development guidelines and AI assistant context
- **[docs/MOKU_PLATFORM_SPECIFICATIONS.md](docs/MOKU_PLATFORM_SPECIFICATIONS.md)** - Detailed hardware specifications from official datasheets
- **[datasheets/](datasheets/)** - Official Liquid Instruments datasheets (Moku:Go, Lab, Pro, Delta)

## License

MIT License - see LICENSE file for details.

## 🤖 AI Agent Integration

This repository is structured for optimal AI agent assistance:

### Documentation for Agents

- **llms.txt** - Quick reference (Tier 1): Platform catalog (4 platforms), routing patterns, deployment API
- **CLAUDE.md** - Deep context (Tier 2): Platform specifications from datasheets, routing validation, integration patterns
- **docs/routing_patterns.md** - MCC routing patterns and best practices
- **docs/MOKU_PLATFORM_SPECIFICATIONS.md** - Detailed hardware specs with datasheet references

### Loading Strategy

**Progressive disclosure pattern:**
1. Start with `llms.txt` (~500 tokens) for platform specs and quick queries
2. Load `CLAUDE.md` (~4k tokens) for detailed integration patterns
3. Load routing_patterns.md when working with signal routing
4. Load source files when debugging platform models

### Integration with Sibling Libraries

- **basic-app-datatypes** - Voltage type validation against platform output ranges
- **riscure-models** - Platform-to-probe connection safety validation

---

**Last Updated:** 2025-11-04 10:35 MST
