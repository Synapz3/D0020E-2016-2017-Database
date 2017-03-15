import time
class UniversalDbObject:
    loaded = False
    table = ""
    data = {}
    def __init__(self,cursor):
        self.cursor = cursor

    def getByFilter(self,table,filter="1=1",*values):
        columns = getColumns(self.cursor,table)
        columnsSTR = ",".join(columns)
        sql = ""
        sql = "SELECT {0} FROM `{1}` WHERE {2}".format(columnsSTR,table,filter)
        self.cursor.execute(sql,tuple(values))
        result = self.cursor.fetchone()
        if len(result) == 0:
            return
        for i in range(0,len(columns)):
            self.data[columns[i]] = result[i]
        self.table = table
        self.loaded = True

    def save(self):
        if self.loaded == False:
            return
        self.data["updatedAt"] = time.strftime('%Y-%m-%d %H:%M:%S')
        columns = getColumns(self.cursor,self.table)
        columnsSTR = "`"+"`=%s,`".join(columns) + "`=%s"
        ##Get the collumns primary key
        sql = "SELECT `COLUMN_NAME`  FROM `INFORMATION_SCHEMA`.`COLUMNS`  WHERE `TABLE_SCHEMA`='mydb' AND `TABLE_NAME`='{0}' and `COLUMN_KEY`='PRI'".format(self.table);
        self.cursor.execute(sql)
        primaryKey = self.cursor.fetchone()[0]
        ##Update data
        sql = "UPDATE `{0}` SET {1} WHERE `{2}`=%s".format(self.table,columnsSTR,primaryKey)
        update = []
        for column in columns:
            update += [self.data[column]]
        update += [self.data[primaryKey]]
        self.cursor.execute(sql,tuple(update))
def getObjectsByFilter(cursor,table,filter):
    pass

def getColumns(cursor,table):
    sql = "SELECT `COLUMN_NAME`  FROM `INFORMATION_SCHEMA`.`COLUMNS`  WHERE `TABLE_SCHEMA`='mydb' AND `TABLE_NAME`='{0}'".format(table);
    cursor.execute(sql)
    result = cursor.fetchall()
    columns = []
    for r in result:
        columns += [r[0]]
    return columns
