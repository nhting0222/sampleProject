# 🏡 실버 쉐어 하우스 웹사이트

Vue 3 + Vite로 구축된 실버 쉐어 하우스 소개 웹사이트입니다.

## ✨ 주요 기능

- **메인 페이지**: 서비스 소개 및 주요 특징 안내
- **하우스 목록**: 다양한 실버 쉐어 하우스 둘러보기
- **하우스 상세**: 각 하우스의 상세 정보 및 제공 서비스 안내
- **문의/예약 폼**: 입주 문의 및 상담 신청
- **반응형 디자인**: 모바일, 태블릿, 데스크탑 모든 기기 지원

## 🛠️ 기술 스택

- **Vue 3**: Composition API 사용
- **Vue Router 4**: 페이지 라우팅
- **Vite**: 빠른 개발 서버 및 빌드 도구

## 📦 설치 및 실행

### 개발 모드 실행
```bash
cd silver-share-house
npm install
npm run dev
```

개발 서버가 `http://localhost:5173/` 에서 실행됩니다.

### 프로덕션 빌드
```bash
npm run build
```

빌드된 파일은 `dist` 폴더에 생성됩니다.

### 프리뷰
```bash
npm run preview
```

## 📂 프로젝트 구조

```
silver-share-house/
├── src/
│   ├── components/         # 재사용 가능한 컴포넌트
│   │   ├── Header.vue      # 헤더 (네비게이션)
│   │   ├── Footer.vue      # 푸터
│   │   └── HouseCard.vue   # 하우스 카드 컴포넌트
│   ├── views/              # 페이지 컴포넌트
│   │   ├── Home.vue        # 메인 페이지
│   │   ├── HouseList.vue   # 하우스 목록
│   │   ├── HouseDetail.vue # 하우스 상세
│   │   └── Contact.vue     # 문의 페이지
│   ├── router/             # 라우터 설정
│   │   └── index.js        # 라우트 정의
│   ├── data/               # 데이터
│   │   └── houses.js       # 하우스 더미 데이터
│   ├── App.vue             # 메인 앱 컴포넌트
│   ├── main.js             # 앱 진입점
│   └── style.css           # 글로벌 스타일
└── package.json
```

## 🎨 페이지 구성

1. **홈 (/)**: 서비스 소개 및 특징
2. **하우스 목록 (/houses)**: 전체 하우스 목록
3. **하우스 상세 (/house/:id)**: 개별 하우스 상세 정보
4. **문의하기 (/contact)**: 입주 문의 폼

## 🔧 커스터마이징

### 하우스 데이터 수정
`src/data/houses.js` 파일에서 하우스 정보를 추가/수정할 수 있습니다.

### 스타일 변경
각 컴포넌트의 `<style scoped>` 섹션에서 개별 스타일을 수정하거나,
`src/style.css`에서 글로벌 스타일을 변경할 수 있습니다.

## 📝 라이선스

MIT
