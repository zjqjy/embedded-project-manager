/** Claude CLI stream-json 事件类型 */

/** 系统初始化事件 */
export interface InitEvent {
  type: 'system'
  subtype: 'init'
  session_id: string
  cwd: string
  skills: string[]
  permissionMode: string
  model: string
}

/** 流式事件 - 文本增量 */
export interface TextDeltaEvent {
  type: 'stream_event'
  event: {
    type: 'content_block_delta'
    index: number
    delta: {
      type: 'text_delta'
      text: string
    }
  }
  session_id: string
}

/** 流式事件 - 思考增量 */
export interface ThinkingDeltaEvent {
  type: 'stream_event'
  event: {
    type: 'content_block_delta'
    index: number
    delta: {
      type: 'thinking_delta'
      thinking: string
    }
  }
  session_id: string
}

/** 工具调用事件 */
export interface ToolUseEvent {
  type: 'assistant'
  message: {
    content: Array<{
      type: 'tool_use'
      id: string
      name: string
      input: Record<string, unknown>
    } | {
      type: 'text'
      text: string
    } | {
      type: 'thinking'
      thinking: string
    }>
  }
  session_id: string
}

/** 工具结果事件 */
export interface ToolResultEvent {
  type: 'user'
  message: {
    content: Array<{
      type: 'tool_result'
      content: string
      is_error?: boolean
      tool_use_id: string
    }>
  }
  session_id: string
  tool_use_result?: string
}

/** 完整消息事件 */
export interface AssistantMessageEvent {
  type: 'assistant'
  message: {
    id: string
    content: Array<{
      type: 'text'
      text: string
    }>
    stop_reason: string | null
    usage: {
      input_tokens: number
      output_tokens: number
    }
  }
}

/** 联合事件类型 */
export type StreamEvent =
  | InitEvent
  | TextDeltaEvent
  | ThinkingDeltaEvent
  | ToolUseEvent
  | ToolResultEvent
  | AssistantMessageEvent

/** 权限模式 */
export type PermissionMode = 'interactive' | 'notify' | 'silent'

/** Claude CLI 调用的参数 */
export interface ClaudeCallOptions {
  prompt: string
  permissionMode: PermissionMode
  onDelta?: (text: string) => void
  onThinking?: (text: string) => void
  onToolUse?: (name: string, input: Record<string, unknown>) => void
  onError?: (error: string) => void
  onComplete?: (fullText: string) => void
  signal?: AbortSignal
}

/** 调用结果 */
export interface ClaudeCallResult {
  text: string
  sessionId: string
  toolUses: Array<{ name: string; input: Record<string, unknown> }>
  usage?: { input_tokens: number; output_tokens: number }
}

/** 工具操作记录 */
export interface ToolOperation {
  type: 'read' | 'write' | 'bash' | 'edit' | 'search' | 'other'
  name: string
  detail: string
  timestamp: Date
  isError?: boolean
}
