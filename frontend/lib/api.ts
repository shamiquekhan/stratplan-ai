import axios from 'axios'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

function formatApiError(detail: unknown, fallback: string): string {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail
      .map((item) => (typeof item === 'string' ? item : item?.msg || JSON.stringify(item)))
      .join('; ')
  }
  if (detail && typeof detail === 'object') return JSON.stringify(detail)
  return fallback
}

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = formatApiError(error.response?.data?.detail, error.message)
    return Promise.reject(new Error(message))
  }
)

export const plansApi = {
  list: (params?: { skip?: number; limit?: number; status?: string }) =>
    api.get('/plans', { params }),
  
  get: (id: number) =>
    api.get(`/plans/${id}`),
  
  create: (data: any) =>
    api.post('/plans', data),
  
  update: (id: number, data: any) =>
    api.patch(`/plans/${id}`, data),
  
  delete: (id: number) =>
    api.delete(`/plans/${id}`),
  
  generate: (id: number, userInputs: any) =>
    api.post(`/plans/${id}/generate`, { plan_id: id, user_inputs: userInputs }),
  
  export: (id: number, format: 'pdf' | 'docx' | 'xlsx', sections?: string[]) =>
    api.post(`/plans/${id}/export`, { plan_id: id, format, sections }, { responseType: 'blob' }),
  
  versions: (id: number) =>
    api.get(`/plans/${id}/versions`),
}

export const healthApi = {
  check: () => api.get('/health'),
}