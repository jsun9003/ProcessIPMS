# -*- coding: utf-8 -*-
import pandas as pd
import os

# 获取当前目录下所有的xlsx文件
xlsx_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]

for xlsx_file in xlsx_files:
    # 读取xlsx文件
    df = pd.read_excel(xlsx_file)
    
    # 过滤掉包含 "False" 或 "Checked" 的行
    df = df[~df.apply(lambda row: row.astype(str).str.contains('False|Checked').any(), axis=1)]
    
    # 获取文件名（不包括扩展名）
    file_name = os.path.splitext(xlsx_file)[0]
    
    # 将数据保存为txt文件
    df.to_csv(f'{file_name}.txt', sep='\t', index=False)
