import sys
import os
import re
import time
import json
import shutil
import ctypes
import winreg
import tempfile
import subprocess
import locale
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ==============================================================================
# CONFIGURATION ET CONSTANTES
# ==============================================================================
APP_DIR = os.path.join(os.environ.get('APPDATA', ''), 'OutilsFichiersPremium')
CONFIG_FILE = os.path.join(APP_DIR, 'config.json')
UNDO_FILE = os.path.join(APP_DIR, 'undo_log.json')
EMPTY_DIR_CLIPBOARD_FILE = os.path.join(APP_DIR, 'empty_dirs_clipboard.json')

os.makedirs(APP_DIR, exist_ok=True)

PYTHONW_EXE = sys.executable.replace("python.exe", "pythonw.exe")
SCRIPT_PATH = os.path.abspath(__file__)

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg", ".ico"],
    "Vidéos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
    "Musiques": [".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".wma"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv", ".rtf", ".md"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
    "Programmes": [".exe", ".msi", ".bat", ".cmd", ".ps1", ".py", ".js", ".html"]
}

I18N = {
    "fr": {
        "app_name": "Outils Fichiers Premium",
        "app_tagline": "Organisation et renommage intelligent",
        "install_ok_title": "Installation",
        "install_ok_msg": "L'outil a été mis à jour avec le moteur d'extraction réparé ! Les dossiers sont désormais parfaitement préservés et déplacés.",
        "menu_gui": "Organiser (Interface Graphique)...",
        "menu_custom": "Rapide : Dossier personnalisé...",
        "menu_1to1": "Rapide : 1 Fichier = 1 Dossier",
        "menu_smart": "Rapide : Catégories Intelligentes",
        "menu_ext": "Rapide : Grouper par Extension",
        "menu_date_ym": "Rapide : Grouper par Mois (ex: 2024-04)",
        "menu_size": "Rapide : Grouper par Taille",
        "menu_alpha": "Rapide : Tranche Alphabétique (A-E...)",
        "menu_prefix": "Rapide : Grouper par Préfixe Commun",
        "menu_extract": "Extraire à la racine du dossier...",
        "menu_extract_bg": "Extraire vers la racine (Sélectif)...",
        "menu_extract_1_level": "Rapide : Extraire 1 niveau",
        "menu_extract_1_level_bg": "Rapide : Extraire 1 niveau uniquement",
        "menu_copy_empty": "Copier pour coller vide ailleurs",
        "menu_paste_empty": "Coller les dossiers vides copiés ici",
        "menu_clean": "Deep Clean du dossier",
        "menu_clean_bg": "Deep Clean (Dossiers vides & poubelles)",
        "menu_undo": "Annuler le dernier rangement",
        "undo_title": "Annulation réussie",
        "undo_msg": "{count} fichier(s) ont été restaurés à leur emplacement d'origine.",
        "copy_empty_title": "Copie dossiers vides",
        "copy_empty_none": "Aucun dossier valide à copier.",
        "copy_empty_done": "{count} nom(s) de dossier mémorisé(s).\n\nUtilisez ensuite le clic droit dans un dossier puis 'Coller les dossiers vides copiés ici'.",
        "paste_empty_title": "Collage dossiers vides",
        "paste_empty_none": "Aucun dossier vide n'a été copié auparavant.",
        "paste_empty_no_target": "Aucun dossier de destination valide.",
        "paste_empty_done": "Opération réussie !\n\n{count} dossier(s) vide(s) créé(s).",
        "silent_title": "Rangement Rapide",
        "silent_done": "Opération silencieuse réussie !\n\n{count} fichier(s) organisé(s).\n\n(Vos paramètres de renommage ont été appliqués automatiquement).",
        "quick_extract_title": "Extraction Rapide",
        "quick_extract_done": "Opération réussie !\n\n{items} élément(s) extrait(s).\n{dirs} dossier(s) vidé(s) et supprimé(s).",
        "clean_title": "Deep Clean Terminé",
        "clean_done": "Nettoyage réussi sur {folders} dossier(s) !\n\n{junk} fichier(s) poubelle supprimé(s).\n{dirs} dossier(s) vide(s) supprimé(s).",
        "mini_title": "Dossier personnalisé",
        "mini_label": "Regrouper {count} élément(s) dans :",
        "format_label": "Formatage :",
        "case_none": "Inchangé",
        "case_lower": "minuscules",
        "case_upper": "MAJUSCULES",
        "case_title": "Titre (Maj)",
        "cancel": "Annuler",
        "extract_title": "Extraction Sélective",
        "extract_where_bg": "Quels fichiers extraire à cet emplacement ?",
        "extract_where": "Quels fichiers extraire des {count} dossier(s) ?",
        "extract_all": "Tout extraire aveuglément (Classique)",
        "extract_category": "Uniquement la catégorie :",
        "extract_extension": "Uniquement l'extension :",
        "extract_depth": "Profondeur d'extraction :",
        "extract_unlimited": "Illimitée (Explorer tous les sous-dossiers et plus)",
        "extract_one_level": "1 Niveau uniquement (Ignorer les dossiers trop profonds)",
        "extract_deep_clean": "Appliquer le 'Deep Clean' sur les dossiers restants",
        "extract_deep_clean_help": "(Supprime Thumbs.db, les fichiers textes 0 octet, puis les dossiers vides)",
        "extract_button": "EXTRAIRE",
        "extract_done_title": "Extraction terminée",
        "extract_done": "Opération réussie !\n\n{items} élément(s) extrait(s).",
        "extract_done_clean": "\n{junk} fichier(s) poubelle supprimé(s).\n{dirs} dossier(s) vide(s) supprimé(s).",
        "status_ready": "{count} fichier(s) prêt(s).",
        "apply": "APPLIQUER",
        "tab_group": " 📁 Trier & Grouper ",
        "basic_grouping": "📌 Classement Basique",
        "group_none": "🚫 Ne pas créer de dossier (Renommer uniquement)",
        "group_custom": "📁 Dossier personnalisé :",
        "group_1to1": "📄 1 Fichier = 1 Dossier (Au nom du fichier)",
        "smart_grouping": "🧠 Classement Intelligent",
        "group_smart": "📚 Catégorie (Images, Vidéos, Musiques, Documents...)",
        "group_ext": "🏷️ Par Extension Exacte (.jpg, .pdf, .mp4...)",
        "group_prefix": "🔗 Préfixe Commun (Avant le 1er tiret/espace)",
        "metadata_grouping": "📊 Classement par Métadonnées",
        "group_date": "📅 Mois de création (ex: 2024-04)",
        "group_date_tree": "🌳 Chronologie Imbriquée (Année \\ Mois)",
        "group_size": "⚖️ Taille (Gros, Moyens, Petits)",
        "group_alpha": "🔤 Alphabétique (A-E, F-J...)",
        "folder_case_title": "✨ Formatage du nom du DOSSIER créé",
        "tab_rename": " ✏️ Renommage ",
        "file_case_title": "🔠 Formatage du nom de FICHIER",
        "case_title_words": "Titre (Majuscule Aux Mots)",
        "deep_clean_title": "🧹 Nettoyage Profond",
        "anti_tags": "Anti-Tags : Supprimer le texte entre [crochets] et (parenthèses)",
        "anti_urls": "Anti-URLs : Supprimer les noms de sites web incrustés",
        "smart_additions": "➕ Ajouts Intelligents",
        "seq_num": "Ajouter une numérotation séquentielle (_01, _02...)",
        "date_stamp": "Horodatage :",
        "date_none": "Aucun",
        "date_prefix": "Préfixe [Date_]",
        "date_suffix": "Suffixe [_Date]",
        "tab_settings": " ⚙️ Paramètres ",
        "conflict_title": "⚠️ Gestion des Conflits (Si le fichier existe déjà)",
        "conflict_rename": "Renommer intelligemment (Ajouter un numéro, ex: Fichier (1).txt)",
        "conflict_overwrite": "Écraser l'ancien fichier (Attention !)",
        "conflict_skip": "Ignorer et ne pas déplacer",
        "language_title": "🌐 Langue / Language",
        "language_note": "Relancez l'installation pour appliquer la langue au menu contextuel Windows.",
        "preview_title": "👁️ Aperçu en Temps Réel",
        "preview_old": "Nom d'origine",
        "preview_new": "Futur Rangement / Nouveau Nom",
        "preview_more": "et {count} autres fichiers...",
        "done_title": "Terminé",
        "done_msg": "Opération réussie !\n\n{count} fichier(s) ont été organisés.\n\n(Astuce : Vous pouvez annuler via le clic droit 'Annuler le dernier rangement').",
        "default_folder": "Nouveau_Dossier",
        "default_file": "Fichier",
        "no_extension": "Sans_Extension",
        "unknown_date": "Date_Inconnue",
        "unknown_size": "Taille_Inconnue",
        "size_large": "1_Gros (+500Mo)",
        "size_medium": "2_Moyens (50-500Mo)",
        "size_small": "3_Petits (-50Mo)",
        "alpha_other": "0-9 & Autres",
        "misc": "Divers",
        "other": "Autres"
    },
    "en": {
        "app_name": "Premium File Tools",
        "app_tagline": "Smart file organization and renaming",
        "install_ok_title": "Installation",
        "install_ok_msg": "Premium File Tools has been installed or updated successfully.",
        "menu_gui": "Organize (Graphical Interface)...",
        "menu_custom": "Quick: Custom folder...",
        "menu_1to1": "Quick: 1 File = 1 Folder",
        "menu_smart": "Quick: Smart Categories",
        "menu_ext": "Quick: Group by Extension",
        "menu_date_ym": "Quick: Group by Month (e.g. 2024-04)",
        "menu_size": "Quick: Group by Size",
        "menu_alpha": "Quick: Alphabetical Range (A-E...)",
        "menu_prefix": "Quick: Group by Common Prefix",
        "menu_extract": "Extract to the parent folder...",
        "menu_extract_bg": "Extract here (Selective)...",
        "menu_extract_1_level": "Quick: Extract one level",
        "menu_extract_1_level_bg": "Quick: Extract one level only",
        "menu_copy_empty": "Copy folders as empty templates",
        "menu_paste_empty": "Paste copied empty folders here",
        "menu_clean": "Deep Clean folder",
        "menu_clean_bg": "Deep Clean (empty folders & junk files)",
        "menu_undo": "Undo last organization",
        "undo_title": "Undo complete",
        "undo_msg": "{count} file(s) have been restored to their original location.",
        "copy_empty_title": "Copy empty folders",
        "copy_empty_none": "No valid folder to copy.",
        "copy_empty_done": "{count} folder name(s) saved.\n\nThen right-click inside a folder and choose 'Paste copied empty folders here'.",
        "paste_empty_title": "Paste empty folders",
        "paste_empty_none": "No empty folder template has been copied yet.",
        "paste_empty_no_target": "No valid destination folder.",
        "paste_empty_done": "Operation successful!\n\n{count} empty folder(s) created.",
        "silent_title": "Quick Organization",
        "silent_done": "Silent operation completed successfully!\n\n{count} file(s) organized.\n\n(Your renaming settings were applied automatically).",
        "quick_extract_title": "Quick Extraction",
        "quick_extract_done": "Operation successful!\n\n{items} item(s) extracted.\n{dirs} emptied folder(s) removed.",
        "clean_title": "Deep Clean Complete",
        "clean_done": "Cleanup completed on {folders} folder(s)!\n\n{junk} junk file(s) removed.\n{dirs} empty folder(s) removed.",
        "mini_title": "Custom folder",
        "mini_label": "Group {count} item(s) into:",
        "format_label": "Formatting:",
        "case_none": "Unchanged",
        "case_lower": "lowercase",
        "case_upper": "UPPERCASE",
        "case_title": "Title Case",
        "cancel": "Cancel",
        "extract_title": "Selective Extraction",
        "extract_where_bg": "Which files should be extracted here?",
        "extract_where": "Which files should be extracted from {count} folder(s)?",
        "extract_all": "Extract everything blindly (Classic)",
        "extract_category": "Only this category:",
        "extract_extension": "Only this extension:",
        "extract_depth": "Extraction depth:",
        "extract_unlimited": "Unlimited (scan all subfolders and deeper)",
        "extract_one_level": "One level only (ignore deeper folders)",
        "extract_deep_clean": "Apply 'Deep Clean' to remaining folders",
        "extract_deep_clean_help": "(Removes Thumbs.db, zero-byte text files, then empty folders)",
        "extract_button": "EXTRACT",
        "extract_done_title": "Extraction complete",
        "extract_done": "Operation successful!\n\n{items} item(s) extracted.",
        "extract_done_clean": "\n{junk} junk file(s) removed.\n{dirs} empty folder(s) removed.",
        "status_ready": "{count} file(s) ready.",
        "apply": "APPLY",
        "tab_group": " 📁 Sort & Group ",
        "basic_grouping": "📌 Basic Grouping",
        "group_none": "🚫 Do not create folders (rename only)",
        "group_custom": "📁 Custom folder:",
        "group_1to1": "📄 1 File = 1 Folder (named after the file)",
        "smart_grouping": "🧠 Smart Grouping",
        "group_smart": "📚 Category (Images, Videos, Music, Documents...)",
        "group_ext": "🏷️ Exact Extension (.jpg, .pdf, .mp4...)",
        "group_prefix": "🔗 Common Prefix (before first dash/space)",
        "metadata_grouping": "📊 Metadata Grouping",
        "group_date": "📅 Creation month (e.g. 2024-04)",
        "group_date_tree": "🌳 Nested Timeline (Year \\ Month)",
        "group_size": "⚖️ Size (Large, Medium, Small)",
        "group_alpha": "🔤 Alphabetical (A-E, F-J...)",
        "folder_case_title": "✨ Created FOLDER name formatting",
        "tab_rename": " ✏️ Renaming ",
        "file_case_title": "🔠 FILE name formatting",
        "case_title_words": "Title Case",
        "deep_clean_title": "🧹 Deep Cleaning",
        "anti_tags": "Anti-Tags: remove text inside [brackets] and (parentheses)",
        "anti_urls": "Anti-URLs: remove embedded website/domain names",
        "smart_additions": "➕ Smart Additions",
        "seq_num": "Add sequential numbering (_01, _02...)",
        "date_stamp": "Date stamp:",
        "date_none": "None",
        "date_prefix": "Prefix [Date_]",
        "date_suffix": "Suffix [_Date]",
        "tab_settings": " ⚙️ Settings ",
        "conflict_title": "⚠️ Conflict handling (if the file already exists)",
        "conflict_rename": "Rename intelligently (add a number, e.g. File (1).txt)",
        "conflict_overwrite": "Overwrite the existing file (careful!)",
        "conflict_skip": "Skip and do not move",
        "language_title": "🌐 Language / Langue",
        "language_note": "Run the installer again to apply this language to the Windows context menu.",
        "preview_title": "👁️ Live Preview",
        "preview_old": "Original name",
        "preview_new": "Future Location / New Name",
        "preview_more": "and {count} more files...",
        "done_title": "Done",
        "done_msg": "Operation successful!\n\n{count} file(s) organized.\n\n(Tip: you can undo from the right-click menu with 'Undo last organization').",
        "default_folder": "New_Folder",
        "default_file": "File",
        "no_extension": "No_Extension",
        "unknown_date": "Unknown_Date",
        "unknown_size": "Unknown_Size",
        "size_large": "1_Large (+500MB)",
        "size_medium": "2_Medium (50-500MB)",
        "size_small": "3_Small (-50MB)",
        "alpha_other": "0-9 & Others",
        "misc": "Misc",
        "other": "Others"
    }
}

