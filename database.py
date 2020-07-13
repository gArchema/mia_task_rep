import psycopg2

class Database:
    def __init__(self, user, password, database, host):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(user=self.user, password=self.password, database=self.database,  host=self.host)

    def disconnect(self):
        self.connection.close()

    def table_exists(self, table_name):
        cursor = self.connection.cursor()
        executable_str = 'SELECT * from information_schema.tables ' \
                         'WHERE table_name=\'' + table_name + '\''
        cursor.execute(executable_str)
        result = bool(cursor.rowcount)
        cursor.close()
        return result

    def create_table(self, ethernet_code_t, country_name_t, third_param_t, file_name_t, third_param_type):
        with self.connection.cursor() as cursor:
            executable_str = 'CREATE TABLE ' + third_param_t + \
                             '(id SERIAL PRIMARY KEY,' \
                             + ethernet_code_t + ' character(2) UNIQUE, ' \
                             + country_name_t  + ' character varying(100), ' \
                             + third_param_t   + ' ' + third_param_type + ', ' \
                             + file_name_t     + ' character varying(100)' \
                             ')'
            cursor.execute(executable_str)
        self.connection.commit()

    def insert_row(self, table, c_1, c_2, c_3, c_4, ethernet_code, country_name, third_param, file_name):
        with self.connection.cursor() as cursor:
            executable_str = 'INSERT INTO ' + table + ' (' + c_1 + ', ' \
                             + c_2 + ', ' \
                             + c_3 + ', ' \
                             + c_4 + ') ' \
                             'VALUES ' \
                             '(' + ethernet_code + ', ' + country_name + ', ' + third_param + ', ' + file_name + ')' \
                             + 'ON CONFLICT (' + c_1 + ') DO ' \
                             'UPDATE ' \
                             'SET ' \
                             + c_2 + ' = ' + country_name + ', ' \
                             + c_3 + ' = ' + third_param + ', ' \
                             + c_4 + ' = ' + file_name + ';'
            cursor.execute(executable_str)
        self.connection.commit()

