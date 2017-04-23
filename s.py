import run, test
import json
#Tornado Libraries
from tornado.web import RequestHandler, Application, asynchronous, removeslash
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import engine, Task, coroutine
import tornado.ioloop
import tornado.web
import hashlib, uuid

class MainHandler(RequestHandler):
	def get(self):
		self.write('Hello World')

class trainModel(RequestHandler):
	@coroutine
	@removeslash
	def post(self):
		pred = run.main()
		self.write(pred)

class testModel(RequestHandler):
	@coroutine
	@removeslash
	def post(self):
		pred = test.test()
		self.write(pred)


class genPredictions(RequestHandler):
	@coroutine
	@removeslash
	def post(self):
		companyName = self.get_argument('companyName')
		pred = run.main()
		data = json.dump(pred)
		
		self.write(data)

application = tornado.web.Application([
	(r'/', MainHandler),
	(r'/train', trainModel),
	(r'/test', testModel)
	],debug=True)
 
def my_callback(result, error):
 	print('result %s' % repr(result))
 	IOLoop.instance().stop()

if __name__ == "__main__":
	application = HTTPServer(application)
	application.listen(6969)
	tornado.ioloop.IOLoop.instance().start()