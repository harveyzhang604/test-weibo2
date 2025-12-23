#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict, Optional
import argparse
import logging
import re
from dataclasses import dataclass
from openai import OpenAI

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ProductIdea:
    """产品创意数据结构"""
    name: str
    core_function: str
    target_users: str
    interestingness_score: float  # 有趣度评分 0-80
    usefulness_score: float  # 有用度评分 0-20
    total_score: float  # 总分 0-100
    market_analysis: str
    score_class: str  # excellent, good, fair


class TrendAnalyzer:
    """热搜趋势分析器"""

    def __init__(self, openai_api_key: Optional[str] = None):
        """
        初始化分析器

        Args:
            openai_api_key: OpenAI API密钥，用于AI分析
        """
        self.openai_api_key = openai_api_key
        if openai_api_key:
            self.client = OpenAI(api_key=openai_api_key)

    async def search_topic_info(self, session: aiohttp.ClientSession, topic: str) -> Dict:
        """
        搜索话题相关信息

        Args:
            session: aiohttp会话
            topic: 话题名称

        Returns:
            搜索结果信息
        """
        # 这里使用示例搜索逻辑，实际应用中需要配置真实的搜索API
        search_results = {
            'news': f'关于"{topic}"的相关新闻报道...',
            'background': f'"{topic}"事件的背景信息...',
            'timeline': f'"{topic}"的事件发展时间线...'
        }

        # 模拟网络请求延迟
        await asyncio.sleep(0.5)

        return search_results

    def generate_product_idea(self, topic: Dict, search_info: Dict) -> ProductIdea:
        """
        基于话题和搜索信息生成产品创意

        Args:
            topic: 热搜话题数据
            search_info: 搜索得到的信息

        Returns:
            产品创意
        """
        if self.openai_api_key:
            # 使用OpenAI API生成创意
            return self._generate_with_ai(topic, search_info)
        else:
            # 使用规则引擎生成创意
            return self._generate_with_rules(topic, search_info)

    def _generate_with_ai(self, topic: Dict, search_info: Dict) -> ProductIdea:
        """使用AI生成产品创意"""
        prompt = f"""
        基于以下微博热搜话题，请生成一个创新的产品创意：

        话题：{topic.get('title', '')}
        热度：{topic.get('heat', '')}
        背景：{search_info.get('background', '')}
        相关新闻：{search_info.get('news', '')}

        请从有趣度（80分）和有用度（20分）的角度来评估创意潜力。
        返回JSON格式的结果，包含：
        - product_name: 产品名称
        - core_function: 核心功能
        - target_users: 目标用户
        - interestingness: 有趣度评分（0-80）
        - usefulness: 有用度评分（0-20）
        - market_analysis: 市场机会分析
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的产品创新分析师，擅长从热点中发现产品机会。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )

            result = json.loads(response.choices[0].message.content)

            # 计算总分
            total_score = result.get('interestingness', 0) + result.get('usefulness', 0)

            # 确定评分等级
            if total_score >= 80:
                score_class = 'excellent'
            elif total_score >= 60:
                score_class = 'good'
            else:
                score_class = 'fair'

            return ProductIdea(
                name=result.get('product_name', ''),
                core_function=result.get('core_function', ''),
                target_users=result.get('target_users', ''),
                interestingness_score=result.get('interestingness', 0),
                usefulness_score=result.get('usefulness', 0),
                total_score=total_score,
                market_analysis=result.get('market_analysis', ''),
                score_class=score_class
            )

        except Exception as e:
            logger.error(f"AI生成创意失败: {e}")
            # 降级到规则引擎
            return self._generate_with_rules(topic, search_info)

    def _generate_with_rules(self, topic: Dict, search_info: Dict) -> ProductIdea:
        """使用规则引擎生成产品创意"""
        title = topic.get('title', '').lower()
        heat = topic.get('heat', 0)

        # 基于关键词的规则
        if '雪' in title or '暴雪' in title or '下雪' in title:
            return ProductIdea(
                name="雪天出行助手",
                core_function="实时天气预警+交通路线规划+应急救援服务",
                target_users="司机、户外工作者、通勤族、旅游爱好者",
                interestingness_score=70,
                usefulness_score=18,
                total_score=88,
                market_analysis="恶劣天气下出行安全保障需求强烈，市场空间巨大",
                score_class="excellent"
            )
        elif '手机壳' in title or '手机' in title:
            return ProductIdea(
                name="智能个性化手机壳",
                core_function="可定制外观+智能显示+无线充电+防摔保护",
                target_users="年轻人、时尚爱好者、科技发烧友",
                interestingness_score=75,
                usefulness_score=14,
                total_score=89,
                market_analysis="手机配件市场庞大，个性化需求强烈",
                score_class="excellent"
            )
        elif '经济' in title or '金融' in title or '理财' in title:
            return ProductIdea(
                name="财经热点解读App",
                core_function="实时政策解读+投资建议+经济趋势分析",
                target_users="投资者、创业者、经济研究者、普通用户",
                interestingness_score=60,
                usefulness_score=17,
                total_score=77,
                market_analysis="经济信息需求稳定增长，专业解读有市场",
                score_class="good"
            )
        elif '无人机' in title or '技术突破' in title:
            return ProductIdea(
                name="科技前沿追踪平台",
                core_function="最新科技动态+专业解读+投资机会分析",
                target_users="科技爱好者、投资者、创业者、研究者",
                interestingness_score=72,
                usefulness_score=16,
                total_score=88,
                market_analysis="科技创新关注度持续走高，前沿信息价值高",
                score_class="excellent"
            )
        elif '微信' in title or '群' in title or '聊天' in title:
            return ProductIdea(
                name="社交群管理大师",
                core_function="群聊备份+消息管理+自动回复+数据分析",
                target_users="群主、社群运营者、企业管理者",
                interestingness_score=65,
                usefulness_score=17,
                total_score=82,
                market_analysis="社群经济兴起，群管理需求激增",
                score_class="excellent"
            )
        elif '药品' in title or '健康' in title or '说明书' in title:
            return ProductIdea(
                name="智能药品管家",
                core_function="药品识别+用药提醒+副作用预警+医生咨询",
                target_users="老年人、慢性病患者、忙碌的上班族",
                interestingness_score=68,
                usefulness_score=19,
                total_score=87,
                market_analysis="健康管理需求刚性，智能用药市场前景广阔",
                score_class="excellent"
            )
        elif '故宫' in title or '文物' in title or '文化' in title:
            return ProductIdea(
                name="AR文化导览",
                core_function="AR实景还原+历史故事讲解+互动体验",
                target_users="游客、学生、文化爱好者、亲子家庭",
                interestingness_score=73,
                usefulness_score=15,
                total_score=88,
                score_class="excellent"
            )
        elif '工作' in title or '职场' in title or '单休' in title or '休息' in title:
            return ProductIdea(
                name="职场权益守护者",
                core_function="劳动法规咨询+工时记录+维权帮助+职场社区",
                target_users="上班族、HR、企业管理者、法律工作者",
                interestingness_score=78,
                usefulness_score=18,
                total_score=96,
                market_analysis="职场权益意识提升，法律服务需求增长",
                score_class="excellent"
            )
        elif '综艺' in title or '剧集' in title or '明星' in title:
            return ProductIdea(
                name="娱乐内容聚合平台",
                core_function="热门内容推荐+观看计划+粉丝社区+周边商城",
                target_users="年轻人、追剧族、粉丝群体",
                interestingness_score=66,
                usefulness_score=13,
                total_score=79,
                market_analysis="娱乐内容消费旺盛，粉丝经济潜力巨大",
                score_class="good"
            )
        elif '键盘' in title or '输入' in title:
            return ProductIdea(
                name="智能输入助手",
                core_function="AI预测输入+多语言支持+表情推荐+快捷短语",
                target_users="手机用户、办公人员、多语言使用者",
                interestingness_score=62,
                usefulness_score=16,
                total_score=78,
                market_analysis="输入是基础需求，效率提升工具价值高",
                score_class="good"
            )
        else:
            # 默认创意
            return ProductIdea(
                name="热点追踪器",
                core_function="实时监控和分析社交媒体热点趋势",
                target_users="市场营销人员、内容创作者、研究人员",
                interestingness_score=55,
                usefulness_score=16,
                total_score=71,
                market_analysis="社交媒体监控工具需求稳定",
                score_class="good"
            )

    async def analyze_topics(self, topics: List[Dict]) -> List[Dict]:
        """
        分析话题列表

        Args:
            topics: 热搜话题列表

        Returns:
            分析结果列表
        """
        results = []

        async with aiohttp.ClientSession() as session:
            tasks = []
            for i, topic in enumerate(topics[:20]):  # 限制处理前20个
                task = self._analyze_single_topic(session, topic, i + 1)
                tasks.append(task)

            results = await asyncio.gather(*tasks)

        return results

    async def _analyze_single_topic(self, session: aiohttp.ClientSession, topic: Dict, rank: int) -> Dict:
        """分析单个话题"""
        try:
            title = topic.get('title', '')
            logger.info(f"正在分析话题 #{rank}: {title}")

            # 搜索相关信息
            search_info = await self.search_topic_info(session, title)

            # 生成产品创意
            product_idea = self.generate_product_idea(topic, search_info)

            # 构建结果
            result = {
                'rank': rank,
                'title': title,
                'heat_value': topic.get('heat', 0),
                'tags': topic.get('tags', ''),
                'event_timeline': self._generate_timeline(search_info),
                'product_name': product_idea.name,
                'core_function': product_idea.core_function,
                'target_users': product_idea.target_users,
                'interestingness': product_idea.interestingness_score,
                'usefulness': product_idea.usefulness_score,
                'score': product_idea.total_score,
                'score_class': product_idea.score_class,
                'market_analysis': product_idea.market_analysis
            }

            logger.info(f"话题 #{rank} 分析完成，得分: {product_idea.total_score}")
            return result

        except Exception as e:
            logger.error(f"分析话题失败: {e}")
            return None

    def _generate_timeline(self, search_info: Dict) -> str:
        """生成事件时间线"""
        # 这里可以根据实际搜索结果生成更详细的时间线
        timeline = search_info.get('timeline', '事件发展脉络...')

        # 添加一些时间点
        return f"""
        <ul>
            <li>事件起始：相关信息开始出现</li>
            <li>发展过程：逐步引发关注</li>
            <li>热点形成：登上微博热搜</li>
            <li>当前状态：{timeline[:100]}...</li>
        </ul>
        """

    def save_results(self, results: List[Dict], output_file: str):
        """保存分析结果"""
        # 过滤空结果
        valid_results = [r for r in results if r is not None]

        # 添加统计信息
        total_count = len(valid_results)
        excellent_count = sum(1 for r in valid_results if r['score'] >= 80)
        good_count = sum(1 for r in valid_results if 60 <= r['score'] < 80)
        avg_score = sum(r['score'] for r in valid_results) / total_count if total_count > 0 else 0

        output_data = {
            'analysis_time': datetime.now().isoformat(),
            'total_topics': total_count,
            'excellent_count': excellent_count,
            'good_count': good_count,
            'avg_score': round(avg_score, 1),
            'topics': valid_results
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        logger.info(f"分析结果已保存到: {output_file}")


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='微博热搜趋势分析工具')
    parser.add_argument('--input', required=True, help='热搜数据文件路径')
    parser.add_argument('--output', default='analysis_results.json', help='输出文件路径')
    parser.add_argument('--openai-key', help='OpenAI API密钥')

    args = parser.parse_args()

    try:
        # 读取热搜数据
        with open(args.input, 'r', encoding='utf-8') as f:
            hot_search_data = json.load(f)

        topics = hot_search_data.get('data', [])
        logger.info(f"加载了 {len(topics)} 个热搜话题")

        # 创建分析器
        analyzer = TrendAnalyzer(args.openai_key)

        # 分析话题
        results = await analyzer.analyze_topics(topics)

        # 保存结果
        analyzer.save_results(results, args.output)

        print(f"\n✅ 分析完成")
        print(f"📊 分析了 {len(results)} 个话题")
        print(f"📁 结果已保存到: {args.output}")

    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        exit(1)


if __name__ == '__main__':
    asyncio.run(main())