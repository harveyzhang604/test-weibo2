#---
name: weibo-hotsearch
description: "微博热搜产品创意分析工具。当用户需要分析微博热搜趋势、从社交媒体热点中提取产品创意、或生成热搜分析报告时使用。Use when user says: '分析微博热搜', '热搜产品创意', '微博趋势分析', 'analyze Weibo trends', '/weibo-hotsearch'"
license: MIT
invocation:
  - /weibo-hotsearch
---

# 微博热搜产品创意分析 (Weibo Hot Search Product Innovation Analyzer)

## 概述

这个skill自动完成以下工作流程：
1. 通过API抓取微博热搜榜单数据
2. 对每个热搜话题进行Web搜索，获取详细背景信息
3. 使用AI分析每个热点，提取产品创意并评分
4. 生成专业的HTML分析报告

## 执行流程

### 第一步：获取微博热搜数据

**首先询问用户API地址**，然后使用WebFetch工具获取数据：

```
用户需提供微博热搜API地址，格式如：
https://api.example.com/weibo/hotsearch
```

**API数据处理**：
- 提取热搜标题、排名、热度值
- 限制分析前10-20条热搜（可根据用户需求调整）
- 保存原始数据到 `weibo_hotsearch_raw.json`

### 第二步：深度搜索每个热搜话题

对每个热搜话题，使用 **WebSearch** 工具搜索：

```markdown
搜索策略：
1. 搜索词：热搜标题 + "新闻" 或 "事件"
2. 获取3-5条相关新闻和背景信息
3. 提取关键信息：
   - 事件起因和经过
   - 涉及人物/机构
   - 公众反应和讨论焦点
   - 相关行业影响
```

**输出格式**（每个热搜）：
```json
{
  "rank": 1,
  "title": "热搜标题",
  "heat": "热度值",
  "background": {
    "summary": "事件概述",
    "timeline": "时间线",
    "key_points": ["关键点1", "关键点2"],
    "public_sentiment": "公众情绪分析",
    "sources": ["来源1", "来源2"]
  }
}
```

### 第三步：AI产品创意分析

对每个热搜进行产品创意分析，评分标准：

#### 评分维度
| 维度 | 权重 | 评估要点 |
|------|------|----------|
| 有趣度 | 80分 | 创意新颖性、话题吸引力、病毒传播潜力、用户参与度 |
| 有用度 | 20分 | 实际问题解决、市场需求、商业可行性、技术实现难度 |
| **总分** | **100分** | 有趣度 + 有用度 |

#### 评级标准
- **优秀 (80-100分)**: 🌟 高创新潜力，强烈推荐开发
- **良好 (60-79分)**: ✅ 中等机会，值得进一步探索
- **一般 (<60分)**: 📝 需要改进，暂时观望

#### 产品创意输出格式
```json
{
  "product_idea": {
    "name": "产品名称（创意、易记）",
    "core_features": [
      "核心功能1：描述",
      "核心功能2：描述",
      "核心功能3：描述"
    ],
    "target_users": {
      "demographics": "年龄、性别、地域特征",
      "behaviors": "用户行为特点",
      "pain_points": "解决的痛点",
      "scenarios": "使用场景"
    },
    "innovation_points": "创新亮点说明"
  },
  "scoring": {
    "interestingness": 75,
    "usefulness": 18,
    "total": 93,
    "rating": "优秀",
    "reasoning": "评分理由说明"
  }
}
```

### 第四步：生成HTML报告

生成文件名格式：`weibo_analysis_report_YYMMDD.html`

