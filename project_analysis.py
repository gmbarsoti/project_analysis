from module_class_builder import checking_db, cursor_generator, master_query, time_entries_query, issues_list_generate, create_module_list, task_table_xls_generator


def project_analysis_execute():
    #checking for DB
    db_file_path = checking_db()
    if db_file_path == -1:
        input("Error: DB not found.\nPress Enter to close this window.")
        
    else:
        
        print("Generating table...")
        try:
            cursor = cursor_generator(db_file_path)
        except:
            input("Error when generating cursor.\nPress Enter to close this window.")
             
        try:
            master_query_consult = master_query(cursor)
            print("DB query was done.")
        except:
            input("Error when querying DB.\nPress Enter to close this window.")
         
        try:
            time_entries_consult = time_entries_query(cursor)
         
            issues_list = issues_list_generate(time_entries_consult)
            print("Issues list was built.")
        except:
            input("Error when building Issues list.\nPress Enter to close this window.")
             
         
        try:
            modules = create_module_list(issues_list, master_query_consult)
            print("Modules list was build.")
        except:
            input("Error when building Modules list.\nPress Enter to close this window.")
     
             
            print("Generating .xlsx file...")
        try:
            task_table_xls_generator(modules)
            print("Table generated.\nThe application has finished.\n")
            input("Press Enter to close this window.")
        except:
            input("\nError when generating .xlsx\nPress Enter to close this window.")
             

if __name__ == "__main__":
    project_analysis_execute()



     
