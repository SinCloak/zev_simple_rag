import request from '@/api'
import type { Session, SessionDetail } from '@/types'

export interface CreateSessionRequest {
  title: string
}

export interface UpdateSessionRequest {
  title?: string
  is_active?: boolean
}

export const sessionsApi = {
  /**
   * Create a new chat session
   */
  create(data: CreateSessionRequest): Promise<Session> {
    return request.post('/v1/sessions', data)
  },

  /**
   * List all active sessions
   */
  list(): Promise<Session[]> {
    return request.get('/v1/sessions')
  },

  /**
   * Get a session by ID with messages
   */
  get(sessionId: string): Promise<SessionDetail> {
    return request.get(`/v1/sessions/${sessionId}`)
  },

  /**
   * Update a session
   */
  update(sessionId: string, data: UpdateSessionRequest): Promise<Session> {
    return request.put(`/v1/sessions/${sessionId}`, data)
  },

  /**
   * Delete (deactivate) a session
   */
  delete(sessionId: string): Promise<void> {
    return request.delete(`/v1/sessions/${sessionId}`)
  },
}
