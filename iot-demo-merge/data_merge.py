import sqlite3

# 源数据库文件列表
source_dbs = [
    "Test-11237-1-250215_1810",
    "Test-11237-1-250216_0930",
    "Test-11237-1-250217_0240",
    "Test-11237-1-250217_1910",
    "Test-11237-1-250218_0950",
    "Test-11237-1-250219_0230",
    "Test-11275-1-250213_1320",
    "Test-11275-1-250214_1110",
    "Test-11275-1-250215_1000",
    "Test-11275-1-250216_1050",
    "Test-11275-1-250217_0930",
    "Test-11299-1-250215_2205",
    "Test-11299-1-250216_1055",
    "Test-11299-1-250217_1814",
    "Test-11299-1-250218_0734",
    "Test-11299-1-250218_2333"
]
target_db = "testdb"  # 目标数据库

# 需要合并的表名
tables_to_merge = [
    "Alarms", "Channels", "Constraints", "CycleDsp", "Cycle_Sensors", "Cycles",
    "Devices", "Features", "Hardware", "Limits", "Log", "PLCReport", "PMDBCKUP", 
    "Program", "SensorLink", "Sensor_Map", "Sensors", "Source", "Statistics", "Status_C01",
    "Trend_C01_F01", "Trend_C01_F02", "Version"
]

# 连接目标数据库
conn_target = sqlite3.connect(target_db)
cursor_target = conn_target.cursor()

for db_index, db in enumerate(source_dbs):
    conn_source = sqlite3.connect(db)
    cursor_source = conn_source.cursor()
    
    for table_name in tables_to_merge:
        # 检查源数据库是否存在该表
        cursor_source.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor_source.fetchone():
            print(f"跳过 {db}，未找到表 {table_name}")
            continue  # 如果该表不存在，则跳过
        
        # 获取表结构
        cursor_source.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        create_table_sql = cursor_source.fetchone()[0]

        # 在目标数据库创建表（如果不存在），并添加 tool_number 字段
        if not cursor_target.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';").fetchone():
            modified_sql = create_table_sql[:-1] + ", tool_number TEXT DEFAULT '' );"
            cursor_target.execute(modified_sql)

        # 复制数据，并添加数据库来源信息
        cursor_source.execute(f"SELECT * FROM {table_name};")
        rows = cursor_source.fetchall()
        # print(rows)

        if rows:
            cursor_source.execute(f"PRAGMA table_info({table_name});")
            columns = [col[1] for col in cursor_source.fetchall()]  # 获取表列名
            # print("eeeeeeeee")
            # 获取主键列名
            primary_key = "ID"

            # 如果有主键字段 db_index+1*100000+row[0]
            if columns[0]=="ID":
                new_rows = [((db_index+1)*100000 + row[0],) + row[1:] + (source_dbs[db_index][7:12],) for row in rows]
                # 创建插入语句，确保包含主键和 tool_number
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}, tool_number) VALUES ({','.join(['?'] * (len(columns) + 1))})"


            else:
                # 对于没有主键的表，按原结构插入
                new_rows = [row + (source_dbs[db_index][7:12],) for row in rows]
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}, tool_number) VALUES ({','.join(['?'] * (len(columns) + 1))})"

            # 如果是 Statistics 表，修改 Source，workpiece 字段
            if table_name == "Statistics":
                new_rows = [row[:columns.index('Source')] + ((db_index+1)*100000+ row[columns.index('Source')],) + row[columns.index('Source')+1:] for row in new_rows]
                new_rows = [row[:columns.index('WorkPiece')] + ((db_index+1)*100000+ row[columns.index('WorkPiece')],) + row[columns.index('WorkPiece')+1:] for row in new_rows]
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}, tool_number) VALUES ({','.join(['?'] * (len(columns) + 1))})"
            
            # if table_name == "Source":
            #     new_rows = [row[:columns.index('Tool_Num')] + ((db_index+1)*100000+ row[columns.index('Tool_Num')],) + row[columns.index('Tool_Num')+1:] for row in new_rows]
            #     insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}, tool_number) VALUES ({','.join(['?'] * (len(columns) + 1))})"

            if table_name == "Trend_C01_F01":
                new_rows = [row[:columns.index('Source')] + ((db_index+1)*100000+ row[columns.index('Source')],) + row[columns.index('Source')+1:] for row in new_rows]
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}, tool_number) VALUES ({','.join(['?'] * (len(columns) + 1))})"
            
            if table_name == "Trend_C01_F02":
                new_rows = [row[:columns.index('Source')] + ((db_index+1)*100000+ row[columns.index('Source')],) + row[columns.index('Source')+1:] for row in new_rows]
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}, tool_number) VALUES ({','.join(['?'] * (len(columns) + 1))})"
                                                
            if table_name == "Log":
                new_rows = [row[:columns.index('WorkPiece')] + ((db_index+1)*100000+ row[columns.index('WorkPiece')],) + row[columns.index('WorkPiece')+1:] for row in new_rows]
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}, tool_number) VALUES ({','.join(['?'] * (len(columns) + 1))})"
                
            # print(new_rows)
            # 插入数据
            cursor_target.executemany(insert_sql, new_rows)
            print(f"成功合并 {len(rows)} 条数据到 {table_name}，来源：{db}")
            conn_target.commit()

    conn_source.close()

# 提交并关闭目标数据库
conn_target.commit()
conn_target.close()

print("所有数据合并完成！")
