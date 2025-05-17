import mysql.connector 

config = {
    "username": "root", 
    "password": "Lzx25226",
    "host":     "localhost", 
    "database": "DBPractice03"
}

def read_relations(file_path="./relations.txt"):
    relations = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("(") and "," in line:
                # 替换中文引号为英文引号
                line = line.replace("‘", "'").replace("’", "'")
                # 去除括号和逗号
                pair = line.strip("(),;")
                a, b = [x.strip().strip("'") for x in pair.split(",")]
                relations.append((a, b))
    return relations

def insert_relations_to_db(relations):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # 创建表（如果不存在）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                father VARCHAR(50),
                son VARCHAR(50)
            )
        """)
        # 插入数据
        for father, son in relations:
            cursor.execute(
                "INSERT INTO relations (father, son) VALUES (%s, %s)",
                (father, son)
            )
        conn.commit()
        print(f"[insert_relations_to_db] 成功插入 {len(relations)} 条父子关系到数据库。")
    except mysql.connector.Error as err:
        print(f"[insert_relations_to_db] 插入数据时发生错误: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            
def drop_relations_table():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS relations")
        conn.commit()
        print("[drop_relations_table] 表 relations 已删除。")
    except mysql.connector.Error as err:
        print(f"[drop_relations_table] 删除表时发生错误: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            
def print_all_brothers():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # 查询所有有相同父亲的兄弟关系
        cursor.execute("""
            SELECT t1.son, t2.son, t1.father
            FROM relations t1
            JOIN relations t2 ON t1.father = t2.father AND t1.son < t2.son
        """)
        results = cursor.fetchall()
        if results:
            print("\n[print_all_brothers] 兄弟关系如下：")
            for bro1, bro2, father in results:
                print(f"{bro1} 和 {bro2} 是兄弟（父亲：{father}）")
        else:
            print("[print_all_brothers] 没有兄弟关系。")
    except mysql.connector.Error as err:
        print(f"[print_all_brothers] 查询兄弟关系时发生错误: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            
def print_all_ancestor_relations():
    """
    打印所有祖宗关系，约定：父亲是祖宗，父亲的祖宗也是祖宗。
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # 使用递归CTE查询所有祖宗关系
        cursor.execute("""
            WITH RECURSIVE ancestors AS (
                SELECT father AS ancestor, son
                FROM relations
                UNION ALL
                SELECT r.father, a.son
                FROM relations r
                JOIN ancestors a ON r.son = a.ancestor
            )
            SELECT ancestor, son FROM ancestors WHERE ancestor != son
        """)
        results = cursor.fetchall()
        if results:
            print("\n[print_all_ancestor_relations] 祖宗关系如下：")
            for ancestor, son in results:
                print(f"{ancestor} 是 {son} 的祖宗")
        else:
            print("[print_all_ancestor_relations] 没有祖宗关系。")
    except mysql.connector.Error as err:
        print(f"[print_all_ancestor_relations] 查询祖宗关系时发生错误: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()