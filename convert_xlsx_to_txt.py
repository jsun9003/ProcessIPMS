# -*- coding: utf-8 -*-
import pandas as pd
import os

# ��ȡ��ǰĿ¼�����е�xlsx�ļ�
xlsx_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]

for xlsx_file in xlsx_files:
    # ��ȡxlsx�ļ�
    df = pd.read_excel(xlsx_file)
    
    # ���˵����� "False" �� "Checked" ����
    df = df[~df.apply(lambda row: row.astype(str).str.contains('False|Checked').any(), axis=1)]
    
    # ��ȡ�ļ�������������չ����
    file_name = os.path.splitext(xlsx_file)[0]
    
    # �����ݱ���Ϊtxt�ļ�
    df.to_csv(f'{file_name}.txt', sep='\t', index=False)
