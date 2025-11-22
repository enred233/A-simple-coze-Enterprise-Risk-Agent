import json
import re
import urllib.parse

# 保持 async 不变
async def main(args):
    # 1. 获取输入文本
    text = args.params.get('llm_response', '')
    
    # 2. 定义默认分数
    scores = {
        "finance_score": 50, "legal_score": 50, "sentiment_score": 50, 
        "operation_score": 50, "compliance_score": 50
    }

    # 3. 正则提取
    try:
        match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if match:
            extracted_data = json.loads(match.group(1))
            scores.update(extracted_data)
    except Exception as e:
        pass 

    # 4. 构建配置参数
    chart_config = {
        "type": "radar",
        "data": {
            "labels": ["Finance (财务)", "Legal (司法)", "Sentiment (舆情)", "Operation (经营)", "Compliance (合规)"],
            "datasets": [{
                "label": "Risk Safety Score", # 风险安全分
                "data": [
                    scores['finance_score'], scores['legal_score'], scores['sentiment_score'],
                    scores['operation_score'], scores['compliance_score']
                ],
                # 填充色：科技蓝，带 40% 透明度
                "backgroundColor": "rgba(54, 162, 235, 0.4)",
                # 边框线：深蓝色，加粗
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 3,
                # 数据点：白色内芯 + 蓝色描边
                "pointBackgroundColor": "#ffffff",
                "pointBorderColor": "rgba(54, 162, 235, 1)",
                "pointBorderWidth": 2,
                "pointRadius": 5,
                "pointHoverRadius": 7
            }]
        },
        "options": {
            "layout": {
                "padding": 20
            },
            "legend": {
                "display": False
            },
            "scale": {
                # 刻度线设置
                "ticks": {
                    "beginAtZero": True,
                    "max": 100,
                    "min": 0,
                    "stepSize": 20,
                    "display": False,
                    "backdropColor": "transparent"
                },
                # 蜘蛛网格线颜色
                "gridLines": {
                    "color": "rgba(128, 128, 128, 0.2)",
                    "circular": True
                },
                # 维度标签字体设置
                "pointLabels": {
                    "fontSize": 14,
                    "fontStyle": "bold",
                    "fontColor": "#2c3e50",
                    "fontFamily": "Arial"
                }
            }
        }
    }
    
    # 5. 生成 URL (加入宽度高度控制，提高清晰度)
    base_url = "https://quickchart.io/chart?w=600&h=500&c="
    chart_url = base_url + urllib.parse.quote(json.dumps(chart_config))
    
    return {
        "chart_url": chart_url
    }