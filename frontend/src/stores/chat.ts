import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { sessionsApi, chatApi } from '@/api'
import type { Session, SessionDetail, Message, ChatRequest, TokenUsage, ReferenceDocument } from '@/types'

export const useChatStore = defineStore('chat', () => {
  // State
  const sessions = ref<Session[]>([])
  const currentSession = ref<SessionDetail | null>(null)
  const isLoading = ref(false)
  const isStreaming = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const currentSessionId = computed(() => currentSession.value?.id)
  const currentMessages = computed(() => currentSession.value?.messages || [])

  // Actions
  async function loadSessions() {
    isLoading.value = true
    error.value = null
    try {
      sessions.value = await sessionsApi.list()
    } catch (e) {
      error.value = 'Failed to load sessions'
      console.error('Failed to load sessions:', e)
    } finally {
      isLoading.value = false
    }
  }

  async function loadSession(sessionId: string) {
    isLoading.value = true
    error.value = null
    try {
      currentSession.value = await sessionsApi.get(sessionId)
      // Update the session in the list too
      const idx = sessions.value.findIndex(s => s.id === sessionId)
      if (idx >= 0) {
        sessions.value[idx] = { ...currentSession.value, message_count: currentSession.value.messages.length }
      }
    } catch (e) {
      error.value = 'Failed to load session'
      console.error('Failed to load session:', e)
    } finally {
      isLoading.value = false
    }
  }

  async function createSession(title?: string) {
    isLoading.value = true
    error.value = null
    try {
      const session = await sessionsApi.create({
        title: title || 'New Conversation',
      })
      sessions.value.unshift(session)
      currentSession.value = { ...session, messages: [] }
      return session
    } catch (e) {
      error.value = 'Failed to create session'
      console.error('Failed to create session:', e)
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function deleteSession(sessionId: string) {
    try {
      await sessionsApi.delete(sessionId)
      sessions.value = sessions.value.filter(s => s.id !== sessionId)
      if (currentSession.value?.id === sessionId) {
        currentSession.value = null
      }
    } catch (e) {
      error.value = 'Failed to delete session'
      console.error('Failed to delete session:', e)
    }
  }

  async function sendMessage(
    message: string,
    options: { enableWebSearch?: boolean; enableDeepThinking?: boolean } = {}
  ) {
    if (!currentSession.value) {
      await createSession()
    }

    if (!currentSession.value) {
      throw new Error('No session available')
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      session_id: currentSession.value.id,
      role: 'user',
      content: message,
      created_at: new Date().toISOString(),
    }
    currentSession.value.messages.push(userMessage)

    const assistantMessage: Message = {
      id: Date.now().toString() + '-ai',
      session_id: currentSession.value.id,
      role: 'assistant',
      content: '',
      created_at: new Date().toISOString(),
    }
    currentSession.value.messages.push(assistantMessage)

    isStreaming.value = true
    let tokenUsage: TokenUsage | undefined
    let references: ReferenceDocument[] | undefined

    try {
      const request: ChatRequest = {
        message,
        session_id: currentSession.value.id,
        enable_web_search: options.enableWebSearch || false,
        enable_deep_thinking: options.enableDeepThinking || false,
      }

      for await (const event of chatApi.stream(request)) {
        switch (event.event_type) {
          case 'content':
            if (event.content) {
              assistantMessage.content += event.content
            }
            break
          case 'token_usage':
            tokenUsage = event.token_usage
            assistantMessage.token_usage = tokenUsage
            break
          case 'references':
            references = event.references
            assistantMessage.references = references
            break
          case 'error':
            throw new Error(event.error || 'Unknown error')
          case 'done':
            break
        }
      }
    } finally {
      isStreaming.value = false
    }

    // Refresh session list to get updated timestamp
    await loadSessions()
  }

  function clearError() {
    error.value = null
  }

  return {
    // State
    sessions,
    currentSession,
    isLoading,
    isStreaming,
    error,
    // Computed
    currentSessionId,
    currentMessages,
    // Actions
    loadSessions,
    loadSession,
    createSession,
    deleteSession,
    sendMessage,
    clearError,
  }
})
