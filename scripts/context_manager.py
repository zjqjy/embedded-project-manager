#!/usr/bin/env python3
"""
嵌入式项目上下文管理器
用于管理项目状态、会话恢复和全局索引
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any


class ProjectContextManager:
    """项目上下文管理器"""
    
    GLOBAL_INDEX_PATH = Path.home() / ".claude" / "embedded-projects-index.md"
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.memory_log_path = self.project_path / "memory-log.md"
        self.project_spec_path = self.project_path / "project-spec.md"
        self.checkpoints_dir = self.project_path / "checkpoints"
        
    def detect_project(self) -> bool:
        """检测当前目录是否为嵌入式项目"""
        return self.memory_log_path.exists() or self.project_spec_path.exists()
    
    def read_memory_log(self) -> Optional[Dict[str, Any]]:
        """读取记忆日志"""
        if not self.memory_log_path.exists():
            return None
        
        content = self.memory_log_path.read_text(encoding="utf-8")
        return self._parse_memory_log(content)
    
    def _parse_memory_log(self, content: str) -> Dict[str, Any]:
        """解析记忆日志内容"""
        result = {
            "project_name": "",
            "project_id": "",
            "current_step": "",
            "step_status": "",
            "retry_count": 0,
            "last_active": "",
            "open_issues": [],
            "next_action": "",
            "session_chain": []
        }
        
        # 提取项目名
        name_match = re.search(r'# 项目记忆日志 - (.+)', content)
        if name_match:
            result["project_name"] = name_match.group(1).strip()
        
        # 提取项目ID
        id_match = re.search(r'\*\*项目ID\*\*: (.+)', content)
        if id_match:
            result["project_id"] = id_match.group(1).strip()
        
        # 提取当前步骤
        step_match = re.search(r'\*\*步骤\*\*: (.+)', content)
        if step_match:
            result["current_step"] = step_match.group(1).strip()
        
        # 提取状态
        status_match = re.search(r'\*\*状态\*\*: (.+)', content)
        if status_match:
            result["step_status"] = status_match.group(1).strip()
        
        # 提取重试次数
        retry_match = re.search(r'第(\d+)次重试', content)
        if retry_match:
            result["retry_count"] = int(retry_match.group(1))
        
        # 提取最后活跃时间
        active_match = re.search(r'\*\*最后活跃\*\*: (.+)', content)
        if active_match:
            result["last_active"] = active_match.group(1).strip()
        
        return result
    
    def generate_session_id(self) -> str:
        """生成会话ID"""
        now = datetime.now()
        return f"sess-{now.strftime('%Y%m%d-%H%M%S')}"
    
    def generate_project_id(self, project_name: str) -> str:
        """生成项目ID"""
        # 将项目名称转换为短ID
        short_name = project_name.lower().replace(" ", "-")[:20]
        now = datetime.now()
        return f"proj-{short_name}-{now.strftime('%y%m%d')}"
    
    def generate_recovery_summary(self) -> str:
        """生成恢复摘要"""
        memory = self.read_memory_log()
        if not memory:
            return "未找到项目记忆日志"
        
        # 计算时间差
        last_active = memory.get("last_active", "未知")
        
        summary = f"""🔍 检测到项目: [{memory.get('project_name', '未知')}]
📍 当前步骤: {memory.get('current_step', '未知')}（第{memory.get('retry_count', 0)}次重试）
⏱️ 最后活跃: {last_active}
📝 待解决问题: {', '.join(memory.get('open_issues', ['无']))}
🎯 下一步行动: {memory.get('next_action', '未知')}

快速命令:
- "继续" → 恢复{memory.get('current_step', '当前')}上下文
- "状态" → 查看详细进度
- "跳过" → 标记完成（不推荐）
- "新建" → 忽略，开始新项目
"""
        return summary
    
    def update_global_index(self, project_info: Dict[str, str]) -> None:
        """更新全局项目索引"""
        # 确保目录存在
        self.GLOBAL_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # 读取现有索引或创建新索引
        if self.GLOBAL_INDEX_PATH.exists():
            content = self.GLOBAL_INDEX_PATH.read_text(encoding="utf-8")
        else:
            content = self._create_default_index()
        
        # 更新项目信息
        content = self._update_project_in_index(content, project_info)
        
        # 写回文件
        self.GLOBAL_INDEX_PATH.write_text(content, encoding="utf-8")
    
    def _create_default_index(self) -> str:
        """创建默认索引内容"""
        return f"""# 嵌入式项目全局索引

