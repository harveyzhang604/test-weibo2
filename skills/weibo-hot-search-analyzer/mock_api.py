#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
微博热搜API模拟服务
提供测试用的热搜数据
"""

from flask import Flask, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# 模拟热搜数据
MOCK_DATA = [
    {
        "title": "OpenAI发布GPT-5",
        "heat": 1580000,
        "tags": "AI 科技 热门",
        "url": "https://weibo.com/hot/openai-gpt5"
    },
    {
        "title": "春节档电影票房破纪录",
        "heat": 1420000,
        "tags": "娱乐 电影 热门",
        "url": "https://weibo.com/hot/spring-movie"
    },
    {
        "title": "新能源汽车降价潮",
        "heat": 1250000,
        "tags": "汽车 经济 热门",
        "url": "https://weibo.com/hot/ev-price"
    },
    {
        "title": "人工智能教育新政策",
        "heat": 1180000,
        "tags": "教育 政策 AI",
        "url": "https://weibo.com/hot/ai-education"
    },
    {
        "title": "职场人健康管理App",
        "heat": 980000,
        "tags": "健康 职场 应用",
        "url": "https://weibo.com/hot/health-app"
    },
    {
        "title": "元宇宙社交平台上线",
        "heat": 920000,
        "tags": "元宇宙 社交 科技",
        "url": "https://weibo.com/hot/metaverse"
    },
    {
        "title": "年轻人的理财新方式",
        "heat": 850000,
        "tags": "理财 年轻人 金融",
        "url": "https://weibo.com/hot/young-finance"
    },
    {
        "title": "智能家居控制系统升级",
        "heat": 780000,
        "tags": "智能家居 物联网 科技",
        "url": "https://weibo.com/hot/smart-home"
    },
    {
        "title": "在线教育新模式探索",
        "heat": 720000,
        "tags": "教育 创新 线上",
        "url": "https://weibo.com/hot/online-education"
    },
    {
        "title": "环保材料重大突破",
        "heat": 680000,
        "tags": "环保 科技 创新",
        "url": "https://weibo.com/hot/green-material"
    },
    {
        "title": "数字藏品交易平台",
        "heat": 620000,
        "tags": "数字藏品 区块链 交易",
        "url": "https://weibo.com/hot/nft-platform"
    },
    {
        "title": "AI绘画工具新功能",
        "heat": 580000,
        "tags": "AI 绘画 创作",
        "url": "https://weibo.com/hot/ai-drawing"
    },
    {
        "title": "心理健康服务普及",
        "heat": 550000,
        "tags": "心理健康 服务 社会",
        "url": "https://weibo.com/hot/mental-health"
    },
    {
        "title": "短视频创作新趋势",
        "heat": 520000,
        "tags": "短视频 创作 媒体",
        "url": "https://weibo.com/hot/video-creation"
    },
    {
        "title": "智慧城市建设项目",
        "heat": 480000,
        "tags": "智慧城市 建设 科技",
        "url": "https://weibo.com/hot/smart-city"
    }
]

@app.route('/hotsearch')
def get_hot_search():
    """返回模拟的热搜数据"""
    return jsonify({
        "code": 0,
        "msg": "success",
        "data": MOCK_DATA,
        "time": datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "ok",
        "message": "Weibo Hot Search Mock API is running"
    })

if __name__ == '__main__':
    print("🚀 微博热搜模拟API服务启动中...")
    print("📍 服务地址: http://localhost:5000")
    print("📊 热搜接口: http://localhost:5000/hotsearch")
    print("💡 提示: 使用 Ctrl+C 停止服务")
    print("-" * 50)

    app.run(host='0.0.0.0', port=5000, debug=True)