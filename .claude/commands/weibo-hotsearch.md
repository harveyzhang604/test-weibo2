# 微博热搜产品创意分析

基于微博热搜数据，使用智能分析引擎生成创新的产品创意，并生成可视化分析报告。

## 执行步骤

1. 获取最新的微博热搜数据
2. 使用规则引擎分析每个热搜话题
3. 生成产品创意并进行评分（有趣度80% + 有用度20%）
4. 输出HTML可视化报告和Markdown摘要

## 命令参数

### 必选参数
- 无（使用默认配置）

### 可选参数
- --api-key: 指定天行数据API密钥（默认使用预设密钥）
- --openai-key: 指定OpenAI API密钥（使用AI分析时需要）
- --output: 指定输出文件前缀（默认：weibo_analysis）
- --topics: 指定分析的话题数量（默认：20）

## 使用示例

```bash
# 基本用法（使用规则引擎）
/weibo-hotsearch

# 使用AI分析引擎
/weibo-hotsearch --openai-key=sk-xxx

# 自定义输出文件名
/weibo-hotsearch --output=my_analysis

# 限制分析前10个话题
/weibo-hotsearch --topics=10
```

## 输出文件

分析完成后会生成以下文件：

1. `{output}_data.json` - 原始热搜数据
2. `{output}_results.json` - 分析结果数据
3. `{output}_report.html` - 可视化HTML报告
4. `{output}_summary.md` - Markdown摘要报告

## 评分体系

- **优秀创意（80分+）**：具有很高的市场潜力和创新性
- **良好创意（60-79分）**：有不错的市场前景
- **一般创意（<60分）**：需要进一步优化

## 技术说明

- 数据源：天行数据微博热搜API
- 分析引擎：规则引擎 + 可选OpenAI GPT
- 报告格式：HTML（可视化） + Markdown（摘要）
- 异步处理：支持并发分析提高效率

## 注意事项

1. 首次使用请确保已安装所需依赖：
   ```bash
   pip install requests aiohttp jinja2 openai
   ```

2. 确保网络连接正常，能够访问微博热搜API

3. HTML报告使用相对路径，建议在本地打开查看

4. AI分析模式需要有效的OpenAI API密钥