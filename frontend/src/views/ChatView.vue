<template>
  <div class="chat-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1 class="app-title">Zev RAG Agent</h1>
        <button class="new-chat-btn" @click="handleNewChat">
          <span class="icon">+</span>
          New Chat
        </button>
      </div>

      <div class="sessions-list">
        <div v-if="chatStore.isLoading && chatStore.sessions.length === 0" class="loading">
          Loading sessions...
        </div>
        <div
          v-for="session in chatStore.sessions"
          :key="session.id"
          class="session-item"
          :class="{ active: chatStore.currentSessionId === session.id }"
          @click="handleSelectSession(session.id)"
        >
          <div class="session-title">{{ session.title }}</div>
          <div class="session-date">{{ formatDate(session.updated_at) }}</div>
          <button
            class="delete-btn"
            @click.stop="handleDeleteSession(session.id)"
            title="Delete session"
          >
            &times;
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Chat Area -->
    <main class="chat-main">
      <!-- Empty State -->
      <div v-if="!chatStore.currentSession" class="empty-state">
        <div class="empty-icon">💬</div>
        <h2>Welcome to Zev RAG Agent</h2>
        <p>Start a new conversation or select an existing one from the sidebar.</p>
        <button class="primary-btn" @click="handleNewChat">Start New Chat</button>
      </div>

      <!-- Chat Messages -->
      <template v-else>
        <div class="chat-header">
          <h2 class="session-title">{{ chatStore.currentSession.title }}</h2>
        </div>

        <div class="messages-container" ref="messagesContainer">
          <div
            v-for="message in chatStore.currentMessages"
            :key="message.id"
            class="message-wrapper"
            :class="message.role"
          >
            <div class="message-avatar">
              {{ message.role === 'user' ? '👤' : '🤖' }}
            </div>
            <div class="message-content">
              <div class="message-header">
                <span class="role">{{ message.role === 'user' ? 'You' : 'AI Assistant' }}</span>
                <span class="time">{{ formatTime(message.created_at) }}</span>
              </div>
              <div
                class="message-text markdown-content"
                v-html="renderMarkdown(message.content)"
              ></div>

              <!-- References -->
              <div v-if="message.references && message.references.length > 0" class="references">
                <div class="references-title">📚 References ({{ message.references.length }})</div>
                <div class="reference-list">
                  <div
                    v-for="(ref, idx) in message.references"
                    :key="idx"
                    class="reference-item"
                  >
                    <div class="ref-source">{{ ref.source || 'Unknown' }}</div>
                    <div class="ref-content">{{ ref.content.substring(0, 150) }}...</div>
                  </div>
                </div>
              </div>

              <!-- Token Usage -->
              <div v-if="message.token_usage" class="token-usage">
                <div class="token-item">
                  <span class="label">Input:</span>
                  <span class="value">{{ message.token_usage.input_tokens || 'N/A' }}</span>
                </div>
                <div class="token-item">
                  <span class="label">Output:</span>
                  <span class="value">{{ message.token_usage.output_tokens || 'N/A' }}</span>
                </div>
                <div class="token-item">
                  <span class="label">RAG:</span>
                  <span class="value">{{ message.token_usage.rag_tokens || 'N/A' }}</span>
                </div>
                <div class="token-item">
                  <span class="label">Total:</span>
                  <span class="value">{{ message.token_usage.total_tokens || 'N/A' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="chatStore.isStreaming" class="message-wrapper assistant">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <div class="input-area">
          <div class="options">
            <label class="option">
              <input
                type="checkbox"
                v-model="enableWebSearch"
                :disabled="chatStore.isStreaming"
              />
              <span>🌐 Web Search</span>
            </label>
            <label class="option">
              <input
                type="checkbox"
                v-model="enableDeepThinking"
                :disabled="chatStore.isStreaming"
              />
              <span>🧠 Deep Thinking</span>
            </label>
          </div>
          <div class="input-wrapper">
            <textarea
              v-model="inputMessage"
              placeholder="Type your message..."
              rows="1"
              @keydown="handleKeyDown"
              :disabled="chatStore.isStreaming"
              ref="textareaRef"
            ></textarea>
            <button
              class="send-btn"
              @click="handleSendMessage"
              :disabled="!inputMessage.trim() || chatStore.isStreaming"
            >
              {{ chatStore.isStreaming ? '...' : 'Send' }}
            </button>
          </div>
        </div>
      </template>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import { useChatStore } from '@/stores/chat'

// Configure marked
marked.setOptions({
  highlight: function(code, lang) {
    const language = hljs.getLanguage(lang) ? lang : 'plaintext'
    return hljs.highlight(code, { language }).value
  },
  breaks: true,
  gfm: true,
})

const chatStore = useChatStore()
const route = useRoute()
const router = useRouter()

const inputMessage = ref('')
const enableWebSearch = ref(false)
const enableDeepThinking = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)
const textareaRef = ref<HTMLTextAreaElement | null>(null)

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } else if (days === 1) {
    return 'Yesterday'
  } else if (days < 7) {
    return date.toLocaleDateString([], { weekday: 'long' })
  } else {
    return date.toLocaleDateString()
  }
}

