# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2021-03-22
### Fixed
- `InstructionWriter.py`: Warning for global volume in "df_variable_sample_n_vol" used to raise even when no volume was given. This is fixed
- `README.md` and `Manual_for_InstructionWriter.pdf`: Describe the need to close the Excel file before running it.

## [1.0.0] - 2021-02-18
### Added
- `InstructionWriter.py`: Input check that every row in the "slot_setup" spreadsheet has an input
- `InstructionWriter.py`: Warning for global volume in "df_variable_sample_n_vol"
- `Manual_for_InstructionWriter.pdf`

## [0.2.0] - 2021-02-18
### Added
- `InstructionWriter.py`: Added-48 well plate format to acceptable layouts of "intuitive"
### Changed
- `README.md`: Further corrected information
- `InstructionWriter.py`: Modified script such that CLI can be run by calling the module directly
- Renamed `SimulateCLI.py` to `SaveLog.py`
### Removed
- `InstructionWriterCLI.py`

## [0.1.2] - 2021-02-08
### Fixed
- `README.md`: Fixed filenames and rearranged information for better logic

## [0.1.1] - 2021-02-05
### Added
- `InstructionWriter.py`: A print line to remind users (me) who might have called the wrong .py script for CLI use.

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
