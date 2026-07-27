# 실행 방법

프로젝트 루트(`08_nlp`)에서 아래 명령을 실행합니다.

## 1. 최초 한 번: Miniforge 가상환경 생성

```bash
conda create --prefix ./.conda python=3.11 -y
```

이미 `./.conda`를 Python 3.12 등 다른 버전으로 생성했다면, 먼저 환경을 삭제한 뒤 다시 만듭니다.

```bash
conda deactivate
conda env remove --prefix ./.conda
conda create --prefix ./.conda python=3.11 -y
```

## 2. 작업할 때: 가상환경 활성화 및 패키지 설치

터미널을 새로 열 때마다 실행합니다.

```bash
conda activate ./.conda
python --version  # Intel Mac에서는 반드시 Python 3.11.x인지 확인
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements.txt`는 현재 장비를 자동 감지해 패키지를 분기합니다.

| 장비 | 적용 제약 |
| --- | --- |
| Intel Mac (`x86_64`) | **Python 3.11 권장** (3.12도 가능), `tensorflow==2.16.2`, `numpy<2`, `scipy<1.17`, `transformers==4.50.0`, `torch==2.2.2` |
| Apple Silicon Mac (`arm64`) | 기본 최신 호환 범위 |

Intel Mac에서는 Miniforge `base` 환경(Python 3.13)을 사용하면 TensorFlow를 설치할 수 없습니다. 반드시 위의 `./.conda` 환경을 활성화한 뒤 설치하세요.

`konlpy`를 사용하는 한국어 형태소 분석 노트북은 Java가 필요합니다. macOS에서는 필요할 때 아래 명령으로 설치할 수 있습니다.

```bash
brew install openjdk
```

## 3. 데이터 준비 및 환경 점검

```bash
python main.py --download-nltk
python -m spacy download en_core_web_sm
python main.py --check
python main.py --print-platform
```

## 4. JupyterLab 실행

```bash
python main.py --lab
```

노트북 목록만 확인하려면 다음 명령을 사용합니다.

```bash
python main.py --list-notebooks
```

## 5. 작업 종료

```bash
conda deactivate
```
