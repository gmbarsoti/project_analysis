import os
import sqlite3

from db_project_analysis_classes import analist, issue

def time_entries_query(cursor):
    cursor.execute("""SELECT *
                    FROM time_entries
                    order by issid;""")
    consult = cursor.fetchall()
    return consult


def issues_list_generate(consult):
    
    issues_list = []
    analist_obj = analist('',[])
    
    for row in consult:
        issues_code = row[1]
        analist_name = row[2]
        time_from_row = row[3]
        
        # mounting issue and  analist objects
        analist_obj = analist(analist_name, [time_from_row])
        
        issue_obj = issue(issues_code, [analist_obj])
        
        # searching for issue_obj in issue list
        found_issue_obj = next((issue_element for issue_element in issues_list if issue_element.code == issues_code), None)
        
        # If not found, add issue_obj to list 
        if found_issue_obj == None:
            
            issues_list.append(issue_obj)
        
        else:
            # object found, saerch for analist
            
            found_analist_obj = next((analist_element for analist_element in found_issue_obj.analists if analist_element.name == analist_name), None)
            # if not found, add analist_obj to this issue
            if found_analist_obj == None:
                
                found_issue_obj.analists.append(analist_obj)
                
            else:
                # analist already in this issue
                # adding time to this analist in this issue
                found_analist_obj.times.append(time_from_row)

    return issues_list





if __name__ == "__main__":
    
    db_dir_path = os.path.abspath(__file__ + "/../db_directory")
    db_file_name = '/tips_project_time_module.db'
    db_file_path = db_dir_path  + db_file_name
    
    #connecting to db
    conn = sqlite3.connect(db_file_path)
    
    cursor = conn.cursor()
    
    
    consult = time_entries_query(cursor)

    
    issue_list = issues_list_generate(consult)
    
    print(len(issue_list))
    issue_code_list = []

    for issue in issue_list:
        
        found = next((x for x in issue_code_list if issue.code == x), None)
        # if not found, add analist_obj to this issue
        if found == None:
            
            issue_code_list.append(found)
        
        
        if len(issue.analists) == 0:
            print(issue.code)
        print(len(issue_code_list))
           
  
        
        
    