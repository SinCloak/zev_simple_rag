// Type definitions for the application

export interface Session {
  id: string
  title: string
  created_at: string
  updated_at: string
  is_active: boolean
  message_count?: number
}

export interface TokenUsage {
  input_tokens?: number
  output_tokens?: number
  rag_tokens?: number
  total_tokens?: number
}

export interface ReferenceDocument {
  source?: string
  content: string
  metadata: Record<string, any>
  similarity_score?: number
}

export interface Message {
  id: string
  session_id: string
  role: 'user' | 'assistant'
  content: string
  created_at: string
  token_usage?: TokenUsage
  references?: ReferenceDocument[]
}

export interface SessionDetail extends Session {
  messages: Message[]
}

export interface ChatRequest {
  message: string
  session_id?: string
  enable_web_search?: boolean
  enable_deep_thinking?: boolean
}

export interface ChatResponse {
  session_id: string
  message: Message
}

export interface StreamEvent {
  event_type: 'content' | 'token_usage' | 'references' | 'done' | 'error'
  content?: string
  token_usage?: TokenUsage
  references?: ReferenceDocument[]
  error?: string
}