> 由 Claude Code - Embedded Project Manager v2 自动生成
> 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 活跃项目

## 最近完成

---

## 全局统计

| 指标 | 数值 |
|------|------|
| 活跃项目数 | 0 |
| 本周完成步骤 | 0 |
| 待解决问题 | 0 |
| 总项目数 | 0 |

---

## 快速命令参考

| 命令 | 说明 |
|------|------|
| `项目索引` | 显示此索引 |
| `恢复项目 <名称>` | 恢复指定项目 |
| `跨项目切换 <名称>` | 保存当前，切换项目 |
| `上下文摘要` | 当前会话摘要 |
"""
    
    def _update_project_in_index(self, content: str, project_info: Dict[str, str]) -> str:
        """在索引中更新项目信息"""
        project_name = project_info.get("name", "未知项目")
        project_short = project_name[:10]
        
        # 检查项目是否已存在
        if project_name in content:
            # 更新现有项目
            pattern = rf"(### \d+\. {re.escape(project_name)}).*?(?=###|\n## |$)"
            replacement = f"""### 1. {project_name}
- **路径**: {project_info.get('path', '')}
- **当前步骤**: {project_info.get('step', '')}
- **最后活跃**: {project_info.get('last_active', datetime.now().strftime('%Y-%m-%d %H:%M'))}
- **待解决**: {project_info.get('issue', '无')}
- **快速恢复**: `恢复项目 {project_short}`

"""
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        else:
            # 添加新项目
            project_entry = f"""### 1. {project_name}
- **路径**: {project_info.get('path', '')}
- **当前步骤**: {project_info.get('step', '')}
- **最后活跃**: {project_info.get('last_active', datetime.now().strftime('%Y-%m-%d %H:%M'))}
- **待解决**: {project_info.get('issue', '无')}
- **快速恢复**: `恢复项目 {project_short}`

"""
            # 插入到活跃项目部分
            content = content.replace(
                "## 活跃项目\n",
                f"## 活跃项目\n\n{project_entry}"
            )
        
        # 更新最后更新时间
        content = re.sub(
            r"> 最后更新: .+",
            f"> 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            content
        )
        
        return content
    
    def save_checkpoint(self, session_id: str, context: Dict[str, Any]) -> None:
        """保存会话检查点"""
        self.checkpoints_dir.mkdir(exist_ok=True)
        
        checkpoint_path = self.checkpoints_dir / f"session-{session_id}.json"
        checkpoint_data = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "project_path": str(self.project_path),
            "context": context
        }
        
        checkpoint_path.write_text(
            json.dumps(checkpoint_data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    
    def load_checkpoint(self, session_id: str) -> Optional[Dict[str, Any]]:
        """加载会话检查点"""
        checkpoint_path = self.checkpoints_dir / f"session-{session_id}.json"
        
        if not checkpoint_path.exists():
            return None
        
        content = checkpoint_path.read_text(encoding="utf-8")
        return json.loads(content)


def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python context_manager.py <命令> [参数]")
        print("命令: detect, summary, update-index, save-checkpoint")
        return
    
    command = sys.argv[1]
    manager = ProjectContextManager()
    
    if command == "detect":
        if manager.detect_project():
            print("检测到嵌入式项目")
            memory = manager.read_memory_log()
            if memory:
                print(f"项目: {memory.get('project_name', '未知')}")
                print(f"当前步骤: {memory.get('current_step', '未知')}")
        else:
            print("未检测到嵌入式项目")
    
    elif command == "summary":
        print(manager.generate_recovery_summary())
    
    elif command == "update-index":
        if len(sys.argv) < 3:
            print("用法: update-index '<json格式的项目信息>'")
            return
        import json
        project_info = json.loads(sys.argv[2])
        manager.update_global_index(project_info)
        print("全局索引已更新")
    
    elif command == "save-checkpoint":
        session_id = manager.generate_session_id()
        context = {"test": "data"}  # 实际使用时传入真实上下文
        manager.save_checkpoint(session_id, context)
        print(f"检查点已保存: {session_id}")
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
