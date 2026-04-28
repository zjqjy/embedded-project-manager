<script setup lang="ts">
import { ref } from 'vue'
import { Delete } from '@element-plus/icons-vue'

const ports = ref<string[]>([])
const selectedPort = ref('')
const baudRate = ref(115200)
const isConnected = ref(false)
const serialLog = ref<string[]>([])

const baudRates = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]

function toggleConnect() {
  if (isConnected.value) {
    isConnected.value = false
    serialLog.value.push(`[${new Date().toLocaleTimeString()}] 已断开`)
  } else {
    // 实际连接逻辑需要 Tauri serialport 后端支持
    isConnected.value = true
    serialLog.value.push(`[${new Date().toLocaleTimeString()}] 已连接 ${selectedPort.value} @ ${baudRate.value}`)
  }
}

function clearLog() {
  serialLog.value = []
}
</script>

<template>
  <div class="serial-panel">
    <div class="panel-header">
      <h2>串口监控</h2>
    </div>

    <div class="serial-body">
      <!-- 配置区 -->
      <el-card shadow="never" class="config-card">
        <el-form :inline="true" size="small" label-width="60px">
          <el-form-item label="端口">
            <el-select v-model="selectedPort" placeholder="选择串口" style="width: 160px">
              <el-option
                v-for="p in ports"
                :key="p"
                :label="p"
                :value="p"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="波特率">
            <el-select v-model="baudRate" style="width: 120px">
              <el-option
                v-for="rate in baudRates"
                :key="rate"
                :label="`${rate}`"
                :value="rate"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              :icon="isConnected ? 'Monitor' : 'Connection'"
              @click="toggleConnect"
            >
              {{ isConnected ? '断开' : '连接' }}
            </el-button>
            <el-button :icon="Delete" @click="clearLog">清空</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 终端区 -->
      <el-card shadow="never" class="terminal-card">
        <div ref="terminalRef" class="terminal">
          <div v-if="serialLog.length === 0" class="terminal-empty">
            未连接或暂无数据
          </div>
          <div v-for="(line, i) in serialLog" :key="i" class="terminal-line">
            {{ line }}
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.serial-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.panel-header h2 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.serial-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow: hidden;
}

.config-card {
  flex-shrink: 0;
}

.terminal-card {
  flex: 1;
  overflow: hidden;
}

.terminal-card :deep(.el-card__body) {
  height: 100%;
  padding: 0;
}

.terminal {
  height: 100%;
  overflow-y: auto;
  background: #1e1e1e;
  color: #d4d4d4;
  font-family: 'Consolas', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.5;
  padding: 12px 16px;
}

.terminal-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #666;
}

.terminal-line {
  white-space: pre-wrap;
  word-break: break-all;
}
</style>
