#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
微博热搜产品创意分析 - 简化演示版
使用预设数据进行演示分析
"""

import os
import sys
import subprocess
from datetime import datetime

def main():
    """主执行函数"""
    print("\n" + "="*80)
    print("微博热搜产品创意分析（演示版）")
    print("="*80)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("使用预设数据进行演示...")
    print("="*80 + "\n")

    # 切换到项目根目录
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # 使用预设的分析数据
    demo_data = "weibo_hotsearch_formatted.json"
    output_prefix = "demo"

    # 检查演示数据是否存在
    if not os.path.exists(demo_data):
        print(f"[错误] 演示数据文件不存在: {demo_data}")
        print("请先运行完整的分析生成演示数据")
        return

    print("\n[信息] 使用演示数据:", demo_data)

    # 运行分析
    print("\n[运行] 分析热搜并生成产品创意...")
    cmd1 = [sys.executable, "skills/weibo-hot-search-analyzer/trend_analyzer.py",
            "--input", demo_data,
            "--output", f"{output_prefix}_analysis.json"]

    try:
        result = subprocess.run(cmd1, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("[成功] 分析完成")
        else:
            print("[警告] 分析有警告")
    except Exception as e:
        print(f"[错误] 分析失败: {e}")
        return

    # 生成报告（会自动添加日期）
    print("\n[运行] 生成可视化报告（自动添加日期）...")
    cmd2 = [sys.executable, "skills/weibo-hot-search-analyzer/report_generator.py",
            "--input", f"{output_prefix}_analysis.json",
            "--output", f"{output_prefix}_report.html",
            "--template", "skills/weibo-hot-search-analyzer/report_template.html",
            "--summary", f"{output_prefix}_summary.md"]

    try:
        result = subprocess.run(cmd2, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("[成功] 报告生成完成")
        else:
            print("[警告] 报告生成有警告")
    except Exception as e:
        print(f"[错误] 报告生成失败: {e}")
        return

    # 显示结果
    from datetime import datetime
    date_str = datetime.now().strftime('%y%m%d')

    print("\n" + "="*80)
    print("演示完成！")
    print("="*80)
    print("\n生成的文件（已自动添加日期）:")
    print(f"1. demo_report_{date_str}.html - 可视化分析报告")
    print(f"2. demo_summary_{date_str}.md - 创意摘要")
    print("\n打开HTML报告查看详细分析结果")

    print("\n" + "="*80)
    print("提示：")
    print(f"- 文件名已添加日期标识: {date_str}")
    print("- 这是演示版本，使用预设数据")
    print("- 实际使用请配置API密钥")
    print("- 运行 /weibo-hotsearch 获取完整功能")
    print("- 如需禁用日期后缀，使用 --no-date 参数")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()