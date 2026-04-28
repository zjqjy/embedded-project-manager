<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  text: string
  loading?: boolean
}>()

const autoScroll = ref(true)
const outputRef = ref<HTMLElement | null>(null)

watch(
  () => props.text,
  () => {
    if (autoScroll.value && outputRef.value) {
      outputRef.value.scrollTop = outputRef.value.scrollHeight
    }
  }
)
</script>

<template>
  <div class="output-panel">
    <el-card shadow="never" class="output-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon><ChatDotSquare /></el-icon>
            <span>输出</span>
            <el-tag v-if="loading" size="small" type="warning" effect="dark">运行中</el-tag>
          </div>
          <el-switch
            v-model="autoScroll"
            active-text="自动滚动"
            size="small"
            inline-prompt
          />
        </div>
      </template>
      <div ref="outputRef" class="output-content">
        <div v-if="!text && !loading" class="output-empty">
          暂无输出，请执行操作
        </div>
        <pre v-else class="output-text">{{ text }}</pre>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.output-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.output-card {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.output-card :deep(.el-card__body) {
  flex: 1;
  overflow: hidden;
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
}

.output-content {
  height: 100%;
  overflow-y: auto;
  padding: 12px 16px;
  background: #1e1e1e;
  color: #d4d4d4;
  font-family: 'Consolas', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.6;
}

.output-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #666;
}

.output-text {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
}
</style>
