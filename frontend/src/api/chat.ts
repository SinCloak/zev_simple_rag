import request from '@/api'
import type { ChatRequest, ChatResponse, StreamEvent } from '@/types'

export const chatApi = {
  /**
   * Send a chat message (non-streaming)
   */
  send(data: ChatRequest): Promise<ChatResponse> {
    return request.post('/v1/chat', data)
  },

  /**
   * Send a chat message with streaming response
   */
  async *stream(data: ChatRequest): AsyncGenerator<StreamEvent, void, unknown> {
    const response = await fetch('/api/v1/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })

    if (!response.ok) {
      throw new Error(`Stream request failed: ${response.status}`)
    }

    const reader = response.body?.getReader()
    if (!reader) {
      throw new Error('No response body')
    }

    const decoder = new TextDecoder()
    let buffer = ''

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            try {
              const event = JSON.parse(data) as StreamEvent
              yield event
              if (event.event_type === 'done' || event.event_type === 'error') {
                return
              }
            } catch (e) {
              console.error('Failed to parse stream event:', e)
            }
          }
        }
      }
    } finally {
      reader.releaseLock()
    }
  },

  /**
   * Trigger document ingestion
   */
  ingest(): Promise<{ message: string; documents_ingested: number }> {
    return request.post('/v1/chat/ingest')
  },
}
