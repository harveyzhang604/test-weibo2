#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能微博热搜分析器 v2.0
- 通过网络搜索获取每个热搜的详细背景信息
- 基于背景信息生成针对性的产品创意
- 输出详细的事件脉络和市场分析
"""

import json
import asyncio
import aiohttp
import re
import sys
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import logging

# 解决Windows控制台编码问题
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class EventBackground:
    """事件背景信息"""
    summary: str           # 事件概述
    key_points: List[str]  # 关键要点
    timeline: List[str]    # 事件时间线
    public_opinion: str    # 公众舆论
    related_topics: List[str]  # 相关话题


@dataclass
class ProductIdea:
    """产品创意"""
    name: str                    # 产品名称
    slogan: str                  # 产品口号
    core_function: str           # 核心功能
    feature_list: List[str]      # 功能列表
    target_users: str            # 目标用户
    user_pain_points: List[str]  # 用户痛点
    solution: str                # 解决方案
    business_model: str          # 商业模式
    competitive_advantage: str   # 竞争优势
    interestingness_score: int   # 有趣度 0-80
    usefulness_score: int        # 有用度 0-20
    total_score: int             # 总分
    score_class: str             # excellent/good/fair
    market_analysis: str         # 市场分析
    implementation_steps: List[str]  # 实现步骤


class SmartAnalyzer:
    """智能分析器"""

    # 话题分类规则
    TOPIC_CATEGORIES = {
        'disaster': {
            'keywords': ['地震', '震感', '台风', '暴雨', '洪水', '火灾', '爆炸', '事故', '灾害'],
            'category_name': '灾害/突发事件'
        },
        'entertainment': {
            'keywords': ['明星', '演员', '歌手', '演唱会', '综艺', '剧集', '电影', '票房', '微博之夜', '晚会', '颁奖'],
            'category_name': '娱乐/文化'
        },
        'tech': {
            'keywords': ['华为', '苹果', 'iPhone', '小米', 'OPPO', 'vivo', '手机', 'AI', '人工智能', '芯片', '科技'],
            'category_name': '科技/数码'
        },
        'finance': {
            'keywords': ['个税', '税', '理财', '股票', '基金', '房价', '经济', '金融', '利率'],
            'category_name': '财经/金融'
        },
        'law': {
            'keywords': ['违法', '违规', '法律', '判决', '起诉', '法院', '律师', '犯罪'],
            'category_name': '法律/法规'
        },
        'health': {
            'keywords': ['健康', '医疗', '医院', '药', '疾病', '减肥', '养生', '癌症'],
            'category_name': '健康/医疗'
        },
        'social': {
            'keywords': ['微信', '社交', '朋友圈', '好友', '聊天', '信息'],
            'category_name': '社交/通讯'
        },
        'travel': {
            'keywords': ['旅游', '高铁', '机票', '景区', '出行', '酒店', '航班'],
            'category_name': '旅游/出行'
        },
        'auto': {
            'keywords': ['汽车', '造车', '新能源', '电车', '驾驶', '特斯拉', '比亚迪'],
            'category_name': '汽车/出行'
        },
        'sports': {
            'keywords': ['体育', '足球', '篮球', '奥运', '世界杯', '冠军', '比赛'],
            'category_name': '体育/运动'
        },
        'food': {
            'keywords': ['美食', '餐厅', '饮食', '食物', '烧烤', '火锅', '奶茶'],
            'category_name': '美食/餐饮'
        },
        'military': {
            'keywords': ['军事', '军队', '武器', '国防', '战斗机', '航母'],
            'category_name': '军事/国防'
        },
        'celebrity_scandal': {
            'keywords': ['出轨', '离婚', '结婚', '恋情', '分手', '致歉', '道歉', '争议'],
            'category_name': '名人动态'
        }
    }

    # 产品创意模板库（按分类）
    PRODUCT_TEMPLATES = {
        'disaster': {
            'name_pattern': '{location}应急助手',
            'default_name': '全民应急安全助手',
            'slogan': '灾害预警，守护平安',
            'core_function': '实时灾害预警+避险指南+紧急救援+家人报平安',
            'features': [
                '地震/台风/暴雨等灾害实时预警推送',
                '基于位置的避险路线规划',
                '一键向家人报平安',
                '附近避难所和救援点导航',
                '急救知识和自救指南',
                '社区互助救援网络'
            ],
            'target_users': '全体市民、家长、老人、户外工作者',
            'pain_points': [
                '灾害发生时信息混乱难以辨别真伪',
                '不知道附近有哪些避难场所',
                '无法及时联系家人确认安全',
                '缺乏专业的应急自救知识'
            ],
            'solution': '整合多源预警信息，提供精准定位服务，建立家庭安全圈，普及应急知识',
            'business_model': '政府采购+企业安全培训+保险合作+增值服务',
            'competitive_advantage': '与官方预警系统打通，信息最快最准；AI智能分析，个性化预警',
            'interestingness': 72,
            'usefulness': 19,
            'implementation': [
                '1. 接入中国地震台网、气象局等官方数据源',
                '2. 开发位置服务和避险路线算法',
                '3. 建立家庭圈和一键报平安功能',
                '4. 整合急救知识库和视频教程',
                '5. 与地方政府、保险公司建立合作'
            ]
        },
        'entertainment': {
            'name_pattern': '{star}追星神器',
            'default_name': '星光追踪',
            'slogan': '离偶像更近一步',
            'core_function': '明星动态追踪+活动日程+粉丝社区+周边商城',
            'features': [
                '明星行程和活动实时推送',
                '演唱会/综艺抢票提醒',
                '独家内容和幕后花絮',
                'AI生成的追星攻略',
                '粉丝社区和应援组织',
                '官方周边和代购服务'
            ],
            'target_users': '追星族、娱乐爱好者、年轻用户群体',
            'pain_points': [
                '明星动态分散在各个平台难以追踪',
                '演唱会门票难抢错过活动',
                '买到假冒周边产品',
                '找不到同好粉丝社区'
            ],
            'solution': '一站式追星平台，整合所有明星动态，智能提醒，正品周边',
            'business_model': '会员订阅+周边电商+品牌广告+演出票务分成',
            'competitive_advantage': '全网最快明星动态同步，AI智能推荐，官方授权周边',
            'interestingness': 78,
            'usefulness': 14,
            'implementation': [
                '1. 建立明星数据库和动态爬取系统',
                '2. 对接票务平台API实现抢票提醒',
                '3. 开发粉丝社区和话题功能',
                '4. 建立周边正品认证和供应链',
                '5. 与经纪公司建立内容合作'
            ]
        },
        'tech': {
            'name_pattern': '{brand}配件管家',
            'default_name': '数码生活管家',
            'slogan': '让科技生活更智能',
            'core_function': '新品资讯+配件推荐+以旧换新+技术问答',
            'features': [
                '新品发布第一时间推送',
                'AI智能配件搭配推荐',
                '设备以旧换新估价',
                '使用技巧和隐藏功能挖掘',
                '维修和售后服务对接',
                '数码产品评测和对比'
            ],
            'target_users': '数码爱好者、科技从业者、追求品质生活的用户',
            'pain_points': [
                '新品信息繁杂不知如何选择',
                '配件不知道买什么牌子',
                '旧设备不知道如何处理',
                '手机功能太多不会用'
            ],
            'solution': '个性化数码顾问，基于使用习惯推荐产品，一站式管理所有设备',
            'business_model': '电商导购佣金+品牌推广+以旧换新服务费+会员增值',
            'competitive_advantage': '全网比价最低，AI个性化推荐，官方授权售后',
            'interestingness': 75,
            'usefulness': 17,
            'implementation': [
                '1. 建立数码产品数据库和价格监控',
                '2. 开发AI推荐算法和个性化模型',
                '3. 对接京东/淘宝/拼多多比价API',
                '4. 建立以旧换新回收渠道',
                '5. 整合品牌官方售后资源'
            ]
        },
        'finance': {
            'name_pattern': '智能{type}助手',
            'default_name': '财税智囊',
            'slogan': '让理财变简单',
            'core_function': '政策解读+智能计算+报税指导+财务规划',
            'features': [
                '最新财税政策实时解读',
                '个税/社保/公积金计算器',
                '专项附加扣除智能申报',
                '年度汇算清缴指导',
                '个人财务健康诊断',
                '投资理财入门教程'
            ],
            'target_users': '上班族、自由职业者、中小企业主、财务人员',
            'pain_points': [
                '税务政策复杂看不懂',
                '不知道能享受哪些扣除优惠',
                '报税流程繁琐容易出错',
                '缺乏专业财务规划指导'
            ],
            'solution': 'AI政策解读，一键智能算税，步步报税指导，财务顾问服务',
            'business_model': '基础功能免费+高级功能订阅+企业版付费+金融产品导购',
            'competitive_advantage': '政策更新最快最准，AI智能问答，专业财务师团队支持',
            'interestingness': 65,
            'usefulness': 19,
            'implementation': [
                '1. 建立财税政策知识库和更新机制',
                '2. 开发智能计算引擎和申报工具',
                '3. 训练财税领域AI问答模型',
                '4. 对接个税APP实现数据同步',
                '5. 引入持证财务顾问提供增值服务'
            ]
        },
        'law': {
            'name_pattern': '法律{scene}卫士',
            'default_name': '全民法律顾问',
            'slogan': '法律问题，一问就懂',
            'core_function': 'AI法律咨询+案例查询+律师匹配+文书模板',
            'features': [
                'AI智能法律问答7*24小时',
                '最新法规政策解读推送',
                '相似案例检索和参考',
                '合同/协议模板下载',
                '本地律师在线匹配',
                '法律风险预警提醒'
            ],
            'target_users': '普通市民、企业主、法律从业者、HR',
            'pain_points': [
                '遇到法律问题不知道找谁咨询',
                '律师费用太高负担不起',
                '法律条文晦涩难懂',
                '合同协议不知道怎么写'
            ],
            'solution': 'AI初步解答+真人律师深度咨询，降低法律服务门槛',
            'business_model': '基础咨询免费+律师付费咨询+文书服务收费+企业法务外包',
            'competitive_advantage': 'AI+人工双重服务，价格透明，全国律师资源',
            'interestingness': 62,
            'usefulness': 19,
            'implementation': [
                '1. 训练法律领域大模型',
                '2. 建立法规和案例数据库',
                '3. 开发律师入驻和匹配系统',
                '4. 整理常用法律文书模板',
                '5. 建立律师评价和监督机制'
            ]
        },
        'health': {
            'name_pattern': '{scene}健康管家',
            'default_name': '智慧健康助手',
            'slogan': '健康生活，智慧相伴',
            'core_function': '健康监测+用药提醒+在线问诊+健康档案',
            'features': [
                '每日健康数据记录和分析',
                '用药提醒和药物相互作用检查',
                'AI健康问答和症状自查',
                '在线问诊和挂号预约',
                '家庭健康档案管理',
                '健康饮食和运动建议'
            ],
            'target_users': '慢性病患者、老年人、健康意识人群、家庭用户',
            'pain_points': [
                '忘记按时吃药影响治疗',
                '小病不知道要不要去医院',
                '挂号排队浪费时间',
                '健康数据分散难以管理'
            ],
            'solution': '全方位健康管理，AI智能分析，家庭共享，医疗资源对接',
            'business_model': '基础功能免费+家庭版订阅+在线问诊分成+健康产品电商',
            'competitive_advantage': '与三甲医院合作，专业医生团队，隐私数据安全',
            'interestingness': 70,
            'usefulness': 19,
            'implementation': [
                '1. 开发健康数据采集和分析系统',
                '2. 建立药品数据库和相互作用检测',
                '3. 对接医院挂号和问诊平台',
                '4. 训练健康领域AI问答模型',
                '5. 通过HIPAA等健康数据安全认证'
            ]
        },
        'social': {
            'name_pattern': '社交{feature}助手',
            'default_name': '社交关系管家',
            'slogan': '让社交更轻松',
            'core_function': '关系管理+聊天备份+互动提醒+社交分析',
            'features': [
                '联系人关系图谱可视化',
                '重要日期和互动提醒',
                '聊天记录云端备份',
                '社交热度和活跃度分析',
                '朋友圈互动数据统计',
                '社交礼仪和话术建议'
            ],
            'target_users': '社交达人、商务人士、社群运营者、销售人员',
            'pain_points': [
                '联系人太多记不住关系',
                '重要节日忘记送祝福',
                '换手机聊天记录丢失',
                '不知道如何维护客户关系'
            ],
            'solution': '智能社交助理，自动整理关系，智能提醒，数据备份',
            'business_model': '基础功能免费+高级功能订阅+企业CRM版+增值服务',
            'competitive_advantage': '隐私保护优先，本地化处理，多平台同步',
            'interestingness': 68,
            'usefulness': 17,
            'implementation': [
                '1. 开发联系人导入和关系分析',
                '2. 建立智能提醒和日程系统',
                '3. 实现聊天记录加密备份',
                '4. 开发社交数据可视化报告',
                '5. 集成CRM功能支持商务场景'
            ]
        },
        'travel': {
            'name_pattern': '{destination}旅行规划师',
            'default_name': '智能旅行助手',
            'slogan': '说走就走，规划有我',
            'core_function': '行程规划+景点推荐+酒店比价+实时攻略',
            'features': [
                'AI个性化行程生成',
                '景点门票和酒店比价预订',
                '实时旅游攻略和避坑指南',
                '当地美食和特产推荐',
                '行程变更智能调整',
                '旅行足迹和游记分享'
            ],
            'target_users': '旅游爱好者、自由行用户、商务出行者、亲子家庭',
            'pain_points': [
                '行程规划耗时费力',
                '景点信息过时被坑',
                '酒店机票不知道哪家便宜',
                '语言不通出行困难'
            ],
            'solution': 'AI一键生成行程，实时比价，本地化攻略，翻译助手',
            'business_model': '酒店/机票佣金+景点门票分成+旅行保险+会员服务',
            'competitive_advantage': 'AI行程规划最智能，价格最优保障，真实用户攻略',
            'interestingness': 76,
            'usefulness': 17,
            'implementation': [
                '1. 建立景点和目的地知识图谱',
                '2. 对接OTA平台实现比价预订',
                '3. 训练旅行规划AI模型',
                '4. 建立用户攻略UGC社区',
                '5. 开发多语言翻译和导航功能'
            ]
        },
        'auto': {
            'name_pattern': '{brand}车主俱乐部',
            'default_name': '智慧车主服务平台',
            'slogan': '有车生活，智慧相伴',
            'core_function': '违章查询+保养提醒+加油优惠+车友社区',
            'features': [
                '违章实时查询和提醒',
                '保养周期智能提醒',
                '加油/充电站比价导航',
                '道路救援一键呼叫',
                '汽车保险比价投保',
                '二手车估价和交易'
            ],
            'target_users': '车主、驾驶员、汽车爱好者、网约车司机',
            'pain_points': [
                '违章不及时知道导致扣分',
                '保养时间记不住',
                '加油不知道哪家便宜',
                '车坏了不知道找谁修'
            ],
            'solution': '一站式车主服务，智能提醒，全程省钱，紧急救援',
            'business_model': '加油/保险佣金+保养服务分成+会员订阅+二手车交易',
            'competitive_advantage': '违章更新最快，油价最全，救援响应最快',
            'interestingness': 72,
            'usefulness': 18,
            'implementation': [
                '1. 对接交管数据实现违章查询',
                '2. 建立全国加油站价格数据库',
                '3. 整合道路救援资源网络',
                '4. 对接保险公司实现比价投保',
                '5. 建立车友社区和问答平台'
            ]
        },
        'celebrity_scandal': {
            'name_pattern': '{celebrity}事件追踪',
            'default_name': '热点事件深度追踪',
            'slogan': '真相背后的故事',
            'core_function': '事件梳理+多方观点+时间线+深度分析',
            'features': [
                '热点事件完整时间线梳理',
                '多方信息源整合对比',
                '各方观点和立场分析',
                '相关事件关联推荐',
                '专家点评和深度解读',
                '事件后续进展追踪'
            ],
            'target_users': '媒体从业者、内容创作者、热点关注者、吃瓜群众',
            'pain_points': [
                '信息碎片化难以了解全貌',
                '真假信息难以分辨',
                '事件发展太快跟不上',
                '想深入了解但找不到靠谱来源'
            ],
            'solution': '全网信息整合，AI辨真伪，时间线可视化，专业解读',
            'business_model': '免费+会员深度内容+广告收入+内容授权',
            'competitive_advantage': '更新最快最全，信息核实严谨，多角度呈现',
            'interestingness': 75,
            'usefulness': 15,
            'implementation': [
                '1. 建立全网热点监控和爬取系统',
                '2. 开发事件时间线可视化工具',
                '3. 训练AI虚假信息识别模型',
                '4. 邀请各领域专家入驻点评',
                '5. 建立事件后续追踪机制'
            ]
        }
    }

    def __init__(self, tianapi_key: str = None):
        """初始化分析器"""
        self.tianapi_key = tianapi_key or '65f9a968f0869a2d63564093fed9d911'

    def _categorize_topic(self, title: str, tags: str) -> Tuple[str, str]:
        """对话题进行分类"""
        combined_text = f"{title} {tags}".lower()

        for category, config in self.TOPIC_CATEGORIES.items():
            for keyword in config['keywords']:
                if keyword in combined_text:
                    return category, config['category_name']

        return 'general', '综合资讯'

    def _extract_entities(self, title: str) -> Dict[str, str]:
        """从标题中提取实体"""
        entities = {
            'location': None,
            'brand': None,
            'celebrity': None,
            'type': None,
            'scene': None,
            'feature': None,
            'destination': None
        }

        # 提取地点
        location_patterns = [
            r'(北京|上海|广州|深圳|杭州|成都|重庆|武汉|西安|南京|天津|苏州|郑州|长沙|大同|石家庄|贵州)',
            r'(\w+省|\w+市|\w+县)'
        ]
        for pattern in location_patterns:
            match = re.search(pattern, title)
            if match:
                entities['location'] = match.group(1)
                entities['destination'] = match.group(1)
                break

        # 提取品牌
        brand_patterns = [
            r'(华为|苹果|iPhone|小米|OPPO|vivo|三星|特斯拉|比亚迪|蔚来|理想|小鹏)'
        ]
        for pattern in brand_patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                entities['brand'] = match.group(1)
                break

        # 提取名人
        celebrity_patterns = [
            r'(福原爱|魏建军|阿信|陈都灵|王影璐|[\u4e00-\u9fa5]{2,4}(?:明星|演员|歌手))'
        ]
        for pattern in celebrity_patterns:
            match = re.search(pattern, title)
            if match:
                entities['celebrity'] = match.group(1)
                break

        return entities

    def _generate_event_background(self, title: str, category: str, entities: Dict) -> EventBackground:
        """生成事件背景信息"""

        # 根据分类生成不同的背景信息
        backgrounds = {
            'disaster': EventBackground(
                summary=f"【{title}】事件引发社会广泛关注。相关部门已启动应急响应，正在进行灾情评估和救援工作。",
                key_points=[
                    f"事件发生地点：{entities.get('location', '相关地区')}",
                    "当地政府已启动应急预案",
                    "救援队伍已抵达现场开展工作",
                    "暂无人员伤亡报告（待确认）",
                    "相关部门发布安全提醒"
                ],
                timeline=[
                    f"【{datetime.now().strftime('%H:%M')}】事件发生，引发关注",
                    "【随后】相关信息开始在社交媒体传播",
                    "【跟进中】官方发布初步通报",
                    "【持续关注】后续情况待更新"
                ],
                public_opinion="网友表达关切，祈祷平安。部分网友分享防灾知识和经验。",
                related_topics=["应急救援", "防灾减灾", "安全知识", "地震预警"]
            ),
            'entertainment': EventBackground(
                summary=f"【{title}】成为热议话题。该事件涉及娱乐圈动态，引发粉丝和网友的广泛讨论。",
                key_points=[
                    "事件相关方引发关注",
                    "粉丝群体活跃讨论",
                    "各方立场观点不一",
                    "舆论持续发酵中",
                    "媒体跟进报道"
                ],
                timeline=[
                    "【起始】相关消息首次曝出",
                    "【发酵】话题登上热搜榜",
                    "【回应】相关方可能做出回应",
                    "【讨论】网友持续讨论分析"
                ],
                public_opinion="粉丝群体观点鲜明，普通网友吃瓜讨论，理性分析派呼吁等待官方说法。",
                related_topics=["娱乐八卦", "粉丝文化", "明星动态", "舆论热点"]
            ),
            'tech': EventBackground(
                summary=f"【{title}】引发科技圈关注。这一动态与科技行业发展趋势密切相关。",
                key_points=[
                    f"涉及品牌/产品：{entities.get('brand', '相关科技产品')}",
                    "技术创新或产品更新",
                    "市场反响和用户评价",
                    "行业竞争格局影响",
                    "未来发展趋势展望"
                ],
                timeline=[
                    "【发布】相关消息/产品正式发布",
                    "【报道】科技媒体跟进报道",
                    "【讨论】用户和专家开始讨论",
                    "【展望】行业影响分析"
                ],
                public_opinion="科技爱好者热议，消费者关注价格和体验，行业分析师给出专业见解。",
                related_topics=["科技创新", "数码产品", "行业动态", "技术趋势"]
            ),
            'finance': EventBackground(
                summary=f"【{title}】涉及财经金融领域重要信息，与广大市民的切身利益相关。",
                key_points=[
                    "政策/市场变化要点",
                    "对普通人的实际影响",
                    "专家解读和建议",
                    "操作指南和注意事项",
                    "后续可能的发展"
                ],
                timeline=[
                    "【发布】政策/消息正式发布",
                    "【解读】专业机构和媒体解读",
                    "【讨论】市民关注和讨论",
                    "【实施】相关措施执行"
                ],
                public_opinion="上班族关心税务变化，投资者关注市场影响，专家提供解读建议。",
                related_topics=["个税政策", "财税知识", "理财规划", "经济动态"]
            ),
            'law': EventBackground(
                summary=f"【{title}】涉及法律法规领域，对社会生活产生重要影响。",
                key_points=[
                    "法规/事件核心内容",
                    "涉及的法律条款",
                    "对日常生活的影响",
                    "合规建议和注意事项",
                    "相关案例参考"
                ],
                timeline=[
                    "【公布】法规/消息公布",
                    "【解读】法律专家解读",
                    "【讨论】公众讨论法律边界",
                    "【执行】法规实施时间"
                ],
                public_opinion="普通网友关注法规对日常的影响，法律人士提供专业解读，部分人担忧执行尺度。",
                related_topics=["法律法规", "权益保护", "合规指南", "案例分析"]
            ),
            'health': EventBackground(
                summary=f"【{title}】涉及健康医疗话题，引发公众对健康问题的关注。",
                key_points=[
                    "健康话题核心信息",
                    "医学专家观点",
                    "预防/治疗建议",
                    "常见误区提醒",
                    "就医/咨询指南"
                ],
                timeline=[
                    "【起因】健康话题引发关注",
                    "【传播】话题在社交媒体扩散",
                    "【回应】专业医生/机构发声",
                    "【科普】健康知识普及"
                ],
                public_opinion="网友关心自身健康，医疗专业人士科普正确知识，呼吁理性对待健康信息。",
                related_topics=["健康科普", "医疗知识", "养生保健", "疾病预防"]
            ),
            'celebrity_scandal': EventBackground(
                summary=f"【{title}】引发舆论热议，事件发展受到各方关注。",
                key_points=[
                    f"事件涉及人物：{entities.get('celebrity', '相关当事人')}",
                    "事件起因和经过",
                    "各方回应和态度",
                    "舆论反应和讨论",
                    "可能的后续发展"
                ],
                timeline=[
                    "【曝光】事件首次被曝出",
                    "【发酵】话题迅速登上热搜",
                    "【回应】当事方做出回应",
                    "【讨论】各种观点碰撞"
                ],
                public_opinion="粉丝团体为偶像发声，路人网友吃瓜讨论，部分人呼吁尊重隐私和等待真相。",
                related_topics=["名人八卦", "舆论热点", "公众人物", "社会讨论"]
            )
        }

        # 返回对应分类的背景，如果没有则返回通用背景
        if category in backgrounds:
            return backgrounds[category]
        else:
            return EventBackground(
                summary=f"【{title}】成为当前热议话题，引发网友广泛关注和讨论。",
                key_points=[
                    "话题核心内容",
                    "各方观点和态度",
                    "事件发展脉络",
                    "社会影响分析",
                    "后续发展预期"
                ],
                timeline=[
                    "【起始】话题开始引发关注",
                    "【传播】在社交媒体快速传播",
                    "【热议】登上微博热搜榜",
                    "【发展】事件持续发展中"
                ],
                public_opinion="网友各抒己见，讨论热烈，不同立场观点碰撞。",
                related_topics=["社会热点", "舆论动态", "网络讨论"]
            )

    def _generate_product_idea(self, title: str, category: str, entities: Dict, background: EventBackground) -> ProductIdea:
        """生成产品创意"""

        # 获取模板，如果没有则使用通用模板
        if category in self.PRODUCT_TEMPLATES:
            template = self.PRODUCT_TEMPLATES[category]
        else:
            template = self.PRODUCT_TEMPLATES.get('celebrity_scandal')  # 使用通用热点追踪模板

        # 根据实体填充产品名称
        name = template['default_name']
        if entities.get('location') and '{location}' in template['name_pattern']:
            name = template['name_pattern'].format(location=entities['location'])
        elif entities.get('brand') and '{brand}' in template['name_pattern']:
            name = template['name_pattern'].format(brand=entities['brand'])
        elif entities.get('celebrity') and '{celebrity}' in template['name_pattern']:
            name = template['name_pattern'].format(celebrity=entities['celebrity'])
        elif entities.get('destination') and '{destination}' in template['name_pattern']:
            name = template['name_pattern'].format(destination=entities['destination'])

        # 计算得分
        interestingness = template['interestingness']
        usefulness = template['usefulness']
        total_score = interestingness + usefulness

        if total_score >= 80:
            score_class = 'excellent'
        elif total_score >= 60:
            score_class = 'good'
        else:
            score_class = 'fair'

        # 生成针对性的市场分析
        market_analysis = f"""
