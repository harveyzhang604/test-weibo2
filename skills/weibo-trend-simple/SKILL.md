#---
name: weibo-trend-simple
description: "微博热搜产品创意分析（简化版）。快速分析微博热搜并生成产品创意报告。Use when: '/weibo-trend-simple', '快速分析热搜', '简单热搜分析'"
license: MIT
invocation:
  - /weibo-trend-simple
---

# 微博热搜产品创意快速分析

## 快速执行流程

### Step 1: 获取热搜数据
```
请提供微博热搜API地址
```

使用WebFetch获取数据，提取前10条热搜。

### Step 2: 快速分析（每条热搜）

对每条热搜执行：
1. **WebSearch** 搜索 "{热搜标题} 新闻 事件"
2. 提取关键信息（1-2句话概述）
3. 生成产品创意：
   - 名称
   - 核心功能（3个）
   - 目标用户
4. 评分（有趣度80 + 有用度20 = 100）

### Step 3: 生成HTML报告

文件名：`weibo_report_{YYMMDD}.html`

**评级样式**：
- 🌟 优秀(80+)：绿色高亮边框
- ✅ 良好(60-79)：橙色边框
- 📝 一般(<60)：普通样式

**报告内容**：
```html
<div class="card {rating}">
  <h2>#{排名} {标题}</h2>
  <p class="score">{分数}分 - {评级}</p>
  <div class="background">{事件概述}</div>
  <div class="product">
    <h3>💡 {产品名}</h3>
    <ul>{核心功能列表}</ul>
    <p>🎯 {目标用户}</p>
  </div>
</div>
```

## HTML模板样式

```css
.card { padding: 20px; margin: 15px 0; border-radius: 12px; }
.card.excellent { border-left: 5px solid #10b981; background: #ecfdf5; }
.card.good { border-left: 5px solid #f59e0b; background: #fffbeb; }
.score { font-size: 1.5em; font-weight: bold; }
```

## 输出示例

```
✅ 分析完成！共分析 10 条热搜

🏆 优秀创意 (3个)：
1. AI陪聊助手 - 92分
2. 情绪追踪器 - 85分
3. 趋势预测APP - 81分

📄 报告：weibo_report_241222.html
```
