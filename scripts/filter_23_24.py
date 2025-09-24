#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从23-24.csv中筛选出在24-25.csv中也存在的学号，生成23-24_neo.csv
"""

import pandas as pd
from pathlib import Path

def filter_csv_by_intersection():
    """根据24-25.csv中的学号筛选23-24.csv"""
    
    file_23_24 = Path("23-24.csv")
    file_24_25 = Path("24-25.csv")
    output_file = Path("23-24_neo.csv")
    
    # 检查文件是否存在
    if not file_23_24.exists():
        print(f"❌ 文件不存在: {file_23_24}")
        return
    
    if not file_24_25.exists():
        print(f"❌ 文件不存在: {file_24_25}")
        return
    
    print(f"正在读取文件...")
    
    # 读取23-24数据（假设没有表头，直接是学号,成绩格式）
    try:
        df_23_24 = pd.read_csv(file_23_24, header=None, names=['学号', '智育成绩'])
        df_23_24 = df_23_24.dropna()  # 去除空行
        df_23_24['学号'] = df_23_24['学号'].astype(str)
    except:
        # 如果有表头
        df_23_24 = pd.read_csv(file_23_24, encoding='utf-8-sig')
        df_23_24 = df_23_24.dropna()
        df_23_24['学号'] = df_23_24['学号'].astype(str)
    
    # 读取24-25数据
    df_24_25 = pd.read_csv(file_24_25, encoding='utf-8-sig')
    df_24_25 = df_24_25.dropna()
    df_24_25['学号'] = df_24_25['学号'].astype(str)
    
    print(f"23-24.csv 原始数据: {len(df_23_24)} 条记录")
    print(f"24-25.csv 参考数据: {len(df_24_25)} 条记录")
    
    # 获取24-25中的学号集合
    student_ids_24_25 = set(df_24_25['学号'].tolist())
    print(f"24-25.csv 中有 {len(student_ids_24_25)} 个学号")
    
    # 筛选23-24中在24-25中也存在的学号
    filtered_df = df_23_24[df_23_24['学号'].isin(student_ids_24_25)].copy()
    
    # 按学号排序
    filtered_df = filtered_df.sort_values('学号').reset_index(drop=True)
    
    print(f"筛选后数据: {len(filtered_df)} 条记录")
    print(f"筛选掉了: {len(df_23_24) - len(filtered_df)} 条记录")
    
    # 检查是否有24-25中的学号在23-24中不存在
    student_ids_23_24 = set(df_23_24['学号'].tolist())
    missing_in_23_24 = student_ids_24_25 - student_ids_23_24
    
    if missing_in_23_24:
        print(f"⚠️  注意: 有 {len(missing_in_23_24)} 个学号在24-25中存在但在23-24中不存在:")
        for student_id in sorted(list(missing_in_23_24))[:10]:  # 只显示前10个
            print(f"  - {student_id}")
        if len(missing_in_23_24) > 10:
            print(f"  ... 还有 {len(missing_in_23_24) - 10} 个")
    else:
        print("✅ 24-25中的所有学号都在23-24中找到了")
    
    # 保存筛选后的数据
    # 不保存表头，保持与原23-24.csv相同的格式
    filtered_df.to_csv(output_file, index=False, header=False, encoding='utf-8-sig')
    
    print(f"\n✅ 筛选完成!")
    print(f"新文件已保存到: {output_file}")
    
    # 显示预览
    print(f"\n📋 新文件预览 (前10行):")
    print(filtered_df.head(10).to_string(index=False, header=False))
    
    print(f"\n📊 统计信息:")
    print(f"原始23-24数据: {len(df_23_24)} 条")
    print(f"参考24-25数据: {len(df_24_25)} 条") 
    print(f"筛选后数据: {len(filtered_df)} 条")
    print(f"匹配率: {len(filtered_df)/len(df_24_25)*100:.1f}%")
    
    return filtered_df

if __name__ == "__main__":
    filter_csv_by_intersection()
