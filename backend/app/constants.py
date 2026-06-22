from typing import Dict, Any, List, Optional

BREED_OPTIONS = {
    "犬": [
        "泰迪", "金毛寻回犬", "拉布拉多", "哈士奇", "萨摩耶", "博美",
        "吉娃娃", "柯基犬", "比熊", "雪纳瑞", "边境牧羊犬", "德国牧羊犬",
        "阿拉斯加", "柴犬", "斗牛犬", "巴哥犬", "约克夏", "马尔济斯",
        "中华田园犬", "其他"
    ],
    "猫": [
        "英国短毛猫", "美国短毛猫", "布偶猫", "暹罗猫", "波斯猫",
        "加菲猫", "缅因猫", "苏格兰折耳猫", "英国长毛猫", "狸花猫",
        "橘猫", "三花猫", "蓝猫", "金渐层", "银渐层", "其他"
    ]
}

VACCINE_TYPES = [
    "狂犬", "猫三联", "犬五联", "犬六联", "犬八联",
    "猫五联", "猫七联", "钩端螺旋体", "犬窝咳", "其他"
]

ALLERGY_TYPES = ["药物", "食物", "跳蚤药", "环境", "其他"]

SEVERITY_LEVELS = ["轻度", "中度", "重度", "危重"]

DIAGNOSIS_SEVERITY_LEVELS = ["轻度", "中度", "重度", "危重"]

MUCOUS_MEMBRANE_COLORS = [
    "粉红色", "苍白", "发绀", "黄疸", "充血", "其他"
]

EXAM_TYPES = [
    "血常规", "生化检查", "尿检", "粪检", "皮肤刮片",
    "细胞学检查", "X光", "B超", "其他"
]

