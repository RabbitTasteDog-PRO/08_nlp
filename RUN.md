# 실행 방법

프로젝트 루트(`08_nlp`)에서 아래 명령을 실행합니다.

## 1. 최초 한 번: 가상환경 생성

```bash
conda env create --prefix ./environment/nlp_env --file ./environment/environment.yml
```

## 2. 작업할 때: 가상환경 활성화

터미널을 새로 열 때마다 실행합니다.

```bash
conda activate ./environment/nlp_env
```

## 3. 프로그램 실행

```bash
python main.py
```

## 4. 작업 종료

```bash
conda deactivate
```

## 패키지 추가 후 환경 설정 저장

Conda 패키지를 설치한 뒤에는 다른 컴퓨터에서도 동일하게 만들 수 있도록 설정 파일을 갱신합니다.

```bash
conda env export --from-history --prefix ./environment/nlp_env > ./environment/environment.yml
```

`pip install`로 설치한 패키지는 `requirements.txt`에도 기록합니다.
