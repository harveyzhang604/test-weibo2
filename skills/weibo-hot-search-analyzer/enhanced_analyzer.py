#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime

def analyze_topic(topic, rank):
    """增强的规则引擎分析"""
    title = topic.get('title', '').lower()

    # 定义关键词和对应的产品创意
    keyword_rules = {
        # 科技手机类
        ('nova', 'huawei', '华为', '手机', 'iphone', 'oppo', 'vivo', '小米'): {
            'name': '智能手机配件推荐平台',
            'core_function': '手机配件智能匹配+个性化定制+一键购买+用户评测',
            'target_users': '手机用户、数码爱好者、时尚人群',
            'interestingness': 72,
            'usefulness': 16,
            'market_analysis': '手机配件市场规模巨大，个性化需求强烈'
        },
        # 个税/财务类
        ('个税', '专项', '扣除', '扣缴', '税', '报税'): {
            'name': '智能个税助手',
            'core_function': '政策解读+专项扣除计算器+报税指导+优化建议',
            'target_users': '上班族、财务人员、自由职业者、企业主',
            'interestingness': 65,
            'usefulness': 19,
            'market_analysis': '每年报税季刚需工具，用户基数庞大'
        },
        # 娱乐/综艺类
        ('综艺', '剧集', '明星', '演员', '晚会', '微博之夜', '颁奖'): {
            'name': '娱乐热点聚合平台',
            'core_function': '明星动态追踪+热门综艺推荐+独家内容+粉丝社区',
            'target_users': '追星族、娱乐爱好者、年轻用户群体',
            'interestingness': 75,
            'usefulness': 14,
            'market_analysis': '娱乐消费市场活跃，粉丝经济潜力巨大'
        },
        # 房产/家居类
        ('房', '楼', '小区', '家具', '装修', '业主'): {
            'name': '智慧社区管理平台',
            'core_function': '物业服务+邻里社交+报修管理+社区团购',
            'target_users': '业主、租户、物业公司、社区商家',
            'interestingness': 68,
            'usefulness': 18,
            'market_analysis': '社区服务数字化转型需求旺盛'
        },
        # 教育类
        ('教育', '学校', '考试', '学生', '老师', '高考', '研究生'): {
            'name': 'AI学习助手',
            'core_function': '智能题库+个性化学习路径+错题分析+知识点讲解',
            'target_users': '学生、家长、教师、考研人群',
            'interestingness': 70,
            'usefulness': 18,
            'market_analysis': '教育市场需求刚性，智能化趋势明显'
        },
        # 健康/医疗类
        ('健康', '医疗', '医院', '药', '病', '养生'): {
            'name': '健康管理助手',
            'core_function': '健康监测+用药提醒+在线问诊+健康档案',
            'target_users': '慢性病患者、老年人、健康意识人群',
            'interestingness': 68,
            'usefulness': 19,
            'market_analysis': '健康管理需求增长，市场前景广阔'
        },
        # 旅游/出行类
        ('旅游', '景区', '旅行', '出行', '机票', '酒店', '高铁'): {
            'name': '智能旅行规划师',
            'core_function': '行程规划+景点推荐+酒店比价+实时攻略',
            'target_users': '旅游爱好者、商务人士、自由行用户',
            'interestingness': 74,
            'usefulness': 16,
            'market_analysis': '旅游市场复苏，个性化需求增强'
        },
        # 汽车类
        ('汽车', '车', '驾驶', '交通', '司机', '驾照'): {
            'name': '车主服务超级APP',
            'core_function': '违章查询+保养提醒+加油优惠+道路救援',
            'target_users': '车主、驾驶员、汽车爱好者',
            'interestingness': 70,
            'usefulness': 18,
            'market_analysis': '汽车后市场服务需求持续增长'
        },
        # 美食类
        ('美食', '餐厅', '吃', '食物', '饭', '烧烤', '火锅'): {
            'name': '美食发现平台',
            'core_function': '附近美食推荐+排队取号+优惠券+美食社区',
            'target_users': '美食爱好者、年轻上班族、吃货群体',
            'interestingness': 76,
            'usefulness': 15,
            'market_analysis': '餐饮消费需求稳定，本地生活服务热门'
        },
        # 就业/职场类
        ('工作', '职场', '招聘', '就业', '面试', '辞职', '996'): {
            'name': '职场助手Pro',
            'core_function': '智能简历优化+面试模拟+职业规划+薪资分析',
            'target_users': '求职者、职场新人、HR、猎头',
            'interestingness': 72,
            'usefulness': 18,
            'market_analysis': '就业市场竞争激烈，求职工具需求大'
        },
        # 电商/购物类
        ('淘宝', '京东', '拼多多', '购物', '优惠', '打折', '直播带货'): {
            'name': '省钱购物助手',
            'core_function': '全网比价+优惠券汇集+历史价格查询+拼单省钱',
            'target_users': '网购用户、精打细算族、家庭主妇',
            'interestingness': 70,
            'usefulness': 18,
            'market_analysis': '电商促销常态化，比价需求持续'
        },
        # 游戏类
        ('游戏', '电竞', '王者', '原神', '英雄联盟', 'lol'): {
            'name': '游戏社交平台',
            'core_function': '组队开黑+战绩分析+游戏攻略+电竞资讯',
            'target_users': '游戏玩家、电竞爱好者、游戏主播',
            'interestingness': 78,
            'usefulness': 13,
            'market_analysis': '游戏市场庞大，社交需求强烈'
        },
        # 投资/理财类
        ('股票', '基金', '投资', '理财', '金融', '经济', '股市'): {
            'name': '智能投资顾问',
            'core_function': '行情分析+投资建议+风险评估+财经资讯',
            'target_users': '投资者、理财新手、金融从业者',
            'interestingness': 65,
            'usefulness': 19,
            'market_analysis': '理财意识提升，智能投顾需求增长'
        },
        # 社交类
        ('微信', '聊天', '朋友圈', '社交', '好友'): {
            'name': '社交关系管理器',
            'core_function': '联系人管理+生日提醒+互动分析+聊天备份',
            'target_users': '社交达人、商务人士、社群运营者',
            'interestingness': 68,
            'usefulness': 17,
            'market_analysis': '社交关系维护需求增加'
        },
        # 宠物类
        ('宠物', '猫', '狗', '萌宠', '铲屎官'): {
            'name': '宠物生活管家',
            'core_function': '健康记录+喂养提醒+宠物社区+附近宠物店',
            'target_users': '宠物主人、宠物爱好者、宠物店主',
            'interestingness': 75,
            'usefulness': 16,
            'market_analysis': '宠物经济快速增长，市场前景好'
        },
        # 运动健身类
        ('运动', '健身', '跑步', '瑜伽', '减肥', '锻炼'): {
            'name': 'AI健身教练',
            'core_function': '个性化训练计划+动作指导+数据追踪+饮食建议',
            'target_users': '健身爱好者、减肥人群、运动新手',
            'interestingness': 74,
            'usefulness': 17,
            'market_analysis': '健身意识提升，智能健身需求大'
        },
        # 天气/自然灾害类
        ('暴雪', '雨', '台风', '天气', '降温', '冷空气'): {
            'name': '智能天气预警助手',
            'core_function': '精准天气预报+灾害预警+出行建议+穿衣指南',
            'target_users': '出行人群、户外工作者、家长',
            'interestingness': 68,
            'usefulness': 19,
            'market_analysis': '天气服务刚需，精准预报价值高'
        },
        # 文化/历史类
        ('故宫', '博物馆', '文物', '历史', '文化', '艺术'): {
            'name': 'AR文化导览',
            'core_function': 'AR实景还原+历史故事讲解+互动体验+文创商城',
            'target_users': '游客、学生、文化爱好者、亲子家庭',
            'interestingness': 76,
            'usefulness': 15,
            'market_analysis': '文化消费升级，数字化体验需求增长'
        },
        # 违法/法律类
        ('违法', '违规', '起诉', '法院', '判决', '律师'): {
            'name': '法律服务助手',
            'core_function': '法律咨询+案例查询+律师匹配+文书模板',
            'target_users': '普通市民、企业主、法律从业者',
            'interestingness': 62,
            'usefulness': 19,
            'market_analysis': '法律意识提升，在线法律服务需求增长'
        },
        # 航天/科技突破类
        ('航天', '火箭', '卫星', '探测', '太空', '嫦娥'): {
            'name': '航天科普平台',
            'core_function': '航天直播+任务追踪+科普教育+航天社区',
            'target_users': '科技爱好者、学生、航天迷',
            'interestingness': 80,
            'usefulness': 14,
            'market_analysis': '航天热度持续，科普教育需求增长'
        },
        # 情感/婚恋类
        ('恋爱', '结婚', '离婚', '相亲', '单身', '脱单'): {
            'name': '智能婚恋平台',
            'core_function': '智能匹配+视频相亲+恋爱指导+情感咨询',
            'target_users': '单身人群、适婚青年、家长',
            'interestingness': 74,
            'usefulness': 16,
            'market_analysis': '婚恋市场需求稳定，智能化匹配有优势'
        },
        # 电影类
        ('电影', '票房', '影院', '首映', '导演'): {
            'name': '观影助手',
            'core_function': '电影推荐+在线购票+影评社区+观影记录',
            'target_users': '电影爱好者、约会人群、影评人',
            'interestingness': 72,
            'usefulness': 16,
            'market_analysis': '电影消费市场回暖，观影需求增长'
        }
    }

    # 匹配关键词
    matched_idea = None
    for keywords, idea in keyword_rules.items():
        for kw in keywords:
            if kw in title:
                matched_idea = idea
                break
        if matched_idea:
            break

    # 如果没有匹配，使用智能默认
    if not matched_idea:
        tags = topic.get('tags', '')
        if '爆' in tags or '热' in tags or '沸' in tags:
            matched_idea = {
                'name': '热点事件追踪器',
                'core_function': '实时热点监控+事件脉络梳理+多源信息汇总+观点分析',
                'target_users': '媒体从业者、内容创作者、市场营销人员',
                'interestingness': 70,
                'usefulness': 16,
                'market_analysis': '热点信息整合需求增加，信息差价值凸显'
            }
        else:
            matched_idea = {
                'name': '智能资讯助手',
                'core_function': '个性化资讯推荐+深度解读+话题讨论+一键分享',
                'target_users': '信息获取者、知识爱好者、社交媒体用户',
                'interestingness': 62,
                'usefulness': 16,
                'market_analysis': '信息碎片化时代，整合价值凸显'
            }

    total_score = matched_idea['interestingness'] + matched_idea['usefulness']
    if total_score >= 80:
        score_class = 'excellent'
    elif total_score >= 60:
        score_class = 'good'
    else:
        score_class = 'fair'

    return {
        'rank': rank,
        'title': topic.get('title', ''),
        'heat_value': topic.get('heat', 0),
        'tags': topic.get('tags', ''),
        'event_timeline': '''
        <ul>
            <li>事件起始：话题开始引发关注</li>
            <li>发展过程：讨论热度逐步上升</li>
            <li>热点形成：登上微博热搜榜</li>
            <li>当前状态：持续发酵中</li>
        </ul>
        ''',
        'product_name': matched_idea['name'],
        'core_function': matched_idea['core_function'],
        'target_users': matched_idea['target_users'],
        'interestingness': matched_idea['interestingness'],
        'usefulness': matched_idea['usefulness'],
        'score': total_score,
        'score_class': score_class,
        'market_analysis': matched_idea['market_analysis']
    }


