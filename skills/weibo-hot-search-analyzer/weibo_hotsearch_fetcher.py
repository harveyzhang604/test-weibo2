#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import argparse
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeiboHotSearchFetcher:
    """微博热搜数据抓取器"""

    def __init__(self, api_url: str):
        """
        初始化抓取器

        Args:
            api_url: 微博热搜API地址
        """
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_hot_search(self) -> List[Dict]:
        """
        获取微博热搜数据

        Returns:
            热搜列表数据
        """
        try:
            logger.info(f"正在获取微博热搜数据: {self.api_url}")
            response = self.session.get(self.api_url, timeout=10)
            response.raise_for_status()

            data = response.json()

            # 根据实际API响应格式解析数据
            if isinstance(data, dict) and 'data' in data and isinstance(data['data'], dict) and 'result' in data['data'] and 'list' in data['data']['result']:
                # 天API格式
                raw_list = data['data']['result']['list']
                hot_search_list = []
                for i, item in enumerate(raw_list):
                    # 清理热度数值
                    hot_num = item.get('hotwordnum', '0').strip()
                    # 移除类别前缀如"剧集 "
                    if ' ' in hot_num and hot_num.split(' ')[0].isdigit():
                        hot_num = hot_num.split(' ')[0]
                    # 转换为数字
                    try:
                        hot_value = int(hot_num.replace(',', ''))
                    except:
                        hot_value = 0

                    hot_search_list.append({
                        'title': item.get('hotword', ''),
                        'heat': hot_value,
                        'tags': item.get('hottag', '').strip(),
                        'rank': i + 1
                    })
            elif isinstance(data, dict) and 'data' in data:
                hot_search_list = data['data']
            else:
                hot_search_list = data

            logger.info(f"成功获取 {len(hot_search_list)} 条热搜数据")
            return hot_search_list

        except requests.RequestException as e:
            logger.error(f"请求失败: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            raise
        except Exception as e:
            logger.error(f"获取热搜数据时发生错误: {e}")
            raise

    def save_data(self, data: List[Dict], output_file: str):
        """
        保存数据到文件

        Args:
            data: 热搜数据
            output_file: 输出文件路径
        """
        try:
            # 添加元数据
            output_data = {
                'fetch_time': datetime.now().isoformat(),
                'total_count': len(data),
                'data': data
            }

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)

            logger.info(f"数据已保存到: {output_file}")

        except Exception as e:
            logger.error(f"保存数据时发生错误: {e}")
            raise


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='微博热搜数据抓取工具')
    parser.add_argument('--api-url', required=True, help='微博热搜API地址')
    parser.add_argument('--output', default='hot_search_data.json', help='输出文件路径')
    parser.add_argument('--delay', type=int, default=1, help='请求间隔（秒）')

    args = parser.parse_args()

    try:
        # 创建抓取器
        fetcher = WeiboHotSearchFetcher(args.api_url)

        # 获取热搜数据
        hot_search_data = fetcher.fetch_hot_search()

        # 保存数据
        fetcher.save_data(hot_search_data, args.output)

        print(f"\n✅ 成功抓取 {len(hot_search_data)} 条热搜数据")
        print(f"📁 数据已保存到: {args.output}")

    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        exit(1)


if __name__ == '__main__':
    main()