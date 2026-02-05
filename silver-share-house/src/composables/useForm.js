import { ref, computed } from 'vue'

export function useForm(initialValues = {}, validationRules = {}) {
  const values = ref({ ...initialValues })
  const errors = ref({})
  const touched = ref({})
  const isSubmitting = ref(false)

  // Validation rules
  const validators = {
    required: (value) => {
      if (!value || (typeof value === 'string' && !value.trim())) {
        return '필수 입력 항목입니다'
      }
      return null
    },
    email: (value) => {
      if (!value) return null
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(value)) {
        return '올바른 이메일 형식이 아닙니다'
      }
      return null
    },
    phone: (value) => {
      if (!value) return null
      const phoneRegex = /^01[0-9]-?[0-9]{3,4}-?[0-9]{4}$/
      if (!phoneRegex.test(value.replace(/-/g, ''))) {
        return '올바른 전화번호 형식이 아닙니다 (예: 010-1234-5678)'
      }
      return null
    },
    minLength: (min) => (value) => {
      if (!value) return null
      if (value.length < min) {
        return `최소 ${min}자 이상 입력해주세요`
      }
      return null
    },
    maxLength: (max) => (value) => {
      if (!value) return null
      if (value.length > max) {
        return `최대 ${max}자까지 입력 가능합니다`
      }
      return null
    }
  }

  // Validate a single field
  const validateField = (fieldName) => {
    const rules = validationRules[fieldName]
    if (!rules) return

    const value = values.value[fieldName]
    let error = null

    for (const rule of rules) {
      if (typeof rule === 'string') {
        // Built-in validator
        error = validators[rule]?.(value)
      } else if (typeof rule === 'function') {
        // Custom validator
        error = rule(value, values.value)
      } else if (typeof rule === 'object') {
        // Validator with params (e.g., { minLength: 5 })
        const [validatorName, param] = Object.entries(rule)[0]
        error = validators[validatorName]?.(param)?.(value)
      }

      if (error) {
        errors.value[fieldName] = error
        return error
      }
    }

    errors.value[fieldName] = null
    return null
  }

  // Validate all fields
  const validateAll = () => {
    let isValid = true
    Object.keys(validationRules).forEach(fieldName => {
      const error = validateField(fieldName)
      if (error) isValid = false
    })
    return isValid
  }

  // Handle field change
  const handleChange = (fieldName, value) => {
    values.value[fieldName] = value
    if (touched.value[fieldName]) {
      validateField(fieldName)
    }
  }

  // Handle field blur
  const handleBlur = (fieldName) => {
    touched.value[fieldName] = true
    validateField(fieldName)
  }

  // Reset form
  const reset = () => {
    values.value = { ...initialValues }
    errors.value = {}
    touched.value = {}
    isSubmitting.value = false
  }

  // Submit handler
  const handleSubmit = async (onSubmit) => {
    // Mark all fields as touched
    Object.keys(validationRules).forEach(field => {
      touched.value[field] = true
    })

    if (!validateAll()) {
      return false
    }

    isSubmitting.value = true
    try {
      await onSubmit(values.value)
      return true
    } catch (error) {
      console.error('Form submission error:', error)
      return false
    } finally {
      isSubmitting.value = false
    }
  }

  // Computed
  const isValid = computed(() => {
    return Object.values(errors.value).every(error => !error)
  })

  const hasErrors = computed(() => {
    return Object.values(errors.value).some(error => error)
  })

  return {
    values,
    errors,
    touched,
    isSubmitting,
    isValid,
    hasErrors,
    handleChange,
    handleBlur,
    validateField,
    validateAll,
    handleSubmit,
    reset
  }
}
