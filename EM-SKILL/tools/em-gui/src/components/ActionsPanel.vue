<script setup lang="ts">
import { ref } from 'vue'
import { QuickActions } from '../claude/prompt-templates'
import OutputPanel from './OutputPanel.vue'
import { callClaude } from '../claude/bridge'

const displayText = ref('')
const isRunning = ref(false)
const currentAction = ref('')
const customCmd = ref('')

async function executeAction(action: typeof QuickActions[number]) {
  if (isRunning.value) return

  isRunning.value = true
  currentAction.value = action.label
  displayText.value = ''

  try {
    await callClaude({
      prompt: action.prompt(),
      permissionMode: 'interactive',
      onDelta: (text) => {
        displayText.value += text
      },
      onError: (err) => {
        displayText.value = `错误: ${err}`
      },
    })
  } finally {
    isRunning.value = false
    currentAction.value = ''
  }
}

async function executeCustom() {
  if (!customCmd.value.trim() || isRunning.value) return

  isRunning.value = true
  currentAction.value = '自定义'
  displayText.value = ''

  try {
    await callClaude({
      prompt: `请执行斜杠命令 ${customCmd.value.trim()}`,
      permissionMode: 'interactive',
      onDelta: (text) => {
        displayText.value += text
      },
      onError: (err) => {
        displayText.value = `错误: ${err}`
      },
    })
  } finally {
    isRunning.value = false
    currentAction.value = ''
  }
}

const iconMap: Record<string, string> = {
  DataBoard: 'DataBoard',
  ChatDotSquare: 'ChatDotSquare',
  Plus: 'Plus',
  Select: 'Select',
  CircleCheck: 'CircleCheck',
  FolderOpened: 'FolderOpened',
  Document: 'Document',
}
</script>

<template>
  <div class="actions-panel">
    <div class="panel-header">
      <h2>快捷操作</h2>
    </div>

    <!-- 快捷操作按钮 -->
    <el-row :gutter="12" class="action-grid">
      <el-col v-for="action in QuickActions" :key="action.id" :span="6">
        <el-card
          shadow="hover"
          class="action-card"
          :class="{ running: isRunning && currentAction === action.label }"
          @click="executeAction(action)"
        >
          <div class="action-content">
            <el-icon :size="28">
              <component :is="iconMap[action.icon] || 'Tools'" />
            </el-icon>
            <span class="action-label">{{ action.label }}</span>
            <el-icon v-if="isRunning && currentAction === action.label" class="spin-icon" :size="16">
              <Loading />
            </el-icon>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 命令输入 -->
    <el-card shadow="never" class="cmd-card">
      <template #header>
        <div class="card-header">
          <el-icon><Edit /></el-icon>
          <span>自定义命令</span>
        </div>
      </template>
      <div class="cmd-input-row">
        <el-input
          v-model="customCmd"
          placeholder="输入自定义命令，如 /em sum"
          clearable
          @keyup.enter="executeCustom"
        />
        <el-button type="primary" :disabled="!customCmd.trim()" @click="executeCustom">
          发送
        </el-button>
      </div>
    </el-card>

    <!-- 输出区域 -->
    <OutputPanel v-if="displayText" :text="displayText" :loading="isRunning" />
  </div>
</template>

<style scoped>
.actions-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.panel-header h2 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.action-grid {
  margin-bottom: 0;
}

.action-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-bottom: 12px;
}

.action-card:hover {
  transform: translateY(-2px);
}

.action-card.running {
  border-color: #409eff;
  background: #ecf5ff;
}

.action-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 0;
  color: #606266;
}

.action-label {
  font-size: 14px;
  font-weight: 600;
}

.spin-icon {
  animation: rotating 1.5s linear infinite;
}

@keyframes rotating {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.cmd-card {
  flex-shrink: 0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
}

.cmd-input-row {
  display: flex;
  gap: 8px;
}
</style>
