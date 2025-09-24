#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学分加权成绩计算脚本
根据大一大二学期学分计算加权平均分并生成排名
"""

import pandas as pd
from pathlib import Path

# 学分配置
CREDITS = {
    'year1': 51.8,  # 大一总学分 (25.4 + 26.4)
    'year2': 48.3,  # 大二总学分 (24.9 + 23.4)
    'total': 100.1  # 总学分
}

def load_data():
    """加载数据文件"""
    print("📚 正在加载数据文件...")
    
    # 加载23-24成绩（大一）
    file_23_24 = Path("23-24.csv")
    if not file_23_24.exists():
        print(f"❌ 文件不存在: {file_23_24}")
        return None, None
    
    # 读取大一成绩（无表头格式）
    df_year1 = pd.read_csv(file_23_24, header=None, names=['学号', '大一成绩'])
    df_year1 = df_year1.dropna()
    df_year1['学号'] = df_year1['学号'].astype(str)
    df_year1['大一成绩'] = pd.to_numeric(df_year1['大一成绩'], errors='coerce')
    
    # 加载24-25成绩（大二）
    file_24_25 = Path("24-25.csv")
    if not file_24_25.exists():
        print(f"❌ 文件不存在: {file_24_25}")
        return None, None
    
    df_year2 = pd.read_csv(file_24_25, encoding='utf-8-sig')
    df_year2 = df_year2.dropna()
    df_year2['学号'] = df_year2['学号'].astype(str)
    df_year2['大二成绩'] = pd.to_numeric(df_year2['课程成绩'], errors='coerce')
    df_year2 = df_year2[['学号', '大二成绩']]
    
    print(f"✅ 大一成绩数据: {len(df_year1)} 条记录")
    print(f"✅ 大二成绩数据: {len(df_year2)} 条记录")
    
    return df_year1, df_year2

def calculate_weighted_grades(df_year1, df_year2):
    """计算学分加权成绩"""
    print("\n🧮 正在计算学分加权成绩...")
    
    # 合并数据，使用外连接确保包含所有学生
    df_merged = pd.merge(df_year2, df_year1, on='学号', how='left')
    
    # 分类学生
    complete_students = df_merged[df_merged['大一成绩'].notna()]  # 有完整成绩的学生
    transfer_students = df_merged[df_merged['大一成绩'].isna()]  # 转入学生（只有大二成绩）
    
    print(f"👥 完整成绩学生: {len(complete_students)} 人")
    print(f"🔄 转入学生: {len(transfer_students)} 人")
    
    results = []
    
    # 计算完整学生的加权成绩
    for _, student in complete_students.iterrows():
        weighted_score = (
            student['大一成绩'] * CREDITS['year1'] + 
            student['大二成绩'] * CREDITS['year2']
        ) / CREDITS['total']
        
        results.append({
            '学号': student['学号'],
            '大一成绩': student['大一成绩'],
            '大二成绩': student['大二成绩'],
            '加权平均分': round(weighted_score, 2),
            '学生类型': '完整'
        })
    
    # 处理转入学生（只有大二成绩）
    for _, student in transfer_students.iterrows():
        results.append({
            '学号': student['学号'],
            '大一成绩': None,
            '大二成绩': student['大二成绩'],
            '加权平均分': round(student['大二成绩'], 2),  # 转入学生直接用大二成绩
            '学生类型': '转入'
        })
    
    # 创建结果DataFrame
    df_results = pd.DataFrame(results)
    
    # 按加权平均分降序排序
    df_results = df_results.sort_values('加权平均分', ascending=False).reset_index(drop=True)
    
    # 添加排名
    df_results['排名'] = range(1, len(df_results) + 1)
    
    # 重新排列列顺序
    df_results = df_results[['排名', '学号', '大一成绩', '大二成绩', '加权平均分', '学生类型']]
    
    return df_results

def save_results(df_results):
    """保存结果"""
    print("\n💾 正在保存结果...")
    
    # 保存完整结果
    output_file = Path("加权成绩排名.csv")
    df_results.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    # 保存简化版（只有排名、学号、加权平均分）
    simple_file = Path("最终排名.csv")
    df_simple = df_results[['排名', '学号', '加权平均分']].copy()
    df_simple.to_csv(simple_file, index=False, encoding='utf-8-sig')
    
    print(f"✅ 完整结果已保存到: {output_file}")
    print(f"✅ 简化排名已保存到: {simple_file}")
    
    return output_file, simple_file

def print_summary(df_results):
    """打印统计摘要"""
    print("\n📊 统计摘要:")
    print("=" * 50)
    
    complete_students = df_results[df_results['学生类型'] == '完整']
    transfer_students = df_results[df_results['学生类型'] == '转入']
    
    print(f"📈 总人数: {len(df_results)} 人")
    print(f"👥 完整成绩学生: {len(complete_students)} 人")
    print(f"🔄 转入学生: {len(transfer_students)} 人")
    
    print(f"\n🏆 成绩统计:")
    print(f"最高分: {df_results['加权平均分'].max():.2f} (排名第1)")
    print(f"最低分: {df_results['加权平均分'].min():.2f} (排名第{len(df_results)})")
    print(f"平均分: {df_results['加权平均分'].mean():.2f}")
    print(f"中位数: {df_results['加权平均分'].median():.2f}")
    
    print(f"\n🥇 前10名:")
    top10 = df_results.head(10)
    for _, student in top10.iterrows():
        type_mark = "🔄" if student['学生类型'] == '转入' else "👤"
        print(f"  {student['排名']:2d}. {type_mark} {student['学号']} - {student['加权平均分']:.2f}分")
    
    print(f"\n📐 学分权重配置:")
    print(f"大一学分: {CREDITS['year1']} ({CREDITS['year1']/CREDITS['total']*100:.1f}%)")
    print(f"大二学分: {CREDITS['year2']} ({CREDITS['year2']/CREDITS['total']*100:.1f}%)")

def main():
    """主函数"""
    print("🎓 学分加权成绩计算系统")
    print("=" * 50)
    
    # 加载数据
    df_year1, df_year2 = load_data()
    if df_year1 is None or df_year2 is None:
        return
    
    # 计算加权成绩
    df_results = calculate_weighted_grades(df_year1, df_year2)
    
    # 保存结果
    output_file, simple_file = save_results(df_results)
    
    # 打印摘要
    print_summary(df_results)
    
    print(f"\n🎉 计算完成! 结果文件:")
    print(f"📄 {output_file} - 详细成绩表")
    print(f"📄 {simple_file} - 最终排名表")

if __name__ == "__main__":
    main()
