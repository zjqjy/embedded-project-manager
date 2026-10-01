# -*- coding: utf-8 -*-
"""测试 Claude CLI 管道通信 - 常驻子进程方案"""
import subprocess
import json
import sys
import os

GIT_BASH = "D:\\ZouJinQiang\\App\\Git\\bin\\bash.exe"
ENV = os.environ.copy()
ENV["CLAUDE_CODE_GIT_BASH_PATH"] = GIT_BASH

def test_p_mode_basic():
    """测试1: -p 模式基础通信"""
    print("=" * 60)
    print("测试1: -p 模式基础通信")
    print("=" * 60)
    try:
        result = subprocess.run(
            ["claude", "-p", "用一句话回复：你好，这是一次管道通信测试", "--output-format", "text"],
            capture_output=True, text=True, timeout=120, env=ENV
        )
        print(f"退出码: {result.returncode}")
        print(f"输出: {result.stdout[:200]}")
        print(f"错误: {result.stderr[:200] if result.stderr else '无'}")
        return result.returncode == 0
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_p_mode_slash_command():
    """测试2: -p 模式调用斜杠命令"""
    print()
    print("=" * 60)
    print("测试2: -p 模式调用 /em stat")
    print("=" * 60)
    try:
        result = subprocess.run(
            ["claude", "-p", "请执行斜杠命令 /em stat，只返回项目名称和当前步骤", "--output-format", "text"],
            capture_output=True, text=True, timeout=120, env=ENV
        )
        print(f"退出码: {result.returncode}")
        if result.stdout:
            # 截取关键信息
            for line in result.stdout.split('\n'):
                if '项目' in line or '当前' in line or '步骤' in line or '状态' in line:
                    print(f"  {line.strip()}")
        print(f"输出总长度: {len(result.stdout)} 字符")
        print(f"错误: {result.stderr[:200] if result.stderr else '无'}")
        return result.returncode == 0 and len(result.stdout) > 0
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_stream_json():
    """测试3: stream-json 流式输出"""
    print()
    print("=" * 60)
    print("测试3: stream-json 流式输出")
    print("=" * 60)
    try:
        result = subprocess.run(
            ["claude", "-p", "回复一句话：管道测试成功", "--output-format", "stream-json", "--verbose"],
            capture_output=True, text=True, timeout=120, env=ENV
        )
        lines = result.stdout.strip().split('\n')
        events = []
        for line in lines:
            if line.strip():
                try:
                    events.append(json.loads(line))
                except:
                    pass

        has_init = any(e.get('type') == 'system' and e.get('subtype') == 'init' for e in events)
        has_stream = any(e.get('type') == 'stream_event' for e in events)
        has_text_delta = False
        for e in events:
            if e.get('type') == 'stream_event':
                ev = e.get('event', {})
                if ev.get('type') == 'content_block_delta':
                    delta = ev.get('delta', {})
                    if delta.get('type') == 'text_delta':
                        has_text_delta = True
                        break

        print(f"总事件数: {len(events)}")
        print(f"包含init事件: {has_init}")
        print(f"包含流式事件: {has_stream}")
        print(f"包含文本增量: {has_text_delta}")

        # 打印 init 中的关键信息
        for e in events:
            if e.get('type') == 'system' and e.get('subtype') == 'init':
                sys_info = e
                print(f"会话ID: {sys_info.get('session_id', 'N/A')}")
                skills = sys_info.get('skills', [])
                has_em = any('EM' in s for s in skills)
                print(f"EM-SKILL已加载: {has_em}")
                break

        return has_init and has_stream
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_session_independence():
    """测试4: 会话独立性（每次-p调用独立）"""
    print()
    print("=" * 60)
    print("测试4: 会话独立性验证")
    print("=" * 60)
    try:
        # 第一次调用：设置值
        r1 = subprocess.run(
            ["claude", "-p", "记住一个临时数字: 77", "--output-format", "text"],
            capture_output=True, text=True, timeout=120, env=ENV
        )
        print(f"第一次调用: {r1.stdout[:100]}")

        # 第二次调用：检查是否能回忆
        r2 = subprocess.run(
            ["claude", "-p", "我刚才让你记住的数字是多少？直接回答数字", "--output-format", "text"],
            capture_output=True, text=True, timeout=120, env=ENV
        )
        print(f"第二次调用: {r2.stdout[:100]}")

        # 如果两次都能正确回复，说明有会话持久化
        cant_remember = "没有" in r2.stdout or "没让" in r2.stdout or "第一次" in r2.stdout or "77" not in r2.stdout
        print(f"结论: 会话独立（无法跨调用恢复上下文）" if cant_remember else "结论: 会话持久化（可跨调用恢复上下文）")
        return cant_remember  # True = 独立
    except Exception as e:
        print(f"错误: {e}")
        return True

