# 微博热搜产品创意分析 Skill

这是一个基于 Claude Code 的 skill，用于分析微博热搜榜单并生成产品创意。

## 功能特性

- 🔥 自动抓取微博热搜数据
- 🔍 深度搜索每个话题的背景信息
- 💡 AI 驱动的产品创意生成
- 📊 基于"有趣度80%+有用度20%"的评分系统
- 📈 生成专业的HTML分析报告

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API

编辑 `config.json` 文件，设置：
- 微博热搜API地址
- OpenAI API密钥（可选，用于更智能的分析）

### 3. 运行分析

```bash
# 步骤1：抓取热搜数据
python weibo_hotsearch_fetcher.py --api-url YOUR_API_URL --output hot_search_data.json

# 步骤2：分析趋势并生成创意
python trend_analyzer.py --input hot_search_data.json --output analysis_results.json --openai-key YOUR_OPENAI_KEY

# 步骤3：生成HTML报告
python report_generator.py --input analysis_results.json --output report.html --summary summary.md
```

### 4. 查看报告

打开 `report.html` 查看完整的分析报告。

## 文件说明

- `SKILL.md` - Skill 定义文件，包含使用说明
- `weibo_hotsearch_fetcher.py` - 微博热搜数据抓取脚本
- `trend_analyzer.py` - 趋势分析和创意生成脚本
- `report_generator.py` - HTML报告生成脚本
- `report_template.html` - HTML报告模板
- `config.json` - 配置文件
- `requirements.txt` - Python依赖包列表

## 使用示例

### 基础使用

```
请分析今天的微博热搜并生成产品创意报告
```

### 高级使用

```
使用微博热搜API获取最新榜单，对前20个话题进行深度分析，重点关注科技和创新领域，生成评分超过80分的产品创意
```

## 评分系统

每个产品创意都会按照以下标准评分：

- **有趣度（80%）**：创意的新颖性、话题热度、趋势契合度
- **有用度（20%）**：实用性、市场需求、可行性

**评分等级**：
- 🟢 优秀（80分以上）：具有高创新潜力
- 🟡 良好（60-79分）：中等机会
- ⚪ 待改进（60分以下）：需要优化

## 自定义配置

### 调整评分权重

在 `config.json` 中修改：

```json
{
  "scoring": {
    "interestingness_weight": 0.7,
    "usefulness_weight": 0.3
  }
}
```

### 设置分析范围

```json
{
  "analysis": {
    "max_topics": 30,
    "search_delay": 1.0
  }
}
```

## 注意事项

1. 需要有效的微博热搜API地址
2. 使用OpenAI API可以获得更好的创意质量
3. 生成的产品创意仅供参考，实际开发需要进一步的市场调研

## 故障排除

### 常见问题

1. **API请求失败**
   - 检查API地址是否正确
   - 确认网络连接正常

2. **AI分析失败**
   - 检查OpenAI API密钥是否有效
   - 确认API配额充足

3. **报告生成失败**
   - 检查模板文件是否存在
   - 确认输入数据格式正确

## 贡献

欢迎提交问题和改进建议！