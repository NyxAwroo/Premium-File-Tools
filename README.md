# Premium File Tools

  **✨[Sponsor this project](https://www.paypal.com/paypalme/NyxAwroo)**

![Windows](https://img.shields.io/badge/Windows-10%20%2F%2011-0078D4?style=for-the-badge&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/UI-Tkinter%20%2F%20ttk-2B579A?style=for-the-badge)
![Languages](https://img.shields.io/badge/Languages-English%20%2F%20Français-22A06B?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**Premium File Tools adds the fast file organization workflows Windows Explorer should already have.**

Windows is excellent at browsing files, but surprisingly limited when you need to quickly organize, rename, group, extract, clean, or prepare folders from a large selection. Premium File Tools fills that gap by adding a practical, time-saving context menu directly inside Explorer.

Instead of opening heavy file managers, writing scripts, or dragging files manually for minutes, you right-click, choose an action, preview when needed, and let the tool do the repetitive work safely.

> French documentation: [README.fr.md](README.fr.md)

## Screenshots

Replace the images below with your own screenshots before publishing.

| Main Organizer | Quick Custom Folder |
|---|---|
| ![Main organizer screenshot](https://github.com/NyxAwroo/Premium-File-Tools/blob/5b4806349630f3d094f29209d76ea81bbc005aa9/screenshots/interface%20(2).png) | ![Quick custom folder screenshot](https://github.com/NyxAwroo/Premium-File-Tools/blob/5b4806349630f3d094f29209d76ea81bbc005aa9/screenshots/2.png) |

| Selective Extraction | Windows Context Menu |
|---|---|
| ![Selective extraction screenshot](https://github.com/NyxAwroo/Premium-File-Tools/blob/5b4806349630f3d094f29209d76ea81bbc005aa9/screenshots/3.png) | ![Context menu screenshot](https://github.com/NyxAwroo/Premium-File-Tools/blob/5b4806349630f3d094f29209d76ea81bbc005aa9/screenshots/1.png)) |

## Why This Exists

Windows Explorer has no native one-click workflow for common organization tasks such as:

- grouping selected files into folders by type, size, month, prefix, or extension;
- renaming many files with cleanup rules and consistent casing;
- previewing where files will go before moving them;
- extracting nested folder contents without doing it manually;
- copying folder names as empty templates;
- cleaning junk files and empty folders from messy directories.

Premium File Tools turns those missing Explorer workflows into fast right-click actions.

## Key Benefits

- **Save time on repetitive file sorting**: group dozens or hundreds of files in seconds.
- **Reduce manual mistakes**: preview destinations before applying changes.
- **Keep Explorer as your workspace**: everything is available from the native right-click menu.
- **Handle large selections safely**: the accumulator system prevents duplicate windows and race-condition issues.
- **Avoid accidental overwrites**: all moves use safe conflict handling.
- **Undo the last organization operation** when needed.
- **Work in English or French** with automatic language detection and a language setting.

## Context Menu Actions

### File Selection Menu

| Action | What It Does |
|---|---|
| **Organize (Graphical Interface)** | Opens the full organizer with sorting, renaming, conflict handling, and live preview. |
| **Quick: Custom folder** | Prompts for a folder name and moves the selected files into it. |
| **Quick: 1 File = 1 Folder** | Creates one folder per file, using each file name as the folder name. |
| **Quick: Smart Categories** | Sorts files into categories such as Images, Videos, Music, Documents, Archives, and Programs. |
| **Quick: Group by Extension** | Groups files into folders named after their extensions, such as JPG, PDF, or MP4. |
| **Quick: Group by Month** | Groups files by month, for example `2026-06`. |
| **Quick: Group by Size** | Sorts files into size ranges. |
| **Quick: Alphabetical Range** | Groups files into alphabetical ranges such as A-E, F-J, and K-O. |
| **Quick: Group by Common Prefix** | Groups files that share the same beginning before the first dash, underscore, or space. |

### Folder Selection Menu

| Action | What It Does |
|---|---|
| **Extract to the parent folder** | Opens a selective extraction window for folders you selected. |
| **Quick: Extract one level** | Moves direct children up one level without manually opening each folder. |
| **Copy folders as empty templates** | Saves the selected folder names so you can recreate the same empty structure elsewhere. |
| **Deep Clean folder** | Removes common junk files and empty subfolders. |

### Folder Background Menu

| Action | What It Does |
|---|---|
| **Extract here (Selective)** | Extracts content from subfolders into the current folder with filters. |
| **Quick: Extract one level only** | Flattens direct subfolders into the current location. |
| **Deep Clean** | Cleans the current folder tree. |
| **Paste copied empty folders here** | Recreates previously copied folder names as empty folders. |
| **Undo last organization** | Restores files moved during the last organization operation. |

## Main Features

### Smart Organization

- Custom destination folder.
- One folder per file.
- Smart category sorting.
- Extension grouping.
- Date/month grouping.
- Size grouping.
- Alphabetical ranges.
- Common-prefix grouping.

### Renaming Tools

- Lowercase, uppercase, title case, snake_case, and kebab-case.
- Remove bracketed tags and parenthesized text.
- Remove embedded URLs and domain names.
- Add sequential numbering.
- Add date prefixes or suffixes.

### Extraction And Cleanup

- Selective extraction by category or extension.
- One-level extraction for fast folder flattening.
- Deep Clean for junk files and empty folders.
- Copy/paste empty folder structures.

### Safety

- Safe move helper for every file operation.
- Conflict modes: rename, overwrite, or skip.
- Undo log for the last organization operation.
- Multi-process accumulator for large Explorer selections.

## Installation

Requirements:

- Windows 10 or Windows 11.
- Python 3 installed.

Recommended installation:

1. Download or clone this repository.
2. Double-click `Install.bat`.
3. Accept the Windows administrator/UAC prompt.
4. Right-click files or folders in Explorer and open **Premium File Tools**.

Manual installation is also possible by double-clicking `Outils_Fichiers.py`.

## Language

Premium File Tools supports English and French.

- On French Windows systems, French is selected automatically.
- On other systems, English is selected automatically.
- You can change the language in the app settings.

To update the Windows context menu language after changing the setting:

1. Open the full organizer.
2. Go to **Settings**.
3. Select **English** or **Français**.
4. Close the app.
5. Run `Install.bat` again.

## Project Structure

```text
Outils_Fichiers.py   Main single-file application
Install.bat         Easy installer with UAC elevation
README.md           English documentation
README.fr.md        French documentation
.gitignore          Git ignore rules
```

## Technical Notes

- Single-file Python application.
- UI built with `tkinter` and `ttk`.
- Windows context menu integration via `winreg`.
- Settings stored in `%APPDATA%\OutilsFichiersPremium\config.json`.
- Undo log stored in `%APPDATA%\OutilsFichiersPremium\undo_log.json`.
- Temporary accumulator files stored in `%TEMP%\OF_Premium`.

## Disclaimer

This tool modifies Windows context menu registry entries during installation. Review the code before use if you plan to deploy it broadly.

---
### 💛 Support the project
Premium File Tools is a free, you can support its development with a donation.

**Donation link:** [PayPal](https://www.paypal.com/paypalme/NyxAwroo) 
// Donations help fund development time, testing, documentation and future improvements. Huge thanks to anyone who contributes 🙏

---

## Credits

Made by NyxAwroo

