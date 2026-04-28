<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from './components/Sidebar.vue'

const activeView = ref('project')
const permissionMode = ref('interactive') // interactive | notify | silent

function onMenuSelect(index: string) {
  activeView.value = index
}
</script>

<template>
  <el-container class="app-container">
    <!-- 顶部标题栏 -->
    <el-header class="app-header">
      <div class="header-left">
        <el-icon :size="22"><Tools /></el-icon>
        <span class="header-title">EM-SKILL GUI</span>
      </div>
      <div class="header-right">
        <span class="perm-label">权限模式:</span>
        <el-select v-model="permissionMode" size="small" style="width: 120px">
          <el-option label="交互模式" value="interactive" />
          <el-option label="通知模式" value="notify" />
          <el-option label="静默模式" value="silent" />
        </el-select>
        <el-button :icon="Setting" circle size="small" />
      </div>
    </el-header>

    <!-- 主体区域 -->
    <el-container class="app-body">
      <!-- 侧边栏 -->
      <Sidebar @menu-select="onMenuSelect" />

      <!-- 主内容区 -->
      <el-main class="app-main">
        <div v-if="activeView === 'project'" class="view-placeholder">
          <el-icon :size="48"><DataBoard /></el-icon>
          <h2>项目管理面板</h2>
          <p>项目状态、步骤进度、待办事项</p>
        </div>

        <div v-else-if="activeView === 'actions'" class="view-placeholder">
          <el-icon :size="48"><Monitor /></el-icon>
          <h2>命令快捷操作区</h2>
          <p>一键执行常用命令</p>
        </div>

        <div v-else-if="activeView === 'serial'" class="view-placeholder">
          <el-icon :size="48"><Connection /></el-icon>
          <h2>串口监控工具</h2>
          <p>串口配置、收发、日志</p>
        </div>

        <div v-else-if="activeView === 'output'" class="view-placeholder">
          <el-icon :size="48"><ChatDotSquare /></el-icon>
          <h2>日志与输出面板</h2>
          <p>Claude 回复、操作记录、日志搜索</p>
        </div>

        <div v-else class="view-placeholder">
          <el-icon :size="48"><Setting /></el-icon>
          <h2>设置</h2>
          <p>GUI 配置与偏好</p>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #2c3e50;
  color: #fff;
  padding: 0 16px;
  height: 48px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.perm-label {
  font-size: 12px;
  color: #aaa;
}

.app-body {
  flex: 1;
  overflow: hidden;
}

.app-main {
  background: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}

.view-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
  gap: 12px;
}

.view-placeholder h2 {
  margin: 0;
  color: #606266;
}

.view-placeholder p {
  margin: 0;
  color: #c0c4cc;
}
</style>
