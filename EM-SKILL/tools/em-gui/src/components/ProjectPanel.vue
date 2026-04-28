<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Refresh, Delete } from '@element-plus/icons-vue'
import { bridgeState, callClaude, clearOperations } from '../claude/bridge'
import OperationLog from './OperationLog.vue'

const statResult = ref('')
const loading = ref(false)

async function fetchStat() {
  loading.value = true
  statResult.value = ''
  try {
    await callClaude({
      prompt: '请执行斜杠命令 /em stat，返回项目状态信息',
      permissionMode: 'notify',
      onDelta: (text) => {
        statResult.value += text
      },
      onError: (err) => {
        statResult.value = `错误: ${err}`
      },
    })
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStat()
})
</script>

<template>
  <div class="project-panel">
    <div class="panel-header">
      <h2>项目面板</h2>
      <div class="header-actions">
        <el-button size="small" :icon="Refresh" :loading="loading" @click="fetchStat">
          刷新状态
        </el-button>
        <el-button size="small" :icon="Delete" @click="clearOperations">
          清除记录
        </el-button>
      </div>
    </div>

    <div class="panel-body">
      <!-- 项目状态 -->
      <el-card class="stat-card" shadow="never">
        <template #header>
          <div class="card-header">
            <el-icon><DataBoard /></el-icon>
            <span>项目状态</span>
          </div>
        </template>
        <div v-if="loading" class="stat-loading">
          <el-icon class="loading-icon" :size="24"><Loading /></el-icon>
          <span>正在获取状态...</span>
        </div>
        <div v-else-if="statResult" class="stat-content">
          <pre>{{ statResult }}</pre>
        </div>
        <div v-else class="stat-empty">
          点击「刷新状态」获取项目信息
        </div>
      </el-card>

      <!-- 操作记录 -->
      <el-card class="log-card" shadow="never">
        <template #header>
          <div class="card-header">
            <el-icon><Document /></el-icon>
            <span>操作记录</span>
          </div>
        </template>
        <OperationLog :operations="bridgeState.operations" />
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.project-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h2 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.panel-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow: hidden;
}

.stat-card {
  flex-shrink: 0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
}

.stat-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
  font-family: 'Consolas', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.6;
  color: #303133;
}

.stat-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  padding: 20px 0;
}

.loading-icon {
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.stat-empty {
  color: #c0c4cc;
  text-align: center;
  padding: 20px;
}

.log-card {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.log-card :deep(.el-card__body) {
  flex: 1;
  overflow-y: auto;
}
</style>
