import mysql.connector

def main():

    # connect
    connect = mysql.connector.connect(user='root', password='root', database=malicious, charset='utf8')
    cursor = connect.cursor()

    name = 'Jack'
    sex = 'male'

    # insert
    cursor.execute('insert into user (name, sex) values (%s, %s)', (name, sex))

    # select
    cursor.execute('select * from user')
    row = cursor.fetchone()

    for i in row:
        print(i)

    # disconnect
    cursor.close()
    connect.close()

if __name__ == '__main__': main()