#### HTML报告结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>微博热搜产品创意分析报告 - {日期}</title>
    <style>
        /* 样式规范 */
        :root {
            --excellent-color: #10b981;  /* 优秀 - 绿色 */
            --good-color: #f59e0b;       /* 良好 - 橙色 */
            --normal-color: #6b7280;     /* 一般 - 灰色 */
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 2rem;
        }

        .report-header {
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 16px;
        }

        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .topic-card {
            background: var(--card-bg);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }

        .topic-card:hover {
            transform: translateY(-2px);
        }

        .topic-card.excellent {
            border-left: 5px solid var(--excellent-color);
            background: linear-gradient(90deg, #ecfdf5 0%, var(--card-bg) 20%);
        }

        .topic-card.good {
            border-left: 5px solid var(--good-color);
            background: linear-gradient(90deg, #fffbeb 0%, var(--card-bg) 20%);
        }

        .score-badge {
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.2rem;
        }

        .score-badge.excellent {
            background: var(--excellent-color);
            color: white;
        }

        .score-badge.good {
            background: var(--good-color);
            color: white;
        }

        .timeline {
            border-left: 3px solid #e2e8f0;
            padding-left: 1.5rem;
            margin: 1rem 0;
        }

        .product-idea {
            background: #f1f5f9;
            border-radius: 12px;
            padding: 1.5rem;
            margin-top: 1rem;
        }

        .feature-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .feature-tag {
            background: #e0e7ff;
            color: #3730a3;
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.875rem;
        }

        .target-users {
            background: #fef3c7;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
        }

        @media print {
            .topic-card { break-inside: avoid; }
        }
    </style>
</head>
<body>
    <header class="report-header">
        <h1>微博热搜产品创意分析报告</h1>
        <p>生成日期：{YYYY年MM月DD日}</p>
        <p>分析热搜数量：{N}条</p>
    </header>

    <section class="summary-stats">
        <div class="stat-card">
            <h3>优秀创意</h3>
            <p class="stat-number">{优秀数量}</p>
        </div>
        <div class="stat-card">
            <h3>良好创意</h3>
            <p class="stat-number">{良好数量}</p>
        </div>
        <div class="stat-card">
            <h3>平均得分</h3>
            <p class="stat-number">{平均分}</p>
        </div>
    </section>

    <!-- 热搜分析列表，按得分降序排列 -->
    <section class="topic-list">
        <!-- 每个热搜话题卡片 -->
        <article class="topic-card {rating-class}">
            <header>
                <span class="rank">#{排名}</span>
                <h2>{热搜标题}</h2>
                <span class="heat">🔥 {热度}</span>
                <span class="score-badge {rating-class}">{总分}分 - {评级}</span>
            </header>

            <section class="background">
                <h3>📰 事件背景</h3>
                <p>{事件概述}</p>
                <div class="timeline">
                    <h4>事件脉络</h4>
                    <!-- 时间线内容 -->
                </div>
            </section>

            <section class="product-idea">
                <h3>💡 产品创意</h3>
                <h4>{产品名称}</h4>
                <div class="feature-list">
                    <!-- 核心功能标签 -->
                </div>
                <div class="target-users">
                    <h5>🎯 目标用户</h5>
                    <p>{目标用户描述}</p>
                </div>
            </section>

            <section class="scoring-detail">
                <h3>📊 评分详情</h3>
                <p>有趣度：{有趣度分数}/80</p>
                <p>有用度：{有用度分数}/20</p>
                <p>评分理由：{reasoning}</p>
            </section>
        </article>
    </section>
</body>
</html>
```

## 完整执行示例

当用户说 "分析微博热搜" 或 "/weibo-hotsearch" 时：

### 1. 确认API地址
```
请提供微博热搜API地址，我将为您获取最新的热搜数据进行分析。

示例API格式：https://api.example.com/weibo/hotsearch
```

### 2. 获取数据后确认
```
已获取到 {N} 条微博热搜数据。
前5条热搜：
1. {标题1} - 热度 {xxx}万
2. {标题2} - 热度 {xxx}万
...

是否开始进行深度分析？（默认分析前10条）
```

### 3. 执行分析
对每条热搜：
- 显示进度：`正在分析第 {n}/{total} 条：{标题}`
- 执行WebSearch搜索背景
- 生成产品创意和评分

### 4. 输出结果
```
✅ 分析完成！

📊 报告概览：
- 优秀创意（80+分）：{n}个
- 良好创意（60-79分）：{n}个
- 平均得分：{avg}分

🏆 TOP 3 产品创意：
1. {产品名} - {分数}分 ⭐优秀
2. {产品名} - {分数}分 ⭐优秀
3. {产品名} - {分数}分 ✅良好

📄 完整报告已保存：weibo_analysis_report_{YYMMDD}.html
```

## 注意事项

1. **API兼容性**：支持返回JSON格式的热搜API
2. **搜索限制**：Web搜索可能有频率限制，建议每条热搜间隔搜索
3. **评分客观性**：评分基于AI分析，建议人工复核高分创意
4. **数据时效性**：热搜数据变化快，建议当天分析当天数据

## 输出文件

| 文件名 | 说明 |
|--------|------|
| `weibo_hotsearch_raw.json` | 原始热搜数据 |
| `weibo_analysis_data.json` | 分析结果数据 |
| `weibo_analysis_report_{YYMMDD}.html` | HTML分析报告 |
| `weibo_analysis_summary_{YYMMDD}.md` | Markdown摘要 |