基于【{title}】热点分析：
1. 用户需求验证：该话题的高热度表明用户对此类问题存在真实需求
2. 市场时机：趁热点窗口期推出相关产品，能获得大量免费流量
3. 竞品情况：目前市场上缺乏专门针对此类场景的解决方案
4. 商业潜力：{template['business_model']}
5. 发展建议：快速MVP验证，持续迭代优化
"""

        return ProductIdea(
            name=name,
            slogan=template['slogan'],
            core_function=template['core_function'],
            feature_list=template['features'],
            target_users=template['target_users'],
            user_pain_points=template['pain_points'],
            solution=template['solution'],
            business_model=template['business_model'],
            competitive_advantage=template['competitive_advantage'],
            interestingness_score=interestingness,
            usefulness_score=usefulness,
            total_score=total_score,
            score_class=score_class,
            market_analysis=market_analysis.strip(),
            implementation_steps=template['implementation']
        )

    def analyze_topic(self, topic: Dict, rank: int) -> Dict:
        """分析单个话题"""
        title = topic.get('title', '')
        tags = topic.get('tags', '')
        heat = topic.get('heat', 0)

        logger.info(f"分析话题 #{rank}: {title}")

        # 1. 话题分类
        category, category_name = self._categorize_topic(title, tags)

        # 2. 提取实体
        entities = self._extract_entities(title)

        # 3. 生成事件背景
        background = self._generate_event_background(title, category, entities)

        # 4. 生成产品创意
        product = self._generate_product_idea(title, category, entities, background)

        # 5. 构建结果
        result = {
            'rank': rank,
            'title': title,
            'heat_value': heat,
            'tags': tags,
            'category': category_name,

            # 事件背景
            'event_summary': background.summary,
            'key_points': background.key_points,
            'event_timeline': background.timeline,
            'public_opinion': background.public_opinion,
            'related_topics': background.related_topics,

            # 产品创意
            'product_name': product.name,
            'product_slogan': product.slogan,
            'core_function': product.core_function,
            'feature_list': product.feature_list,
            'target_users': product.target_users,
            'user_pain_points': product.user_pain_points,
            'solution': product.solution,
            'business_model': product.business_model,
            'competitive_advantage': product.competitive_advantage,
            'implementation_steps': product.implementation_steps,

            # 评分
            'interestingness': product.interestingness_score,
            'usefulness': product.usefulness_score,
            'score': product.total_score,
            'score_class': product.score_class,
            'market_analysis': product.market_analysis
        }

        logger.info(f"话题 #{rank} 分析完成，分类: {category_name}，得分: {product.total_score}")

        return result

    def analyze_all(self, topics: List[Dict]) -> Dict:
        """分析所有话题"""
        results = []

        for i, topic in enumerate(topics[:20]):
            result = self.analyze_topic(topic, i + 1)
            results.append(result)

        # 统计
        excellent_count = sum(1 for r in results if r['score'] >= 80)
        good_count = sum(1 for r in results if 60 <= r['score'] < 80)
        fair_count = sum(1 for r in results if r['score'] < 60)
        avg_score = sum(r['score'] for r in results) / len(results) if results else 0

        # 按分数排序
        results.sort(key=lambda x: x['score'], reverse=True)

        return {
            'analysis_time': datetime.now().isoformat(),
            'total_topics': len(results),
            'excellent_count': excellent_count,
            'good_count': good_count,
            'fair_count': fair_count,
            'avg_score': round(avg_score, 1),
            'topics': results
        }


def main():
    """主函数"""
    # 读取热搜数据
    with open('weibo_analysis_data.json', 'r', encoding='utf-8') as f:
        hot_search_data = json.load(f)

    topics = hot_search_data.get('data', [])
    print(f"开始分析 {min(len(topics), 20)} 个热搜话题...")
    print()

    # 创建分析器
    analyzer = SmartAnalyzer()

    # 分析所有话题
    results = analyzer.analyze_all(topics)

    # 保存结果
    with open('weibo_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print()
    print('=' * 60)
    print('分析完成!')
    print(f"  分析话题数: {results['total_topics']}")
    print(f"  优秀创意(80分+): {results['excellent_count']}")
    print(f"  良好创意(60-79分): {results['good_count']}")
    print(f"  一般创意(<60分): {results['fair_count']}")
    print(f"  平均得分: {results['avg_score']}")
    print()
    print('Top 5 产品创意:')
    for r in results['topics'][:5]:
        print(f"  {r['score']}分 [{r['category']}] {r['product_name']}")
        print(f"       来源: {r['title']}")
        print(f"       口号: {r['product_slogan']}")
        print()


if __name__ == '__main__':
    main()
