from string import ascii_uppercase
from db_project_analysis_classes import table_header
import xlsxwriter
import os

def header_line(workbook, worksheet):
    
    # Add a bold format to use to highlight cells.
    header_format = workbook.add_format({'bold': True,
                                     'align': 'center',
                                     'valign': 'vcenter',
                                     'fg_color': '#D7E4BC',
                                     'border': 1})

    worksheet.freeze_panes(1, 0)
    
    # Add a number format for cells with money.
     
    # Write header line.
    header_list = ['Parent Project', 'Module Code', 'Module Name', 'Task Name', 'Issue Total Time (h)', 'Items Quantity', 'Time Per Item (h)']
    
    alphabet_list = iter(ascii_uppercase)
    letter = next(alphabet_list)
    i = 0
    while letter <= 'G':
        first_row_cell = letter + '1'
        worksheet.write(first_row_cell, header_list[i], header_format)
        i += 1
        letter = next(alphabet_list)
    
    column_limits = 0
    table_header_list = []
    table_header_size_list = [4, 4, 40, 10, 4, 4, 4]
    
    iter_table_header_size = iter(table_header_size_list) 
    
    for name in header_list:
        table_header_obj = table_header(name, next(iter_table_header_size))
        table_header_list.append(table_header_obj)
        
    for table_header_obj in table_header_list:
        module_code_format = workbook.add_format()
        module_code_format.set_center_across()
        width = table_header_obj.total_size()
        worksheet.set_column(column_limits, column_limits, width, module_code_format)
        column_limits += 1

    
    
def task_table_xls_generator(modules):
    
    module_code = ''
    module_name = ''
    module_project_parent_code = ''
    task_name = ''
    issue_total_time = ''
    items_quantity = ''
    time_per_item = ''    
    
    # Create a workbook and add a worksheet.
    xlsx_file_name = 'Tabela_de_Projetos.xlsx'
    xlsx_file_path = './../' + xlsx_file_name
    workbook = xlsxwriter.Workbook(xlsx_file_path)
    worksheet = workbook.add_worksheet()
    
    #Creating header line
    header_line(workbook, worksheet)
    
    # Start from the first cell below the headers.
    row = 1
    col = 0
    
    for module_obj in modules:
        module_code = str(module_obj.code)
        module_name = module_obj.name
        module_project_parent_code = module_obj.project_parent_code
        
        for task in module_obj.tasks:
            task_name = task.name
            issue_total_time = str( format( task.total_time, '.2f' ) )
            items_quantity = str(task.items_quantity)
            time_per_item = str(format( task.calculate_time_per_item(), '.2f' ))
                     
            data_line = [module_project_parent_code, module_code, module_name, task_name, issue_total_time, items_quantity, time_per_item]
            worksheet.write_row(row, col, data_line)
            row += 1
            
            
    workbook.close()
    