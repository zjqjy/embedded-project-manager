# S7-A 技术验证报告 - Claude CLI 管道通信

**日期**: 2026-04-28
**需求ID**: 20260428-em-skill-gui

---

## 验证目标

1. Claude CLI 是否支持非交互式管道通信
2. 斜杠命令（/em xxx）是否能通过管道调用
3. 流式输出是否可行（GUI实时渲染）
4. 会话持久化方案
5. 权限控制方案
6. 调用性能评估

---

## 验证结果

### 1. -p / --print 非交互模式 ✅

| 项目 | 结果 |
|------|------|
| 基础通信 | ✅ 可正常收发消息 |
| 输出格式 | text(默认) / json / stream-json |
| 流式输出 | ✅ `--output-format stream-json --verbose` 逐字输出 |
| 启动参数 | `claude -p "<prompt>" --permission-mode <mode>` |

**stream-json 输出结构**:
```
{"type":"system","subtype":"init","session_id":"xxx", "skills":[...]}  // 初始化信息
{"type":"stream_event","event":{"type":"content_block_delta","delta":{"type":"text_delta","text":"逐字输出"}}}  // 流式文本
{"type":"assistant","message":{...}}  // 完整消息
```

### 2. 斜杠命令支持 ✅

| 方式 | 结果 |
|------|------|
| 直接传入 `/em stat` | ❌ 被解释为文件路径 |
| 自然语言引导 `"请执行斜杠命令 /em stat"` | ✅ 正常执行并返回结果 |

**结论**: GUI不能直接传入`/em xxx`，需要通过自然语言提示引导Claude执行斜杠命令。

### 3. 流式输出 ✅ (stream-json)

- `--output-format stream-json --verbose --include-partial-messages`
- 产生逐字增量事件（text_delta），适合GUI实时渲染
- 包含 thinking 事件（可忽略或展示思考过程）
- 最终输出完整 assistant 消息

### 4. 会话持久化 ⚠️

| 方案 | 结果 | 说明 |
|------|------|------|
| `-p`每次独立调用 | ✅ 可用 | 每次新会话，无上下文，平均耗时约15-30秒/次 |
| `--session-id <uuid>` | ❌ 不能复用 | 会话关闭后不能重新使用同一ID |
| `--resume <id>` | ❌ -p模式下不支持 | 交互模式才支持会话恢复 |
| 交互子进程（stdin管道） | ❌ 复杂 | 需要PTY，Windows下git-bash兼容性问题 |

**GUI方案**: 每次GUI操作发起一次独立的 `claude -p` 调用。**简单可靠**。

### 5. 权限控制 ✅

| 模式 | 文件写入 | 命令执行 | 说明 |
|------|---------|---------|------|
| `default` | 弹窗询问 | 弹窗询问 | 交互模式适用 |
| `acceptEdits` | ✅ 自动允许 | ⚠️ 部分 | 自动接受文件编辑操作 |
| `bypassPermissions` | ✅ 自动允许 | ✅ 自动允许 | 跳过所有权限检查 |
| `dontAsk` | ❌ 自动拒绝 | ❌ 自动拒绝 | 静默拒绝所有权限 |

**推荐**: `--permission-mode acceptEdits`（安全且满足EM-SKILL的文件操作需求）

### 6. 调用性能

| 指标 | 数值 |
|------|------|
| 首次调用耗时 | 约15-30秒（含模型加载） |
| 后续调用耗时 | 约10-25秒（利用缓存） |
| 输出延迟 | 流式模式下首字约3-8秒出现 |

**优化思路**: GUI可预留1-2个预热连接，减少首次等待感。

---

## GUI通信架构方案

### 推荐方案: -p 单次调用模式

```
用户点击"查看状态"按钮
  → GUI构造prompt: "请执行斜杠命令 /em stat"
  → 启动: claude -p "<prompt>" --output-format stream-json --verbose --permission-mode acceptEdits
  → 实时解析stdout的stream-json事件
  → GUI逐字渲染文本到界面
  → 完成
```

### 架构要点

| 项目 | 方案 |
|------|------|
| 通信模式 | `claude -p` 单次调用（非持久会话） |
| 输出格式 | `stream-json`（逐字流式） |
| 权限模式 | `acceptEdits`（自动接受文件操作） |
| 斜杠命令 | 自然语言引导（非直接传入） |
| 进程管理 | 每次操作新建子进程，完成后销毁 |
| 并发控制 | 串行执行，同一时间只有一个Claude进程 |

### 优点
- 实现简单，无需处理PTY/交互式管道
- 每次调用独立，不会互相影响
- 进程用完即销毁，无资源泄漏
- `stream-json`支持实时渲染

### 缺点
- 每次调用约15-30秒（模型加载）+ 执行时间
- 无上下文记忆（但EM操作大部分是独立命令）

---

## 7. 串口通信方案（Tauri Rust）✅

| 项目 | 评估结果 |
|------|---------|
| Rust serialport crate | ✅ 成熟稳定，v4.9.0，Windows Tier 1支持 |
| 备选 serial2 crate | ✅ 更简洁API，支持多线程并发读写 |
| 功能覆盖 | 端口枚举/打开/关闭/读写/波特率/DTR/RTS全支持 |
| 与原pyserial兼容 | ✅ 功能完全覆盖，可完全移植 |
| Tauri IPC集成 | ✅ Rust后端暴露command，Vue前端invoke调用 |

**Tauri串口架构**:
```
Vue串口组件 → invoke('serial_list_ports') → Rust serialport crate
           → invoke('serial_open', {port, baudrate})
           → listen('serial-data', callback)  // 事件监听实时数据
           → invoke('serial_write', {data})
           → invoke('serial_close')
```

**关键区别**:
- pyserial → `serialport` Rust crate（API不同但功能等价）
- tkinter UI → 重写为 Vue 组件
- MCP接口 → GUI直接内置，不再需要MCP

---

## 后续优化方向

1. **预热机制**: GUI启动时自动发一条简单预热请求
2. **Prompt模板**: 斜杠命令的prompt封装为模板，保证一致性
3. **超时处理**: 设置合理超时（建议120秒），超时后重试
4. **错误恢复**: Claude进程异常退出时自动重试
