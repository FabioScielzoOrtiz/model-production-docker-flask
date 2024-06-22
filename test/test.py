def file_type(file_path):
    return file_path.split('/')[-1].split('.')[-1].lower()

print(file_type(r"C:\Users\fscielzo\Documents\Videos-Projects\model into production\model-production-docker-flask\data\madrid_houses.csv") in ['csv'])

print('end')

    
