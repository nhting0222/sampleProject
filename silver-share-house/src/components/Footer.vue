<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>🏡 실버쉐어하우스</h3>
          <p>행복한 노후, 함께하는 공간</p>
        </div>

        <div class="footer-section">
          <h4>바로가기</h4>
          <ul>
            <li><router-link to="/">홈</router-link></li>
            <li><router-link to="/houses">하우스 둘러보기</router-link></li>
            <li><router-link to="/contact">문의하기</router-link></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4>고객센터</h4>
          <ul>
            <li>📞 1588-1234</li>
            <li>📧 contact@silvershare.com</li>
            <li>⏰ 평일 09:00 - 18:00</li>
          </ul>
        </div>

        <div class="footer-section">
          <h4>본사</h4>
          <ul>
            <li>서울시 강남구 테헤란로 123</li>
            <li>실버쉐어빌딩 5층</li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2024 실버쉐어하우스. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #2d3748;
  color: white;
  padding: 3rem 0 1rem;
  margin-top: 4rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
}

.footer-section h4 {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: #a0aec0;
}

.footer-section p {
  color: #cbd5e0;
  line-height: 1.6;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section li {
  margin-bottom: 0.5rem;
  color: #cbd5e0;
  line-height: 1.6;
}

.footer-section a {
  color: #cbd5e0;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-section a:hover {
  color: white;
}

.footer-bottom {
  padding-top: 2rem;
  border-top: 1px solid #4a5568;
  text-align: center;
}

.footer-bottom p {
  color: #a0aec0;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
  }
}
</style>
