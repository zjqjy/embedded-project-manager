/**
 * Claude CLI 桥接模块
 *
 * 通过 Tauri IPC 调用 Rust 后端管理 claude -p 子进程，
 * 解析 stream-json 事件并分发到前端回调。
 */

import { ref, readonly, type Ref } from 'vue'
import { invoke } from '@tauri-apps/api/core'
import { listen, type UnlistenFn } from '@tauri-apps/api/event'
import type {
  ClaudeCallOptions,
  ClaudeCallResult,
  StreamEvent,
  ToolOperation,
  PermissionMode,
} from './types'

/** 桥接状态 */
export interface BridgeState {
  isRunning: boolean
  currentOperation: string
  operations: ToolOperation[]
  lastResult: string
}

/** 全局桥接状态 */
const state: Ref<BridgeState> = ref({
  isRunning: false,
  currentOperation: '',
  operations: [],
  lastResult: '',
})

export const bridgeState = readonly(state)

/** 当前的事件监听注销函数 */
let unlistenLine: UnlistenFn | null = null
let unlistenDone: UnlistenFn | null = null

/**
 * 添加操作记录
 */
function addOperation(op: ToolOperation) {
  state.value.operations = [...state.value.operations, op]
}

/**
 * 解析 stream-json 事件行
 */
function parseStreamLine(line: string): StreamEvent | null {
  try {
    return JSON.parse(line) as StreamEvent
  } catch {
    return null
  }
}

/**
 * 将工具调用名映射为友好名称
 */
function getToolOperationType(name: string): ToolOperation['type'] {
  switch (name) {
    case 'Read': return 'read'
    case 'Write': return 'write'
    case 'Edit': return 'edit'
    case 'Bash': return 'bash'
    case 'Grep':
    case 'Glob':
    case 'WebSearch': return 'search'
    default: return 'other'
  }
}

/**
 * 获取工具调用的详细信息
 */
function getToolDetail(name: string, input: Record<string, unknown>): string {
  switch (name) {
    case 'Read':
      return `读取 ${input.file_path || input.path || ''}`
    case 'Write':
      return `写入 ${input.file_path || ''}`
    case 'Edit':
      return `编辑 ${input.file_path || ''}`
    case 'Bash':
      return `执行: ${String(input.command || '').slice(0, 80)}`
    case 'Grep':
      return `搜索: ${input.pattern || ''}`
    case 'Glob':
      return `查找: ${input.pattern || ''}`
    case 'WebSearch':
      return `搜索: ${input.query || ''}`
    default:
      return `${name}: ${JSON.stringify(input).slice(0, 60)}`
  }
}

/**
 * 调用 Claude CLI（通过 Tauri IPC -> Rust 后端）
 *
 * @param options 调用参数
 * @returns 解析结果
 */
export async function callClaude(options: ClaudeCallOptions): Promise<ClaudeCallResult> {
  const {
    prompt,
    permissionMode,
    onDelta,
    onThinking,
    onToolUse,
    onError,
    onComplete,
    signal,
  } = options

  state.value.isRunning = true
  state.value.currentOperation = prompt.slice(0, 50)

  const result: ClaudeCallResult = {
    text: '',
    sessionId: '',
    toolUses: [],
  }

  return new Promise((resolve, reject) => {
    let settled = false

    // 监听 Tauri 事件
    Promise.all([
      listen<{ line: string; is_error: boolean }>('claude-line', (event) => {
        if (signal?.aborted || settled) return

        const { line, is_error: isError } = event.payload

        // 尝试解析 JSON 事件行
        const parsed = parseStreamLine(line)
        if (!parsed) {
          // 非 JSON 行（如日志），忽略或作为错误输出
          if (isError) {
            onError?.(line)
          }
          return
        }

        if (parsed.type === 'system' && parsed.subtype === 'init') {
          result.sessionId = parsed.session_id
        } else if (parsed.type === 'stream_event') {
          const ev = parsed.event
          if (ev.type === 'content_block_delta') {
            const delta = ev.delta
            if (delta.type === 'text_delta') {
              result.text += delta.text
              onDelta?.(delta.text)
            } else if (delta.type === 'thinking_delta') {
              onThinking?.(delta.thinking)
            }
          }
        } else if (parsed.type === 'assistant') {
          const msg = parsed.message
          if (msg.content) {
            for (const block of msg.content) {
              if (block.type === 'tool_use') {
                const detail = getToolDetail(block.name, block.input)
                result.toolUses.push({
                  name: block.name,
                  input: block.input,
                })
                onToolUse?.(block.name, block.input)
                addOperation({
                  type: getToolOperationType(block.name),
                  name: block.name,
                  detail,
                  timestamp: new Date(),
                })
              }
            }
          }
        }
      }).then((fn) => { unlistenLine = fn }),

      listen<{ success: boolean; error: string | null }>('claude-done', (event) => {
        if (settled) return
        settled = true

        state.value.isRunning = false
        state.value.lastResult = result.text

        cleanup()

        if (event.payload.success) {
          onComplete?.(result.text)
          resolve(result)
        } else {
          const errMsg = event.payload.error || 'Claude 进程异常退出'
          onError?.(errMsg)
          reject(new Error(errMsg))
        }
      }).then((fn) => { unlistenDone = fn }),
    ]).then(() => {
      // 监听就绪后，启动 Claude 进程
      invoke('call_claude', {
        prompt,
        permissionMode,
      }).catch((err: string) => {
        if (settled) return
        settled = true
        state.value.isRunning = false
        cleanup()
        onError?.(err)
        reject(new Error(err))
      })
    })

    // 处理 AbortSignal 取消
    if (signal) {
      signal.addEventListener('abort', () => {
        if (settled) return
        cancelClaude()
      })
    }
  })
}

/**
 * 取消当前 Claude 调用
 */
export async function cancelClaude() {
  try {
    await invoke('cancel_claude')
  } catch {
    // 忽略，可能没有运行中的进程
  }
  state.value.isRunning = false
  cleanup()
}

/**
 * 清理事件监听
 */
function cleanup() {
  unlistenLine?.()
  unlistenLine = null
  unlistenDone?.()
  unlistenDone = null
}

/**
 * 清除操作记录
 */
export function clearOperations() {
  state.value.operations = []
}

/**
 * 获取权限模式对应的说明
 */
export function getPermissionModeDescription(mode: PermissionMode): string {
  switch (mode) {
    case 'interactive':
      return '每次操作需用户确认（默认）'
    case 'notify':
      return '自动允许，日志显示操作记录'
    case 'silent':
      return '自动允许，无提示'
  }
}

/**
 * 旧版兼容：创建 AbortController
 */
export function createAbortController(): AbortController {
  return new AbortController()
}
