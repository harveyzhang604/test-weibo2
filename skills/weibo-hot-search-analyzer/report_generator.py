#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from typing import List, Dict
import argparse
import logging
from jinja2 import Environment, FileSystemLoader
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """HTML报告生成器"""

    def __init__(self, template_path: str):
        """
        初始化报告生成器

        Args:
            template_path: HTML模板文件路径
        """
        self.template_path = template_path
        self.env = Environment(
            loader=FileSystemLoader(os.path.dirname(template_path))
        )

    def generate_report(self, analysis_data: Dict, output_file: str):
        """
        生成HTML报告

        Args:
            analysis_data: 分析结果数据
            output_file: 输出HTML文件路径
        """
        try:
            # 加载模板
            template_name = os.path.basename(self.template_path)
            template = self.env.get_template(template_name)

            # 准备模板数据
            template_data = {
                'date': datetime.now().strftime('%Y年%m月%d日 %H:%M'),
                'total_topics': analysis_data.get('total_topics', 0),
                'excellent_count': analysis_data.get('excellent_count', 0),
                'good_count': analysis_data.get('good_count', 0),
                'avg_score': analysis_data.get('avg_score', 0),
                'topics': analysis_data.get('topics', [])
            }

            # 按分数排序话题（高分在前）
            template_data['topics'].sort(key=lambda x: x.get('score', 0), reverse=True)

            # 渲染HTML
            html_content = template.render(**template_data)

            # 添加自定义CSS和JavaScript增强
            html_content = self._enhance_html(html_content)

            # 保存文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            logger.info(f"HTML报告已生成: {output_file}")

        except Exception as e:
            logger.error(f"生成报告失败: {e}")
            raise

    def _enhance_html(self, html_content: str) -> str:
        """
        增强HTML内容

        Args:
            html_content: 原始HTML内容

        Returns:
            增强后的HTML内容
        """
        # 添加交互功能
        script = """
        <script>
        // 添加一些交互功能
        document.addEventListener('DOMContentLoaded', function() {
            // 展开/收起详情功能
            const sections = document.querySelectorAll('.section');
            sections.forEach(section => {
                const h3 = section.querySelector('h3');
                if (h3) {
                    h3.style.cursor = 'pointer';
                    h3.addEventListener('click', function() {
                        const content = section.querySelector('.event-timeline, .product-idea, .score-breakdown');
                        if (content) {
                            content.style.display = content.style.display === 'none' ? 'block' : 'none';
                        }
                    });
                }
            });

            // 高亮高分创意
            const scoreBadges = document.querySelectorAll('.score-badge');
            scoreBadges.forEach(badge => {
                const score = parseInt(badge.textContent);
                if (score >= 80) {
                    badge.style.animation = 'pulse 2s infinite';
                }
            });

            // 添加打印按钮
            const header = document.querySelector('.header');
            const printBtn = document.createElement('button');
            printBtn.textContent = '🖨️ 打印报告';
            printBtn.style.cssText = `
                position: absolute;
                top: 20px;
                right: 20px;
                padding: 10px 20px;
                background: white;
                color: #667eea;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            `;
            printBtn.onclick = () => window.print();
            header.style.position = 'relative';
            header.appendChild(printBtn);
        });
        </script>

        <style>
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        .score-excellent {
            animation: pulse 2s infinite;
        }

        @media print {
            button { display: none !important; }
        }
        </style>
        """

        # 在</body>标签前插入脚本
        html_content = html_content.replace('</body>', script + '</body>')

        return html_content

    def generate_summary_report(self, analysis_data: Dict) -> str:
        """
        生成摘要报告（Markdown格式）

        Args:
            analysis_data: 分析结果数据

        Returns:
            Markdown格式的摘要报告
        """
        topics = analysis_data.get('topics', [])
        topics_sorted = sorted(topics, key=lambda x: x.get('score', 0), reverse=True)

        markdown = f"""# 微博热搜产品创意分析摘要

## 分析概况
- 分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 分析话题数：{analysis_data.get('total_topics', 0)}
- 优秀创意（80分+）：{analysis_data.get('excellent_count', 0)}
- 良好创意（60-79分）：{analysis_data.get('good_count', 0)}
- 平均得分：{analysis_data.get('avg_score', 0)}

## Top 5 产品创意

"""

        for i, topic in enumerate(topics_sorted[:5]):
            markdown += f"""
### {i+1}. {topic.get('product_name', '')} - {topic.get('score', 0)}分

**来源热搜**：#{topic.get('rank', 0)} {topic.get('title', '')}

**核心功能**：{topic.get('core_function', '')}

**目标用户**：{topic.get('target_users', '')}

**评分详情**：
- 有趣度：{topic.get('interestingness', 0)}/80
- 有用度：{topic.get('usefulness', 0)}/20

**市场分析**：{topic.get('market_analysis', '')}

---

"""

        return markdown


def add_date_to_filename(filename: str, date_str: str = None) -> str:
    """
    给文件名添加日期

    Args:
        filename: 原始文件名
        date_str: 日期字符串，格式为YYMMDD，如果为None则使用当前日期

    Returns:
        带日期的文件名
    """
    if date_str is None:
        date_str = datetime.now().strftime('%y%m%d')

    # 分离文件名和扩展名
    name, ext = os.path.splitext(filename)

    # 在扩展名前插入日期
    return f"{name}_{date_str}{ext}"


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='HTML报告生成工具')
    parser.add_argument('--input', required=True, help='分析结果JSON文件路径')
    parser.add_argument('--output', default='weibo_hotsearch_report.html', help='输出HTML文件路径')
    parser.add_argument('--template', default='report_template.html', help='HTML模板文件路径')
    parser.add_argument('--summary', help='输出Markdown摘要文件路径（可选）')
    parser.add_argument('--no-date', action='store_true', help='不在文件名中添加日期')

    args = parser.parse_args()

    try:
        # 读取分析数据
        with open(args.input, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)

        # 添加日期到文件名（除非指定了--no-date）
        if not args.no_date:
            # 生成日期字符串（YYMMDD格式）
            date_str = datetime.now().strftime('%y%m%d')

            # 更新HTML文件名
            html_output = add_date_to_filename(args.output, date_str)

            # 如果有摘要文件，也添加日期
            summary_output = None
            if args.summary:
                summary_output = add_date_to_filename(args.summary, date_str)
        else:
            html_output = args.output
            summary_output = args.summary

        # 创建报告生成器
        generator = ReportGenerator(args.template)

        # 生成HTML报告
        generator.generate_report(analysis_data, html_output)

        # 生成摘要报告（如果指定）
        if summary_output:
            summary_content = generator.generate_summary_report(analysis_data)
            with open(summary_output, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            logger.info(f"Markdown摘要已生成: {summary_output}")

        print(f"\n报告生成成功")
        print(f"HTML报告: {html_output}")
        if summary_output:
            print(f"Markdown摘要: {summary_output}")

    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        exit(1)


if __name__ == '__main__':
    main()