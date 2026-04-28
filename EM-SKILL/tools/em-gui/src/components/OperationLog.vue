<script setup lang="ts">
import type { ToolOperation } from '../claude/types'

defineProps<{
  operations: readonly ToolOperation[]
}>()

const iconMap: Record<string, string> = {
  read: 'Document',
  write: 'EditPen',
  edit: 'Edit',
  bash: 'Terminal',
  search: 'Search',
  other: 'QuestionFilled',
}

const labelMap: Record<string, string> = {
  read: '读取',
  write: '写入',
  edit: '编辑',
  bash: '命令',
  search: '搜索',
  other: '其他',
}

function formatTime(date: Date): string {
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}
</script>

<template>
  <div class="operation-log">
    <div v-if="operations.length === 0" class="empty">
      暂无操作记录
    </div>
    <div
      v-for="(op, index) in [...operations].reverse()"
      :key="index"
      class="log-item"
      :class="{ error: op.isError }"
    >
      <el-icon :size="14" class="log-icon">
        <component :is="iconMap[op.type] || 'QuestionFilled'" />
      </el-icon>
      <span class="log-label">{{ labelMap[op.type] || op.type }}</span>
      <span class="log-detail">{{ op.detail }}</span>
      <span class="log-time">{{ formatTime(op.timestamp) }}</span>
    </div>
  </div>
</template>

<style scoped>
.operation-log {
  font-size: 13px;
  line-height: 1.6;
}

.empty {
  color: #c0c4cc;
  text-align: center;
  padding: 20px;
}

.log-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 0;
  border-bottom: 1px solid #f0f0f0;
}

.log-item.error {
  color: #f56c6c;
}

.log-icon {
  flex-shrink: 0;
  color: #909399;
}

.log-label {
  flex-shrink: 0;
  font-weight: 600;
  color: #606266;
  min-width: 28px;
}

.log-detail {
  flex: 1;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.log-time {
  flex-shrink: 0;
  color: #c0c4cc;
  font-size: 12px;
}
</style>
