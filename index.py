import tornado.web
import tornado.ioloop
import json
import psycopg2
import os

class mainRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
class listRequestHandler(tornado.web.RequestHandler):
    def get(self):
        fh = open("list.txt", "r")
        fruits = fh.read().splitlines()
        fh.close()
        self.write(json.dumps(fruits))
    def post(self):
        fruit = self.get_argument("fruit")
        fh = open("list.txt", "a")
        fh.write(f"{fruit}\n")
        fh.close()
        self.write(json.dumps({"message": "Fruit added successfully."}))

class employeeRequestHandler(tornado.web.RequestHandler):
    def initialize(self, con):
        self.con = con
        self.cur = con.cursor()

    def get(self):
        self.cur.execute("select * from employee")
        rows = self.cur.fetchall()
        self.write(json.dumps(rows))

    def post(self):
        newEmp = self.get_argument("emp")
        self.cur.execute("insert into employee (name) values (%s)", (newEmp,))
        self.con.commit()
        self.write({"message":"Employee added successfully"})


    
if __name__ == "__main__":
    con = psycopg2.connect(
        host = "10.9.176.23",
        database =  "postgres",
        user = "postgres",
        password = os.environ['POSTGRES_PASSWORD']
        )

    app = tornado.web.Application([
        (r"/", mainRequestHandler),
        (r"/list", listRequestHandler),
        (r"/employee", employeeRequestHandler, {
            'con': con
        })
    ])
    
    port = 8080
    app.listen(port)
    print(f"Application is ready and listening on port {port}")
    tornado.ioloop.IOLoop.current().start()