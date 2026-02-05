/**
 * Standard error handling utilities for XDR Management
 */

// Error codes mapping to user-friendly messages
const ERROR_MESSAGES = {
  // Authentication errors
  UNAUTHORIZED: '인증이 필요합니다. 다시 로그인해주세요.',
  FORBIDDEN: '이 작업을 수행할 권한이 없습니다.',
  INVALID_CREDENTIALS: '아이디 또는 비밀번호가 올바르지 않습니다.',

  // Resource errors
  EVENT_NOT_FOUND: '이벤트를 찾을 수 없습니다.',
  INCIDENT_NOT_FOUND: '인시던트를 찾을 수 없습니다.',
  ASSET_NOT_FOUND: '자산을 찾을 수 없습니다.',
  ALERT_RULE_NOT_FOUND: '알림 규칙을 찾을 수 없습니다.',
  USER_NOT_FOUND: '사용자를 찾을 수 없습니다.',

  // Validation errors
  VALIDATION_ERROR: '입력값이 올바르지 않습니다.',

  // Server errors
  INTERNAL_SERVER_ERROR: '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
  NETWORK_ERROR: '네트워크 연결을 확인해주세요.',

  // Default
  UNKNOWN_ERROR: '알 수 없는 오류가 발생했습니다.'
}

/**
 * Parse API error response
 * @param {Error} error - Axios error object
 * @returns {Object} Parsed error object
 */
export function parseApiError(error) {
  if (!error.response) {
    return {
      code: 'NETWORK_ERROR',
      message: ERROR_MESSAGES.NETWORK_ERROR,
      details: null,
      status: 0
    }
  }

  const { status, data } = error.response

  // Handle standard error response format
  if (data?.error) {
    return {
      code: data.error.code || 'UNKNOWN_ERROR',
      message: ERROR_MESSAGES[data.error.code] || data.error.message || ERROR_MESSAGES.UNKNOWN_ERROR,
      details: data.error.details,
      status
    }
  }

  // Handle FastAPI validation errors
  if (data?.detail && Array.isArray(data.detail)) {
    const messages = data.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join(', ')
    return {
      code: 'VALIDATION_ERROR',
      message: messages,
      details: data.detail,
      status
    }
  }

  // Handle simple detail message
  if (data?.detail) {
    return {
      code: 'HTTP_ERROR',
      message: data.detail,
      details: null,
      status
    }
  }

  // Fallback
  return {
    code: 'UNKNOWN_ERROR',
    message: ERROR_MESSAGES.UNKNOWN_ERROR,
    details: null,
    status
  }
}

/**
 * Get user-friendly error message
 * @param {Error} error - Axios error object
 * @returns {string} User-friendly error message
 */
export function getErrorMessage(error) {
  const parsed = parseApiError(error)
  return parsed.message
}

/**
 * Check if error is authentication related
 * @param {Error} error - Axios error object
 * @returns {boolean}
 */
export function isAuthError(error) {
  return error.response?.status === 401
}

/**
 * Check if error is permission related
 * @param {Error} error - Axios error object
 * @returns {boolean}
 */
export function isPermissionError(error) {
  return error.response?.status === 403
}

/**
 * Check if error is not found
 * @param {Error} error - Axios error object
 * @returns {boolean}
 */
export function isNotFoundError(error) {
  return error.response?.status === 404
}

/**
 * Check if error is validation related
 * @param {Error} error - Axios error object
 * @returns {boolean}
 */
export function isValidationError(error) {
  return error.response?.status === 422
}

/**
 * Check if error is server error
 * @param {Error} error - Axios error object
 * @returns {boolean}
 */
export function isServerError(error) {
  return error.response?.status >= 500
}

/**
 * Check if error is network error
 * @param {Error} error - Axios error object
 * @returns {boolean}
 */
export function isNetworkError(error) {
  return !error.response
}

export default {
  parseApiError,
  getErrorMessage,
  isAuthError,
  isPermissionError,
  isNotFoundError,
  isValidationError,
  isServerError,
  isNetworkError,
  ERROR_MESSAGES
}
