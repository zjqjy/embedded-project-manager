<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from './components/Sidebar.vue'
import ProjectPanel from './components/ProjectPanel.vue'
import ActionsPanel from './components/ActionsPanel.vue'
import SerialMonitor from './components/SerialMonitor.vue'
import OutputPanel from './components/OutputPanel.vue'
import OperationLog from './components/OperationLog.vue'
import { bridgeState } from './claude/bridge'

const activeView = ref('project')
const permissionMode = ref('interactive')
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
      </div>
    </el-header>

    <!-- 主体区域 -->
    <el-container class="app-body">
      <!-- 侧边栏 -->
      <Sidebar :active="activeView" @select="activeView = $event" />

      <!-- 主内容区 -->
      <el-main class="app-main">
        <ProjectPanel v-if="activeView === 'project'" />
        <ActionsPanel v-else-if="activeView === 'actions'" />
        <SerialMonitor v-else-if="activeView === 'serial'" />

        <!-- 日志输出页面 -->
        <div v-else-if="activeView === 'output'" class="output-page">
          <div class="panel-header">
            <h2>日志输出</h2>
          </div>
          <el-row :gutter="12" class="output-split">
            <el-col :span="16">
              <OutputPanel :text="bridgeState.lastResult" />
            </el-col>
            <el-col :span="8">
              <el-card shadow="never" class="log-sidebar">
                <template #header>
                  <div class="card-header">
                    <el-icon><Document /></el-icon>
                    <span>操作记录</span>
                  </div>
                </template>
                <OperationLog :operations="bridgeState.operations" />
              </el-card>
            </el-col>
          </el-row>
        </div>

        <!-- 设置页面 -->
        <div v-else class="settings-page">
          <div class="panel-header">
            <h2>设置</h2>
          </div>
          <el-card shadow="never">
            <el-form label-width="120px" size="small">
              <el-form-item label="权限模式">
                <el-select v-model="permissionMode" style="width: 200px">
                  <el-option label="交互模式（每次确认）" value="interactive" />
                  <el-option label="通知模式（自动允许）" value="notify" />
                  <el-option label="静默模式（无提示）" value="silent" />
                </el-select>
                <div class="form-tip">
                  控制 Claude 操作文件时的权限行为
                </div>
              </el-form-item>
              <el-divider />
              <el-form-item label="项目路径">
                <el-input
                  :model-value="'D:\\DeskTop\\WorkSpace\\Code\\embedded-project-manager'"
                  disabled
                />
              </el-form-item>
            </el-form>
          </el-card>
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

/* 日志页面布局 */
.output-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.output-split {
  flex: 1;
  overflow: hidden;
}

.output-split :deep(.el-col) {
  height: 100%;
}

.log-sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.log-sidebar :deep(.el-card__body) {
  flex: 1;
  overflow-y: auto;
}

/* 面板公共样式 */
.panel-header h2 {
  margin: 0 0 12px 0;
  font-size: 18px;
  color: #303133;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
}

.form-tip {
  font-size: 12px;
  color: #c0c4cc;
  margin-top: 4px;
}
</style>
