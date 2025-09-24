#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将CSV成绩数据转换为JSON格式，供前端查询使用
"""

import pandas as pd
import json
from pathlib import Path

def convert_csv_to_json():
    """将加权成绩排名.csv转换为JSON格式"""
    
    # 读取CSV文件
    csv_file = Path("final_results/加权成绩排名.csv")
    if not csv_file.exists():
        print(f"❌ 文件不存在: {csv_file}")
        return
    
    print("📚 正在读取CSV数据...")
    df = pd.read_csv(csv_file, encoding='utf-8-sig')
    
    print(f"✅ 成功读取 {len(df)} 条记录")
    
    # 转换为字典格式，以学号为键
    data = {}
    for _, row in df.iterrows():
        student_id = str(row['学号'])
        data[student_id] = {
            "排名": int(row['排名']),
            "学号": student_id,
            "大一成绩": row['大一成绩'] if pd.notna(row['大一成绩']) else None,
            "大二成绩": float(row['大二成绩']),
            "加权平均分": float(row['加权平均分']),
            "学生类型": row['学生类型']
        }
    
    # 保存为JSON文件
    output_file = Path("data.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON文件已保存到: {output_file}")
    
    # 显示统计信息
    complete_students = len([v for v in data.values() if v['学生类型'] == '完整'])
    transfer_students = len([v for v in data.values() if v['学生类型'] == '转入'])
    
    print(f"\n📊 数据统计:")
    print(f"总学生数: {len(data)}")
    print(f"完整成绩学生: {complete_students}")
    print(f"转入学生: {transfer_students}")
    print(f"最高分: {max(v['加权平均分'] for v in data.values()):.2f}")
    print(f"最低分: {min(v['加权平均分'] for v in data.values()):.2f}")
    
    return data

if __name__ == "__main__":
    convert_csv_to_json()
