### flask 权限管理系统知识点总结

+ ##### 建表:four_leaf_clover:

  多对多关联删除字段需要加`passive_deletes = True` 默认这个参数是为False 的 如

  ```python
  roles= db.relationship('Role',secondary = 'user_roles',backref = 'user_role',passive_deletes = True)
  ```

  自关联 需要加参数`remote_side` 

  ```python
  menu_gp = db.relationship ("Auth",remote_side = [id])#自关联
  ```

  一对多关联

  ```python
  menu_id = db.Column(db.Integer,db.ForeignKey('menus.id'))

  menu = db.relationship ("Menu",backref = 'menu')
  ```

  多对多关联，不同于Django 关联表需要自己创建

  ```python
  class User_Roles(db.Model):
      __tablename__ = "user_roles"
      id = db.Column (db.Integer,primary_key = True)
      user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
      role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
      
      
  auths = db.relationship ('Auth',secondary = 'role_auths',backref = 'role_auth') 
  users = db.relationship ('User',secondary = 'user_roles',backref = 'role_user') 
  ```

+ **使用Flask-Migrate 创建数据库迁移命令**:four_leaf_clover:

  ```python
  from flask_script import Manager
  from flask_migrate import MigrateCommand,Migrate
  from app import create_app,db
  app = create_app ()
  manage = Manager (app)
  migrate = Migrate (app,db)
  manage.add_command ('db',MigrateCommand)
  if __name__ == '__main__':
      # app.run (debug = True)
      manage.run ()
  ```

  `pycharm Termial` 命令行执行 `python manage.py db init` 这个时候会生成一个`migrations`文件夹,然后再执行 `python manage.py db migrate` 然后再执行 `python manage.py upgrade` 这个时候 数据库迁移就完成了

  **注意**

  如果是第一次执行数据库迁移命令时，必须在你的`db.init_app(app)` 后面将所有的数据表导入，不然是不会创建数据表的如

  ```python
     	db.init_app (app)
      from .models import Auth,Role,User,Group,Menu #这一步很重要，很重要，很重要
  ```

+ **利用`app.before_app_request` 达到Django 的中间件效果:four_leaf_clover:**

  可以在`config` 文件中 配置上白名单免验证路径，注意 flask 中静态文件的请求也会走伪中间件，在白名单中把以static开头的这些url 都加上`VALID_URL = ["/admin/login/","/static.*"]` 不然可能会出现页面加载有样式，其他代码同Django rbac 初始化 权限信息同Django rbac 只是查询的方式有一点不同

+ **在视图函数外使用数据库查询操作**

  如果使用了`create_app` 来做的话，貌似你在其他的地方就不能使用数据库查询操作了，如在form表单中你需要执行数据库查询操作，如果直接写的话会报错

  ```python
    File "D:\python 3.5\lib\site-packages\flask_sqlalchemy\__init__.py", line 912, in get_app
      'No application found. Either work inside a view function or push'
  RuntimeError: No application found. Either work inside a view function or push an application context. See http://flask-sqlalchemy.pocoo.org/contexts/.
  ```

  这时候在form表单中要重写基类的`__init__` 方法,或者在视图函数中执行查询操作，将结果赋值给表单字段

  或者不要写create_app 这个函数了，直接实例化Flask类

  ```python
  def __init__(self,*args,**kwargs):#重写FlaskForm的__init__ 方法
      super ().__init__ (*args,**kwargs)
      self.menu_id.choices = [(v.id,v.name) for v in Menu.query.all()]
      
  form = MenuForm() #视图函数中赋值
      if request.method == "GET":
          form.menu_id.choices = [(v.id,v.name) for v in Menu.query.all ()]

  from flask_sqlalchemy import SQLAlchemy # 在__init__ 文件中直接实例化Flask类
  from flask import Flask
  app = Flask(__name__)
  from config import Config
  app.config.from_object(Config)
  Config.init_app(app)
  db = SQLAlchemy(app)
  from .models import Auth,Role,User,Group,Menu
  ```

+ **Not a valid choice 提交表单报错**

  在执行表单提交的时候(**自关联权限的时候Null为空表示可以作为菜单**) 但是这时候,如果你不填值的话会报错

  wtform 有一个预验证的方法`pre_validate` 如果确定代码没有问题，这时候需要继承SelectField(一般都是这个类会报这个错) 重写 `pre_validate` 这个函数直接pass 不需要做预验证就行

  ```python
  class xxx(SelectField):#(类起名起的随意了点哈)

      def pre_validate (self,form):
          pass
  #然后让你的字段继承你写的这个类就是了
  class yyyForm(FlaskForm):
      yyy = xxx(label = 'ddd',........)
  ```

+ ###### Flask 多重路由指向同一视图

  ```python
  @admin.route("/menu/list/<int:page>/",methods = ["GET"])#有页码走这里
  @admin.route("/menu/list/",methods = ["GET"])#无页码走这里 
  ```

+ **解决sqlalchemy讨厌的warning提示** 

  ```python
  def create_app():
      app = Flask(__name__)
      app.config.from_object(Config) # 在db.init_app(app)之前先加载配置文件
      Config.init_app(app)
      db.init_app (app)
  ```

+ **每次重启项目，都会重新登录**

  ```python
  #参照狗书 如果想提高系统安全性，SECRET_KEY = os.urandom (24) 写成这样，每次都会随机生成24位随机字符串，但是每次都需要重新登录，所以还是改成一般的 SECRET_KEY = 'sssss'
  ```

+ **使用全局变量g** 

  ```python
  #自动生成表单的函数每个视图函数都需要导入，这时候可以用g来保存这个值
  from app.tempaltetags.rbac_menu import menu_html
  g.menu_dict = menu_html() # g 要放在 伪中间件中验证通过后，不然取不到值
  ```

+ **Flask-Migrate 检测不到`db.string()` 长度的变化**

  ```python
  # 修改migrations下的env.py 添加参数compare_type = True
  context.configure(connection=connection,
       target_metadata=target_metadata,
       process_revision_directives=process_revision_directives,
       compare_type = True,   #compare_type默认为False,不检测数据变化
  ```

  ​