function formatTime(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function renderMarkdown(content: string): string {
  const html = marked.parse(content) as string
  return DOMPurify.sanitize(html)
}

async function handleNewChat() {
  try {
    const session = await chatStore.createSession()
    router.push(`/session/${session.id}`)
  } catch (e) {
    console.error('Failed to create session:', e)
  }
}

async function handleSelectSession(sessionId: string) {
  if (chatStore.currentSessionId !== sessionId) {
    await chatStore.loadSession(sessionId)
    router.push(`/session/${sessionId}`)
  }
}

async function handleDeleteSession(sessionId: string) {
  if (confirm('Are you sure you want to delete this session?')) {
    await chatStore.deleteSession(sessionId)
    if (chatStore.currentSessionId === sessionId) {
      router.push('/')
    }
  }
}

async function handleSendMessage() {
  if (!inputMessage.value.trim() || chatStore.isStreaming) return

  const message = inputMessage.value
  inputMessage.value = ''

  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
  }

  try {
    await chatStore.sendMessage(message, {
      enableWebSearch: enableWebSearch.value,
      enableDeepThinking: enableDeepThinking.value,
    })
  } catch (e) {
    console.error('Failed to send message:', e)
  }
}

function handleKeyDown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSendMessage()
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// Auto-resize textarea
watch(inputMessage, () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
    textareaRef.value.style.height = Math.min(textareaRef.value.scrollHeight, 200) + 'px'
  }
})

// Watch messages and scroll
watch(
  () => chatStore.currentMessages,
  () => scrollToBottom(),
  { deep: true }
)

// Handle route changes
watch(
  () => route.params.sessionId,
  async (sessionId) => {
    if (sessionId && typeof sessionId === 'string') {
      if (!chatStore.currentSession || chatStore.currentSession.id !== sessionId) {
        await chatStore.loadSession(sessionId)
      }
    }
  },
  { immediate: true }
)

onMounted(async () => {
  await chatStore.loadSessions()

  const sessionId = route.params.sessionId
  if (sessionId && typeof sessionId === 'string') {
    await chatStore.loadSession(sessionId)
  }
})
</script>

<style lang="scss" scoped>
.chat-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* Sidebar */
.sidebar {
  width: 280px;
  background: var(--surface-color);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.app-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 0.75rem;
}

.new-chat-btn {
  width: 100%;
  padding: 0.625rem 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: background 0.2s;

  &:hover {
    background: var(--primary-hover);
  }
}

.sessions-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.loading {
  padding: 1rem;
  color: var(--text-secondary);
  text-align: center;
}

.session-item {
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  position: relative;
  transition: background 0.2s;

  &:hover {
    background: var(--background-color);
  }

  &.active {
    background: #eef2ff;
  }

  .session-title {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding-right: 1.5rem;
  }

  .session-date {
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 0.25rem;
  }

  .delete-btn {
    position: absolute;
    right: 0.5rem;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: var(--text-secondary);
    font-size: 1.25rem;
    cursor: pointer;
    width: 1.5rem;
    height: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0.25rem;
    opacity: 0;
    transition: opacity 0.2s, background 0.2s;

    &:hover {
      background: var(--error-color);
      color: white;
    }
  }

  &:hover .delete-btn {
    opacity: 1;
  }
}

/* Main Chat Area */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--background-color);
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;

  .empty-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
  }

  h2 {
    font-size: 1.5rem;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }

  p {
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
  }
}

.primary-btn {
  padding: 0.75rem 2rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;

  &:hover {
    background: var(--primary-hover);
  }
}

.chat-header {
  padding: 1rem 2rem;
  background: var(--surface-color);
  border-bottom: 1px solid var(--border-color);

  .session-title {
    font-size: 1.125rem;
    font-weight: 600;
  }
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.message-wrapper {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;

  &.user {
    flex-direction: row-reverse;

    .message-content {
      background: #eef2ff;
    }
  }

  &.assistant {
    .message-content {
      background: var(--surface-color);
    }
  }
}

.message-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
}

.message-content {
  flex: 1;
  max-width: 800px;
  padding: 1rem 1.25rem;
  border-radius: 1rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.message-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;

  .role {
    font-weight: 600;
    font-size: 0.875rem;
  }

  .time {
    font-size: 0.75rem;
    color: var(--text-secondary);
  }
}

.message-text {
  word-wrap: break-word;
  overflow-wrap: anywhere;
}

.typing-indicator {
  display: flex;
  gap: 0.25rem;
  padding: 0.5rem 0;

  span {
    width: 0.5rem;
    height: 0.5rem;
    background: var(--text-secondary);
    border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out both;

    &:nth-child(1) { animation-delay: -0.32s; }
    &:nth-child(2) { animation-delay: -0.16s; }
  }
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* References */
.references {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.references-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.reference-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.reference-item {
  padding: 0.5rem 0.75rem;
  background: var(--background-color);
  border-radius: 0.375rem;
  border-left: 3px solid var(--primary-color);
}

.ref-source {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 0.25rem;
}

.ref-content {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

/* Token Usage */
.token-usage {
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.token-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.75rem;

  .label {
    color: var(--text-secondary);
  }

  .value {
    font-weight: 600;
    color: var(--primary-color);
  }
}

/* Input Area */
.input-area {
  padding: 1rem 2rem 2rem;
  background: var(--surface-color);
  border-top: 1px solid var(--border-color);
}

.options {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 0.75rem;
}

.option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
  cursor: pointer;

  input {
    cursor: pointer;
  }
}

.input-wrapper {
  display: flex;
  gap: 0.75rem;
  align-items: flex-end;
}

textarea {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  font-size: 1rem;
  font-family: inherit;
  resize: none;
  max-height: 200px;
  overflow-y: auto;
  transition: border-color 0.2s;

  &:focus {
    outline: none;
    border-color: var(--primary-color);
  }

  &:disabled {
    background: var(--background-color);
    cursor: not-allowed;
  }
}

.send-btn {
  padding: 0.75rem 1.5rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;

  &:hover:not(:disabled) {
    background: var(--primary-hover);
  }

  &:disabled {
    background: var(--secondary-color);
    cursor: not-allowed;
  }
}
</style>
