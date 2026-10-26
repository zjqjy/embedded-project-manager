# 命令: /em vault (vault 连接与状态)

## 功能
把任意项目连接到知识库 vault（一次配置全局生效），查看连接状态与入库摘要。

## 触发
```
/em vault connect <vault路径>    # 连接（自检后写 ~/.em/config.json）
/em vault status                 # 连接状态
/em vault briefing               # 近 7 天入库摘要（含待确认卡数）
```

## connect 执行流程

1. 路径自检（脚本内做）：目录存在 + 含 `AGENTS.md` 或 `30_方法论/`
2. 写 `~/.em/config.json`：
   ```bash
   python "<SKILL_DIR>/tools/vault/em_config.py" --set <路径>
   ```
   > 若 em_config.py 无 --set 入口，直接让用户/AI 写入 JSON：
   > `{"vault_path": "<绝对路径>"}`
3. 报告：
   ```
   🔗 vault 已连接: <路径>
      快捕区: 08_快捕/（现有 N 张卡）
      下次起 /em note、/em ask 直接可用
   ```

## status

读 `~/.em/config.json` + 校验路径存活；未配置则提示 connect。附带统计：`08_快捕/` 各 status 卡数。

## briefing

```bash
python "<SKILL_DIR>/tools/vault/search.py" briefing
```
输出近 7 天入库列表 + 快捕/待确认/已归档计数 + vault 最近 commit。

## 设计原则
- 配置文件只有一项 `vault_path`——多机各自 connect 本机路径（EM-SKILL 多设备约定不冲突）
- 不存密钥、不存其他状态；分拣状态在 `~/.em/triage_state.json`（hook 自动维护）

## 相关文件
- `tools/vault/em_config.py` / `search.py`
