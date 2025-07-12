from d9core.engine.file_manager import ensure_user_docs
from d9core.ui.terminal import run_terminal

def main():
    print("Ensuring User Docs")
    ensure_user_docs()
    print("Done")
    run_terminal()

if __name__ == "__main__":
    main()