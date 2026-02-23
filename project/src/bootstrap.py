import os
import sys
from pathlib import Path

def project_root() -> Path:
    """
    This file is at: <project_root>/src/bootstrap.py
    """
    return Path(__file__).resolve().parents[1]

def vendor_dir() -> Path:
    """
    Vendor code is at: <project_root>/vendor/code_rag
    """
    return project_root() / "vendor" / "code_rag"

def setup_vendor_path(verbose: bool = True) -> Path:
    """
    Make vendor modules importable via:
      import config_data
      import rag
      import knowledge_base
      ...
    """
    vdir = vendor_dir()
    if not vdir.exists():
        raise FileNotFoundError(f"vendor dir not found: {vdir}")

    # Put vendor dir at the front so it wins over other same-named modules
    if str(vdir) not in sys.path:
        sys.path.insert(0, str(vdir))

    if verbose:
        print("✅ Added vendor to sys.path:", vdir)
        print("✅ sys.path[0] =", sys.path[0])
        for f in ["config_data.py", "rag.py", "knowledge_base.py", "vector_stores.py"]:
            print(f"   - {f}: {(vdir / f).exists()}")

    return vdir

def set_dashscope_key(key: str | None = None):
    """
    Set DASHSCOPE_API_KEY.
    If you already set it in system env, you can skip passing key.
    """
    if key:
        os.environ["DASHSCOPE_API_KEY"] = key

    if not os.environ.get("DASHSCOPE_API_KEY"):
        raise RuntimeError("DASHSCOPE_API_KEY not set. Set env var or pass key=...")

def patch_runtime_paths(runtime_name: str = "runtime", verbose: bool = True):
    """
    Patch vendor config paths to use <project_root>/<runtime_name>/...
    WITHOUT editing vendor source files.
    Call this BEFORE creating RagService / KnowledgeBaseService.
    """
    setup_vendor_path(verbose=False)
    import config_data as config

    root = project_root()
    runtime = root / runtime_name
    runtime.mkdir(parents=True, exist_ok=True)

    # Store generated data under your project
    config.persist_directory = str(runtime / "chroma_db")
    config.chat_history_path = str(runtime / "chat_history")
    config.md5_path = str(runtime / "md5.text")

    if verbose:
        print("✅ runtime:", runtime)
        print("✅ persist_directory:", config.persist_directory)
        print("✅ chat_history_path:", config.chat_history_path)
        print("✅ md5_path:", config.md5_path)

    return config, runtime