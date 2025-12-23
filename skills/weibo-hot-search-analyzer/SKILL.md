#---
name: weibo-hot-search-analyzer
description: "Comprehensive Weibo hot search analysis tool that fetches trending topics, researches background information using web search, and generates product innovation ideas with scoring. Use when user asks to analyze Weibo trending topics, extract product opportunities from social media trends, or generate innovation reports from hot search data."
license: MIT
---

# Weibo Hot Search Product Innovation Analyzer

## Overview

This skill analyzes Weibo hot search trends to extract product innovation opportunities. It automatically fetches trending topics, performs comprehensive research on each topic, and generates actionable product ideas with scoring based on innovation potential.

## Key Features

- **Automated Data Collection**: Fetches Weibo hot search rankings via API
- **Comprehensive Research**: Uses web search to gather background information for each trending topic
- **AI-Powered Analysis**: Analyzes trends and extracts product opportunities
- **Innovation Scoring**: Evaluates ideas based on interestingness (80%) and usefulness (20%)
- **Professional Reporting**: Generates HTML reports with detailed analysis and rankings

## Workflow

### 1. Data Collection Phase
- Fetch Weibo hot search data using the provided API endpoint
- Extract topic rankings, heat values, and descriptions
- Structure data for analysis

### 2. Research Phase
For each trending topic:
- Perform web searches to gather:
  - News coverage and articles
  - Background context and event timeline
  - Public sentiment and discussions
  - Related market trends

### 3. Analysis Phase
For each researched topic:
- Analyze the underlying user needs and pain points
- Identify market gaps and opportunities
- Generate product concepts with:
  - **Name**: Creative and memorable product name
  - **Core Functionality**: Key features and value proposition
  - **Target Audience**: Detailed user demographics and behaviors

### 4. Scoring System
Evaluate each product idea using:
- **Interestingness (80%)**: Novelty, creativity, trend alignment
- **Usefulness (20%)**: Practical value, market demand, feasibility
- **Total Score**: 0-100 scale with ratings:
  - Excellent (80+): High innovation potential
  - Good (60-79): Moderate opportunity
  - Development Needed (below 60): Requires refinement

### 5. Report Generation
Create comprehensive HTML report including:
- Executive summary of trends
- Detailed analysis for each topic:
  - Event timeline and background
  - Product innovation details
  - Score and rating
- Visual hierarchy highlighting top opportunities
- Actionable recommendations

## Prerequisites

1. **API Access**: Weibo hot search API endpoint
2. **Web Search**: Enabled search capabilities
3. **Python Environment**: For data processing scripts
4. **HTML Generation**: Template rendering capabilities

## Implementation Steps

### Step 1: Fetch Hot Search Data
Use the `weibo_hotsearch_fetcher.py` script to:
```python
# Example usage
python weibo_hotsearch_fetcher.py --api-url YOUR_API_ENDPOINT --output hot_search_data.json
```

### Step 2: Process and Analyze
Run the analysis pipeline:
```python
# Analyze trends and generate ideas
python trend_analyzer.py --input hot_search_data.json --output analysis_results.json
```

### Step 3: Generate Report
Create the final HTML report:
```python
# Generate comprehensive report
python report_generator.py --input analysis_results.json --output report.html
```

## Output Format

The skill generates:
1. **JSON Data Files**: Structured data for each processing stage
2. **HTML Report**: Professional report with:
   - Responsive design
   - Color-coded rankings
   - Expandable detail sections
   - Print-friendly styling

## Customization Options

### Adjusting Scoring Weights
Modify scoring parameters in `config.json`:
```json
{
  "scoring": {
    "interestingness_weight": 0.8,
    "usefulness_weight": 0.2,
    "excellent_threshold": 80,
    "good_threshold": 60
  }
}
```

### Customizing Product Categories
Edit `product_categories.json` to focus on specific industries:
```json
{
  "categories": ["Technology", "Lifestyle", "Entertainment", "Education"],
  "exclude_keywords": ["controversial", "sensitive"]
}
```

## Error Handling

The skill includes robust error handling for:
- API failures and rate limits
- Search result unavailability
- Data parsing errors
- Report generation issues

## Best Practices

1. **Regular Updates**: Run analysis daily to capture emerging trends
2. **Validation**: Manually review top-scored ideas for feasibility
3. **Integration**: Combine with other trend data sources for completeness
4. **Documentation**: Save reports with timestamps for trend tracking

## Limitations

- Depends on API availability and accuracy
- Web search results may vary by region
- Scoring is subjective and should be validated
- Product ideas require additional market research

## Examples

### Basic Usage
```
Analyze today's Weibo hot search and generate product innovation report
```

### Advanced Usage
```
Fetch Weibo hot search data, research each topic thoroughly, and create a detailed HTML report highlighting product opportunities with scores above 75
```

### Custom Analysis
```
Focus on technology trends from Weibo hot search, generate product ideas for B2B applications, and rank them by market potential
```