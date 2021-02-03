# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Unreleased
- Further checks of Excel inputs in `InstructionWriter.py`

## [0.1.0] - 2021-02-03
### Added
- A basic `InstructionWriter.py` with most input checks for import
- An IW interface for use in command lines, `InstructionWriterCLI.py`
- A simulator for use in command lines, `SimulateCLI.py`
- All custom labware definitions
- A README.md completed with images from `./img`
- Example Excel files `instructions_io/example_*.xlsx` illustrating the different layouts available for use with the InsructionWriter
- Corresponding text files containing instructions written from the Excel files
- 6 OT-2 protocol files that covered most if not all variations of pipette actions for most molecular cloning operations
- Simulated log files from the 6 example OT-2 protocols
- MIT license file