CATEGORY_LABELS = {
    "fr": {
        "Images": "Images", "Vidéos": "Vidéos", "Musiques": "Musiques",
        "Documents": "Documents", "Archives": "Archives", "Programmes": "Programmes"
    },
    "en": {
        "Images": "Images", "Vidéos": "Videos", "Musiques": "Music",
        "Documents": "Documents", "Archives": "Archives", "Programmes": "Programs"
    }
}

def get_language(config=None):
    if config and config.get("language") in ("fr", "en"):
        return config["language"]
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            if saved.get("language") in ("fr", "en"):
                return saved["language"]
    except Exception:
        pass
    loc = (locale.getdefaultlocale()[0] or "").lower()
    return "fr" if loc.startswith("fr") else "en"

def tr(key, lang=None):
    lang = lang or get_language()
    return I18N.get(lang, I18N["fr"]).get(key, I18N["fr"].get(key, key))

def trf(key, lang=None, **kwargs):
    return tr(key, lang).format(**kwargs)

def category_label(key, lang=None):
    lang = lang or get_language()
    return CATEGORY_LABELS.get(lang, CATEGORY_LABELS["fr"]).get(key, key)

def category_values(lang=None):
    return [category_label(key, lang) for key in CATEGORIES.keys()]

def category_key_from_label(label, lang=None):
    lang = lang or get_language()
    labels = CATEGORY_LABELS.get(lang, CATEGORY_LABELS["fr"])
    for key, translated in labels.items():
        if label == translated or label == key:
            return key
    return label

# Classe Win32 unique pour les fenêtres Maître. Définie au niveau module pour
# être accessible à la fois par launch_accumulator (qui cherche) et par les
# classes GUI (qui la déclarent). Invisible pour l'utilisateur.
MASTER_WINDOW_CLASS = "OutilsFichiersPremium_MasterWnd_v1"

# ==============================================================================
# FONCTIONS UTILITAIRES (DÉPLACEMENT SÉCURISÉ & FORMATAGE)
# ==============================================================================
def safe_move(src, dst, conflict_mode="rename"):
    if not os.path.exists(dst):
        shutil.move(src, dst)
        return dst
    if conflict_mode == "skip":
        return None
    if conflict_mode == "overwrite":
        shutil.move(src, dst)
        return dst
    
    base, ext = os.path.splitext(dst)
    counter = 1
    new_dst = f"{base} ({counter}){ext}"
    while os.path.exists(new_dst):
        counter += 1
        new_dst = f"{base} ({counter}){ext}"
    shutil.move(src, new_dst)
    return new_dst

def apply_case(text, case_type):
    if case_type == "lower": return text.lower()
    if case_type == "upper": return text.upper()
    if case_type == "title": return text.title()
    if case_type == "snake": return re.sub(r'[-\s]+', '_', text).lower()
    if case_type == "kebab": return re.sub(r'[_ \s]+', '-', text).lower()
    return text

def calculate_new_path(file_path, index, config):
    """Calcule le nouveau chemin en appliquant toutes les règles du config."""
    lang = get_language(config)
    parent_dir = os.path.dirname(file_path)
    old_name = os.path.basename(file_path)
    name_no_ext, ext = os.path.splitext(old_name)

    new_name = name_no_ext

    # 1. Nettoyage
    if config.get("clean_tags"):
        new_name = re.sub(r'\[.*?\]|\(.*?\)', '', new_name).strip()
    if config.get("clean_urls"):
        new_name = re.sub(r'(?i)\b(?:https?://|www\.)\S+\b|\b\w+\.(?:com|net|org|fr|io|me|co)\b', '', new_name).strip()

    # 2. Casse du nom de fichier
    case = config.get("rename_case", "none")
    if case == "lower": new_name = new_name.lower()
    elif case == "upper": new_name = new_name.upper()
    elif case == "title": new_name = new_name.title()
    elif case == "snake": new_name = re.sub(r'[-\s]+', '_', new_name).lower()
    elif case == "kebab": new_name = re.sub(r'[_ \s]+', '-', new_name).lower()

    new_name = new_name.strip(" _-")
    if not new_name: new_name = tr("default_file", lang)

    # 3. Ajouts (Date / Sequence)
    add_date = config.get("add_date", "none")
    if add_date != "none":
        try: date_str = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d")
        except: date_str = datetime.now().strftime("%Y-%m-%d")
        if add_date == "prefix": new_name = f"{date_str}_{new_name}"
        else: new_name = f"{new_name}_{date_str}"

    if config.get("seq_num"):
        new_name = f"{new_name}_{index:02d}"

    new_filename = new_name + ext

    # 4. Groupement
    g_mode = config.get("group_mode", "none")
    target_folder = ""
    folder_name = ""

    if g_mode == "custom":
        folder_name = config.get("custom_folder", tr("default_folder", lang)).strip() or tr("default_folder", lang)
    elif g_mode == "1to1":
        folder_name = name_no_ext
    elif g_mode == "smart":
        cat = tr("other", lang)
        ext_lower = ext.lower()
        for c, exts in CATEGORIES.items():
            if ext_lower in exts:
                cat = category_label(c, lang)
                break
        folder_name = cat
    elif g_mode == "ext":
        folder_name = ext.lstrip('.') if ext else tr("no_extension", lang)
        folder_name = folder_name.upper()
    elif g_mode == "date_ym":
        try: folder_name = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m")
        except: folder_name = tr("unknown_date", lang)
    elif g_mode == "date_tree":
        try: 
            d = datetime.fromtimestamp(os.path.getmtime(file_path))
            folder_name = os.path.join(str(d.year), f"{d.month:02d}_{d.strftime('%B')}")
        except: folder_name = tr("unknown_date", lang)
    elif g_mode == "size":
        try:
            sz = os.path.getsize(file_path)
            if sz > 1024*1024*500: folder_name = tr("size_large", lang)
            elif sz > 1024*1024*50: folder_name = tr("size_medium", lang)
            else: folder_name = tr("size_small", lang)
        except: folder_name = tr("unknown_size", lang)
    elif g_mode == "alpha":
        first_char = name_no_ext[0].upper() if name_no_ext else "#"
        if 'A' <= first_char <= 'E': folder_name = "A-E"
        elif 'F' <= first_char <= 'J': folder_name = "F-J"
        elif 'K' <= first_char <= 'O': folder_name = "K-O"
        elif 'P' <= first_char <= 'T': folder_name = "P-T"
        elif 'U' <= first_char <= 'Z': folder_name = "U-Z"
        else: folder_name = tr("alpha_other", lang)
    elif g_mode == "prefix":
        prefix = re.split(r'[-_\s]', name_no_ext)[0]
        folder_name = prefix if prefix else tr("misc", lang)
        
    if g_mode != "none" and folder_name:
        if g_mode not in ["date_tree", "ext", "size", "alpha"]:
            folder_name = apply_case(folder_name, config.get("folder_case", "none"))
        target_folder = os.path.join(parent_dir, folder_name)
    else:
        target_folder = parent_dir

    return os.path.join(target_folder, new_filename)

# ==============================================================================
# INSTALLATION DU MENU CONTEXTUEL (Registre Windows)
# ==============================================================================
def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{SCRIPT_PATH}"', None, 1)

