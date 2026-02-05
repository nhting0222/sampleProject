<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1>행복한 노후, 함께하는 공간</h1>
        <p>실버 쉐어하우스에서 따뜻한 공동체 생활을 시작하세요</p>
        <router-link to="/houses" class="btn-primary">하우스 둘러보기</router-link>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="container">
        <h2>왜 실버 쉐어하우스인가요?</h2>
        <div class="feature-grid">
          <div class="feature-card">
            <div class="icon">👥</div>
            <h3>함께하는 생활</h3>
            <p>혼자가 아닌 따뜻한 이웃과 함께하는 일상</p>
          </div>
          <div class="feature-card">
            <div class="icon">💰</div>
            <h3>합리적인 비용</h3>
            <p>경제적 부담을 줄이고 질 높은 생활 제공</p>
          </div>
          <div class="feature-card">
            <div class="icon">🏥</div>
            <h3>건강 관리</h3>
            <p>전문적인 건강 관리 및 의료 서비스</p>
          </div>
          <div class="feature-card">
            <div class="icon">🎨</div>
            <h3>다양한 프로그램</h3>
            <p>문화, 취미, 운동 등 풍성한 활동</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta">
      <div class="container">
        <h2>새로운 삶을 시작하세요</h2>
        <p>더 자세한 정보가 필요하신가요?</p>
        <router-link to="/contact" class="btn-secondary">문의하기</router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 120px 20px;
  text-align: center;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero-content p {
  font-size: 1.3rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.btn-primary {
  display: inline-block;
  padding: 15px 40px;
  background: white;
  color: #667eea;
  text-decoration: none;
  border-radius: 50px;
  font-weight: 600;
  transition: transform 0.3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
}

.features {
  padding: 80px 20px;
  background: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.features h2 {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  color: #333;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #667eea;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

.cta {
  padding: 80px 20px;
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  color: white;
  text-align: center;
}

.cta h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.cta p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.btn-secondary {
  display: inline-block;
  padding: 15px 40px;
  background: transparent;
  color: white;
  text-decoration: none;
  border: 2px solid white;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-secondary:hover {
  background: white;
  color: #667eea;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }

  .hero-content p {
    font-size: 1rem;
  }

  .features h2,
  .cta h2 {
    font-size: 2rem;
  }
}
</style>
