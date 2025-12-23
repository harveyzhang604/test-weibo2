#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
微博热搜产品创意分析 - 完整运行脚本 v2.0
整合数据获取、智能分析、报告生成的完整流程
"""

import json
import requests
import os
import sys
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import argparse
import logging

# 解决Windows控制台编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 导入智能分析器
from smart_analyzer import SmartAnalyzer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeiboHotSearchPipeline:
    """微博热搜分析完整流程"""

    def __init__(self, api_key: str = None, output_prefix: str = 'weibo_analysis'):
        """
        初始化流程

        Args:
            api_key: 天行数据API密钥
            output_prefix: 输出文件前缀
        """
        self.api_key = api_key or '65f9a968f0869a2d63564093fed9d911'
        self.output_prefix = output_prefix
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # 初始化分析器
        self.analyzer = SmartAnalyzer(self.api_key)

    def fetch_hot_search(self) -> list:
        """获取微博热搜数据"""
        url = f'https://apis.tianapi.com/weibohot/index?key={self.api_key}'

        logger.info("正在获取微博热搜数据...")

        try:
            response = requests.get(url, timeout=15)
            response.encoding = 'utf-8'
            data = response.json()

            if data.get('code') == 200:
                result_list = data.get('result', {}).get('list', [])
                logger.info(f"成功获取 {len(result_list)} 条热搜数据")

                # 转换数据格式
                hot_search_list = []
                for i, item in enumerate(result_list):
                    hot_num = item.get('hotnum', '0')
                    try:
                        if isinstance(hot_num, str):
                            hot_value = int(hot_num.replace(',', '').strip())
                        else:
                            hot_value = int(hot_num)
                    except:
                        hot_value = 0

                    hot_search_list.append({
                        'title': item.get('hotword', ''),
                        'heat': hot_value,
                        'tags': item.get('hottag', '').strip() if item.get('hottag') else '',
                        'rank': i + 1
                    })

                return hot_search_list
            else:
                logger.error(f"API请求失败: {data}")
                return []

        except Exception as e:
            logger.error(f"获取热搜数据失败: {e}")
            return []

    def save_raw_data(self, data: list, filename: str):
        """保存原始数据"""
        output_data = {
            'fetch_time': datetime.now().isoformat(),
            'total_count': len(data),
            'data': data
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        logger.info(f"原始数据已保存到: {filename}")

    def generate_html_report(self, analysis_data: dict, output_file: str):
        """生成HTML报告"""
        template_path = os.path.join(self.base_dir, 'report_template_v2.html')

        env = Environment(loader=FileSystemLoader(self.base_dir))
        template = env.get_template('report_template_v2.html')

        # 准备模板数据
        template_data = {
            'date': datetime.now().strftime('%Y年%m月%d日 %H:%M'),
            'total_topics': analysis_data.get('total_topics', 0),
            'excellent_count': analysis_data.get('excellent_count', 0),
            'good_count': analysis_data.get('good_count', 0),
            'avg_score': analysis_data.get('avg_score', 0),
            'topics': analysis_data.get('topics', [])
        }

        # 渲染HTML
        html_content = template.render(**template_data)

        # 保存文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info(f"HTML报告已生成: {output_file}")

    def generate_markdown_summary(self, analysis_data: dict) -> str:
        """生成Markdown摘要"""
        topics = analysis_data.get('topics', [])

        markdown = f"""# 微博热搜产品创意分析报告

## 📊 分析概况

| 指标 | 数值 |
|------|------|
| 分析时间 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| 分析话题数 | {analysis_data.get('total_topics', 0)} |
| 优秀创意（80分+） | {analysis_data.get('excellent_count', 0)} |
| 良好创意（60-79分） | {analysis_data.get('good_count', 0)} |
| 平均得分 | {analysis_data.get('avg_score', 0)} |

---

## 🏆 Top 5 产品创意

"""

        for i, topic in enumerate(topics[:5]):
            markdown += f"""
### {i+1}. {topic.get('product_name', '')} ({topic.get('score', 0)}分)

**📰 来源热搜**: #{topic.get('rank', 0)} {topic.get('title', '')}

**📂 分类**: {topic.get('category', '')}

**🎯 产品口号**: "{topic.get('product_slogan', '')}"

**💡 核心功能**: {topic.get('core_function', '')}

**👥 目标用户**: {topic.get('target_users', '')}

#### 事件背景
{topic.get('event_summary', '')}

#### 关键要点
"""
            for point in topic.get('key_points', []):
                markdown += f"- {point}\n"

            markdown += """
#### 功能清单
"""
            for feature in topic.get('feature_list', [])[:4]:
                markdown += f"- {feature}\n"

            markdown += f"""
