# verify_resources Module Documentation

## Overview

The `verify_resources` module is responsible for checking the integrity of game resources (audio files, graphics, and maps) and providing an interface to repair corrupted or missing files. It only works when the project is in root folders with source code available. For compiled versions (`.exe`, `.deb`), it cannot recover corrupted or missing files.

## Main Features

- **Resource Verification:** Checks if all necessary files are present and intact.
- **Error Interface:** Displays a graphical interface showing missing or corrupted files.
- **Automatic Repair:** Attempts to repair missing or corrupted files (only in development mode).
- **Report Generation:** Exports a report with problematic files.

## Limitations

- **Compiled Versions:** Repair is not possible in compiled versions (`.exe`, `.deb`). If problems occur with executables, users should report the issue through the official repository.
- **Dependencies:** Requires the project to be in root folders with source code available to work properly.

## Main Classes

### ErrorInterface

Responsible for displaying the graphical error interface and managing user interaction.

**Main Methods:**

- `repair_file(filepath)`: Attempts to repair a missing or corrupted file.
- `repair_all()`: Attempts to repair all problematic files.
- `export_report()`: Exports a report listing problematic files.
- `run()`: Runs the graphical interface.

### ResourceVerifier

Responsible for verifying the integrity of game resources.

**Main Methods:**

- `verify_file(category, subcategory, filename)`: Verifies a specific file.
- `verify_all(loading_callback=None)`: Verifies all game resources.
- `show_error_interface()`: Displays the graphical error interface.

## How to Use

### Resource Verification:


```python
verifier = ResourceVerifier()
verifier.verify_all()
```

### File Repair:

- In development versions, the graphical interface will allow repairing missing or corrupted files.
- In compiled versions, the interface will inform that repair is not possible and guide the user to report the issue.

### Report Export:

The graphical interface allows exporting a report with problematic files to facilitate troubleshooting.

## Common Error Messages

- **Missing File:** Indicates a required file was not found.
- **Corrupted File:** Indicates a file is present but cannot be read correctly.
- **Repair Denied:** In compiled versions, informs that repair is not possible and advises the user to reinstall the game or report the issue.

## Recommendations

- **For Developers:** Keep a backup copy of resources in a backup directory to facilitate automatic repair.
- **For Users:** If you encounter problems with compiled versions, report the issue in the official game repository, including details about the error and the operating system used.

## Example Error Report

```text

=== RPG Eldoria Resource Check Report ===

Date: 2023-10-25 14:30:45

Missing files:
  - graphics/monsters/raccoon/attack/0.png
  - audio/music/main.ogg

Corrupted files:
  - graphics/ui/dialog/DialogInfo_0.png
```

---

This document should be used as a reference to understand and troubleshoot issues related to game resources.
