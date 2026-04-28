<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  'menu-select': [index: string]
}>()

const activeIndex = ref('project')

function handleSelect(index: string) {
  activeIndex.value = index
  emit('menu-select', index)
}
</script>

<template>
  <el-aside width="200px" class="app-sidebar">
    <el-menu
      :default-active="activeIndex"
      @select="handleSelect"
      class="sidebar-menu"
    >
      <el-menu-item index="project">
        <el-icon><DataBoard /></el-icon>
        <span>项目面板</span>
      </el-menu-item>

      <el-menu-item index="actions">
        <el-icon><Monitor /></el-icon>
        <span>快捷操作</span>
      </el-menu-item>

      <el-menu-item index="serial">
        <el-icon><Connection /></el-icon>
        <span>串口监控</span>
      </el-menu-item>

      <el-menu-item index="output">
        <el-icon><ChatDotSquare /></el-icon>
        <span>日志输出</span>
      </el-menu-item>

      <el-menu-item index="settings">
        <el-icon><Setting /></el-icon>
        <span>设置</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<style scoped>
.app-sidebar {
  background: #fff;
  border-right: 1px solid #e4e7ed;
}

.sidebar-menu {
  border-right: none;
}
</style>
