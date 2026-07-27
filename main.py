"""08_nlp 학습 노트북 환경을 점검하고 JupyterLab을 실행한다."""

from __future__ import annotations

import argparse
import importlib.util
import platform
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent

# 모듈명: requirements.txt의 배포 패키지명
BASE_REQUIRED_MODULES = {
    "gdown": "gdown",
    "ipykernel": "ipykernel",
    "jupyterlab": "jupyterlab",
    "kss": "kss",
    "konlpy": "konlpy",
    "mecab_ko_dic": "mecab-ko-dic",
    "matplotlib": "matplotlib",
    "networkx": "networkx",
    "nltk": "nltk",
    "pandas": "pandas",
    "sklearn": "scikit-learn",
    "spacy": "spacy",
    "tensorflow": "tensorflow",
    "wordcloud": "wordcloud",
}

NLTK_RESOURCES = {
    "punkt": "tokenizers/punkt",
    "punkt_tab": "tokenizers/punkt_tab",
    "stopwords": "corpora/stopwords",
    "wordnet": "corpora/wordnet",
    "averaged_perceptron_tagger_eng": "taggers/averaged_perceptron_tagger_eng",
    "vader_lexicon": "sentiment/vader_lexicon.zip",
}


def platform_profile() -> tuple[str, bool]:
    """현재 장비에 적용되는 requirements.txt 호환 프로필을 반환한다."""
    is_intel_macos = sys.platform == "darwin" and platform.machine().lower() == "x86_64"
    if is_intel_macos:
        return "macOS Intel", True
    if sys.platform == "darwin" and platform.machine().lower() == "arm64":
        return "macOS Apple Silicon", False
    return f"{platform.system()} {platform.machine()}", False


def required_modules() -> dict[str, str]:
    """현재 플랫폼에 필요한 직접 의존성 모듈을 반환한다."""
    modules = dict(BASE_REQUIRED_MODULES)
    _, is_intel_macos = platform_profile()
    if is_intel_macos:
        modules.update(
            {
                "numpy": "numpy (<2)",
                "scipy": "scipy (<1.17)",
                "torch": "torch (==2.2.2)",
                "transformers": "transformers (==4.50.0)",
            }
        )
    else:
        modules.update(
            {
                "numpy": "numpy",
                "torch": "torch",
                "transformers": "transformers",
            }
        )
    return modules


def python_version_supported() -> bool:
    """Intel Mac의 TensorFlow·PyTorch 공통 지원 Python 버전을 확인한다."""
    _, is_intel_macos = platform_profile()
    if not is_intel_macos:
        return True
    return (3, 11) <= sys.version_info[:2] <= (3, 12)


def missing_packages() -> list[str]:
    """설치되지 않은 직접 의존성을 반환한다. import는 실행하지 않는다."""
    return [
        package
        for module, package in required_modules().items()
        if importlib.util.find_spec(module) is None
    ]


def missing_nltk_resources() -> list[str]:
    try:
        import nltk
    except ModuleNotFoundError:
        return list(NLTK_RESOURCES)

    missing = []
    for name, resource_path in NLTK_RESOURCES.items():
        try:
            nltk.data.find(resource_path)
        except LookupError:
            missing.append(name)
    return missing


def download_nltk_resources() -> None:
    import nltk

    for resource in missing_nltk_resources():
        print(f"NLTK 데이터 다운로드: {resource}")
        nltk.download(resource, quiet=False)


def list_notebooks() -> None:
    notebooks = sorted(ROOT.rglob("*.ipynb"))
    if not notebooks:
        print("노트북을 찾지 못했습니다.")
        return

    print("학습 노트북:")
    for notebook in notebooks:
        print(f"- {notebook.relative_to(ROOT)}")


def check_environment() -> bool:
    print(f"Python: {sys.executable}")
    print(f"Version: {sys.version.split()[0]}")
    profile, is_intel_macos = platform_profile()
    print(f"Platform: {profile}")
    if is_intel_macos:
        print(
            "Profile: Intel Mac "
            "(Python 3.11–3.12, tensorflow==2.16.2, numpy<2, scipy<1.17, "
            "transformers==4.50.0, torch==2.2.2)"
        )
    else:
        print("Profile: Apple Silicon/기본")

    if not python_version_supported():
        print("\nIntel Mac 프로필은 TensorFlow 2.16.2와 PyTorch 2.2.2를 함께 사용하므로 Python 3.11 또는 3.12가 필요합니다.")
        print("현재 Python을 사용하지 말고 프로젝트 환경을 만드세요:")
        print("conda create --prefix ./.conda python=3.11 -y")
        print("conda activate ./.conda")
        return False

    missing = missing_packages()
    if missing:
        print("\n미설치 패키지:")
        for package in missing:
            print(f"- {package}")
        print("\n설치 명령: python -m pip install -r requirements.txt")
        return False

    nltk_missing = missing_nltk_resources()
    if nltk_missing:
        print("\nNLTK 데이터가 일부 없습니다: " + ", ".join(nltk_missing))
        print("다운로드 명령: python main.py --download-nltk")

    if importlib.util.find_spec("en_core_web_sm") is None:
        print("\nspaCy 영어 모델이 없습니다.")
        print("설치 명령: python -m spacy download en_core_web_sm")

    print("\n패키지 점검을 완료했습니다.")
    return True


def start_jupyter_lab() -> int:
    if not check_environment():
        print("환경을 준비한 뒤 JupyterLab을 실행할 수 있습니다.", file=sys.stderr)
        return 1
    return subprocess.call([sys.executable, "-m", "jupyter", "lab"], cwd=ROOT)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Python, 패키지, NLTK 데이터를 점검합니다.")
    parser.add_argument("--download-nltk", action="store_true", help="노트북에 필요한 NLTK 데이터를 다운로드합니다.")
    parser.add_argument("--list-notebooks", action="store_true", help="프로젝트 노트북 목록을 표시합니다.")
    parser.add_argument("--print-platform", action="store_true", help="현재 장비에 적용되는 패키지 프로필을 표시합니다.")
    parser.add_argument("--lab", action="store_true", help="JupyterLab을 실행합니다.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.download_nltk:
        download_nltk_resources()
    if args.list_notebooks:
        list_notebooks()
    if args.print_platform:
        profile, is_intel_macos = platform_profile()
        print(f"Platform: {profile}")
        print("Profile: Intel Mac" if is_intel_macos else "Profile: Apple Silicon/기본")
    if args.lab:
        return start_jupyter_lab()

    # 옵션 없이 실행해도 현재 인터프리터가 올바른지 바로 알 수 있게 한다.
    if not any((args.check, args.download_nltk, args.list_notebooks, args.print_platform)):
        return 0 if check_environment() else 1
    if args.check:
        return 0 if check_environment() else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
