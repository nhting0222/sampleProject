<template>
  <div class="contact">
    <div class="page-header">
      <h1>입주 문의</h1>
      <p>궁금하신 점이 있으시면 언제든지 문의해주세요</p>
    </div>

    <div class="container">
      <div class="contact-content">
        <div class="contact-form-wrapper">
          <form @submit.prevent="onSubmit" class="contact-form" v-if="!submitted">
            <div class="form-group" :class="{ error: touched.name && errors.name }">
              <label for="name">이름 *</label>
              <input
                type="text"
                id="name"
                :value="values.name"
                @input="handleChange('name', $event.target.value)"
                @blur="handleBlur('name')"
                placeholder="이름을 입력해주세요"
              />
              <span v-if="touched.name && errors.name" class="error-message">
                {{ errors.name }}
              </span>
            </div>

            <div class="form-group" :class="{ error: touched.phone && errors.phone }">
              <label for="phone">연락처 *</label>
              <input
                type="tel"
                id="phone"
                :value="values.phone"
                @input="handleChange('phone', $event.target.value)"
                @blur="handleBlur('phone')"
                placeholder="010-1234-5678"
              />
              <span v-if="touched.phone && errors.phone" class="error-message">
                {{ errors.phone }}
              </span>
            </div>

            <div class="form-group" :class="{ error: touched.email && errors.email }">
              <label for="email">이메일</label>
              <input
                type="email"
                id="email"
                :value="values.email"
                @input="handleChange('email', $event.target.value)"
                @blur="handleBlur('email')"
                placeholder="example@email.com"
              />
              <span v-if="touched.email && errors.email" class="error-message">
                {{ errors.email }}
              </span>
            </div>

            <div class="form-group">
              <label for="house">관심 하우스</label>
              <select
                id="house"
                :value="values.selectedHouse"
                @change="handleChange('selectedHouse', $event.target.value)"
              >
                <option value="">선택해주세요</option>
                <option v-for="house in houses" :key="house.id" :value="house.name">
                  {{ house.name }} - {{ house.location }}
                </option>
              </select>
            </div>

            <div class="form-group" :class="{ error: touched.message && errors.message }">
              <label for="message">문의 내용 *</label>
              <textarea
                id="message"
                :value="values.message"
                @input="handleChange('message', $event.target.value)"
                @blur="handleBlur('message')"
                rows="6"
                placeholder="문의하실 내용을 자세히 작성해주세요"
              ></textarea>
              <span v-if="touched.message && errors.message" class="error-message">
                {{ errors.message }}
              </span>
            </div>

            <button
              type="submit"
              class="btn-submit"
              :disabled="isSubmitting || !isValid"
            >
              {{ isSubmitting ? '전송 중...' : '문의하기' }}
            </button>
          </form>

          <div v-if="submitted" class="success-message">
            <div class="success-icon">✅</div>
            <h3>문의가 접수되었습니다!</h3>
            <p>빠른 시일 내에 연락드리겠습니다.</p>
          </div>
        </div>

        <div class="contact-info-card">
          <h2>연락처 안내</h2>

          <div class="info-item">
            <div class="info-icon">📞</div>
            <div>
              <h4>전화 문의</h4>
              <p>1588-1234</p>
            </div>
          </div>

          <div class="info-item">
            <div class="info-icon">📧</div>
            <div>
              <h4>이메일</h4>
              <p>contact@silvershare.com</p>
            </div>
          </div>

          <div class="info-item">
            <div class="info-icon">⏰</div>
            <div>
              <h4>상담 시간</h4>
              <p>평일 09:00 - 18:00</p>
              <p>주말 및 공휴일 휴무</p>
            </div>
          </div>

          <div class="info-item">
            <div class="info-icon">📍</div>
            <div>
              <h4>본사 주소</h4>
              <p>서울시 강남구 테헤란로 123</p>
              <p>실버쉐어빌딩 5층</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { houses } from '../data/houses'
import { useForm } from '../composables/useForm'
import { useToast } from '../composables/useToast'

const submitted = ref(false)
const toast = useToast()

// Form validation rules
const validationRules = {
  name: ['required', { minLength: 2 }],
  phone: ['required', 'phone'],
  email: ['email'],
  message: ['required', { minLength: 10 }]
}

const {
  values,
  errors,
  touched,
  isSubmitting,
  isValid,
  handleChange,
  handleBlur,
  handleSubmit,
  reset
} = useForm(
  {
    name: '',
    phone: '',
    email: '',
    selectedHouse: '',
    message: ''
  },
  validationRules
)

const onSubmit = async () => {
  const success = await handleSubmit(async (formData) => {
    console.log('Form submitted:', formData)

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Show success state
    submitted.value = true
    toast.success('문의가 성공적으로 접수되었습니다!', 3000)

    // Reset form after 3 seconds
    setTimeout(() => {
      submitted.value = false
      reset()
    }, 3000)
  })

  if (!success) {
    toast.error('입력 내용을 확인해주세요', 2000)
  }
}
</script>

<style scoped>
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
}

.page-header h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.page-header p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
}

.contact-content {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 3rem;
}

.contact-form-wrapper {
  position: relative;
}

.contact-form {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
}

.form-group textarea {
  resize: vertical;
  font-family: inherit;
}

.form-group.error input,
.form-group.error select,
.form-group.error textarea {
  border-color: #ef4444;
}

.error-message {
  display: block;
  color: #ef4444;
  font-size: 0.85rem;
  margin-top: 0.5rem;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.btn-submit {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.success-message {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: white;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.success-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.success-message h3 {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.success-message p {
  color: #666;
  font-size: 1.1rem;
}

.contact-info-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  height: fit-content;
  position: sticky;
  top: 20px;
}

.contact-info-card h2 {
  font-size: 1.8rem;
  margin-bottom: 2rem;
  color: #333;
}

.info-item {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e9ecef;
}

.info-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.info-icon {
  font-size: 2rem;
  min-width: 50px;
}

.info-item h4 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.info-item p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

@media (max-width: 768px) {
  .contact-content {
    grid-template-columns: 1fr;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .contact-info-card {
    position: static;
  }
}
</style>