def main():
    # 读取热搜数据
    with open('weibo_analysis_data.json', 'r', encoding='utf-8') as f:
        hot_search_data = json.load(f)

    topics = hot_search_data.get('data', [])[:20]

    # 分析所有话题
    results = []
    for i, topic in enumerate(topics):
        result = analyze_topic(topic, i + 1)
        results.append(result)
        print(f"分析完成: #{result['rank']} {result['title'][:15]}... -> {result['product_name']} ({result['score']}分)")

    # 统计
    excellent_count = sum(1 for r in results if r['score'] >= 80)
    good_count = sum(1 for r in results if 60 <= r['score'] < 80)
    avg_score = sum(r['score'] for r in results) / len(results)

    # 保存结果
    output_data = {
        'analysis_time': datetime.now().isoformat(),
        'total_topics': len(results),
        'excellent_count': excellent_count,
        'good_count': good_count,
        'avg_score': round(avg_score, 1),
        'topics': results
    }

    with open('weibo_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print()
    print('=' * 60)
    print('分析完成!')
    print(f'  分析话题数: {len(results)}')
    print(f'  优秀创意(80分+): {excellent_count}')
    print(f'  良好创意(60-79分): {good_count}')
    print(f'  平均得分: {avg_score:.1f}')
    print()
    print('Top 5 产品创意:')
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    for r in sorted_results[:5]:
        print(f"  {r['score']}分 - {r['product_name']} (来源: {r['title'][:20]})")


if __name__ == '__main__':
    main()