LAB_REFERENCE_RANGES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "血常规": {
        "WBC": {"name": "白细胞计数", "unit": "×10^9/L", "min": 6.0, "max": 17.0, "species": "通用"},
        "RBC": {"name": "红细胞计数", "unit": "×10^12/L", "min_dog": 5.5, "max_dog": 8.5, "min_cat": 5.0, "max_cat": 10.0},
        "HGB": {"name": "血红蛋白", "unit": "g/L", "min_dog": 120, "max_dog": 180, "min_cat": 80, "max_cat": 150},
        "HCT": {"name": "红细胞压积", "unit": "%", "min_dog": 37, "max_dog": 55, "min_cat": 25, "max_cat": 45},
        "PLT": {"name": "血小板计数", "unit": "×10^9/L", "min": 200, "max": 500, "species": "通用"},
        "NEU%": {"name": "中性粒细胞百分比", "unit": "%", "min": 60, "max": 77, "species": "通用"},
        "LYM%": {"name": "淋巴细胞百分比", "unit": "%", "min": 12, "max": 30, "species": "通用"},
        "MON%": {"name": "单核细胞百分比", "unit": "%", "min": 3, "max": 10, "species": "通用"},
        "EOS%": {"name": "嗜酸性粒细胞百分比", "unit": "%", "min": 2, "max": 10, "species": "通用"},
        "BAS%": {"name": "嗜碱性粒细胞百分比", "unit": "%", "min": 0, "max": 1, "species": "通用"},
    },
    "生化检查": {
        "ALT": {"name": "谷丙转氨酶", "unit": "U/L", "min_dog": 10, "max_dog": 100, "min_cat": 10, "max_cat": 100},
        "AST": {"name": "谷草转氨酶", "unit": "U/L", "min_dog": 10, "max_dog": 50, "min_cat": 10, "max_cat": 50},
        "ALP": {"name": "碱性磷酸酶", "unit": "U/L", "min_dog": 20, "max_dog": 150, "min_cat": 10, "max_cat": 100},
        "GGT": {"name": "谷氨酰转肽酶", "unit": "U/L", "min_dog": 1, "max_dog": 10, "min_cat": 1, "max_cat": 10},
        "TP": {"name": "总蛋白", "unit": "g/L", "min_dog": 54, "max_dog": 78, "min_cat": 60, "max_cat": 80},
        "ALB": {"name": "白蛋白", "unit": "g/L", "min_dog": 24, "max_dog": 40, "min_cat": 25, "max_cat": 45},
        "GLB": {"name": "球蛋白", "unit": "g/L", "min_dog": 27, "max_dog": 44, "min_cat": 28, "max_cat": 51},
        "TBIL": {"name": "总胆红素", "unit": "μmol/L", "min_dog": 2, "max_dog": 15, "min_cat": 2, "max_cat": 15},
        "BUN": {"name": "尿素氮", "unit": "mmol/L", "min_dog": 2.5, "max_dog": 9.6, "min_cat": 3.5, "max_cat": 9.2},
        "CREA": {"name": "肌酐", "unit": "μmol/L", "min_dog": 44, "max_dog": 159, "min_cat": 53, "max_cat": 177},
        "GLU": {"name": "血糖", "unit": "mmol/L", "min_dog": 3.3, "max_dog": 6.7, "min_cat": 3.9, "max_cat": 7.5},
        "CA": {"name": "钙", "unit": "mmol/L", "min_dog": 2.2, "max_dog": 3.0, "min_cat": 2.1, "max_cat": 2.9},
        "PHOS": {"name": "磷", "unit": "mmol/L", "min_dog": 0.8, "max_dog": 1.9, "min_cat": 1.0, "max_cat": 2.4},
        "NA": {"name": "钠", "unit": "mmol/L", "min_dog": 140, "max_dog": 155, "min_cat": 147, "max_cat": 162},
        "K": {"name": "钾", "unit": "mmol/L", "min_dog": 3.7, "max_dog": 5.8, "min_cat": 3.8, "max_cat": 5.6},
        "CL": {"name": "氯", "unit": "mmol/L", "min_dog": 105, "max_dog": 122, "min_cat": 110, "max_cat": 127},
        "AMY": {"name": "淀粉酶", "unit": "U/L", "min_dog": 500, "max_dog": 1500, "min_cat": 500, "max_cat": 1500},
        "LIPA": {"name": "脂肪酶", "unit": "U/L", "min_dog": 200, "max_dog": 1800, "min_cat": 200, "max_cat": 1800},
        "CK": {"name": "肌酸激酶", "unit": "U/L", "min_dog": 50, "max_dog": 400, "min_cat": 50, "max_cat": 400},
    },
    "尿检": {
        "COLOR": {"name": "颜色", "unit": "", "normal": ["淡黄色", "黄色", "琥珀色"]},
        "CLARITY": {"name": "透明度", "unit": "", "normal": ["清亮", "透明"]},
        "SG": {"name": "比重", "unit": "", "min_dog": 1.015, "max_dog": 1.045, "min_cat": 1.020, "max_cat": 1.050},
        "PH": {"name": "pH值", "unit": "", "min_dog": 5.5, "max_dog": 7.5, "min_cat": 5.5, "max_cat": 7.5},
        "PRO": {"name": "蛋白质", "unit": "", "normal": ["阴性", "-", "±"]},
        "GLU": {"name": "葡萄糖", "unit": "", "normal": ["阴性", "-"]},
        "KET": {"name": "酮体", "unit": "", "normal": ["阴性", "-"]},
        "BIL": {"name": "胆红素", "unit": "", "normal": ["阴性", "-"]},
        "URO": {"name": "尿胆原", "unit": "", "normal": ["正常", "±", "+"]},
        "BLD": {"name": "潜血", "unit": "", "normal": ["阴性", "-"]},
        "LEU": {"name": "白细胞", "unit": "", "normal": ["阴性", "-"]},
        "NIT": {"name": "亚硝酸盐", "unit": "", "normal": ["阴性", "-"]},
    },
    "粪检": {
        "CONSISTENCY": {"name": "性状", "unit": "", "normal": ["成形", "软便"]},
        "COLOR": {"name": "颜色", "unit": "", "normal": ["棕色", "黄褐色"]},
        "PARASITE": {"name": "寄生虫", "unit": "", "normal": ["未见", "阴性"]},
        "OVA": {"name": "虫卵", "unit": "", "normal": ["未见", "阴性"]},
        "WBC": {"name": "白细胞", "unit": "/HP", "min": 0, "max": 3},
        "RBC": {"name": "红细胞", "unit": "/HP", "min": 0, "max": 2},
        "FAT": {"name": "脂肪滴", "unit": "", "normal": ["少量", "未见"]},
    },
    "皮肤刮片": {
        "FUNGUS": {"name": "真菌", "unit": "", "normal": ["阴性", "未见"]},
        "MITE": {"name": "螨虫", "unit": "", "normal": ["阴性", "未见"]},
        "BACTERIA": {"name": "细菌", "unit": "", "normal": ["少量", "未见"]},
    },
    "细胞学检查": {
        "CELL_TYPE": {"name": "细胞类型", "unit": "", "normal": []},
        "INFLAMMATION": {"name": "炎症细胞", "unit": "", "normal": ["少量", "未见"]},
        "NEOPLASIA": {"name": "肿瘤细胞", "unit": "", "normal": ["未见"]},
    }
}

