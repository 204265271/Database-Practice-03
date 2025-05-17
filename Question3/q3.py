import os
import sqlite3
import pandas as pd
from tabulate import tabulate
from sentence_transformers import SentenceTransformer
import numpy as np

def q3_full_stage():
    TRAINING_DATA_FILE = "sts-b-train.txt"
    DB_FILE = "p3-q3.db"
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 创建 sentence 表
    cursor.execute('''
    CREATE TABLE sentence (
        sid INTEGER PRIMARY KEY AUTOINCREMENT,
        sentence1 TEXT NOT NULL,
        sentence2 TEXT NOT NULL,
        similar_score REAL NOT NULL,
        sen1_vector BLOB,
        sen2_vector BLOB,
        vecSim_score REAL
    )
    ''')
    conn.commit()

    # 加载数据到数据库
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), TRAINING_DATA_FILE), 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) != 3:
                continue
            sentence1, sentence2, score = parts
            cursor.execute('''
                INSERT INTO sentence (sentence1, sentence2, similar_score)
                VALUES (?, ?, ?)
            ''', (sentence1, sentence2, float(score)))

    conn.commit()

    # 加载预训练的句子嵌入模型
    print("[q3] Loading sentence embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # 查询所有数据
    cursor.execute("SELECT sid, sentence1, sentence2 FROM sentence")
    rows = cursor.fetchall()

    # 处理每一行，计算向量和相似度
    for sid, sentence1, sentence2 in rows:
        # 生成句子向量
        sen1_vector = model.encode(sentence1)
        sen2_vector = model.encode(sentence2)

        # 计算余弦相似度
        vec_sim_score = np.dot(sen1_vector, sen2_vector) / (np.linalg.norm(sen1_vector) * np.linalg.norm(sen2_vector))

        # 将向量和相似度插入表中
        cursor.execute('''
            UPDATE sentence
            SET sen1_vector = ?, sen2_vector = ?, vecSim_score = ?
            WHERE sid = ?
        ''', (sen1_vector.tobytes(), sen2_vector.tobytes(), float(vec_sim_score), sid))

    conn.commit()

    # 打印更新后的前 20 行
    print("\n[q3] Updated table with vector embeddings and similarity scores:")
    df = pd.read_sql_query("""
        SELECT sid, sentence1, sentence2, similar_score, vecSim_score FROM sentence
    """, conn)
    print(tabulate(df.head(20), headers='keys', tablefmt='grid', showindex=False))

    # 关闭数据库连接
    cursor.close()
    conn.close()