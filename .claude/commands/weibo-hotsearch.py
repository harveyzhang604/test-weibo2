#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
微博热搜产品创意分析 - 斜杠命令执行脚本
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime

# 默认配置
DEFAULT_API_KEY = "65f9a968f0869a2d63564093fed9d911"
WEIBO_API_URL = "https://apis.tianapi.com/weibohot/index"
DEFAULT_OUTPUT_PREFIX = "weibo_analysis"
DEFAULT_TOPICS = 20

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='微博热搜产品创意分析')

    parser.add_argument('--api-key',
                       default=DEFAULT_API_KEY,
                       help=f'天行数据API密钥 (默认: {DEFAULT_API_KEY[:10]}...)')

    parser.add_argument('--openai-key',
                       help='OpenAI API密钥 (可选，使用AI分析时需要)')

    parser.add_argument('--output',
                       default=DEFAULT_OUTPUT_PREFIX,
                       help=f'输出文件前缀 (默认: {DEFAULT_OUTPUT_PREFIX})')

    parser.add_argument('--topics',
                       type=int,
                       default=DEFAULT_TOPICS,
                       help=f'分析的话题数量 (默认: {DEFAULT_TOPICS})')

    return parser.parse_args()

def run_command(cmd, description):
    """运行命令并返回结果"""
    print(f"\n{'='*60}")
    print(f"[运行] {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            print("[成功] 操作完成")
        else:
            print(f"[警告] 操作完成，返回码: {result.returncode}")

        return result.returncode == 0
    except Exception as e:
        print(f"[错误] {str(e)}")
        return False

def main():
    """主执行函数"""
    # 解析参数
    args = parse_arguments()

    # 显示启动信息
    print("\n" + "="*80)
    print("微博热搜产品创意分析系统")
    print("="*80)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"分析话题数: {args.topics}")
    print(f"输出前缀: {args.output}")
    if args.openai_key:
        print("分析模式: AI驱动")
    else:
        print("分析模式: 规则引擎")
    print("="*80 + "\n")

    # 构建文件路径
    skills_dir = "skills/weibo-hot-search-analyzer"

    # 获取项目根目录（斜杠命令执行时的当前目录）
    base_dir = os.getcwd()

    fetcher_script = os.path.join(base_dir, skills_dir, "weibo_hotsearch_fetcher.py")
    analyzer_script = os.path.join(base_dir, skills_dir, "trend_analyzer.py")
    reporter_script = os.path.join(base_dir, skills_dir, "report_generator.py")
    template_file = os.path.join(base_dir, skills_dir, "report_template.html")

    # 构建输出文件路径
    # 注意：HTML和Markdown文件会自动添加日期后缀
    data_file = f"{args.output}_data.json"
    analysis_file = f"{args.output}_results.json"
    html_report = f"{args.output}_report.html"  # 会被自动添加日期，如: weibo_analysis_report_251212.html
    md_summary = f"{args.output}_summary.md"    # 会被自动添加日期，如: weibo_analysis_summary_251212.md

    # 构建API URL
    api_url = f"{WEIBO_API_URL}?key={args.api_key}"

    # 步骤1: 获取热搜数据
    success = run_command(
        [sys.executable, fetcher_script,
         "--api-url", api_url,
         "--output", data_file],
        "步骤1: 获取微博热搜数据"
    )

    if not success:
        print("\n[错误] 获取热搜数据失败！")
        print("可能原因：")
        print("1. 网络连接问题")
        print("2. API密钥无效或已达限制")
        return

    # 步骤2: 运行分析
    analyzer_cmd = [sys.executable, analyzer_script,
                   "--input", data_file,
                   "--output", analysis_file]

    if args.openai_key:
        analyzer_cmd.extend(["--openai-key", args.openai_key])

    success = run_command(
        analyzer_cmd,
        "步骤2: 分析热搜并生成产品创意"
    )

    if not success:
        print("\n[错误] 趋势分析失败！")
        return

    # 步骤3: 生成报告（默认会自动添加日期）
    success = run_command(
        [sys.executable, reporter_script,
         "--input", analysis_file,
         "--output", html_report,
         "--template", template_file,
         "--summary", md_summary],
        "步骤3: 生成可视化报告（自动添加日期）"
    )

    if not success:
        print("\n[错误] 报告生成失败！")
        return

    # 步骤4: 显示结果摘要
    print("\n" + "="*80)
    print("分析结果摘要")
    print("="*80)

    try:
        # 读取分析结果
        result_path = os.path.join(base_dir, analysis_file)
        with open(result_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"\n统计信息:")
        print(f"  - 分析话题数: {data.get('total_topics', 0)}")
        print(f"  - 优秀创意(80分+): {data.get('excellent_count', 0)}")
        print(f"  - 良好创意(60-79分): {data.get('good_count', 0)}")
        print(f"  - 平均得分: {data.get('avg_score', 0)}")

        # 显示Top 5创意
        topics = sorted(data.get('topics', []),
                       key=lambda x: x.get('score', 0),
                       reverse=True)[:5]

        print(f"\nTop 5 产品创意:")
        for i, topic in enumerate(topics, 1):
            print(f"\n{i}. {topic.get('product_name', '')} - {topic.get('score', 0)}分")
            print(f"   来源: #{topic.get('rank', 0)} {topic.get('title', '')}")
            print(f"   功能: {topic.get('core_function', '')}")

    except Exception as e:
        print(f"\n[警告] 无法读取分析结果: {e}")

    # 步骤5: 输出文件信息
    print("\n" + "="*80)
    print("生成的文件")
    print("="*80)

    # 获取日期字符串
    date_str = datetime.now().strftime('%y%m%d')

    output_files = [
        (data_file, "原始热搜数据"),
        (analysis_file, "分析结果"),
        (f"{args.output}_report_{date_str}.html", "HTML报告（带日期）"),
        (f"{args.output}_summary_{date_str}.md", "Markdown摘要（带日期）")
    ]

    for filename, desc in output_files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"  ✓ {filename} - {desc} ({size} bytes)")
        else:
            print(f"  ✗ {filename} - {desc} (未生成)")

    # 步骤6: 提示信息
    print("\n" + "="*80)
    print("提示")
    print("="*80)
    print("1. 打开HTML报告查看完整可视化分析")
    print(f"   文件路径: {os.path.join(base_dir, args.output)}_report_{date_str}.html")
    print("\n2. Markdown摘要适合快速分享")
    print(f"   文件路径: {os.path.join(base_dir, args.output)}_summary_{date_str}.md")
    print("\n3. 文件名已自动添加日期标识（格式：YYMMDD）")
    print(f"   今天的日期: {date_str}")
    print("\n4. 使用AI分析可获得更精准的创意")
    print("   /weibo-hotsearch --openai-key=你的OpenAI密钥")
    print("\n5. 如需禁用日期后缀，使用 --no-date 参数")

    print("\n" + "="*80)
    print("分析完成！")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()