ICD_VET_CODES: List[Dict[str, str]] = [
    {"code": "A00-B99", "name": "某些传染病和寄生虫病", "category": "传染病"},
    {"code": "B88.0", "name": "耳螨感染", "category": "寄生虫病"},
    {"code": "B88.1", "name": "疥螨感染", "category": "寄生虫病"},
    {"code": "B88.2", "name": "蠕形螨感染", "category": "寄生虫病"},
    {"code": "B36.9", "name": "皮肤真菌病", "category": "真菌病"},
    {"code": "C00-D48", "name": "肿瘤", "category": "肿瘤"},
    {"code": "D36.9", "name": "良性肿瘤", "category": "肿瘤"},
    {"code": "C80.9", "name": "恶性肿瘤", "category": "肿瘤"},
    {"code": "E00-E90", "name": "内分泌、营养和代谢疾病", "category": "内分泌"},
    {"code": "E10-E14", "name": "糖尿病", "category": "内分泌"},
    {"code": "E14.9", "name": "糖尿病", "category": "内分泌"},
    {"code": "E03.9", "name": "甲状腺功能减退症", "category": "内分泌"},
    {"code": "E05.9", "name": "甲状腺功能亢进症", "category": "内分泌"},
    {"code": "F00-F99", "name": "精神和行为障碍", "category": "神经"},
    {"code": "G00-G99", "name": "神经系统疾病", "category": "神经"},
    {"code": "G40.9", "name": "癫痫", "category": "神经"},
    {"code": "H00-H59", "name": "眼和附器疾病", "category": "眼科"},
    {"code": "H10.9", "name": "结膜炎", "category": "眼科"},
    {"code": "H25.9", "name": "白内障", "category": "眼科"},
    {"code": "H60-H95", "name": "耳和乳突疾病", "category": "耳科"},
    {"code": "H66.9", "name": "中耳炎", "category": "耳科"},
    {"code": "I00-I99", "name": "循环系统疾病", "category": "心血管"},
    {"code": "I50.9", "name": "心力衰竭", "category": "心血管"},
    {"code": "I10", "name": "高血压", "category": "心血管"},
    {"code": "J00-J99", "name": "呼吸系统疾病", "category": "呼吸"},
    {"code": "J06.9", "name": "上呼吸道感染", "category": "呼吸"},
    {"code": "J18.9", "name": "肺炎", "category": "呼吸"},
    {"code": "J40-J47", "name": "慢性阻塞性肺病", "category": "呼吸"},
    {"code": "J45.9", "name": "支气管哮喘", "category": "呼吸"},
    {"code": "J98.4", "name": "肺炎", "category": "呼吸"},
    {"code": "K00-K93", "name": "消化系统疾病", "category": "消化"},
    {"code": "K12.9", "name": "口腔炎", "category": "消化"},
    {"code": "K29.9", "name": "胃炎", "category": "消化"},
    {"code": "K31.9", "name": "胃病", "category": "消化"},
    {"code": "K52.9", "name": "肠炎", "category": "消化"},
    {"code": "K59.0", "name": "便秘", "category": "消化"},
    {"code": "K59.1", "name": "腹泻", "category": "消化"},
    {"code": "K85.9", "name": "胰腺炎", "category": "消化"},
    {"code": "K86.9", "name": "胰腺疾病", "category": "消化"},
    {"code": "L00-L99", "name": "皮肤和皮下组织疾病", "category": "皮肤"},
    {"code": "L08.9", "name": "皮肤感染", "category": "皮肤"},
    {"code": "L20-L30", "name": "皮炎和湿疹", "category": "皮肤"},
    {"code": "L29.9", "name": "瘙痒症", "category": "皮肤"},
    {"code": "M00-M99", "name": "肌肉骨骼系统和结缔组织疾病", "category": "骨科"},
    {"code": "M13.9", "name": "关节炎", "category": "骨科"},
    {"code": "M19.9", "name": "骨关节病", "category": "骨科"},
    {"code": "M54.5", "name": "腰背痛", "category": "骨科"},
    {"code": "N00-N99", "name": "泌尿生殖系统疾病", "category": "泌尿"},
    {"code": "N10", "name": "急性肾小管-间质肾炎", "category": "泌尿"},
    {"code": "N19", "name": "肾衰竭", "category": "泌尿"},
    {"code": "N21.0", "name": "膀胱结石", "category": "泌尿"},
    {"code": "N20.0", "name": "肾结石", "category": "泌尿"},
    {"code": "O00-O99", "name": "妊娠、分娩和产褥期疾病", "category": "产科"},
    {"code": "P00-P96", "name": "起源于围生期的某些疾病", "category": "儿科"},
    {"code": "Q00-Q99", "name": "先天性畸形、变形和染色体异常", "category": "先天"},
    {"code": "R00-R99", "name": "症状、体征和临床与实验室异常所见", "category": "症状"},
    {"code": "R50.9", "name": "发热", "category": "症状"},
    {"code": "R10.9", "name": "腹痛", "category": "症状"},
    {"code": "R19.6", "name": "腹泻", "category": "症状"},
    {"code": "R53.8", "name": "虚弱", "category": "症状"},
    {"code": "R51", "name": "头痛", "category": "症状"},
    {"code": "S00-T98", "name": "损伤、中毒和外因的某些其他后果", "category": "外伤"},
    {"code": "T90.9", "name": "外伤后遗症", "category": "外伤"},
    {"code": "T14.9", "name": "损伤", "category": "外伤"},
    {"code": "T36-T78", "name": "中毒和其他外因", "category": "中毒"},
    {"code": "T39.9", "name": "药物中毒", "category": "中毒"},
    {"code": "V01-Y98", "name": "外界因素的某些其他后果", "category": "其他"},
    {"code": "Z00-Z99", "name": "影响健康状态和与保健机构接触的因素", "category": "其他"},
    {"code": "Z00.0", "name": "健康体检", "category": "其他"},
    {"code": "Z25.1", "name": "狂犬病疫苗接种", "category": "预防接种"},
    {"code": "Z29.9", "name": "预防接种", "category": "预防接种"},
]


