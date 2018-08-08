class module_class:
    name = ''
    code = ''
    tasks = []
    project_parent_code = ''
    
    def __init__(self, name, code, tasks, project_parent_code):
        self.name = name
        self.code = code
        self.tasks = tasks
        self.project_parent_code = project_parent_code
    
class table_header:
    name = ''
    additional_size = 0
    
    def __init__(self, name, additional_size):
        self.name = name
        self.additional_size = additional_size
        
    def total_size(self):
        return len(self.name) + self.additional_size

class task:
    issue_code = ''
    total_time = 0
    name = ''
    items_quantity = 0
    analists = []
    
    def __init__(self, issue_object, name, items_quantity):
        self.issue_code = issue_object.code
        self.total_time = issue_object.total_time()
        self.name = name
        self.items_quantity = items_quantity
        self.analists = issue_object.analists
        
    def calculate_time_per_item(self):
        
        if self.items_quantity==0:
            time_per_item = 0
        else:
            time_per_item = self.total_time/self.items_quantity
        
        return time_per_item
        
class analist:
    name = ''
    times = []
    def __init__(self, name, times):
        self.name = name
        self.times = times
        
    def total_time(self):
        total_time = 0
        for time in self.times:
            total_time += time
            
        return total_time

class issue:
    code = 0
    analists = []
    def __init__(self, code, analists):
        self.code = code
        self.analists = analists

    def total_time(self):
        total_time = 0
        
        for analist in self.analists:
            total_time += analist.total_time()
            
        return total_time
        
class pack_to_task:
    issue = 0
    task_name = ''
    items_quantity = 0
    
    def __init__(self, issue, task_name, items_quantity):
        
        self.issue = issue
        self.task_name = task_name
        self.items_quantity = items_quantity
        
            
            
        
        
        
        
        