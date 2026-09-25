from pathlib import Path


def ensure_repo_layout():
    folders = [
        Path("backend/uploads"),
        Path("backend/results"),
        Path("backend/logs"),
        Path("backend/database"),
        Path("ml/weights"),
        Path("dataset/raw"),
        Path("dataset/processed"),
        Path("dataset/annotations"),
        Path("docs"),
        Path("tests/backend"),
        Path("tests/ml"),
        Path("tests/frontend"),
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    ensure_repo_layout()
    print("Repository layout ensured.")
