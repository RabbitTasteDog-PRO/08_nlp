# 프로젝트 로컬 Conda 환경

이 폴더의 `nlp_env/`는 각 컴퓨터에서 생성하는 로컬 Conda 가상환경입니다.
Git에는 올리지 않고, `environment.yml`만 공유합니다.

## 최초 한 번: 환경 만들기

프로젝트 루트에서 실행합니다.

```bash
conda env create --prefix ./environment/nlp_env --file ./environment/environment.yml
```

## 작업할 때: 환경 활성화 및 실행

```bash
conda activate ./environment/nlp_env
python main.py
```

## 패키지를 추가했다면

```bash
conda activate ./environment/nlp_env
conda install 패키지이름
conda env export --from-history --prefix ./environment/nlp_env > ./environment/environment.yml
```

`pip install`로 설치한 패키지는 별도로 `requirements.txt`에 기록합니다.