def install_context_menu():
    if not is_admin():
        run_as_admin()
        sys.exit()
    lang = get_language()

    legacy_keys = [
        r"HKCR\*\shell\OutilsFichiers",
        r"HKCR\Directory\Background\shell\OutilsFichiers",
        r"HKCR\Directory\shell\OutilsFichiers",
        r"HKCR\Folder\shell\OutilsFichiers",
        r"HKCR\Folder\shell\OutilsFichiersCopyEmptyDirs",
        r"HKCU\Software\Classes\Folder\shell\OutilsFichiers",
        r"HKCU\Software\Classes\Folder\shell\OutilsFichiersCopyEmptyDirs",
        r"HKLM\Software\Classes\Folder\shell\OutilsFichiers",
        r"HKLM\Software\Classes\Folder\shell\OutilsFichiersCopyEmptyDirs"
    ]
    for key in legacy_keys:
        subprocess.run(['reg', 'delete', key, '/f'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def create_key(path):
        try: winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, path)
        except: pass
    def set_value(path, name, value, vtype=winreg.REG_SZ):
        try:
            key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, name, 0, vtype, value)
            winreg.CloseKey(key)
        except: pass

    # --- MENU SUR LES FICHIERS (CASCADE AVEC RACCOURCIS) ---
    base_file = r"*\shell\OutilsFichiers"
    create_key(base_file)
    set_value(base_file, "MUIVerb", tr("app_name", lang))
    set_value(base_file, "Icon", "imageres.dll,-103")
    set_value(base_file, "SubCommands", "") 

    create_key(f"{base_file}\\shell\\01_GUI")
    set_value(f"{base_file}\\shell\\01_GUI", "MUIVerb", tr("menu_gui", lang))
    set_value(f"{base_file}\\shell\\01_GUI", "Icon", "imageres.dll,-103")
    create_key(f"{base_file}\\shell\\01_GUI\\command")
    set_value(f"{base_file}\\shell\\01_GUI\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate gui "%1"')

    create_key(f"{base_file}\\shell\\01a_custom")
    set_value(f"{base_file}\\shell\\01a_custom", "MUIVerb", tr("menu_custom", lang))
    set_value(f"{base_file}\\shell\\01a_custom", "Icon", "imageres.dll,-112")
    create_key(f"{base_file}\\shell\\01a_custom\\command")
    set_value(f"{base_file}\\shell\\01a_custom\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate custom_prompt "%1"')

    create_key(f"{base_file}\\shell\\02_1to1")
    set_value(f"{base_file}\\shell\\02_1to1", "MUIVerb", tr("menu_1to1", lang))
    set_value(f"{base_file}\\shell\\02_1to1", "Icon", "shell32.dll,-44")
    set_value(f"{base_file}\\shell\\02_1to1", "CommandFlags", 32, winreg.REG_DWORD)
    create_key(f"{base_file}\\shell\\02_1to1\\command")
    set_value(f"{base_file}\\shell\\02_1to1\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate 1to1 "%1"')

    create_key(f"{base_file}\\shell\\03_smart")
    set_value(f"{base_file}\\shell\\03_smart", "MUIVerb", tr("menu_smart", lang))
    set_value(f"{base_file}\\shell\\03_smart", "Icon", "imageres.dll,-109")
    create_key(f"{base_file}\\shell\\03_smart\\command")
    set_value(f"{base_file}\\shell\\03_smart\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate smart "%1"')

    create_key(f"{base_file}\\shell\\04_ext")
    set_value(f"{base_file}\\shell\\04_ext", "MUIVerb", tr("menu_ext", lang))
    set_value(f"{base_file}\\shell\\04_ext", "Icon", "imageres.dll,-114")
    create_key(f"{base_file}\\shell\\04_ext\\command")
    set_value(f"{base_file}\\shell\\04_ext\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate ext "%1"')

    create_key(f"{base_file}\\shell\\05_date_ym")
    set_value(f"{base_file}\\shell\\05_date_ym", "MUIVerb", tr("menu_date_ym", lang))
    set_value(f"{base_file}\\shell\\05_date_ym", "Icon", "imageres.dll,-112")
    create_key(f"{base_file}\\shell\\05_date_ym\\command")
    set_value(f"{base_file}\\shell\\05_date_ym\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate date_ym "%1"')

    create_key(f"{base_file}\\shell\\06_size")
    set_value(f"{base_file}\\shell\\06_size", "MUIVerb", tr("menu_size", lang))
    set_value(f"{base_file}\\shell\\06_size", "Icon", "imageres.dll,-110")
    create_key(f"{base_file}\\shell\\06_size\\command")
    set_value(f"{base_file}\\shell\\06_size\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate size "%1"')

    create_key(f"{base_file}\\shell\\07_alpha")
    set_value(f"{base_file}\\shell\\07_alpha", "MUIVerb", tr("menu_alpha", lang))
    set_value(f"{base_file}\\shell\\07_alpha", "Icon", "shell32.dll,-137")
    create_key(f"{base_file}\\shell\\07_alpha\\command")
    set_value(f"{base_file}\\shell\\07_alpha\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate alpha "%1"')

    create_key(f"{base_file}\\shell\\08_prefix")
    set_value(f"{base_file}\\shell\\08_prefix", "MUIVerb", tr("menu_prefix", lang))
    set_value(f"{base_file}\\shell\\08_prefix", "Icon", "shell32.dll,-253")
    create_key(f"{base_file}\\shell\\08_prefix\\command")
    set_value(f"{base_file}\\shell\\08_prefix\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate prefix "%1"')

    # --- MENU SUR LES DOSSIERS SÉLECTIONNÉS (Cascade Clic Droit) ---
    base_dir = r"Directory\shell\OutilsFichiers"
    create_key(base_dir)
    set_value(base_dir, "MUIVerb", tr("app_name", lang))
    set_value(base_dir, "Icon", "shell32.dll,-44")
    set_value(base_dir, "MultiSelectModel", "Player")
    set_value(base_dir, "SubCommands", "")

    create_key(f"{base_dir}\\shell\\01_Extract")
    set_value(f"{base_dir}\\shell\\01_Extract", "MUIVerb", tr("menu_extract", lang))
    set_value(f"{base_dir}\\shell\\01_Extract", "Icon", "imageres.dll,-102")
    create_key(f"{base_dir}\\shell\\01_Extract\\command")
    set_value(f"{base_dir}\\shell\\01_Extract\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate extract "%1"')

    create_key(f"{base_dir}\\shell\\01b_Extract1Level")
    set_value(f"{base_dir}\\shell\\01b_Extract1Level", "MUIVerb", tr("menu_extract_1_level", lang))
    set_value(f"{base_dir}\\shell\\01b_Extract1Level", "Icon", "imageres.dll,-102")
    create_key(f"{base_dir}\\shell\\01b_Extract1Level\\command")
    set_value(f"{base_dir}\\shell\\01b_Extract1Level\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate extract_1_level "%1"')

    create_key(f"{base_dir}\\shell\\02_CopyEmptyDirs")
    set_value(f"{base_dir}\\shell\\02_CopyEmptyDirs", "MUIVerb", tr("menu_copy_empty", lang))
    set_value(f"{base_dir}\\shell\\02_CopyEmptyDirs", "Icon", "shell32.dll,-16769")
    set_value(f"{base_dir}\\shell\\02_CopyEmptyDirs", "MultiSelectModel", "Player")
    set_value(f"{base_dir}\\shell\\02_CopyEmptyDirs", "CommandFlags", 32, winreg.REG_DWORD)
    create_key(f"{base_dir}\\shell\\02_CopyEmptyDirs\\command")
    set_value(f"{base_dir}\\shell\\02_CopyEmptyDirs\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate copy_empty_dirs "%1"')

    create_key(f"{base_dir}\\shell\\03_Clean")
    set_value(f"{base_dir}\\shell\\03_Clean", "MUIVerb", tr("menu_clean", lang))
    set_value(f"{base_dir}\\shell\\03_Clean", "Icon", "imageres.dll,-53")
    create_key(f"{base_dir}\\shell\\03_Clean\\command")
    set_value(f"{base_dir}\\shell\\03_Clean\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate clean "%1"')

    # Secours Windows 10/11 : certains clics droits sur dossiers passent par
    # "Folder" plutôt que "Directory". On garde la même cascade complète pour
    # éviter une entrée séparée dans le volet principal.
    base_folder = r"Folder\shell\OutilsFichiers"
    create_key(base_folder)
    set_value(base_folder, "MUIVerb", tr("app_name", lang))
    set_value(base_folder, "Icon", "shell32.dll,-44")
    set_value(base_folder, "MultiSelectModel", "Player")
    set_value(base_folder, "SubCommands", "")

    create_key(f"{base_folder}\\shell\\01_Extract")
    set_value(f"{base_folder}\\shell\\01_Extract", "MUIVerb", tr("menu_extract", lang))
    set_value(f"{base_folder}\\shell\\01_Extract", "Icon", "imageres.dll,-102")
    create_key(f"{base_folder}\\shell\\01_Extract\\command")
    set_value(f"{base_folder}\\shell\\01_Extract\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate extract "%1"')

    create_key(f"{base_folder}\\shell\\01b_Extract1Level")
    set_value(f"{base_folder}\\shell\\01b_Extract1Level", "MUIVerb", tr("menu_extract_1_level", lang))
    set_value(f"{base_folder}\\shell\\01b_Extract1Level", "Icon", "imageres.dll,-102")
    create_key(f"{base_folder}\\shell\\01b_Extract1Level\\command")
    set_value(f"{base_folder}\\shell\\01b_Extract1Level\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate extract_1_level "%1"')

    create_key(f"{base_folder}\\shell\\02_CopyEmptyDirs")
    set_value(f"{base_folder}\\shell\\02_CopyEmptyDirs", "MUIVerb", tr("menu_copy_empty", lang))
    set_value(f"{base_folder}\\shell\\02_CopyEmptyDirs", "Icon", "shell32.dll,-16769")
    set_value(f"{base_folder}\\shell\\02_CopyEmptyDirs", "MultiSelectModel", "Player")
    set_value(f"{base_folder}\\shell\\02_CopyEmptyDirs", "CommandFlags", 32, winreg.REG_DWORD)
    create_key(f"{base_folder}\\shell\\02_CopyEmptyDirs\\command")
    set_value(f"{base_folder}\\shell\\02_CopyEmptyDirs\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate copy_empty_dirs "%1"')

    create_key(f"{base_folder}\\shell\\03_Clean")
    set_value(f"{base_folder}\\shell\\03_Clean", "MUIVerb", tr("menu_clean", lang))
    set_value(f"{base_folder}\\shell\\03_Clean", "Icon", "imageres.dll,-53")
    create_key(f"{base_folder}\\shell\\03_Clean\\command")
    set_value(f"{base_folder}\\shell\\03_Clean\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate clean "%1"')

    # --- MENU EN ARRIÈRE-PLAN DES DOSSIERS (Quand on clique dans le vide) ---
    base_bg = r"Directory\Background\shell\OutilsFichiers"
    create_key(base_bg)
    set_value(base_bg, "MUIVerb", tr("app_name", lang))
    set_value(base_bg, "Icon", "shell32.dll,-44")
    set_value(base_bg, "SubCommands", "")

    create_key(f"{base_bg}\\shell\\01_Extract")
    set_value(f"{base_bg}\\shell\\01_Extract", "MUIVerb", tr("menu_extract_bg", lang))
    set_value(f"{base_bg}\\shell\\01_Extract", "Icon", "imageres.dll,-102")
    create_key(f"{base_bg}\\shell\\01_Extract\\command")
    set_value(f"{base_bg}\\shell\\01_Extract\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate bg_extract "%V"')
    
    create_key(f"{base_bg}\\shell\\01b_Extract1Level")
    set_value(f"{base_bg}\\shell\\01b_Extract1Level", "MUIVerb", tr("menu_extract_1_level_bg", lang))
    set_value(f"{base_bg}\\shell\\01b_Extract1Level", "Icon", "imageres.dll,-102")
    create_key(f"{base_bg}\\shell\\01b_Extract1Level\\command")
    set_value(f"{base_bg}\\shell\\01b_Extract1Level\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate bg_extract_1_level "%V"')

    create_key(f"{base_bg}\\shell\\02_Clean")
    set_value(f"{base_bg}\\shell\\02_Clean", "MUIVerb", tr("menu_clean_bg", lang))
    set_value(f"{base_bg}\\shell\\02_Clean", "Icon", "imageres.dll,-53")
    create_key(f"{base_bg}\\shell\\02_Clean\\command")
    set_value(f"{base_bg}\\shell\\02_Clean\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate clean "%V"')

    create_key(f"{base_bg}\\shell\\03_PasteEmptyDirs")
    set_value(f"{base_bg}\\shell\\03_PasteEmptyDirs", "MUIVerb", tr("menu_paste_empty", lang))
    set_value(f"{base_bg}\\shell\\03_PasteEmptyDirs", "Icon", "shell32.dll,-16763")
    set_value(f"{base_bg}\\shell\\03_PasteEmptyDirs", "CommandFlags", 32, winreg.REG_DWORD)
    create_key(f"{base_bg}\\shell\\03_PasteEmptyDirs\\command")
    set_value(f"{base_bg}\\shell\\03_PasteEmptyDirs\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --accumulate paste_empty_dirs "%V"')

    create_key(f"{base_bg}\\shell\\04_Undo")
    set_value(f"{base_bg}\\shell\\04_Undo", "MUIVerb", tr("menu_undo", lang))
    set_value(f"{base_bg}\\shell\\04_Undo", "Icon", "shell32.dll,-252")
    set_value(f"{base_bg}\\shell\\04_Undo", "CommandFlags", 32, winreg.REG_DWORD)
    create_key(f"{base_bg}\\shell\\04_Undo\\command")
    set_value(f"{base_bg}\\shell\\04_Undo\\command", "", f'"{PYTHONW_EXE}" "{SCRIPT_PATH}" --undo')

    messagebox.showinfo(tr("install_ok_title", lang), tr("install_ok_msg", lang))
    sys.exit()

# ==============================================================================
# ACTIONS D'ARRIÈRE-PLAN (Extraction, Nettoyage, Annulation)
# ==============================================================================
def undo_last_action():
    if not os.path.exists(UNDO_FILE): return
    with open(UNDO_FILE, 'r', encoding='utf-8') as f: log = json.load(f)
    if not log: return

    restored = 0
    for new_path, old_path in log.items():
        if os.path.exists(new_path) and not os.path.exists(old_path):
            os.makedirs(os.path.dirname(old_path), exist_ok=True)
            shutil.move(new_path, old_path)
            restored += 1

    with open(UNDO_FILE, 'w', encoding='utf-8') as f: json.dump({}, f)
    
    root = tk.Tk(); root.withdraw()
    messagebox.showinfo(tr("undo_title"), trf("undo_msg", count=restored))
    root.destroy()

def clean_empty_folders(target_dir, deep_clean=True):
    """Nettoie uniquement l'intérieur du dossier (le dossier cible lui-même est géré ailleurs)"""
    if not os.path.isdir(target_dir): return 0, 0
    deleted_count, junk_count = 0, 0
    junk_files = ['thumbs.db', '.ds_store', 'desktop.ini']

    for root_dir, dirs, files in os.walk(target_dir, topdown=False):
        if deep_clean and root_dir != target_dir:
            for f in files:
                f_lower = f.lower()
                f_path = os.path.join(root_dir, f)
                if f_lower in junk_files or (f_lower.endswith('.txt') and os.path.getsize(f_path) == 0):
                    try: os.remove(f_path); junk_count += 1
                    except: pass
        for dir_name in dirs:
            dir_path = os.path.join(root_dir, dir_name)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    deleted_count += 1
            except: pass
    return deleted_count, junk_count

def get_available_folder_path(path):
    """Retourne un chemin de dossier libre en ajoutant (1), (2), etc. si besoin."""
    if not os.path.exists(path):
        return path

    counter = 1
    new_path = f"{path} ({counter})"
    while os.path.exists(new_path):
        counter += 1
        new_path = f"{path} ({counter})"
    return new_path

def copy_empty_folder_names(folders):
    """Mémorise uniquement les noms des dossiers sélectionnés pour les recoller vides ailleurs."""
    folder_names = []
    for folder in folders:
        if os.path.isdir(folder):
            name = os.path.basename(os.path.normpath(folder))
            if name:
                folder_names.append(name)

    root = tk.Tk(); root.withdraw()
    if not folder_names:
        messagebox.showwarning(tr("copy_empty_title"), tr("copy_empty_none"))
        root.destroy()
        return

    data = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "folder_names": folder_names
    }
    with open(EMPTY_DIR_CLIPBOARD_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    messagebox.showinfo(
        tr("copy_empty_title"),
        trf("copy_empty_done", count=len(folder_names))
    )
    root.destroy()

def paste_empty_folder_names(target_dirs):
    """Crée dans le dossier cible les dossiers mémorisés, sans recopier leur contenu."""
    try:
        with open(EMPTY_DIR_CLIPBOARD_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        folder_names = data.get("folder_names", [])
    except:
        folder_names = []

    root = tk.Tk(); root.withdraw()
    if not folder_names:
        messagebox.showwarning(tr("paste_empty_title"), tr("paste_empty_none"))
        root.destroy()
        return

    targets = [d for d in target_dirs if os.path.isdir(d)]
    if not targets:
        messagebox.showwarning(tr("paste_empty_title"), tr("paste_empty_no_target"))
        root.destroy()
        return

    created = 0
    for target_dir in targets:
        for name in folder_names:
            safe_name = os.path.basename(os.path.normpath(name))
            if not safe_name:
                continue
            folder_path = get_available_folder_path(os.path.join(target_dir, safe_name))
            try:
                os.makedirs(folder_path, exist_ok=False)
                created += 1
            except: pass

    messagebox.showinfo(
        tr("paste_empty_title"),
        trf("paste_empty_done", count=created)
    )
    root.destroy()

def perform_extraction(source_dir, target_dir=None, mode="all", cat=None, ext=None, max_depth=0, deep_clean=True):
    """Fonction d'extraction unifiée. Topdown=True garantit que les dossiers sont déplacés entiers."""
    source_dir = os.path.normpath(source_dir)
    if target_dir is None:
        target_dir = source_dir
    target_dir = os.path.normpath(target_dir)

    extracted_count = 0

    # L'utilisation de topdown=True permet de déplacer des dossiers entiers SANS explorer leur contenu
    for root, dirs, files in os.walk(source_dir, topdown=True):
        if root == target_dir:
            continue

        rel_path = os.path.relpath(root, source_dir)
        depth = 0 if rel_path == '.' else len(rel_path.split(os.sep))

        # Si on dépasse la profondeur demandée, on demande à l'explorateur d'arrêter de creuser ici
        if max_depth > 0 and depth >= max_depth:
            dirs.clear()
            continue

        # 1. Déplacement des fichiers
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            move_it = False

            if mode == "all": move_it = True
            elif mode == "cat" and file_ext in CATEGORIES.get(category_key_from_label(cat), []): move_it = True
            elif mode == "ext" and file_ext == ext: move_it = True

            if move_it:
                src = os.path.join(root, file)
                dst = os.path.join(target_dir, file)
                if src != dst:
                    try:
                        safe_move(src, dst, conflict_mode="rename")
                        extracted_count += 1
                    except: pass
                    
        # 2. Déplacement des DOSSIERS entiers (Seulement pour mode 'all' avant de franchir la profondeur max)
        if mode == "all" and max_depth > 0 and depth == max_depth - 1:
            # On boucle sur une copie ([:]) pour pouvoir modifier la liste 'dirs' originale
            for d in dirs[:]:
                src_dir = os.path.join(root, d)
                dst_dir = os.path.join(target_dir, d)
                if src_dir != dst_dir:
                    try:
                        safe_move(src_dir, dst_dir, conflict_mode="rename")
                        extracted_count += 1
                        # Le dossier a été déplacé entier à la racine, on l'enlève pour ne pas l'explorer !
                        dirs.remove(d)
                    except: pass

    # Nettoyage de l'intérieur du dossier source
    del_dirs, junk_files = clean_empty_folders(source_dir, deep_clean=deep_clean)

    # NOUVEAU: Si le dossier qu'on a vidé N'EST PAS le dossier d'arrière plan, et qu'il est vide, on l'efface
    if source_dir != target_dir:
        try:
            if not os.listdir(source_dir):
                os.rmdir(source_dir)
                del_dirs += 1
        except: pass

    return extracted_count, del_dirs, junk_files

def execute_silent_action(files, mode, custom_folder_name=None, override_folder_case=None):
    """Exécute une action rapide en arrière-plan en utilisant les réglages de l'utilisateur."""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except:
        config = {"conflict": "rename"}
    
    config["group_mode"] = mode
    if custom_folder_name:
        config["custom_folder"] = custom_folder_name
    if override_folder_case is not None:
        config["folder_case"] = override_folder_case
        
    conflict_mode = config.get("conflict", "rename")
    
    undo_log = {}
    success_count = 0

    for i, old_path in enumerate(files):
        if not os.path.exists(old_path): continue

        target_path = calculate_new_path(old_path, i+1, config)
        if old_path == target_path: continue

        target_dir = os.path.dirname(target_path)
        if target_dir: os.makedirs(target_dir, exist_ok=True)

        try:
            final_target = safe_move(old_path, target_path, conflict_mode)
            if final_target:
                undo_log[final_target] = old_path
                success_count += 1
        except: pass

    if undo_log:
        with open(UNDO_FILE, 'w', encoding='utf-8') as f:
            json.dump(undo_log, f)
            
    if success_count > 0:
        root = tk.Tk(); root.withdraw()
        messagebox.showinfo(tr("silent_title"), trf("silent_done", count=success_count))
        root.destroy()

# ==============================================================================
# LANCEUR / ACCUMULATEUR (Empêche l'ouverture de multiples processus)
# ==============================================================================
def _drain_late_writers(temp_dir, list_file, already_collected, seen_set, max_wait=2.0):
    """
    Récupère les fichiers écrits par les processus Windows retardataires.
    Appelé après l'élection du Maître pour rattraper les vagues tardives.
    Aspire à la fois selected.txt (retardataires intra-session) et inbox.txt
    (autres instances Windows 11 multi-explorer).
    Retourne la liste enrichie (sans doublons, ordre préservé).
    """
    result = list(already_collected)
    inbox_file = os.path.join(temp_dir, "inbox.txt")
    start = time.time()
    stable_since = time.time()
    STABLE = 0.4
    POLL = 0.1
    last_size = -1

    def _aspirate(path):
        """Aspire le contenu d'un fichier et l'ajoute à result via renommage atomique."""
        drain_p = path + ".drain"
        try:
            os.replace(path, drain_p)
            with open(drain_p, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    p = line.strip()
                    if p and p not in seen_set and os.path.exists(p):
                        seen_set.add(p)
                        result.append(p)
            try: os.remove(drain_p)
            except OSError: pass
        except OSError:
            pass

    while time.time() - start < max_wait:
        time.sleep(POLL)
        # L'inbox est écrite atomiquement par les autres instances → on l'aspire dès qu'elle apparaît
        if os.path.exists(inbox_file):
            _aspirate(inbox_file)

        if os.path.exists(list_file):
            try:
                cur_size = os.path.getsize(list_file)
            except OSError:
                cur_size = -1
            if cur_size != last_size:
                last_size = cur_size
                stable_since = time.time()
            elif time.time() - stable_since >= STABLE and last_size > 0:
                _aspirate(list_file)
                last_size = -1
                stable_since = time.time()

    # Récupération finale (selected.txt et inbox)
    for f in (list_file, inbox_file):
        if os.path.exists(f):
            _aspirate(f)
    return result


def launch_accumulator(mode, target_file):
    temp_dir = os.path.join(tempfile.gettempdir(), "OF_Premium")
    os.makedirs(temp_dir, exist_ok=True)
    list_file = os.path.join(temp_dir, "selected.txt")
    lock_file = os.path.join(temp_dir, "lock.tmp")
    gui_sentinel = os.path.join(temp_dir, "gui_open.lock")  # Barrière #2 anti-double-fenêtre
    debug_log = os.path.join(temp_dir, "debug.log")

    # === LOGGING DIAGNOSTIQUE ===
    # Chaque processus (Maître ou esclave) écrit ses étapes dans debug.log
    # avec son PID et un timestamp précis (au millième de seconde).
    # Cela permet de diagnostiquer toute race condition après-coup.
    _t_start = time.time()
    def _log(msg):
        try:
            ts = time.time() - _t_start
            line = f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] PID={os.getpid():>5} t+{ts:6.3f}s | {msg}\n"
            with open(debug_log, "a", encoding="utf-8") as lf:
                lf.write(line)
                lf.flush()
        except Exception:
            pass

    _log(f"START mode={mode} target={os.path.basename(target_file)} python={sys.executable}")

    # --- 1. ÉCRITURE ROBUSTE DE LA SÉLECTION ---
    # On écrit notre ligne puis on force l'écriture physique sur le disque (fsync)
    # pour que le processus Maître la voie immédiatement.
    for attempt in range(5):
        try:
            with open(list_file, "a", encoding="utf-8") as f:
                f.write(target_file + "\n")
                f.flush()
                os.fsync(f.fileno())
            _log(f"WRITE_OK attempt={attempt+1}")
            break
        except (PermissionError, OSError) as e:
            # Le fichier est peut-être verrouillé une fraction de seconde par
            # le Maître pendant son renommage : on réessaie brièvement.
            _log(f"WRITE_RETRY attempt={attempt+1} err={type(e).__name__}")
            time.sleep(0.05)

    # --- 2. ÉLECTION DU MAÎTRE (Named Mutex Windows = atomique kernel-level) ---
    # On utilise CreateMutexW de l'API Windows : c'est une primitive de synchronisation
    # garantie atomique par le kernel, contrairement à os.open(O_EXCL) sur fichier
    # qui peut souffrir de races sur NTFS / OneDrive / antivirus / etc.
    #
    # Comportement :
    #   - CreateMutexW retourne TOUJOURS un handle valide (sauf erreur grave)
    #   - GetLastError() == ERROR_ALREADY_EXISTS (183) si un autre process l'a déjà créé
    #   - Le mutex se libère AUTOMATIQUEMENT à la mort du process (kernel le sait)
    #     → plus besoin de gérer les "locks orphelins" manuellement
    #   - Le préfixe "Global\" partage le mutex entre fenêtres Explorer isolées
    MUTEX_NAME = "Global\\OutilsFichiersPremium_Accumulator_Mutex_v3"
    ERROR_ALREADY_EXISTS = 183

    kernel32 = ctypes.windll.kernel32
    kernel32.CreateMutexW.restype = ctypes.c_void_p
    kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_wchar_p]

    mutex_handle = kernel32.CreateMutexW(None, True, MUTEX_NAME)
    last_error = kernel32.GetLastError()
    is_master = (last_error != ERROR_ALREADY_EXISTS)

    _log(f"MUTEX handle={mutex_handle} last_error={last_error} is_master={is_master}")

    if not is_master:
        # Un autre process est déjà Maître. On ferme notre handle et on quitte.
        # Notre ligne a déjà été écrite dans selected.txt à l'étape 1.
        if mutex_handle:
            kernel32.CloseHandle(mutex_handle)
        _log("SLAVE_EXIT")
        sys.exit(0)

    _log("BECAME_MASTER")

    # Nous sommes le Maître. Le mutex restera vivant jusqu'à la fin du processus
    # (ou jusqu'à un appel explicite à CloseHandle ci-dessous).
    # On garde aussi un lock_file textuel pour compatibilité avec le drainage
    # (le code de drainage utilise list_file mais pas lock_file directement).
    try:
        with open(lock_file, "w", encoding="ascii") as f:
            f.write(str(os.getpid()))
    except OSError:
        pass

    # Garantie de nettoyage en cas de crash : on libère le mutex et on supprime
    # les fichiers temporaires. CloseHandle libère le mutex au niveau kernel,
    # ce qui permet à un futur clic-droit de redevenir Maître proprement.
    import atexit
    def _release_master_mutex():
        nonlocal mutex_handle
        try:
            if mutex_handle:
                kernel32.ReleaseMutex(mutex_handle)
                kernel32.CloseHandle(mutex_handle)
                mutex_handle = None
                _log("MUTEX_RELEASED")
        except Exception as e:
            _log(f"MUTEX_RELEASE_ERR {type(e).__name__}")
            mutex_handle = None

    def _cleanup_master():
        _log("CLEANUP_MASTER")
        _release_master_mutex()
        try:
            if mutex_handle:
                kernel32.ReleaseMutex(mutex_handle)
                kernel32.CloseHandle(mutex_handle)
        except Exception:
            pass
        for tmp in (list_file, lock_file, gui_sentinel, os.path.join(temp_dir, "inbox.txt")):
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except OSError:
                pass
    atexit.register(_cleanup_master)

    # --- 3. ATTENTE INTELLIGENTE : on attend que la sélection se "stabilise" ---
    # Au lieu d'un sleep(0.8) aveugle, le Maître surveille la taille du fichier.
    # Tant que Windows ajoute des processus, le fichier grossit. Quand il reste
    # stable assez longtemps, c'est que tous les éléments ont été reçus.
    STABLE_DELAY = 0.8      # durée de stabilité requise — augmentée pour le multi-Explorer
    MAX_WAIT = 15.0         # filet de sécurité absolu (secondes)
    POLL = 0.1

    def _file_signature():
        try:
            st = os.stat(list_file)
            return (st.st_size, st.st_mtime)
        except OSError:
            return (0, 0)

    start = time.time()
    last_sig = _file_signature()
    stable_since = time.time()

    # On attend un minimum incompressible pour laisser Windows démarrer les 1ers process
    time.sleep(0.3)

    while True:
        time.sleep(POLL)
        sig = _file_signature()
        if sig != last_sig:
            # Le fichier a encore changé : un nouveau process a écrit. On réarme.
            last_sig = sig
            stable_since = time.time()
        elif time.time() - stable_since >= STABLE_DELAY:
            # Aucun changement depuis STABLE_DELAY : la sélection est complète.
            break
        if time.time() - start >= MAX_WAIT:
            break

    # --- 4. PRISE DE POSSESSION ATOMIQUE DE LA LISTE ---
    # CRITIQUE : on RENOMME le fichier au lieu de le lire-puis-supprimer.
    # Le renommage est atomique : un esclave retardataire qui voudrait écrire
    # recréera un "selected.txt" neuf (traité ci-dessous), au lieu d'être perdu.
    processing_file = os.path.join(temp_dir, f"processing_{os.getpid()}.txt")
    files = []
    try:
        os.replace(list_file, processing_file)
    except OSError:
        processing_file = list_file  # repli : on lit le fichier en place

    try:
        with open(processing_file, "r", encoding="utf-8", errors="replace") as f:
            files = [line.strip() for line in f if line.strip()]
    except OSError:
        files = []

    # --- 5. RÉCUPÉRATION DES RETARDATAIRES ---
    # Si un processus très lent a écrit APRÈS notre renommage, un nouveau
    # "selected.txt" existe. On le récupère pour ne perdre aucun fichier.
    time.sleep(0.4)
    if os.path.exists(list_file):
        try:
            with open(list_file, "r", encoding="utf-8", errors="replace") as f:
                files += [line.strip() for line in f if line.strip()]
        except OSError:
            pass

    # --- 6. NETTOYAGE DES FICHIERS TEMPORAIRES ---
    # IMPORTANT : on NE supprime PAS le lock_file ici. Tant que ce processus Maître
    # tourne (notamment quand il affiche une mini-fenêtre Tkinter), il doit garder
    # son lock pour empêcher qu'un processus retardataire ne devienne un 2ème Maître
    # concurrent et n'ouvre une 2ème fenêtre. Le lock sera supprimé en fin de fonction.
    for tmp in (processing_file,):
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except OSError:
            pass

    # On ne garde que les éléments existant réellement sur le disque,
    # en supprimant les doublons SANS casser l'ordre de sélection.
    seen = set()
    valid_files = []
    for path in files:
        if path and path not in seen and os.path.exists(path):
            seen.add(path)
            valid_files.append(path)

    if not valid_files:
        return

    unique_files = valid_files

    # --- BARRIÈRE #2 : détection inter-session via FindWindowW (API Win32) ---
    # Windows 11 isole les processus selon l'explorer.exe d'origine. Les mutex
    # nommés et les fichiers sentinelles peuvent donc être cloisonnés par session.
    # FindWindowW, en revanche, scanne TOUT le bureau utilisateur indépendamment
    # de l'explorer hôte → c'est notre seul moyen fiable de détecter qu'une
    # autre instance affiche déjà une fenêtre de l'application.
    #
    # Stratégie : si une fenêtre nommée "OutilsFichiersPremium_MASTER_WINDOW" existe,
    # on écrit nos fichiers dans une "inbox" partagée et on quitte sans rien afficher.
    # Le Maître #1 lira cette inbox pendant son drainage continu.
    MASTER_WINDOW_CLASS_LOCAL = MASTER_WINDOW_CLASS  # Pour la lisibilité
    inbox_file = os.path.join(temp_dir, "inbox.txt")

    user32 = ctypes.windll.user32
    user32.FindWindowW.restype = ctypes.c_void_p
    user32.FindWindowW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]

    INTERACTIVE_MODES = {"gui", "custom_prompt", "extract", "bg_extract"}
    if mode in INTERACTIVE_MODES:
        # FindWindowW(className, windowName) : on cherche par classe car la classe
        # est invisible pour l'utilisateur (contrairement au titre) → on peut
        # garder un titre cosmétique propre "Dossier personnalisé".
        existing_window = user32.FindWindowW(MASTER_WINDOW_CLASS, None)
        _log(f"FINDWINDOW result={existing_window}")
        if existing_window:
            # Une autre instance affiche déjà sa fenêtre. On lui transmet nos fichiers
            # via l'inbox partagée (avec retry car plusieurs nous peuvent écrire en même temps).
            _log(f"MASTER_WINDOW_FOUND → forwarding {len(unique_files)} files to existing instance")
            for attempt in range(10):
                try:
                    with open(inbox_file, "a", encoding="utf-8") as f:
                        for path in unique_files:
                            f.write(path + "\n")
                        f.flush()
                        os.fsync(f.fileno())
                    _log(f"INBOX_WROTE {len(unique_files)} files (attempt={attempt+1})")
                    break
                except (PermissionError, OSError) as e:
                    _log(f"INBOX_RETRY attempt={attempt+1} err={type(e).__name__}")
                    time.sleep(0.05)
            # On quitte sans afficher de fenêtre
            try:
                if mutex_handle:
                    kernel32.ReleaseMutex(mutex_handle)
                    kernel32.CloseHandle(mutex_handle)
            except Exception:
                pass
            sys.exit(0)
        else:
            _log("NO_MASTER_WINDOW → this process will be the master GUI")

    if mode == "gui":
        # On continue à drainer pendant que la GUI s'ouvre (cas où le user clique
        # avec une très grosse sélection : Windows envoie les processus en plusieurs vagues)
        unique_files = _drain_late_writers(temp_dir, list_file, unique_files, seen, max_wait=2.0)
        app = PremiumOrganizerApp(unique_files)
        app.run()
    elif mode == "custom_prompt":
        # CORRECTIF MAJEUR : on draine les retardataires PENDANT que la mini-fenêtre
        # est affichée. Sinon les processus Windows qui arrivent après l'ouverture
        # de la fenêtre voient le lock pris et quittent en perdant leurs fichiers.
        _log(f"OPENING_MINI_PROMPT with {len(unique_files)} files")
        prompt = MiniPromptApp(unique_files)
        # On lance un draineur en arrière-plan via un after() Tkinter pour récupérer
        # les processus retardataires sans bloquer la fenêtre.
        prompt.attach_late_drainer(temp_dir, list_file, seen)
        folder, f_case = prompt.run()
        # GARDE ANTI-ULTRA-RETARDATAIRES : pour les très grosses sélections,
        # Windows peut continuer à lancer des processus jusqu'à plusieurs secondes
        # après l'ouverture initiale. On draine une dernière fois après la fermeture
        # de la fenêtre, sinon ces retardataires deviendraient Maître #2.
        if folder:  # Seulement si l'utilisateur a validé (sinon on annule tout)
            # On utilise le seen_set VIVANT du prompt (mis à jour par _poll_drain)
            # pour éviter les doublons ou les manqués lors du drain final.
            live_seen = prompt._drain_seen if prompt._drain_seen is not None else seen
            final_files = _drain_late_writers(
                temp_dir, list_file,
                prompt.get_final_files(), live_seen, max_wait=2.5
            )
            _release_master_mutex()
            execute_silent_action(final_files, "custom",
                                  custom_folder_name=folder,
                                  override_folder_case=f_case)

    # --- GESTION DE L'EXTRACTION ---
    elif mode in ["extract", "bg_extract"]:
        is_bg = (mode == "bg_extract")
        app = SelectiveExtractApp(unique_files, is_background=is_bg)
        app.run()

    elif mode in ["extract_1_level", "bg_extract_1_level"]:
        _release_master_mutex()
        is_bg = (mode == "bg_extract_1_level")
        ext_tot, del_tot, junk_tot = 0, 0, 0
        for d in unique_files:
            if os.path.isdir(d):
                if is_bg:
                    # Si c'est un clic d'arrière-plan, on extrait les enfants directs
                    for sub in os.listdir(d):
                        sub_path = os.path.join(d, sub)
                        if os.path.isdir(sub_path):
                            e, dd, j = perform_extraction(source_dir=sub_path, target_dir=d, mode="all", max_depth=1, deep_clean=True)
                            ext_tot += e; del_tot += dd; junk_tot += j
                else:
                    # Si c'est un clic ciblé, on extrait le dossier vers son parent
                    target_dir = os.path.dirname(os.path.normpath(d))
                    e, dd, j = perform_extraction(source_dir=d, target_dir=target_dir, mode="all", max_depth=1, deep_clean=True)
                    ext_tot += e; del_tot += dd; junk_tot += j
        root = tk.Tk(); root.withdraw()
        messagebox.showinfo(tr("quick_extract_title"), trf("quick_extract_done", items=ext_tot, dirs=del_tot))
        root.destroy()

    elif mode == "clean":
        _release_master_mutex()
        del_tot, junk_tot = 0, 0
        for d in unique_files:
            if os.path.isdir(d):
                dd, j = clean_empty_folders(d, deep_clean=True)
                del_tot += dd; junk_tot += j
        root = tk.Tk(); root.withdraw()
        messagebox.showinfo(tr("clean_title"), trf("clean_done", folders=len(unique_files), junk=junk_tot, dirs=del_tot))
        root.destroy()

    elif mode == "copy_empty_dirs":
        _release_master_mutex()
        copy_empty_folder_names(unique_files)

    elif mode == "paste_empty_dirs":
        _release_master_mutex()
        paste_empty_folder_names(unique_files)

    else:
        _release_master_mutex()
        execute_silent_action(unique_files, mode)

    # --- 7. PHASE DE GARDE FINALE ---
    # On garde le lock vivant pendant 3 secondes supplémentaires pour avaler
    # les ultra-retardataires de Windows. Sans ça, un processus lancé très tard
    # par Windows (jusqu'à plusieurs secondes après le clic) ne trouverait plus
    # ni le lock ni la mini-fenêtre, et lancerait un cycle entièrement nouveau.
    # Pendant cette garde, on absorbe silencieusement leurs écritures, y compris
    # dans l'inbox des instances multi-explorer.
    guard_end = time.time() + 3.0
    while time.time() < guard_end:
        time.sleep(0.2)
        # Si un retardataire a recréé selected.txt ou inbox.txt, on les vide
        for f in (list_file, inbox_file):
            if os.path.exists(f):
                try: os.remove(f)
                except OSError: pass

    # --- 8. NETTOYAGE FINAL DU LOCK ---
    # Le Maître relâche son verrou. À partir de maintenant, un nouveau clic-droit
    # pourra démarrer un nouveau cycle. L'atexit fera de toute façon le nettoyage
    # en cas d'erreur.
    for tmp in (list_file, lock_file, gui_sentinel, inbox_file):
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except OSError:
            pass

# ==============================================================================
# MINI INTERFACE POUR LE DOSSIER PERSONNALISÉ
# ==============================================================================
class MiniPromptApp:
    def __init__(self, files):
        self.files = list(files)
        self.folder_name = None
        self.folder_case = None
        # Pour le drainage en arrière-plan des processus retardataires
        self._drain_temp_dir = None
        self._drain_list_file = None
        self._drain_seen = None
        self._drain_last_size = -1
        self._drain_stable_since = None
        
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f: self.config = json.load(f)
        except:
            self.config = {}
        self.lang = get_language(self.config)

        # IMPORTANT : on passe className pour que la fenêtre porte une classe Win32
        # unique détectable par FindWindowW. Cela permet à d'autres instances de
        # cette application (lancées en parallèle par Windows 11 multi-explorer)
        # de détecter notre fenêtre et de nous envoyer leurs fichiers via l'inbox
        # au lieu d'ouvrir une 2ème fenêtre.
        self.root = tk.Tk(className=MASTER_WINDOW_CLASS)
        self.root.title(tr("mini_title", self.lang))
        self.root.geometry("450x190")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#F8FAFC")

        style = ttk.Style()
        style.theme_use('vista')
        
        self.cases = {
            tr("case_none", self.lang): "none",
            tr("case_lower", self.lang): "lower",
            tr("case_upper", self.lang): "upper",
            tr("case_title", self.lang): "title",
            "snake_case": "snake",
            "kebab-case": "kebab"
        }
        self.inv_cases = {v: k for k, v in self.cases.items()}

        # On garde une référence pour pouvoir mettre à jour le compteur en temps réel
        self.lbl_title = tk.Label(self.root, text=trf("mini_label", self.lang, count=len(self.files)), font=("Segoe UI", 11, "bold"), bg="#F8FAFC", fg="#005FB8")
        self.lbl_title.pack(pady=(15, 5))
        
        self.entry = ttk.Entry(self.root, font=("Segoe UI", 10))
        self.entry.insert(0, tr("default_folder", self.lang))
        self.entry.pack(fill=tk.X, padx=30, pady=5)
        self.entry.focus()
        self.entry.selection_range(0, tk.END)

        f_opt = tk.Frame(self.root, bg="#F8FAFC")
        f_opt.pack(fill=tk.X, padx=30, pady=5)
        tk.Label(f_opt, text=tr("format_label", self.lang), bg="#F8FAFC", font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.cb_case = ttk.Combobox(f_opt, values=list(self.cases.keys()), state="readonly", width=15)
        saved_case = self.config.get("folder_case", "none")
        self.cb_case.set(self.inv_cases.get(saved_case, tr("case_none", self.lang)))
        self.cb_case.pack(side=tk.LEFT, padx=5)

        btn_frame = tk.Frame(self.root, bg="#F8FAFC")
        btn_frame.pack(pady=10)

        btn_ok = tk.Button(btn_frame, text="✅ OK", command=self.on_ok, bg="#005FB8", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=3, cursor="hand2")
        btn_ok.pack(side=tk.LEFT, padx=5)
        
        btn_cancel = tk.Button(btn_frame, text=f"❌ {tr('cancel', self.lang)}", command=self.root.destroy, bg="#E2E8F0", fg="#334155", font=("Segoe UI", 10, "bold"), relief="flat", padx=10, pady=3, cursor="hand2")
        btn_cancel.pack(side=tk.LEFT, padx=5)

        self.root.bind('<Return>', lambda e: self.on_ok())
        self.root.bind('<Escape>', lambda e: self.root.destroy())

    def on_ok(self):
        val = self.entry.get().strip()
        self.folder_name = val if val else tr("default_folder", self.lang)
        selected_case_text = self.cb_case.get()
        self.folder_case = self.cases.get(selected_case_text, "none")
        self.root.destroy()
        
    def attach_late_drainer(self, temp_dir, list_file, seen_set):
        """Active la récupération en arrière-plan des processus Windows retardataires
        ET des autres instances qui nous envoient leurs fichiers via l'inbox."""
        self._drain_temp_dir = temp_dir
        self._drain_list_file = list_file
        self._drain_inbox_file = os.path.join(temp_dir, "inbox.txt")
        self._drain_seen = seen_set
        self._drain_stable_since = time.time()
        # Démarre le polling Tkinter (non bloquant)
        self.root.after(150, self._poll_drain)

    def _poll_drain(self):
        """Appelé périodiquement par Tkinter pour aspirer les retardataires
        ET récupérer les fichiers envoyés par les autres instances via l'inbox."""
        try:
            # 1) Drainage du selected.txt (retardataires Windows sur la même session)
            if self._drain_list_file and os.path.exists(self._drain_list_file):
                try:
                    cur_size = os.path.getsize(self._drain_list_file)
                except OSError:
                    cur_size = -1
                
                if cur_size != self._drain_last_size:
                    # Le fichier grossit encore : on attend la stabilité
                    self._drain_last_size = cur_size
                    self._drain_stable_since = time.time()
                elif cur_size > 0 and time.time() - self._drain_stable_since >= 0.4:
                    # Stable depuis 0.4s : on aspire
                    drain_path = self._drain_list_file + ".drain"
                    try:
                        os.replace(self._drain_list_file, drain_path)
                        added = 0
                        with open(drain_path, "r", encoding="utf-8", errors="replace") as f:
                            for line in f:
                                p = line.strip()
                                if p and p not in self._drain_seen and os.path.exists(p):
                                    self._drain_seen.add(p)
                                    self.files.append(p)
                                    added += 1
                        try: os.remove(drain_path)
                        except OSError: pass
                        self._drain_last_size = -1
                        self._drain_stable_since = time.time()
                        # Mise à jour visuelle du compteur (l'utilisateur voit la sélection grandir)
                        if added > 0:
                            self.lbl_title.config(text=trf("mini_label", self.lang, count=len(self.files)))
                    except OSError:
                        pass

            # 2) Drainage de l'inbox (fichiers envoyés par d'autres instances
            # de Windows 11 multi-explorer qui ont détecté notre fenêtre).
            # Cet inbox est crucial : c'est lui qui empêche le bug "double fenêtre".
            if hasattr(self, '_drain_inbox_file') and self._drain_inbox_file and os.path.exists(self._drain_inbox_file):
                inbox_drain = self._drain_inbox_file + ".drain"
                try:
                    os.replace(self._drain_inbox_file, inbox_drain)
                    added_inbox = 0
                    with open(inbox_drain, "r", encoding="utf-8", errors="replace") as f:
                        for line in f:
                            p = line.strip()
                            if p and p not in self._drain_seen and os.path.exists(p):
                                self._drain_seen.add(p)
                                self.files.append(p)
                                added_inbox += 1
                    try: os.remove(inbox_drain)
                    except OSError: pass
                    if added_inbox > 0:
                        self.lbl_title.config(text=trf("mini_label", self.lang, count=len(self.files)))
                except OSError:
                    pass
        except Exception:
            pass
        # On reprogramme tant que la fenêtre est ouverte
        try:
            self.root.after(200, self._poll_drain)
        except tk.TclError:
            pass  # La fenêtre a été détruite

    def get_final_files(self):
        """Renvoie la liste finale après drainage complet, en filtrant les fichiers disparus."""
        return [p for p in self.files if os.path.exists(p)]

    def run(self):
        self.root.mainloop()
        return self.folder_name, self.folder_case

# ==============================================================================
# L'APPLICATION D'EXTRACTION SÉLECTIVE (GUI)
# ==============================================================================
class SelectiveExtractApp:
    def __init__(self, target_dirs, is_background=False):
        if isinstance(target_dirs, str):
            self.target_dirs = [target_dirs]
        else:
            self.target_dirs = target_dirs
            
        self.is_background = is_background
        self.lang = get_language()
            
        self.root = tk.Tk(className=MASTER_WINDOW_CLASS)
        self.root.title(tr("extract_title", self.lang))
        self.root.geometry("500x470")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#F8FAFC")

        style = ttk.Style()
        style.theme_use('vista')

        self.var_mode = tk.StringVar(value="all")
        self.var_cat = tk.StringVar(value=category_label("Vidéos", self.lang))
        self.var_ext = tk.StringVar(value=".pdf")
        self.var_deep_clean = tk.BooleanVar(value=True)
        self.var_max_depth = tk.IntVar(value=0)

        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.root, bg="#FFFFFF", pady=15, padx=20)
        header.pack(fill=tk.X)
        tk.Label(header, text=f"🌪️ {tr('extract_title', self.lang)}", font=("Segoe UI", 16, "bold"), bg="#FFFFFF", fg="#0F172A").pack(side=tk.LEFT)
        tk.Frame(self.root, bg="#E2E8F0", height=1).pack(fill=tk.X)

        body = tk.Frame(self.root, bg="#F8FAFC", padx=20, pady=15)
        body.pack(fill=tk.BOTH, expand=True)
        
        lbl_text = tr("extract_where_bg", self.lang) if self.is_background else trf("extract_where", self.lang, count=len(self.target_dirs))
        tk.Label(body, text=lbl_text, font=("Segoe UI", 11, "bold"), bg="#F8FAFC", fg="#005FB8").pack(anchor=tk.W, pady=(0, 10))
        ttk.Radiobutton(body, text=tr("extract_all", self.lang), variable=self.var_mode, value="all").pack(anchor=tk.W, pady=5)

        f_cat = tk.Frame(body, bg="#F8FAFC")
        f_cat.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(f_cat, text=tr("extract_category", self.lang), variable=self.var_mode, value="cat").pack(side=tk.LEFT)
        ttk.Combobox(f_cat, textvariable=self.var_cat, values=category_values(self.lang), state="readonly", width=15).pack(side=tk.LEFT, padx=10)

        f_ext = tk.Frame(body, bg="#F8FAFC")
        f_ext.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(f_ext, text=tr("extract_extension", self.lang), variable=self.var_mode, value="ext").pack(side=tk.LEFT)
        ttk.Entry(f_ext, textvariable=self.var_ext, width=10).pack(side=tk.LEFT, padx=10)

        ttk.Separator(body, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        tk.Label(body, text=tr("extract_depth", self.lang), font=("Segoe UI", 10, "bold"), bg="#F8FAFC", fg="#005FB8").pack(anchor=tk.W, pady=(0, 5))
        ttk.Radiobutton(body, text=tr("extract_unlimited", self.lang), variable=self.var_max_depth, value=0).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(body, text=tr("extract_one_level", self.lang), variable=self.var_max_depth, value=1).pack(anchor=tk.W, pady=2)

        ttk.Separator(body, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        ttk.Checkbutton(body, text=f"🧼 {tr('extract_deep_clean', self.lang)}", variable=self.var_deep_clean).pack(anchor=tk.W)
        tk.Label(body, text=tr("extract_deep_clean_help", self.lang), font=("Segoe UI", 8), bg="#F8FAFC", fg="#64748B").pack(anchor=tk.W, padx=25)

        footer = tk.Frame(self.root, bg="#FFFFFF", pady=15, padx=20)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Frame(self.root, bg="#E2E8F0", height=1).pack(fill=tk.X, side=tk.BOTTOM)

        btn_ok = tk.Button(footer, text=f"✅ {tr('extract_button', self.lang)}", command=self.execute, bg="#005FB8", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=5, cursor="hand2")
        btn_ok.pack(side=tk.RIGHT, padx=5)
        btn_cancel = tk.Button(footer, text=f"❌ {tr('cancel', self.lang)}", command=self.root.destroy, bg="#F1F5F9", fg="#334155", font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=5, cursor="hand2")
        btn_cancel.pack(side=tk.RIGHT, padx=5)

    def execute(self):
        mode = self.var_mode.get()
        cat = category_key_from_label(self.var_cat.get(), self.lang)
        ext = self.var_ext.get().lower().strip()
        deep_clean = self.var_deep_clean.get()
        max_depth = self.var_max_depth.get()
        
        if not ext.startswith('.') and ext: ext = '.' + ext

        extracted_total, del_dirs_total, junk_files_total = 0, 0, 0
        
        for d in self.target_dirs:
            if os.path.isdir(d):
                if self.is_background:
                    for sub in os.listdir(d):
                        sub_path = os.path.join(d, sub)
                        if os.path.isdir(sub_path):
                            e, dd, j = perform_extraction(
                                source_dir=sub_path, target_dir=d, mode=mode, cat=cat, ext=ext, max_depth=max_depth, deep_clean=deep_clean
                            )
                            extracted_total += e
                            del_dirs_total += dd
                            junk_files_total += j
                else:
                    target = os.path.dirname(os.path.normpath(d))
                    e, dd, j = perform_extraction(
                        source_dir=d, target_dir=target, mode=mode, cat=cat, ext=ext, max_depth=max_depth, deep_clean=deep_clean
                    )
                    extracted_total += e
                    del_dirs_total += dd
                    junk_files_total += j

        msg = trf("extract_done", self.lang, items=extracted_total)
        if deep_clean:
            msg += trf("extract_done_clean", self.lang, junk=junk_files_total, dirs=del_dirs_total)
        
        messagebox.showinfo(tr("extract_done_title", self.lang), msg)
        self.root.destroy()

    def run(self):
        self.root.mainloop()

# ==============================================================================
# L'APPLICATION GRAPHIQUE (UX/UI Premium)
# ==============================================================================
class PremiumOrganizerApp:
    def __init__(self, files):
        self.files = files
        self.lang = get_language()
        self.root = tk.Tk(className=MASTER_WINDOW_CLASS)
        self.root.title(tr("app_name", self.lang))
        self.root.geometry("1200x800")
        self.root.minsize(950, 650)
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#F8FAFC")

        self.style = ttk.Style()
        self.style.theme_use('vista')

        self.style.configure('.', font=('Segoe UI', 10))
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=[15, 8])
        self.style.configure('Treeview', rowheight=30, font=('Segoe UI', 9), borderwidth=0)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#F1F5F9', foreground='#334155')
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) 

        self.config = self.load_config()
        self.preview_data = [] 

        self.build_ui()
        self.update_preview()

    def load_config(self):
        lang = get_language()
        default = {
            "group_mode": "custom", "custom_folder": tr("default_folder", lang),
            "rename_case": "none", "folder_case": "none", "clean_tags": False, "clean_urls": False,
            "seq_num": False, "add_date": "none", "conflict": "rename", "language": lang
        }
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f: return {**default, **json.load(f)}
        except: return default

    def save_config(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f: json.dump(self.config, f)

    def build_ui(self):
        self.lang = get_language(self.config)
        self.var_group = tk.StringVar(value=self.config["group_mode"])
        self.var_custom_folder = tk.StringVar(value=self.config["custom_folder"])
        self.var_case = tk.StringVar(value=self.config.get("rename_case", "none"))
        self.var_folder_case = tk.StringVar(value=self.config.get("folder_case", "none"))
        self.var_clean_tags = tk.BooleanVar(value=self.config["clean_tags"])
        self.var_clean_urls = tk.BooleanVar(value=self.config["clean_urls"])
        self.var_seq_num = tk.BooleanVar(value=self.config["seq_num"])
        self.var_add_date = tk.StringVar(value=self.config["add_date"])
        self.var_conflict = tk.StringVar(value=self.config["conflict"])
        self.var_language = tk.StringVar(value=self.config.get("language", self.lang))

        for var in [self.var_group, self.var_custom_folder, self.var_case, self.var_folder_case, self.var_clean_tags, 
                    self.var_clean_urls, self.var_seq_num, self.var_add_date, self.var_conflict, self.var_language]:
            var.trace_add('write', lambda *args: self.root.after(50, self.update_preview))

        header_frame = tk.Frame(self.root, bg="#FFFFFF", pady=15, padx=20)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text=f"🚀 {tr('app_name', self.lang)}", font=("Segoe UI", 18, "bold"), bg="#FFFFFF", fg="#0F172A").pack(side=tk.LEFT)
        tk.Label(header_frame, text=tr("app_tagline", self.lang), font=("Segoe UI", 11), bg="#FFFFFF", fg="#64748B").pack(side=tk.LEFT, padx=15, anchor=tk.S)
        tk.Frame(self.root, bg="#E2E8F0", height=1).pack(fill=tk.X)

        footer_bg = tk.Frame(self.root, bg="#FFFFFF", pady=15, padx=20)
        footer_bg.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Frame(self.root, bg="#E2E8F0", height=1).pack(fill=tk.X, side=tk.BOTTOM)
        
        self.lbl_status = tk.Label(footer_bg, text=trf("status_ready", self.lang, count=len(self.files)), font=("Segoe UI", 11, "bold"), bg="#FFFFFF", fg="#0F172A")
        self.lbl_status.pack(side=tk.LEFT)

        btn_ok = tk.Button(footer_bg, text=f"✅ {tr('apply', self.lang)}", command=self.execute, bg="#005FB8", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", padx=25, pady=6, cursor="hand2")
        btn_ok.pack(side=tk.RIGHT, padx=5)
        btn_ok.bind("<Enter>", lambda e: btn_ok.config(bg="#0078D4"))
        btn_ok.bind("<Leave>", lambda e: btn_ok.config(bg="#005FB8"))
        
        btn_cancel = tk.Button(footer_bg, text=f"❌ {tr('cancel', self.lang)}", command=self.root.destroy, bg="#F1F5F9", fg="#334155", font=("Segoe UI", 11, "bold"), relief="flat", padx=15, pady=6, cursor="hand2")
        btn_cancel.pack(side=tk.RIGHT, padx=10)
        btn_cancel.bind("<Enter>", lambda e: btn_cancel.config(bg="#E2E8F0"))
        btn_cancel.bind("<Leave>", lambda e: btn_cancel.config(bg="#F1F5F9"))

        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)

        notebook = ttk.Notebook(left_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # TAB 1 : DOSSIER
        tab_group = ttk.Frame(notebook)
        notebook.add(tab_group, text=tr("tab_group", self.lang))
        ttk.Label(tab_group, text=tr("basic_grouping", self.lang), font=('Segoe UI', 12, 'bold'), foreground='#005FB8').pack(anchor=tk.W, padx=15, pady=(15, 5))
        ttk.Radiobutton(tab_group, text=tr("group_none", self.lang), variable=self.var_group, value="none").pack(anchor=tk.W, padx=30, pady=3)
        
        f_custom = ttk.Frame(tab_group)
        f_custom.pack(fill=tk.X, padx=30, pady=3)
        ttk.Radiobutton(f_custom, text=tr("group_custom", self.lang), variable=self.var_group, value="custom").pack(side=tk.LEFT)
        ttk.Entry(f_custom, textvariable=self.var_custom_folder, width=25, font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(tab_group, text=tr("group_1to1", self.lang), variable=self.var_group, value="1to1").pack(anchor=tk.W, padx=30, pady=3)
        ttk.Separator(tab_group, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=10)

        ttk.Label(tab_group, text=tr("smart_grouping", self.lang), font=('Segoe UI', 12, 'bold'), foreground='#005FB8').pack(anchor=tk.W, padx=15, pady=(5, 5))
        ttk.Radiobutton(tab_group, text=tr("group_smart", self.lang), variable=self.var_group, value="smart").pack(anchor=tk.W, padx=30, pady=3)
        ttk.Radiobutton(tab_group, text=tr("group_ext", self.lang), variable=self.var_group, value="ext").pack(anchor=tk.W, padx=30, pady=3)
        ttk.Radiobutton(tab_group, text=tr("group_prefix", self.lang), variable=self.var_group, value="prefix").pack(anchor=tk.W, padx=30, pady=3)
        ttk.Separator(tab_group, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=10)

        ttk.Label(tab_group, text=tr("metadata_grouping", self.lang), font=('Segoe UI', 12, 'bold'), foreground='#005FB8').pack(anchor=tk.W, padx=15, pady=(5, 5))
        f_meta1 = ttk.Frame(tab_group)
        f_meta1.pack(fill=tk.X, padx=30, pady=3)
        ttk.Radiobutton(f_meta1, text=tr("group_date", self.lang), variable=self.var_group, value="date_ym").pack(side=tk.LEFT)
        ttk.Radiobutton(f_meta1, text=tr("group_date_tree", self.lang), variable=self.var_group, value="date_tree").pack(side=tk.LEFT, padx=30)
        
        f_meta2 = ttk.Frame(tab_group)
        f_meta2.pack(fill=tk.X, padx=30, pady=3)
        ttk.Radiobutton(f_meta2, text=tr("group_size", self.lang), variable=self.var_group, value="size").pack(side=tk.LEFT)
        ttk.Radiobutton(f_meta2, text=tr("group_alpha", self.lang), variable=self.var_group, value="alpha").pack(side=tk.LEFT, padx=56)
        ttk.Separator(tab_group, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=10)

        ttk.Label(tab_group, text=tr("folder_case_title", self.lang), font=('Segoe UI', 12, 'bold'), foreground='#005FB8').pack(anchor=tk.W, padx=15, pady=(5, 5))
        f_fcase = ttk.Frame(tab_group)
        f_fcase.pack(fill=tk.X, padx=30, pady=3)
        ttk.Radiobutton(f_fcase, text=tr("case_none", self.lang), variable=self.var_folder_case, value="none").pack(side=tk.LEFT)
        ttk.Radiobutton(f_fcase, text=tr("case_lower", self.lang), variable=self.var_folder_case, value="lower").pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(f_fcase, text=tr("case_upper", self.lang), variable=self.var_folder_case, value="upper").pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(f_fcase, text=tr("case_title", self.lang), variable=self.var_folder_case, value="title").pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(f_fcase, text="snake_case", variable=self.var_folder_case, value="snake").pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(f_fcase, text="kebab-case", variable=self.var_folder_case, value="kebab").pack(side=tk.LEFT, padx=15)

        # TAB 2 : RENOMMAGE
        tab_rename = ttk.Frame(notebook)
        notebook.add(tab_rename, text=tr("tab_rename", self.lang))
        ttk.Label(tab_rename, text=tr("file_case_title", self.lang), font=('Segoe UI', 12, 'bold'), foreground='#005FB8').pack(anchor=tk.W, padx=15, pady=(15, 5))
        f_case1 = ttk.Frame(tab_rename)
        f_case1.pack(fill=tk.X, padx=30, pady=3)
        ttk.Radiobutton(f_case1, text=tr("case_none", self.lang), variable=self.var_case, value="none").pack(side=tk.LEFT)
        ttk.Radiobutton(f_case1, text=tr("case_lower", self.lang), variable=self.var_case, value="lower").pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(f_case1, text=tr("case_upper", self.lang), variable=self.var_case, value="upper").pack(side=tk.LEFT, padx=15)
        f_case2 = ttk.Frame(tab_rename)
        f_case2.pack(fill=tk.X, padx=30, pady=3)
        ttk.Radiobutton(f_case2, text=tr("case_title_words", self.lang), variable=self.var_case, value="title").pack(side=tk.LEFT)
        ttk.Radiobutton(f_case2, text="snake_case", variable=self.var_case, value="snake").pack(side=tk.LEFT, padx=13)
        ttk.Radiobutton(f_case2, text="kebab-case", variable=self.var_case, value="kebab").pack(side=tk.LEFT, padx=18)
        ttk.Separator(tab_rename, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=15)

        ttk.Label(tab_rename, text=tr("deep_clean_title", self.lang), font=('Segoe UI', 12, 'bold'), foreground='#005FB8').pack(anchor=tk.W, padx=15, pady=(5, 5))
        ttk.Checkbutton(tab_rename, text=tr("anti_tags", self.lang), variable=self.var_clean_tags).pack(anchor=tk.W, padx=30, pady=3)
        ttk.Checkbutton(tab_rename, text=tr("anti_urls", self.lang), variable=self.var_clean_urls).pack(anchor=tk.W, padx=30, pady=3)
        ttk.Separator(tab_rename, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=15)

        ttk.Label(tab_rename, text=tr("smart_additions", self.lang), font=('Segoe UI', 12, 'bold'), foreground='#005FB8').pack(anchor=tk.W, padx=15, pady=(5, 5))
        ttk.Checkbutton(tab_rename, text=tr("seq_num", self.lang), variable=self.var_seq_num).pack(anchor=tk.W, padx=30, pady=3)
        f_date = ttk.Frame(tab_rename)
        f_date.pack(fill=tk.X, padx=30, pady=8)
        ttk.Label(f_date, text=tr("date_stamp", self.lang), font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        ttk.Radiobutton(f_date, text=tr("date_none", self.lang), variable=self.var_add_date, value="none").pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(f_date, text=tr("date_prefix", self.lang), variable=self.var_add_date, value="prefix").pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(f_date, text=tr("date_suffix", self.lang), variable=self.var_add_date, value="suffix").pack(side=tk.LEFT, padx=15)

        # TAB 3 : PARAMETRES
        tab_settings = ttk.Frame(notebook)
        notebook.add(tab_settings, text=tr("tab_settings", self.lang))
        ttk.Label(tab_settings, text=tr("conflict_title", self.lang), font=('Segoe UI', 12, 'bold'), foreground='#005FB8').pack(anchor=tk.W, padx=15, pady=(15, 5))
        ttk.Radiobutton(tab_settings, text=tr("conflict_rename", self.lang), variable=self.var_conflict, value="rename").pack(anchor=tk.W, padx=30, pady=5)
        ttk.Radiobutton(tab_settings, text=tr("conflict_overwrite", self.lang), variable=self.var_conflict, value="overwrite").pack(anchor=tk.W, padx=30, pady=5)
        ttk.Radiobutton(tab_settings, text=tr("conflict_skip", self.lang), variable=self.var_conflict, value="skip").pack(anchor=tk.W, padx=30, pady=5)
        ttk.Separator(tab_settings, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=15)
        ttk.Label(tab_settings, text=tr("language_title", self.lang), font=('Segoe UI', 12, 'bold'), foreground='#005FB8').pack(anchor=tk.W, padx=15, pady=(5, 5))
        ttk.Radiobutton(tab_settings, text="Français", variable=self.var_language, value="fr").pack(anchor=tk.W, padx=30, pady=3)
        ttk.Radiobutton(tab_settings, text="English", variable=self.var_language, value="en").pack(anchor=tk.W, padx=30, pady=3)
        ttk.Label(tab_settings, text=tr("language_note", self.lang), foreground="#64748B").pack(anchor=tk.W, padx=30, pady=(5, 0))

        # RIGHT PANEL : Live Preview
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        f_prev_header = ttk.Frame(right_frame)
        f_prev_header.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(f_prev_header, text=tr("preview_title", self.lang), font=("Segoe UI", 12, "bold"), foreground='#005FB8').pack(side=tk.LEFT)

        columns = ("old", "new")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", selectmode="none")
        self.tree.heading("old", text=tr("preview_old", self.lang))
        self.tree.heading("new", text=tr("preview_new", self.lang))
        self.tree.column("old", width=250)
        self.tree.column("new", width=450)
        self.tree.tag_configure('evenrow', background='#F8FAFC')
        self.tree.tag_configure('oddrow', background='#FFFFFF')
        
        scroll_y = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll_y.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    def update_preview(self):
        self.lang = self.var_language.get()
        self.config.update({
            "group_mode": self.var_group.get(), "custom_folder": self.var_custom_folder.get(),
            "rename_case": self.var_case.get(), "folder_case": self.var_folder_case.get(), "clean_tags": self.var_clean_tags.get(),
            "clean_urls": self.var_clean_urls.get(), "seq_num": self.var_seq_num.get(),
            "add_date": self.var_add_date.get(), "conflict": self.var_conflict.get(),
            "language": self.var_language.get()
        })
        self.save_config()

        for item in self.tree.get_children(): self.tree.delete(item)
        self.preview_data.clear()
        preview_count = min(len(self.files), 100)
        
        for i, f in enumerate(self.files):
            new_path = calculate_new_path(f, i+1, self.config)
            self.preview_data.append((f, new_path))
            
            if i < preview_count:
                parent_dir = os.path.dirname(f)
                display_new = new_path.replace(parent_dir + "\\", ".\\")
                row_tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=(os.path.basename(f), display_new), tags=(row_tag,))
        
        if len(self.files) > 100:
            self.tree.insert("", "end", values=("...", trf("preview_more", self.lang, count=len(self.files)-100)), tags=('oddrow',))

    def execute(self):
        conflict_mode = self.var_conflict.get()
        undo_log = {}
        success_count = 0

        for old_path, target_path in self.preview_data:
            if not os.path.exists(old_path): continue
            if old_path == target_path: continue

            target_dir = os.path.dirname(target_path)
            if target_dir: os.makedirs(target_dir, exist_ok=True)

            try:
                final_target = safe_move(old_path, target_path, conflict_mode)
                if final_target:
                    undo_log[final_target] = old_path
                    success_count += 1
            except: pass

        with open(UNDO_FILE, 'w', encoding='utf-8') as f: json.dump(undo_log, f)
        messagebox.showinfo(tr("done_title", self.lang), trf("done_msg", self.lang, count=success_count))
        self.root.destroy()

    def run(self):
        self.root.mainloop()

# ==============================================================================
# POINT D'ENTRÉE DU SCRIPT
# ==============================================================================
if __name__ == "__main__":
    if len(sys.argv) == 1:
        install_context_menu()
    else:
        action = sys.argv[1]
        target = sys.argv[2] if len(sys.argv) > 2 else ""

        if action == "--accumulate":
            mode = sys.argv[2]
            target_f = sys.argv[3] if len(sys.argv) > 3 else ""
            launch_accumulator(mode, target_f)
            
        elif action == "--undo":
            undo_last_action()
            
        elif action == "--extract":
            # Si appelé de manière détournée sans accumulateur
            if os.path.isdir(target):
                SelectiveExtractApp([target], is_background=False).run()
                
        elif action == "--clean":
            if os.path.isdir(target):
                del_dirs, junk_files = clean_empty_folders(target, deep_clean=True)
                root = tk.Tk(); root.withdraw()
                messagebox.showinfo(tr("clean_title"), trf("clean_done", folders=1, junk=junk_files, dirs=del_dirs))
                root.destroy()
