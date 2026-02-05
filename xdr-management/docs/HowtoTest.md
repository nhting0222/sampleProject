# XDR Management Platform - 테스트 가이드

## 개요

이 문서는 XDR Management Platform의 개선 사항, 추가된 파일, 실행 방법 및 테스트 계정 정보를 포함합니다.

---

## 완료된 개선 사항

| # | 작업 | 설명 |
|---|------|------|
| 1 | **인증/권한 시스템** | JWT 기반 인증, RBAC (Admin/Analyst/Viewer) 역할 기반 접근 제어 |
| 2 | **데이터베이스** | SQLite + SQLAlchemy ORM, 감사 로그 테이블 추가 |
| 3 | **테스트 코드** | Backend: pytest, Frontend: vitest |
| 4 | **에러 처리** | 표준화된 에러 응답 형식, Toast 알림 시스템 |
| 5 | **TypeScript** | 타입 정의 파일, API 클라이언트 TypeScript 전환 |
| 6 | **스토어 분리** | 도메인별 Pinia 스토어 분리 (events, incidents, assets, alerts, dashboard) |
| 7 | **모니터링** | 구조화된 JSON 로깅, 메트릭 수집, 헬스체크 엔드포인트 |

---

## 추가된 파일 목록

### Backend

```
backend/
├── app/
│   ├── core/
│   │   ├── __init__.py         # Core 모듈 초기화
│   │   ├── config.py           # 환경 설정 관리 (Settings)
│   │   ├── security.py         # JWT 인증, 비밀번호 해싱, RBAC
│   │   ├── database.py         # SQLAlchemy 데이터베이스 설정
│   │   ├── exceptions.py       # 표준화된 예외 클래스
│   │   ├── logging.py          # 구조화 로깅, 메트릭 수집기
│   │   └── init_data.py        # 데이터베이스 시드 데이터
│   │
│   ├── middleware/
│   │   ├── __init__.py         # Middleware 모듈 초기화
│   │   └── logging.py          # 요청 로깅 미들웨어
│   │
│   ├── routes/
│   │   ├── __init__.py         # Routes 모듈 초기화
│   │   ├── auth.py             # 인증 API (login, register, me, refresh)
│   │   └── monitoring.py       # 모니터링 API (health, metrics)
│   │
│   ├── db_models.py            # SQLAlchemy ORM 모델 정의
│   │
│   └── tests/
│       ├── __init__.py         # Tests 모듈 초기화
│       ├── conftest.py         # pytest 설정 및 fixtures
│       ├── test_auth.py        # 인증 API 테스트
│       ├── test_events.py      # 이벤트 API 테스트
│       ├── test_incidents.py   # 인시던트 API 테스트
│       └── test_dashboard.py   # 대시보드, 자산, 알림 API 테스트
│
├── requirements.txt            # Python 패키지 의존성 (업데이트됨)
└── xdr_management.db           # SQLite 데이터베이스 파일 (자동 생성)
```

### Frontend

```
src/
├── types/
│   └── index.ts               # TypeScript 타입 정의 (모든 인터페이스)
│
├── stores/
│   ├── index.ts               # 스토어 통합 export
│   ├── auth.ts                # 인증 상태 관리
│   ├── auth.js                # 인증 상태 관리 (JS 버전)
│   ├── events.ts              # 이벤트 상태 관리
│   ├── incidents.ts           # 인시던트 상태 관리
│   ├── assets.ts              # 자산 상태 관리
│   ├── alerts.ts              # 알림 규칙 상태 관리
│   ├── dashboard.ts           # 대시보드 상태 관리
│   └── toast.js               # Toast 알림 상태 관리
│
├── utils/
│   ├── api.ts                 # TypeScript API 클라이언트
│   ├── api.js                 # JavaScript API 클라이언트 (업데이트됨)
│   └── errorHandler.js        # 에러 처리 유틸리티
│
├── views/
│   └── Login.vue              # 로그인 페이지 컴포넌트
│
├── components/
│   ├── Header.vue             # 헤더 컴포넌트 (업데이트됨 - 사용자 메뉴 추가)
│   └── ToastContainer.vue     # Toast 알림 컨테이너
│
├── router/
│   └── index.js               # 라우터 설정 (업데이트됨 - 인증 가드 추가)
│
├── tests/
│   ├── setup.js               # Vitest 설정
│   ├── auth.test.js           # Auth 스토어 테스트
│   └── components.test.js     # 컴포넌트 테스트
│
├── App.vue                    # 루트 컴포넌트 (업데이트됨)
├── vite-env.d.ts              # Vite 타입 선언
│
├── tsconfig.json              # TypeScript 설정
├── tsconfig.node.json         # Node TypeScript 설정
├── vitest.config.js           # Vitest 설정
└── package.json               # npm 패키지 (업데이트됨)
```

