from db_project_analysis_classes import module_class, task
import sqlite3
import os
from issid_analists_times import issues_list_generate, time_entries_query
from xls_module import task_table_xls_generator
from pathlib import Path


def master_query(cursor):
    # 1 - Get hust projects that have issid
    # 2 - Get tasks that have an issid assigned to it and the number of items per task
    # 3 - Get tasks names 
    # 4 - Get project parents names
    full_query = """select five.issid, five.proname, five.modid, five.traname, five.funcount, six.project_parent_name
                    from
                        (select distinct three.issid, three.proid, three.proname, three.modid, four.traname, three.funcount, three.proparentid 
                        from
                        
                            (select one.proparentid, one.issid, one.proid, one.proname, one.modid, one.traid, two.funcount 
                            from
                            
                                (select project.proparentid, project.proid, project.proname, project.modid, issues.traid, issues.issid 
                                from project 
                                inner join issues 
                                where project.proid = issues.proid) as one
                                
                            inner join modules_functions as two
                            where one.modid = two.modid and one.traid = two.traid) as three
                            
                        inner join trackers as four
                        where four.traid = three.traid) as five
                    inner join (select proname as project_parent_name, proid
                                from project
                                where proparentid = 10) as six
                    where six.proid = five.proparentid"""

    cursor.execute(full_query)
    consult = cursor.fetchall()
    return consult    

def cursor_generator(db_file_path):
    
    #connecting to db
    conn = sqlite3.connect(db_file_path)
    
    cursor = conn.cursor()
    
    return cursor

    
def create_module_list(issues_list, consult):
    
    module_name = ''
    module_code = 0
    module_project_parent_code = ''
    module_list = []
    
    for consult_tuple in consult:
        
        module_name = consult_tuple[1]
        module_code = consult_tuple[2]
        module_project_parent_code = consult_tuple[5] 
        
        issue_code = consult_tuple[0]
        task_name =  consult_tuple[3]
        items_quantity = consult_tuple[4]
        
        
        # mouting module object
        new_module = module_class(module_name, module_code, [], module_project_parent_code)
        
        found_module = next((module for module in module_list if module.code == new_module.code), None)
        
        # add new module to module list if it is not in module list
        if found_module == None:
            module_list.append(new_module)
        
        
        # mouting task object
        found_issue_obj = next((issue for issue in issues_list if issue.code == issue_code), None)
        
        if found_issue_obj == None:
            pass
            #===================================================================
            # print("Issue: ", issue_code )
            # print("No one developed this issue ")
            # print("It will not be used to evaluate on the statistic")
            #===================================================================
        else:
                
            new_task = task(found_issue_obj, task_name, items_quantity)
            
            
            # place this task to its module
            
            found_module = next((module for module in module_list if module.code == new_module.code), None)
            
            found_module.tasks.append(new_task) 

        
    return module_list

def checking_db():
    
    db_dir_path = os.path.abspath(__file__ + "/../../db_directory")
    db_file_name = '/tips_project_time_module.db'
    db_file_path = db_dir_path  + db_file_name
    

    file_to_open = Path(db_file_path)
     
    if not file_to_open.is_file():
        print("Data Base NOT FOUND at db_directory.")
        print("\nDB file name must be: tips_project_time_module.db\n")
        return -1
    else:
        print("Data Base found at db_directory.")
        return db_file_path