#### 用户痛点
"""
            for pain in topic.get('user_pain_points', [])[:3]:
                markdown += f"- {pain}\n"

            markdown += f"""
#### 解决方案
{topic.get('solution', '')}

#### 商业模式
{topic.get('business_model', '')}

#### 评分详情
- 有趣度: {topic.get('interestingness', 0)}/80
- 有用度: {topic.get('usefulness', 0)}/20
- **总分: {topic.get('score', 0)}/100**

---

"""

        markdown += """
## 📋 完整话题列表

| 排名 | 话题 | 分类 | 产品创意 | 得分 |
|------|------|------|----------|------|
"""
        for topic in topics:
            markdown += f"| #{topic.get('rank', 0)} | {topic.get('title', '')[:20]}... | {topic.get('category', '')} | {topic.get('product_name', '')} | {topic.get('score', 0)}分 |\n"

        markdown += """

---

> 本报告由AI智能分析引擎自动生成，仅供参考。
> 实际产品开发需进行进一步的市场调研、用户访谈和可行性分析。
"""

        return markdown

    def run(self, topics_count: int = 20) -> dict:
        """运行完整流程"""
        # 生成文件名前缀（使用YYMMDD格式，如251222）
        date_prefix = datetime.now().strftime('%y%m%d')
        date_str = date_prefix

        print("\n" + "=" * 60)
        print("🚀 微博热搜产品创意分析 v2.0")
        print("=" * 60 + "\n")

        # 1. 获取热搜数据
        print("📡 步骤1: 获取微博热搜数据...")
        hot_search_data = self.fetch_hot_search()

        if not hot_search_data:
            print("❌ 获取热搜数据失败，请检查网络或API密钥")
            return None

        # 保存原始数据
        data_file = os.path.join(self.base_dir, f'{date_str}_{self.output_prefix}_data.json')
        self.save_raw_data(hot_search_data, data_file)
        print(f"   ✓ 获取到 {len(hot_search_data)} 条热搜数据\n")

        # 2. 智能分析
        print(f"🔍 步骤2: 智能分析热搜话题（分析前 {min(topics_count, len(hot_search_data))} 条）...")
        analysis_results = self.analyzer.analyze_all(hot_search_data[:topics_count])

        # 保存分析结果
        results_file = os.path.join(self.base_dir, f'{date_str}_{self.output_prefix}_results.json')
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=2)
        print(f"   ✓ 分析完成，结果已保存\n")

        # 3. 生成HTML报告
        print("📊 步骤3: 生成可视化HTML报告...")
        html_file = os.path.join(self.base_dir, f'{date_str}_{self.output_prefix}_report.html')
        self.generate_html_report(analysis_results, html_file)
        print(f"   ✓ HTML报告: {html_file}\n")

        # 4. 生成Markdown摘要
        print("📝 步骤4: 生成Markdown摘要报告...")
        markdown_content = self.generate_markdown_summary(analysis_results)
        md_file = os.path.join(self.base_dir, f'{date_str}_{self.output_prefix}_summary.md')
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"   ✓ Markdown摘要: {md_file}\n")

        # 5. 输出统计信息
        print("=" * 60)
        print("✅ 分析完成！")
        print("=" * 60)
        print(f"\n📈 分析统计:")
        print(f"   • 分析话题数: {analysis_results['total_topics']}")
        print(f"   • 优秀创意(80分+): {analysis_results['excellent_count']}")
        print(f"   • 良好创意(60-79分): {analysis_results['good_count']}")
        print(f"   • 平均得分: {analysis_results['avg_score']}")

        print(f"\n🏆 Top 5 产品创意:")
        for i, topic in enumerate(analysis_results['topics'][:5]):
            print(f"   {i+1}. [{topic['score']}分] {topic['product_name']}")
            print(f"      来源: {topic['title'][:30]}...")
            print(f"      口号: {topic['product_slogan']}")

        print(f"\n📁 输出文件:")
        print(f"   • 原始数据: {os.path.basename(data_file)}")
        print(f"   • 分析结果: {os.path.basename(results_file)}")
        print(f"   • HTML报告: {os.path.basename(html_file)}")
        print(f"   • MD摘要: {os.path.basename(md_file)}")
        print()

        return analysis_results


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='微博热搜产品创意分析工具 v2.0')
    parser.add_argument('--api-key', help='天行数据API密钥')
    parser.add_argument('--output', default='weibo_analysis', help='输出文件前缀')
    parser.add_argument('--topics', type=int, default=20, help='分析的话题数量')

    args = parser.parse_args()

    # 创建流程实例
    pipeline = WeiboHotSearchPipeline(
        api_key=args.api_key,
        output_prefix=args.output
    )

    # 运行分析
    pipeline.run(topics_count=args.topics)


if __name__ == '__main__':
    main()
