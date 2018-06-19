# mpmatrix

* Tools for wechat mp platform matrix.
* Design for operating.
* Respect wechat eco. , pay attention to UnionID.

## arch desc

* app: backend application based on Flask
* face: frontend application based on Vue
* stone: runtime env. Docker, Nginx, Gunicore, Supervisor
* api: api proxy to other worlds, eg. wechat api proxy, wechat access token middleware


## dev conf

face dev:
```bash
cd face
npm run dev
```

app dev with face dist:
```bash
cd face
npm run build
cd mpmatrix
FLASK_APP=run.py FLASK_DEBUG=1 flask run
```

## restful api support with flask-restplus
Ref: 
[Building beautiful REST APIs using Flask, Swagger UI and Flask-RESTPlus](http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/)
