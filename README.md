# 微博热搜产品创意分析工具

> 基于 AI 的微博热搜趋势分析与产品创新创意生成工具

## 项目简介

本项目通过分析微博热搜榜单，自动提取产品创新机会并生成专业的分析报告。利用 AI 技术深度挖掘热点话题背后的用户需求和市场趋势，为产品创新提供数据支持。

## 功能特性

- 🔥 **自动抓取热搜数据** - 通过 API 获取实时微博热搜榜单
- 🔍 **智能话题研究** - 自动搜索和整理每个话题的背景信息
- 💡 **AI 创意生成** - 基于热搜趋势生成产品创新概念
- 📊 **多维度评分系统** - 有趣度(80%) + 有用度(20%) 智能评分
- 📈 **专业报告输出** - 生成 HTML 可视化报告和 Markdown 摘要

## 项目结构

```
test-weibo2/
├── .claude/
│   └── commands/              # Claude Code 命令定义
│       ├── weibo-hotsearch.md
│       ├── weibo-hotsearch.py
│       ├── weibo-trend-simple.md
│       └── weibo-trend-simple.py
├── skills/
│   ├── weibo-hot-search-analyzer/  # 核心分析工具
│   │   ├── run_analysis.py         # 主运行脚本
│   │   ├── smart_analyzer.py       # 智能分析引擎
│   │   ├── trend_analyzer.py       # 趋势分析器
│   │   ├── weibo_hotsearch_fetcher.py  # 数据抓取
│   │   ├── report_generator.py     # 报告生成器
│   │   ├── report_template_v2.html # HTML 报告模板
│   │   ├── config.json             # 配置文件
│   │   └── requirements.txt        # Python 依赖
│   ├── weibo-hotsearch/            # Skill 定义
│   └── weibo-trend-simple/         # 简化版 Skill
└── README.md
```

## 快速开始

### 环境要求

- Python 3.8+
- Claude Code (用于使用 Skill 功能)

### 安装依赖

```bash
cd skills/weibo-hot-search-analyzer
pip install -r requirements.txt
```

### 配置 API

编辑 `config.json`，设置天行数据 API 密钥：

```json
{
  "api_key": "your_api_key_here"
}
```

获取 API 密钥: https://www.tianapi.com/

### 运行分析

```bash
# 方式1: 使用 Claude Code Skill
# 在 Claude Code 中执行:
/weibo-hotsearch

# 方式2: 直接运行 Python 脚本
python run_analysis.py --topics 20
```

### 输出文件

运行后会生成以下文件：

| 文件 | 说明 |
|------|------|
| `YYMMDD_weibo_analysis_data.json` | 原始热搜数据 |
| `YYMMDD_weibo_analysis_results.json` | 分析结果数据 |
| `YYMMDD_weibo_analysis_report.html` | 可视化 HTML 报告 |
| `YYMMDD_weibo_analysis_summary.md` | Markdown 摘要报告 |

## 使用示例

### Claude Code Skill

**基础使用**：
```
请分析今天的微博热搜并生成产品创意报告
```

**高级使用**：
```
使用微博热搜API获取最新榜单，对前20个话题进行深度分析，
重点关注科技和创新领域，生成评分超过80分的产品创意
```

### 命令行参数

```bash
python run_analysis.py --help

# 指定分析话题数量
python run_analysis.py --topics 30

# 自定义输出文件前缀
python run_analysis.py --output my_analysis

# 使用自定义 API 密钥
python run_analysis.py --api-key YOUR_API_KEY
```

## 评分系统

每个产品创意按以下标准评分：

- **有趣度 (80%)** - 创意新颖性、话题热度、趋势契合度
- **有用度 (20%)** - 实用性、市场需求、可行性

**评级标准**：
- 🟢 优秀 (80分+) - 高创新潜力
- 🟡 良好 (60-79分) - 中等机会
- ⚪ 待改进 (60分以下) - 需要优化

## 报告示例

HTML 报告包含：
- 📊 分析概况统计
- 🏆 Top 5 产品创意详解
- 📰 完整话题列表
- 📈 可视化数据展示

## 技术栈

- **数据获取**: Requests API
- **智能分析**: AI/LLM 集成
- **报告生成**: Jinja2 模板引擎
- **配置管理**: JSON

## 注意事项

1. 需要有效的天行数据 API 密钥
2. 分析大量话题可能需要较长时间
3. 生成的产品创意仅供参考，实际开发需进一步市场调研

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

**仓库地址**: https://github.com/harveyzhang604/test-weibo2.git
