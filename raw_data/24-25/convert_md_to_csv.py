#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将24-25排名.md中的Markdown表格数据转换为CSV格式
"""

import pandas as pd
import re
from pathlib import Path

def convert_md_to_csv():
    """将Markdown表格转换为CSV"""
    
    input_file = Path("24-25排名.md")
    output_file = Path("24-25.csv")
    
    if not input_file.exists():
        print(f"❌ 文件不存在: {input_file}")
        return
    
    print(f"正在读取文件: {input_file}")
    
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析数据
    data = []
    lines = content.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        
        # 跳过空行和分隔线
        if not line or line.startswith('|---') or '----' in line:
            continue
            
        # 处理表格行
        if line.startswith('|') and line.endswith('|'):
            # 移除首尾的|，然后分割
            cells = [cell.strip() for cell in line[1:-1].split('|')]
            
            # 确保有两列数据且不是表头
            if len(cells) >= 2 and cells[0] != '学号' and cells[0] != '----------':
                student_id = cells[0].strip()
                score = cells[1].strip()
                
                # 验证学号格式（应该是数字）和成绩格式
                if student_id and score and student_id.isdigit() and score.replace('.', '').replace('-', '').isdigit():
                    data.append({
                        '学号': student_id,
                        '课程成绩': float(score)
                    })
    
    if not data:
        print("❌ 没有找到有效的数据")
        return
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 按学号排序
    df = df.sort_values('学号').reset_index(drop=True)
    
    # 保存为CSV
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"✅ 转换完成!")
    print(f"共提取了 {len(df)} 条记录")
    print(f"保存到文件: {output_file}")
    
    # 显示数据预览
    print(f"\n📋 数据预览:")
    print("前5行:")
    print(df.head().to_string(index=False))
    print("\n后5行:")
    print(df.tail().to_string(index=False))
    
    # 统计信息
    print(f"\n📊 统计信息:")
    print(f"最高分: {df['课程成绩'].max()}")
    print(f"最低分: {df['课程成绩'].min()}")
    print(f"平均分: {df['课程成绩'].mean():.2f}")
    
    return df

if __name__ == "__main__":
    convert_md_to_csv()