def check_abnormal_value(
    exam_type: str,
    item_key: str,
    value: Any,
    species: Optional[str] = None
) -> Dict[str, Any]:
    exam_ranges = LAB_REFERENCE_RANGES.get(exam_type, {})
    item_range = exam_ranges.get(item_key)
    
    if not item_range:
        return {"is_abnormal": False, "message": "无参考范围"}
    
    result = {
        "is_abnormal": False,
        "message": "正常",
        "reference": item_range.get("name", item_key),
        "unit": item_range.get("unit", ""),
        "value": value
    }
    
    if "normal" in item_range:
        if isinstance(value, str):
            if value.strip() not in item_range["normal"]:
                result["is_abnormal"] = True
                result["message"] = f"异常，正常值：{', '.join(item_range['normal'])}"
        return result
    
    if isinstance(value, (int, float)):
        species_key = species if species in ["犬", "猫"] else "dog"
        species_prefix = "dog" if species == "犬" else ("cat" if species == "猫" else "dog")
        
        if item_range.get("species") == "通用":
            min_val = item_range.get("min")
            max_val = item_range.get("max")
        else:
            min_val = item_range.get(f"min_{species_prefix}") or item_range.get("min")
            max_val = item_range.get(f"max_{species_prefix}") or item_range.get("max")
        
        if min_val is not None and max_val is not None:
            result["reference_range"] = f"{min_val}-{max_val} {result['unit']}".strip()
            if value < min_val:
                result["is_abnormal"] = True
                result["message"] = "偏低"
                result["direction"] = "low"
            elif value > max_val:
                result["is_abnormal"] = True
                result["message"] = "偏高"
                result["direction"] = "high"
    
    return result


def analyze_lab_exam(
    exam_type: str,
    result_data: Dict[str, Any],
    species: Optional[str] = None
) -> Dict[str, Any]:
    analysis = {}
    has_abnormal = False
    
    for key, value in result_data.items():
        check_result = check_abnormal_value(exam_type, key, value, species)
        analysis[key] = check_result
        if check_result["is_abnormal"]:
            has_abnormal = True
    
    return {
        "analysis": analysis,
        "has_abnormal": has_abnormal,
        "total_count": len(result_data),
        "abnormal_count": sum(1 for v in analysis.values() if v["is_abnormal"])
    }