---

## 실행 방법

### 사전 요구사항

- **Python 3.9+**
- **Node.js 18+**
- **npm 또는 yarn**

### Backend 실행

```bash
# 1. backend 디렉토리로 이동
cd xdr-management/backend

# 2. 가상환경 생성 (권장)
python -m venv venv

# 3. 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. 의존성 설치
pip install -r requirements.txt

# 5. 서버 실행
python main.py
```

Backend 서버가 `http://localhost:8000`에서 실행됩니다.

- **API 문서**: http://localhost:8000/docs (Swagger UI)
- **헬스체크**: http://localhost:8000/api/monitoring/health

### Frontend 실행

```bash
# 1. xdr-management 디렉토리로 이동
cd xdr-management

# 2. 의존성 설치
npm install

# 3. 개발 서버 실행
npm run dev
```

Frontend 서버가 `http://localhost:5175`에서 실행됩니다.

---

## 테스트 실행

### Backend 테스트 (pytest)

```bash
cd xdr-management/backend

# 모든 테스트 실행
pytest

# 상세 출력
pytest -v

# 특정 테스트 파일 실행
pytest tests/test_auth.py

# 커버리지 포함
pytest --cov=app
```

### Frontend 테스트 (vitest)

```bash
cd xdr-management

# 테스트 실행
npm run test

# UI 모드로 테스트
npm run test:ui

# 커버리지 포함
npm run test:coverage

# 타입 체크
npm run type-check
```

---

## 테스트 계정

| 역할 | 사용자명 | 비밀번호 | 권한 |
|------|----------|----------|------|
| **Admin** | `admin` | `admin123` | 모든 기능 접근 가능 |
| **Analyst** | `analyst` | `analyst123` | 조회, 생성, 수정 가능 (삭제 불가) |
| **Viewer** | `viewer` | `viewer123` | 조회만 가능 |

### 역할별 권한 상세

| 기능 | Admin | Analyst | Viewer |
|------|:-----:|:-------:|:------:|
| 이벤트 조회 | O | O | O |
| 이벤트 생성/수정 | O | O | X |
| 이벤트 삭제 | O | X | X |
| 인시던트 조회 | O | O | O |
| 인시던트 생성/수정 | O | O | X |
| 자산 조회 | O | O | O |
| 알림 규칙 조회 | O | O | O |
| 알림 규칙 수정 | O | X | X |
| 메트릭 조회 | O | X | X |

---

## API 엔드포인트

### 인증 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/auth/login` | 로그인 (form-data) |
| POST | `/api/auth/login/json` | 로그인 (JSON) |
| GET | `/api/auth/me` | 현재 사용자 정보 |
| POST | `/api/auth/refresh` | 토큰 갱신 |
| POST | `/api/auth/register` | 사용자 등록 |

### 모니터링 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/monitoring/health` | 헬스체크 |
| GET | `/api/monitoring/metrics` | 메트릭 조회 (Admin) |
| POST | `/api/monitoring/metrics/reset` | 메트릭 리셋 (Admin) |
| GET | `/api/monitoring/ready` | Readiness 체크 |
| GET | `/api/monitoring/live` | Liveness 체크 |

### 기존 API (인증 필요)

| Method | Endpoint | 설명 | 권한 |
|--------|----------|------|------|
| GET | `/api/events` | 이벤트 목록 | Viewer+ |
| POST | `/api/events` | 이벤트 생성 | Analyst+ |
| DELETE | `/api/events/{id}` | 이벤트 삭제 | Admin |
| GET | `/api/incidents` | 인시던트 목록 | Viewer+ |
| GET | `/api/assets` | 자산 목록 | Viewer+ |
| GET | `/api/alerts` | 알림 규칙 목록 | Viewer+ |
| PUT | `/api/alerts/{id}` | 알림 규칙 수정 | Admin |
| GET | `/api/dashboard/stats` | 대시보드 통계 | Viewer+ |

---

## 문제 해결

### Backend 관련

**1. 모듈을 찾을 수 없음**
```bash
# PYTHONPATH 설정
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# 또는 backend 폴더에서 실행
cd backend && python main.py
```

**2. 데이터베이스 초기화**
```bash
# xdr_management.db 파일 삭제 후 재시작
rm xdr_management.db
python main.py
```

### Frontend 관련

**1. 타입 에러**
```bash
# TypeScript 설정 확인
npm run type-check
```

**2. 로그인 후 리다이렉트 안됨**
- 브라우저 localStorage 확인
- `xdr_token`, `xdr_user` 키 존재 여부 확인

---

## 추가 정보

- **Backend 포트**: 8000
- **Frontend 포트**: 5175
- **WebSocket**: `ws://localhost:8000/ws`
- **데이터베이스**: SQLite (`xdr_management.db`)

---

*문서 작성일: 2026-02-05*
