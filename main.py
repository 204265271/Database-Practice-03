from Question1.q1 import *
from Question2.q2 import *
import Question3.q3 
import os

def init_db():
    try: 
        mydb = mysql.connector.connect(
            username = "root", 
            password = "Lzx25226",
            host = "localhost",
        )
        
        mycursor = mydb.cursor() 
        mycursor.execute("CREATE DATABASE IF NOT EXISTS DBPractice03")
        mycursor.execute("USE DBPractice03")
        
        print(f"[main] create database DBPractice03")
    
    except mysql.connector.Error as err:
        print(f"[main] create database DBPractice03 failed: {err}") 
    finally:
        # 确保关闭游标和数据库连接
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if mydb.is_connected():
            mydb.close()
            print("[main] database connection closed") 

if __name__ == "__main__":
    init_db()

    # Question 1
    print() 
    print("         ### Question 1 ###           ")
    print()
    drop_relations_table()
    insert_relations_to_db(read_relations(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Question1", "relations.txt")))
    print_all_brothers()
    print_all_ancestor_relations()
    
    # Question 2
    print()
    print("         ### Question 2 ###           ")
    print()
    lecture_data = load_lecture_data_from_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Question2", "example.json"))
    print("Query1: print all data in a LectureData")
    query1(lecture_data)
    print()
    print("Query2: count the number of QA structures in a LectureData")
    query2(lecture_data)
    print() 
    print("Flatten the JSON file to an 1NF table")
    flatten_lecture_data_to_1nf(lecture_data)
    
    # Question 3
    print()
    print("         ### Question 3 ###           ")
    print()
    Question3.q3.q3_full_stage()
    