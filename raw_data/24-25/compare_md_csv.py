#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
比较24-25排名.md和24-25.csv中的数据是否一致
"""

import pandas as pd
import re
from pathlib import Path

def extract_md_data(md_file):
    """从Markdown文件提取数据"""
    print(f"正在读取Markdown文件: {md_file}")
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    data = []
    lines = content.strip().split('\n')
    
    for line_num, line in enumerate(lines, 1):
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
                if student_id and score and student_id.isdigit():
                    try:
                        score_float = float(score)
                        data.append({
                            '学号': student_id,
                            '课程成绩': score_float,
                            '行号': line_num
                        })
                    except ValueError:
                        continue
    
    print(f"从Markdown提取了 {len(data)} 条记录")
    return data

def extract_csv_data(csv_file):
    """从CSV文件提取数据"""
    print(f"正在读取CSV文件: {csv_file}")
    
    df = pd.read_csv(csv_file, encoding='utf-8-sig')
    
    # 转换为字典列表格式，便于比较
    data = []
    for index, row in df.iterrows():
        if pd.notna(row['学号']) and pd.notna(row['课程成绩']):
            data.append({
                '学号': str(int(row['学号'])) if isinstance(row['学号'], float) else str(row['学号']),
                '课程成绩': float(row['课程成绩']),
                '行号': index + 2  # CSV文件第1行是表头，所以+2
            })
    
    print(f"从CSV提取了 {len(data)} 条记录")
    return data

def compare_data(md_data, csv_data):
    """比较两个数据集"""
    print("\n开始比对数据...")
    
    # 转换为DataFrame便于比较
    md_df = pd.DataFrame(md_data)
    csv_df = pd.DataFrame(csv_data)
    
    print(f"Markdown数据行数: {len(md_df)}")
    print(f"CSV数据行数: {len(csv_df)}")
    
    if len(md_df) == 0:
        print("❌ Markdown数据为空!")
        return False
    
    if len(csv_df) == 0:
        print("❌ CSV数据为空!")
        return False
    
    # 按学号排序
    md_df = md_df.sort_values('学号').reset_index(drop=True)
    csv_df = csv_df.sort_values('学号').reset_index(drop=True)
    
    # 找出不匹配的记录
    mismatches = []
    all_student_ids = set(md_df['学号'].tolist() + csv_df['学号'].tolist())
    
    for student_id in sorted(all_student_ids):
        md_row = md_df[md_df['学号'] == student_id]
        csv_row = csv_df[csv_df['学号'] == student_id]
        
        if md_row.empty:
            mismatches.append(f"学号 {student_id}: 在Markdown中未找到")
        elif csv_row.empty:
            mismatches.append(f"学号 {student_id}: 在CSV中未找到")
        else:
            md_score = md_row.iloc[0]['课程成绩']
            csv_score = csv_row.iloc[0]['课程成绩']
            
            # 比较分数（允许小的浮点数误差）
            if abs(md_score - csv_score) > 0.001:
                mismatches.append(f"学号 {student_id}: 课程成绩不匹配 (MD: {md_score}, CSV: {csv_score})")
    
    # 输出结果
    if not mismatches:
        print("✅ 所有数据完全一致!")
        print(f"共比对了 {len(all_student_ids)} 个学生的记录")
        return True
    else:
        print(f"❌ 发现 {len(mismatches)} 处不匹配:")
        for mismatch in mismatches[:20]:  # 只显示前20个不匹配项
            print(f"  - {mismatch}")
        
        if len(mismatches) > 20:
            print(f"  ... 还有 {len(mismatches) - 20} 个不匹配项")
        
        return False

def main():
    """主函数"""
    md_file = Path("24-25排名.md")
    csv_file = Path("24-25.csv")
    
    if not md_file.exists():
        print(f"❌ Markdown文件不存在: {md_file}")
        return
    
    if not csv_file.exists():
        print(f"❌ CSV文件不存在: {csv_file}")
        return
    
    try:
        # 提取数据
        md_data = extract_md_data(md_file)
        csv_data = extract_csv_data(csv_file)
        
        # 比对数据
        is_match = compare_data(md_data, csv_data)
        
        # 保存详细比对结果到文件
        if md_data and csv_data:
            md_df = pd.DataFrame(md_data).drop('行号', axis=1)
            csv_df = pd.DataFrame(csv_data).drop('行号', axis=1)
            
            # 保存提取的数据
            md_df.to_csv("md_extracted_data.csv", index=False, encoding='utf-8-sig')
            csv_df.to_csv("csv_extracted_data.csv", index=False, encoding='utf-8-sig')
            print(f"\n📊 详细数据已保存到:")
            print(f"  - md_extracted_data.csv")
            print(f"  - csv_extracted_data.csv")
        
        if is_match:
            print("\n🎉 验证完成: Markdown和CSV文档数据完全一致!")
        else:
            print("\n⚠️  验证完成: 发现数据不一致，请查看上面的详细信息")
            
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
