/**
 * Prompt 模板 - 用于生成 Claude CLI 命令提示词
 */

export const Prompts = {
  /** 查看项目状态 */
  stat: () =>
    `请执行斜杠命令 /em stat，返回项目状态信息`,

  /** 存量接入 */
  si: (path: string) =>
    `请执行斜杠命令 /em si "${path}"，完成存量项目接入`,

  /** 进入讨论流程 */
  disc: (topic?: string) =>
    topic
      ? `请执行斜杠命令 /em disc，讨论主题：${topic}`
      : `请执行斜杠命令 /em disc，进入讨论流程`,

  /** 新功能开发 */
  new: (description: string) =>
    `请执行斜杠命令 /em new ${description}，开始新功能开发讨论`,

  /** 验证步骤 */
  verify: (step: string) =>
    `请执行斜杠命令 /em verify ${step}，执行验证流程`,

  /** 提交结果 */
  result: (status: string) =>
    `请执行斜杠命令 /em result ${status}，提交验证结果`,

  /** 归档 */
  archive: () =>
    `请执行斜杠命令 /em arch，执行归档操作`,

  /** 上下文摘要 */
  summary: () =>
    `请执行斜杠命令 /em sum，生成上下文摘要`,

  /** 自定义命令 */
  custom: (command: string) =>
    `请执行斜杠命令 ${command}`,

  /** 普通对话 */
  chat: (message: string) =>
    `${message}`,
} as const

/** 快捷操作列表 */
export const QuickActions = [
  { id: 'stat', label: '查看状态', icon: 'DataBoard', prompt: Prompts.stat },
  { id: 'disc', label: '讨论', icon: 'ChatDotSquare', prompt: () => Prompts.disc() },
  { id: 'new', label: '新功能', icon: 'Plus', prompt: () => Prompts.new('') },
  { id: 'verify', label: '验证', icon: 'Select', prompt: () => Prompts.verify('') },
  { id: 'result', label: '提交结果', icon: 'CircleCheck', prompt: () => Prompts.result('') },
  { id: 'archive', label: '归档', icon: 'FolderOpened', prompt: Prompts.archive },
  { id: 'summary', label: '摘要', icon: 'Document', prompt: Prompts.summary },
] as const

/** 权限模式对应的 CLI 参数映射 */
export const PermissionModeMap: Record<string, string> = {
  interactive: 'default',
  notify: 'acceptEdits',
  silent: 'acceptEdits',
}
