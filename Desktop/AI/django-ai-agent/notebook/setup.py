import os
import pathlib
import sys 
NOTEBOOKS_DIR = pathlib.Path(__file__).parent.resolve()
REPO_DIR = NOTEBOOKS_DIR.parent
DJANGO_PROJECT_ROOT = REPO_DIR / "src"
DJANGO_SETTINGS_MODULE = "cfehome.settings"

def init(verbose = False):
    try:
        import nest_asyncio
        nest_asyncio.apply()
        if verbose:
            print("Applied nest_asyncio patch for Jupyter notebooks.")
    except ImportError:
        if verbose:
            print("nest_asyncio not installed. If you encounter issues with async code, consider installing it.")
            
    os.chdir(DJANGO_PROJECT_ROOT)
    sys.path.insert(0, str(DJANGO_PROJECT_ROOT))
    if verbose:
        print(f"Changed working directory to {DJANGO_PROJECT_ROOT}")
        print(f"Added {DJANGO_PROJECT_ROOT} to sys.path")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    import django
    django.setup()