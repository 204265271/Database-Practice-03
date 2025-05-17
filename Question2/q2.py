import mysql.connector
import json 

config = {
    "username": "root", 
    "password": "Lzx25226",
    "host":     "localhost", 
    "database": "DBPractice03"
}

class QA:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer

class KnowledgePoint:
    def __init__(self, key_point: str = "", explanation: str = "", qa: QA = None):
        self.key_point = key_point
        self.explanation = explanation
        self.qa = qa

class Section:
    def __init__(self, section_title: str = "", knowledge_points: list = None):
        self.section_title = section_title
        self.knowledge_points = knowledge_points if knowledge_points else []

class LectureData:
    def __init__(self, chapter: str = "", sections: list = None, question_bank: list = None):
        self.chapter = chapter
        self.sections = sections if sections else []
        self.question_bank = question_bank if question_bank else []
        
def load_lecture_data_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 假设 example.json 没有 chapter 字段，可以手动指定
    lecture = LectureData(chapter="关系规范化理论")
    
    # 处理 sections
    for section in data.get("sections", []):
        section_title = section.get("section_title", "")
        knowledge_points = []
        for kp in section.get("knowledge_points", []):
            key_point = kp.get("key_point", "")
            explanation = kp.get("explanation", "")
            qa_data = kp.get("qa")
            qa = QA(qa_data["question"], qa_data["answer"]) if qa_data else None
            knowledge_points.append(KnowledgePoint(key_point, explanation, qa))
        lecture.sections.append(Section(section_title, knowledge_points))
    
    # 处理 question_bank
    question_bank = []
    for qb in data.get("question_bank", []):
        question = qb.get("question", "")
        answer = qb.get("answer", "")
        question_bank.append(QA(question, answer))
    lecture.question_bank = question_bank
    
    return lecture

# the first query: for all section name 
def query1(lecture_data: LectureData):
    print("Section Titles:")
    for section in lecture_data.sections:
        print(f"  - {section.section_title}")
        
# the second query: count the number of qa structures in the lecture-data struct 
def query2(lecture_data: LectureData):
    qa_count = 0
    for section in lecture_data.sections:
        for kp in section.knowledge_points:
            if kp.qa:
                qa_count += 1
    qa_count += len(lecture_data.question_bank)  # 加上 question_bank 中的 QA 数量
    print(f"Total number of QA structures: {qa_count}")

# the additional query: print all data in the lecture struct
def query(lecture_data: LectureData):
    print(f"Chapter: {lecture_data.chapter}")
    print("\nSections:")
    for section in lecture_data.sections:
        print(f"  Section Title: {section.section_title}")
        for kp in section.knowledge_points:
            print(f"    Key Point: {kp.key_point}")
            print(f"    Explanation: {kp.explanation}")
            if kp.qa:
                print(f"      Question: {kp.qa.question}")
                print(f"      Answer: {kp.qa.answer}")
    print("\nQuestion Bank:")
    for qa in lecture_data.question_bank:
        print(f"  Question: {qa.question}")
        print(f"  Answer: {qa.answer}")
        
def flatten_lecture_data_to_1nf(lecture_data: LectureData):
    conn = None
    cursor = None
    try:
        # 连接数据库
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        table_name = "LectureData_1NF"
        
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"[flatten_lecture_data_to_1nf] 表 {table_name} 已删除。")

        # 创建 1NF 表
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                chapter VARCHAR(255),
                section_title VARCHAR(255),
                key_point VARCHAR(255),
                explanation TEXT,
                question TEXT,
                answer TEXT
            )
        """)

        # 扁平化数据并插入到表中
        for section in lecture_data.sections:
            for kp in section.knowledge_points:
                question = kp.qa.question if kp.qa else None
                answer = kp.qa.answer if kp.qa else None
                cursor.execute(f"""
                    INSERT INTO {table_name} (chapter, section_title, key_point, explanation, question, answer)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (lecture_data.chapter, section.section_title, kp.key_point, kp.explanation, question, answer))

        # 提交事务
        conn.commit()

        # 打印表的所有内容
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        print(f"\nContents of table '{table_name}':")
        for row in rows:
            print()
            print(row)

    except mysql.connector.Error as err:
        print(f"[flatten_lecture_data_to_1nf] Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()