def test_claude_path_issue():
    """测试5: 直接传入 /em 前缀的问题"""
    print()
    print("=" * 60)
    print("测试5: /em 直接作为前缀的问题")
    print("=" * 60)
    try:
        result = subprocess.run(
            ["claude", "-p", "/em stat", "--output-format", "text"],
            capture_output=True, text=True, timeout=120, env=ENV
        )
        # 检查是否被当作路径处理
        is_path_error = "path" in result.stdout.lower() or "outside" in result.stdout.lower()
        if is_path_error:
            print("直接传入 /em stat → 被解释为文件路径 ❌")
        else:
            print("直接传入 /em stat → 作为命令执行 ✅")
        print(f"输出预览: {result.stdout[:200]}")
        return is_path_error
    except Exception as e:
        print(f"错误: {e}")
        return True

def test_process_duration():
    """测试6: -p 模式每次调用耗时"""
    import time
    print()
    print("=" * 60)
    print("测试6: -p 模式调用耗时")
    print("=" * 60)
    times = []
    for i in range(3):
        start = time.time()
        try:
            subprocess.run(
                ["claude", "-p", f"回复一个词：测试{i+1}", "--output-format", "text"],
                capture_output=True, text=True, timeout=120, env=ENV
            )
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"  第{i+1}次: {elapsed:.1f}秒")
        except Exception as e:
            print(f"  第{i+1}次: 错误 {e}")
    if times:
        avg = sum(times) / len(times)
        print(f"平均耗时: {avg:.1f}秒")
    return times


if __name__ == "__main__":
    results = {}

    results['basic'] = test_p_mode_basic()
    results['slash'] = test_p_mode_slash_command()
    results['stream'] = test_stream_json()
    results['independent'] = test_session_independence()
    results['path_issue'] = test_claude_path_issue()
    results['duration'] = test_process_duration()

    print()
    print("=" * 60)
    print("技术验证总结")
    print("=" * 60)
    print(f"1. -p模式基础通信:     {'✅' if results['basic'] else '❌'}")
    print(f"2. 斜杠命令支持:       {'✅' if results['slash'] else '❌'}")
    print(f"3. stream-json流式:    {'✅' if results['stream'] else '❌'}")
    print(f"4. 会话独立:           {'✅（每次独立）' if results.get('independent', True) else '❌（持久化）'}")
    print(f"5. 直接/em路径问题:    {'⚠️ 有' if results.get('path_issue', True) else '✅ 无'}")
    if results.get('duration'):
        avg = sum(results['duration']) / len(results['duration'])
        print(f"6. 平均调用耗时:       {avg:.1f}秒")

    print()
    print("关键结论:")
    print("- GUI通信方案: claude -p + stream-json 模式")
    print("- 斜杠命令调用: 需要通过自然语言引导，不能直接传 /em xxx")
    print("- 每次调用独立: 每次-p调用都是全新会话（无上下文）")
    print("- 流式渲染: stream-json 提供逐字输出，可实时渲染到GUI")
    print("- 启动耗时: 约 {:.1f}秒/次（含模型加载）".format(avg if results.get('duration') else 0))
