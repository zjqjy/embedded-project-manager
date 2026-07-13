# 🎓 EM-SKILL Learning Mode

> 以工程化为核心，以项目带动学习。每个主题 = 一张 README 卡片。

## 🌐 学习拓扑图

```mermaid
flowchart TB
    subgraph L1["L1 Learn"]
        A[调研知识] --> B[知识打包]
    end
    subgraph L2["L2 Pack"]
        B --> C[概念图沉淀]
    end
    subgraph L3["L3 Practice"]
        C --> D[编码实现]
    end
    subgraph L4["L4 Verify"]
        D --> E[实战验证]
    end
    subgraph L5["L5 Surface"]
        E --> F[README 卡片]
    end

    F --> G[视频录制]
    G --> H[社区分享]

    style L1 fill:#e1f5fe
    style L5 fill:#fff3e0
```

## 📇 主题卡片墙

| 主题 | 状态 | 复杂度 | 完成日期 | 标签 |
|------|------|--------|----------|------|
| [OTA 固件升级](topics/ota-firmware-upgrade/) | ✅ L5 | 🔴 High | 2026-07-13 | `stm32` `ota` `bootloader` |

## 🔗 知识图谱

```mermaid
graph LR
    A[Bootloader 原理] --> B[OTA 固件升级]
    B --> C[固件签名与验签]
    B --> D[Flash 磨损均衡]
    E[CRC 校验] --> B
    F[中断机制] -.-> B
```

## 📊 学习统计

- **已完成主题**: 1
- **进行中主题**: 0
- **总代码行数**: ~2,400
- **总踩坑记录**: 7

---

*Powered by EM-SKILL v4.1 | [项目主页](https://github.com/zjqjy/embedded-project-manager)*
