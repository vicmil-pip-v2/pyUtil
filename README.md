# Python Utility Toolkit

A collection of **utility functions and helpers** for managing Python virtual environments,
pip packages, file system operations, GitHub/GDrive downloads, zip/tar extraction,
and subprocess execution.

---

## 🚀 Features

### 🔧 Environment & Pip Management

- Create and manage Python virtual environments (`python_virtual_environment`)
- Install pip packages into venvs (`pip_install_packages_in_virtual_environment`)
- Detect whether modules are installed (`module_installed`)
- Load packages from other virtual environments (`include_other_venv`)
- Manage requirements files (`parse_requirements`)
- `PipManager` class for automatic module checking and installation

### 🗂 File & Directory Utilities

- Safe recursive copy with protection (`safe_copy_directory`)
- Recursive copy with `.gitignore`-style filtering (`safe_copy_directory_with_ignore`)
- Delete folders and files (`delete_folder_with_contents`, `delete_file`)
- Write text to files (`write_text_to_file`)
- Search for files by name (`find_files_by_name`)
- List installed "vicmil packages" (`list_installed_vicmil_packages`)

### 🌐 Web & Networking

- Open a browser or serve HTML files locally (`open_webbrowser`, `serve_html_page`)
- Download files from Google Drive (`download_file_from_google_drive`)
- Download GitHub repos as ZIP archives (`download_github_repo_as_zip`)

### 📦 Archive Handling

- Extract `.tar.gz` files (`untar_file`)
- Extract `.zip` files (`unzip_file`)
- Extract `.zip` files without top-level folder (`unzip_without_top_dir`)

### ⚙️ Subprocess Helpers

- Run shell/PowerShell commands (`run_command`)
- Invoke Python scripts in specific venvs (`invoke_python_file_using_subprocess`)

### 🔑 Miscellaneous

- `.gitignore`-like matcher (`GitignorePatternMatcher`)
- Hash paths (`hash_path`)
- Generate random strings (`generate_random_letters`, `generate_random_numbers`)

---

## 📦 Installation

Clone the repository:

```bash
git clone git@github.com:vizpip/py_util.git
cd py_util
```

(Optional) set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

Install dependencies (only when needed):

```bash
pip install -r requirements.txt
```

---

## 🔍 Usage

Import the utilities into your Python code:

```python
from utils import PipManager, safe_copy_directory, run_command

# Example: ensure numpy is installed in a local venv
pm = PipManager()
pm.add_module("numpy", "numpy")
pm.install_missing_modules()

# Example: copy a directory
safe_copy_directory("src", "backup")

# Example: run a command
run_command("echo Hello World")
```

---

## 🧪 Testing

Run unit tests (if available):

```bash
pytest
```

---

## 📄 License

MIT License.
Feel free to use in personal and commercial projects.
