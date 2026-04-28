<script setup lang="ts">
import type { ToolOperation } from '../claude/types'

const props = withDefaults(defineProps<{
  visible: boolean
  operation: ToolOperation | null
}>(), {
  visible: false,
})

const emit = defineEmits<{
  approve: []
  reject: []
  close: []
}>()

const iconMap: Record<string, string> = {
  read: 'Document',
  write: 'EditPen',
  edit: 'Edit',
  bash: 'Terminal',
  search: 'Search',
  other: 'QuestionFilled',
}

const colorMap: Record<string, string> = {
  read: '#409eff',
  write: '#e6a23c',
  edit: '#67c23a',
  bash: '#909399',
  search: '#9b59b6',
  other: '#606266',
}

function handleApprove() {
  emit('approve')
}

function handleReject() {
  emit('reject')
}
</script>

<template>
  <el-dialog
    :model-value="visible"
    title="权限确认"
    width="420px"
    :close-on-click-modal="false"
    @close="emit('close')"
  >
    <div v-if="operation" class="perm-content">
      <div class="perm-icon" :style="{ background: colorMap[operation.type] + '20', color: colorMap[operation.type] }">
        <el-icon :size="28"><component :is="iconMap[operation.type] || 'QuestionFilled'" /></el-icon>
      </div>
      <div class="perm-info">
        <div class="perm-name">{{ operation.name }}</div>
        <div class="perm-detail">{{ operation.detail }}</div>
      </div>
    </div>

    <template #footer>
      <el-button @click="handleReject">拒绝</el-button>
      <el-button type="primary" @click="handleApprove">允许</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.perm-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 0;
}

.perm-icon {
  width: 52px;
  height: 52px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.perm-info {
  flex: 1;
}

.perm-name {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.perm-detail {
  font-size: 13px;
  color: #909399;
  word-break: break-all;
}
</style>
