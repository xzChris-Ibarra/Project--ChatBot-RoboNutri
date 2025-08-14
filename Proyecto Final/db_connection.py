server = 'LAPTOP-G4TRQ1CS' # Ejemplo: 'localhost', '.\SQLEXPRESS', 'yourserver.database.windows.net' 
database = 'ChatbotDB' # El nombre de tu base de datos
username = 'sa' # Tu usuario de SQL Server
password = '22demarzo' # Tu contraseña de SQL Server 
driver = '{ODBC Driver 17 for SQL Server}' # Asegúrate de que este driver esté instalado en tu sistema 
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'