import tornado.ioloop
import tornado.web
import os
import tornado.httpserver
import tornado.options
from tornado.options import define, options
import tormysql
from tornado import gen
import random
import string
import bcrypt
import tornado.escape
import unicodedata
import markdown
import hashlib
import tornado.locks
import json
from datetime import datetime

define("port", default=8000, help="run on the given port", type=int)


pool = tormysql.helpers.ConnectionPool(
    max_connections = 20, #max open connections
    idle_seconds = 7200, #conntion idle timeout time, 0 is not timeout
    wait_connection_timeout = 3, #wait connection timeout
    host = "127.0.0.1",
    user = "root",
    passwd = "imbatman",
    db = "blog_db",
    charset = "utf8"
)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    @tornado.gen.coroutine
    def any_author_exists(self):
        return bool(pool.execute("Select * from user_details"))
        
    def get_current_user_email(self):
        return self.get_secure_cookie("username")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        email =self.get_current_user()
        entry1 = yield pool.execute("SELECT * FROM blog_details order by blog_likes DESC")
        entry2 = yield pool.execute("SELECT * FROM blog_details where blog_owner_email = '"+email.decode('ASCII')+"'")
        entry3 = yield pool.execute("SELECT blog_r_id FROM blog_reviews where action_like = '"+email.decode('ASCII')+"'")
        entry4 = yield pool.execute("SELECT blog_r_id FROM blog_reviews where action_dislike = '"+email.decode('ASCII')+"'")
        data1=entry1.fetchall()
        data2=entry2.fetchall()
        
        if entry3.rowcount or entry4.rowcount:
            print(" 3 jare h")
            data3 = entry3.fetchall()
            data4 = entry4.fetchall()    
            data=[data1,data2,data3,data4]
            self.render("index.html", entries=data)

        else:
            data=[data1,data2]
            self.render("index.html", entries=data)



class LoginHandler(BaseHandler):
     @tornado.gen.coroutine
     def get(self):
        # # If there are no authors, redirect to the account creation page.
        if not self.any_author_exists():
            print(self.any_author_exists())
            self.redirect("/register")
        else:
            self.render("login.html", error=None)
     @tornado.gen.coroutine       
     def post(self):

        author = yield pool.execute("SELECT * FROM user_details WHERE user_email ='"+tornado.escape.xhtml_escape(self.get_argument("useremail"))+"'")
        if author.rowcount==0:
            self.render("login.html", error="user not found")
            return
        
        else:
            data = author.fetchall()
            password = tornado.escape.xhtml_escape(self.get_argument("password"))
            # password = password.encode('utf-8') 
            # pass1 = hashlib.sha1(password).digest()
            # pass2 = hashlib.sha1(pass1).hexdigest()
            # pass2 = "#" + pass2.upper()
            if password == data[0][2]:
                self.set_secure_cookie("user", str(data[0][4]))
                self.set_secure_cookie("username", data[0][1])
                self.redirect(self.get_argument("next", "/"))
            else:
                self.render("login.html", error="incorrect password")



class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.clear_cookie("username")
        self.redirect(self.get_argument("next", self.reverse_url("main")))


class RegisterHandler(LoginHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render('registration.html')
    @tornado.gen.coroutine
    def post(self):
        getemail = tornado.escape.xhtml_escape(self.get_argument("email"))
        cursor = yield pool.execute("Select * from user_details where user_email='"+getemail+"'")
        already_taken = cursor.rowcount
        cursor.close()
        if already_taken!=0:
            #raise tornado.web.HTTPError(400, "author already created")
            error_msg = u"?error=" + tornado.escape.url_escape("Login name already taken")
            self.render("registration.html")
            return
        userid=''.join(random.choice(string.ascii_letters) for i in range(10))
        username = tornado.escape.xhtml_escape(self.get_argument("username"))
        password = tornado.escape.xhtml_escape(self.get_argument("password"))
        # password = password.encode('utf-8')
        # pass1 = hashlib.sha1(password).digest()
        # pass2 = hashlib.sha1(pass1).hexdigest()
        # pass2 = "#" + pass2.upper() 
        cursor = yield pool.execute("INSERT INTO `user_details` (`user_id`, `user_name`, `user_password`, `user_email`) VALUES ('"+userid+"', '"+username+"','"+password+"', '"+getemail+"');")
        cursor.close()
        self.redirect(self.get_argument("next", self.reverse_url("main")))
 

class ComposeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        current_user_email = self.get_current_user()
        self.render("grid.html",status=None)

    @tornado.gen.coroutine
    def post(self):
        current_user_email = self.get_current_user()
        cursor = yield pool.execute("SELECT * from `user_details` where `user_email` = '"+current_user_email.decode('ASCII')+"';")
        data = cursor.fetchall()
        cursor.close()
#        blogid = data[0][4]
        time = datetime.now()
        formatted_date = time.strftime('%Y-%m-%d %H:%M:%S')
        title = tornado.escape.xhtml_escape(self.get_argument("title"))
        category = tornado.escape.xhtml_escape(self.get_argument("checkboxes"))
        # print(tornado.escape.xhtml_escape(self.get_argument("checkboxes")))
        text = tornado.escape.xhtml_escape(self.get_argument("desc"))
        blogid=''.join(random.choice(string.ascii_letters) for i in range(10))
        blogowner=data[0][1]
        blogowneremail = data[0][4]
        button = "btn btn-light btn-lg"
        cursor = yield pool.execute("INSERT INTO `blog_details` (`blog_id`, `blog_title`, `blog_desc`, `blog_owner_email`, `blog_owner_name`, `button_config`, `blog_category`, `blog_publish_time`) VALUES ('"+blogid+"', '"+title+"','"+text+"', '"+blogowneremail+"', '"+blogowner+"', '"+button+"', '"+category+"', '"+formatted_date+"');")
        cursor.close()
        self.render("grid.html", status="Publihed Successfully")

class LikeHandler(tornado.web.RequestHandler):
   
    @tornado.gen.coroutine
    def post(self):
        blogid = self.request.arguments
        reviewid = ''.join(random.choice(string.ascii_letters) for i in range(10))
        reviewdby_by_like = self.get_secure_cookie("user")
        reviewdby_by_like = reviewdby_by_like.decode('ASCII')
        for key, values in blogid.items():
            blogid = key
        cursor = yield pool.execute("INSERT INTO `blog_reviews` (`action_id`, `blog_r_id`, `action_like`) VALUES ('"+reviewid+"', '"+blogid+"','"+reviewdby_by_like+"');")
        cursor.close()
        cursor = yield pool.execute("SELECT blog_likes from blog_details WHERE blog_id= '"+blogid+"';")
        like_count = cursor.fetchall()
        print(like_count[0][0])
        cnt=0
        cursor.close()
        if like_count[0][0] is None or like_count == 0:
            cnt=1
            cursor = yield pool.execute("UPDATE blog_details SET blog_likes=1,button_config='btn btn-primary btn-lg' WHERE blog_id= '"+blogid+"';")
        else:
            cnt=like_count[0][0]+1
            cursor = yield pool.execute("UPDATE blog_details SET blog_likes=blog_likes+1 WHERE blog_id= '"+blogid+"';")
        self.xsrf_token
        cursor.close()
        self.write(json.dumps({"status": "ok", "sent": blogid, "cnt": cnt}))

        self.finish()



class UnlikeHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        blogid = self.request.arguments
        reviewdby_by_like = self.get_secure_cookie("user")
        reviewdby_by_like = reviewdby_by_like.decode('ASCII')
        for key, values in blogid.items():
            blogid = key
        # useful code goes here
        cursor = yield pool.execute("UPDATE blog_details SET blog_likes=blog_likes-1 WHERE blog_id= '"+blogid+"';")
        cursor.close()
        cursor = yield pool.execute("SELECT blog_likes from blog_details WHERE blog_id= '"+blogid+"';")
        like_count = cursor.fetchall()
        cnt=like_count[0][0]
        cursor.close()
        cursor = yield pool.execute("DELETE FROM blog_reviews WHERE blog_r_id = '"+blogid+"' and action_like = '"+reviewdby_by_like+"'")
        cursor.close()
        self.xsrf_token
        self.write(json.dumps({"status": "ok", "sent": blogid, "cnt": cnt}))

        self.finish()


class DislikeHandler(tornado.web.RequestHandler):
    # @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        blogid = self.request.arguments
        reviewid = ''.join(random.choice(string.ascii_letters) for i in range(10))
        reviewdby_by_dislike = self.get_secure_cookie("user")
        reviewdby_by_dislike = reviewdby_by_dislike.decode('ASCII')

        for key, values in blogid.items():
            blogid = key
        blogid = blogid[3:]
        cursor = yield pool.execute("INSERT INTO `blog_reviews` (`action_id`, `blog_r_id`, `action_dislike`) VALUES ('"+reviewid+"', '"+blogid+"', '"+reviewdby_by_dislike+"');")
        cursor.close()
        cur = yield pool.execute("SELECT `blog_dislikes` from `blog_details` WHERE blog_id= '"+blogid+"';")
        cur.close()
        dislike_count = cur.fetchall()
        print(dislike_count)
        print(dislike_count[0][0])
        cnt=0
        cursor.close()
        if dislike_count[0][0] is None or dislike_count == 0:
            cnt=1
            cursor = yield pool.execute("UPDATE blog_details SET blog_dislikes=1,button_config='btn btn-primary btn-lg' WHERE blog_id= '"+blogid+"';")
        else:
            cnt=cnt+dislike_count[0][0]
            cursor = yield pool.execute("UPDATE blog_details SET blog_dislikes=blog_dislikes+1 WHERE blog_id= '"+blogid+"';")
        self.xsrf_token
        cursor.close()
        self.write(json.dumps({"status": "ok", "sent": blogid, "cnt": cnt}))

        self.finish()



class Undo_DislikeHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        blogid = self.request.arguments
        reviewdby_by_dislike = self.get_secure_cookie("user")
        reviewdby_by_dislike = reviewdby_by_dislike.decode('ASCII')
        for key, values in blogid.items():
            blogid = key
        # useful code goes here
        blogid = blogid[3:]
        cursor = yield pool.execute("UPDATE blog_details SET blog_dislikes=blog_dislikes-1 WHERE blog_id= '"+blogid+"';")
        cursor.close()
        cursor = yield pool.execute("DELETE FROM blog_reviews WHERE blog_r_id = '"+blogid+"' and action_dislike = '"+reviewdby_by_dislike+"'")
        cursor.close()
        cursor = yield pool.execute("SELECT `blog_dislikes` from `blog_details` WHERE blog_id= '"+blogid+"';")
        dislike_count = cursor.fetchall()
        print(dislike_count[0][0])
        cnt=dislike_count[0][0]
        cursor.close()
        self.xsrf_token
        self.write(json.dumps({"status": "ok", "sent": blogid, "cnt": cnt}))

        self.finish()


class ViewpostHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        email =self.get_current_user()
        blogid = tornado.escape.xhtml_escape(self.get_argument("id"))
        print(blogid)
        current_user_email = self.get_current_user()
        cursor= yield pool.execute("SELECT * from blog_details where blog_id = '"+blogid+"'")
        cursor.close() 
        cur = cursor.fetchall()
        time = cur[0][10]
        cursor= yield pool.execute("SELECT * from blog_comments where comment_blogid = '"+blogid+"'")
        cursor.close()
        cursor = cursor.fetchall()
        entry2 = yield pool.execute("SELECT * FROM blog_details where blog_owner_email = '"+email.decode('ASCII')+"'")
        entry2.close()
        entry2 = entry2.fetchall()
        date = str(time.day)+"-"+str(time.month)+"-"+str(time.year)
        self.render("single.html",data=cur,date=date,comm=cursor,entry2=entry2)

   
        
class CommentHandler(BaseHandler):
    @tornado.gen.coroutine
    def post(self):
        print("m yaha hoo")
        comment_by_email = self.get_current_user()
        
        comment_by_name = yield pool.execute("SELECT user_name from user_details where user_email = '"+comment_by_email.decode('ASCII')+"'")
        comment_by_name.close()
        comment_by_name = comment_by_name.fetchall()
        comment_by_name = comment_by_name[0][0]
        time = datetime.now()
        data= self.request.arguments
        formatted_date = time.strftime('%Y-%m-%d %H:%M:%S')
        blogid = data['id'][0]
        blogid = blogid.decode('ASCII')
        title = data['title'][0]
        title=title.decode('ASCII')
        text = data['text'][0]
        text=text.decode('ASCII')
        commentid=''.join(random.choice(string.ascii_letters) for i in range(10))
        cursor = yield pool.execute("INSERT INTO `blog_comments` (`comment_id`, `comment_title`, `comment_body`, `comment_by`, `comment_blogid`, `comment_time`, `comment_by_name`) VALUES ('"+commentid+"', '"+title+"','"+text+"', '"+comment_by_email.decode('ASCII')+"', '"+blogid+"', '"+formatted_date+"', '"+comment_by_name+"');")
        cursor.close()
        self.xsrf_token
        # # self.render()
        self.write('{"msg":"success"}')
        self.finish()


class EditPostHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        blogid = self.request.arguments
        print(blogid)
        for key, values in blogid.items():
            blogid = key
        data = yield pool.execute("SELECT * from blog_details WHERE blog_id = '"+blogid+"'")
        data.close()
        data=data.fetchall()
        print(data)
        self.render("edit.html",status=None,data=data)

    @tornado.gen.coroutine
    def post(self):
        blogid = tornado.escape.xhtml_escape(self.get_argument("blogid"))
        title = tornado.escape.xhtml_escape(self.get_argument("title"))
        category=tornado.escape.xhtml_escape(self.get_argument("checkboxes"))
        time = datetime.now()
        formatted_date = time.strftime('%Y-%m-%d %H:%M:%S')
        text = tornado.escape.xhtml_escape(self.get_argument("desc"))
        blogid=''.join(random.choice(string.ascii_letters) for i in range(10))
        button = "btn btn-light btn-lg"
        
        print("""UPDATE `blog_details` SET `blog_title` = %s, `blog_desc` = %s, `blog_category` = %s, `blog_last_update` = %s WHERE `blog_id` = %s ;""", (title,text,category,formatted_date,blogid))
        cursor = yield pool.execute("UPDATE `blog_details` SET `blog_title` = %s, `blog_desc` = %s, `blog_category` = %s, `blog_last_update` = %s WHERE `blog_id` = %s ;", (title,text,category,formatted_date,blogid))
        cursor.close()
        print("Success")
        self.redirect('/')

class DeletePostHandler(MainHandler):
    @tornado.gen.coroutine
    def post(self):
        blogid = self.request.arguments
        for key,value in blogid.items():
            blogid = key
        q1 = yield pool.execute("DELETE FROM blog_details where blog_id = '"+blogid+"'")
        q2 = yield pool.execute("DELETE FROM blog_reviews WHERE blog_r_id = '"+blogid+"'")
        q3 = yield pool.execute("DELETE FROM blog_comments WHERE comment_blogid = '"+blogid+"'")
        self.write('{"status":"success","blogid":"'+blogid+'"}')

class ProfileHandler(MainHandler):
    @tornado.gen.coroutine
    def get(self):
        current_user_email = self.get_secure_cookie("user")
        current_user_email = current_user_email.decode('ASCII')
        cursor= yield pool.execute("SELECT * from user_details where user_email = '"+current_user_email+"'")
        cursor.close()
        cursor = cursor.fetchall()
        
        # self.write("<html><body><h4>Hi Everyone</h4></body></html>")
        self.render("profile.html" , entries = cursor)


class ScHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        email =self.get_current_user()
        entry1 = yield pool.execute("SELECT * FROM blog_details where blog_category = 'science' order by blog_likes DESC")
        entry2 = yield pool.execute("SELECT * FROM blog_details where blog_owner_email = '"+email.decode('ASCII')+"'")
        entry3 = yield pool.execute("SELECT blog_r_id FROM blog_reviews where action_like = '"+email.decode('ASCII')+"'")
        entry4 = yield pool.execute("SELECT blog_r_id FROM blog_reviews where action_dislike = '"+email.decode('ASCII')+"'")
        data1=entry1.fetchall()
        data2=entry2.fetchall()
        
        if entry3.rowcount or entry4.rowcount:
            print(" 3 jare h")
            data3 = entry3.fetchall()
            data4 = entry4.fetchall()    
            data=[data1,data2,data3,data4]
            self.render("index.html", entries=data)

        else:
            data=[data1,data2]
            self.render("index.html", entries=data)


class PolHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        email =self.get_current_user()
        entry1 = yield pool.execute("SELECT * FROM blog_details where blog_category = 'political' order by blog_likes DESC")
        entry2 = yield pool.execute("SELECT * FROM blog_details where blog_owner_email = '"+email.decode('ASCII')+"'")
        entry3 = yield pool.execute("SELECT blog_r_id FROM blog_reviews where action_like = '"+email.decode('ASCII')+"'")
        entry4 = yield pool.execute("SELECT blog_r_id FROM blog_reviews where action_dislike = '"+email.decode('ASCII')+"'")
        data1=entry1.fetchall()
        data2=entry2.fetchall()
        
        if entry3.rowcount or entry4.rowcount:
            print(" 3 jare h")
            data3 = entry3.fetchall()
            data4 = entry4.fetchall()    
            data=[data1,data2,data3,data4]
            self.render("index.html", entries=data)

        else:
            data=[data1,data2]
            self.render("index.html", entries=data)

class EntHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        email =self.get_current_user()
        entry1 = yield pool.execute("SELECT * FROM blog_details where blog_category = 'entertainment' order by blog_likes DESC")
        entry2 = yield pool.execute("SELECT * FROM blog_details where blog_owner_email = '"+email.decode('ASCII')+"'")
        entry3 = yield pool.execute("SELECT blog_r_id FROM blog_reviews where action_like = '"+email.decode('ASCII')+"'")
        entry4 = yield pool.execute("SELECT blog_r_id FROM blog_reviews where action_dislike = '"+email.decode('ASCII')+"'")
        data1=entry1.fetchall()
        data2=entry2.fetchall()
        
        if entry3.rowcount or entry4.rowcount:
            print(" 3 jare h")
            data3 = entry3.fetchall()
            data4 = entry4.fetchall()    
            data=[data1,data2,data3,data4]
            self.render("index.html", entries=data)

        else:
            data=[data1,data2]
            self.render("index.html", entries=data)    
class E404handler(tornado.web.RequestHandler):
    def prepare(self):
        self.set_status(404)
        self.render("404.html")

class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "login_url": "/login",
            'template_path': os.path.join(base_dir, "web"),
            'static_path': os.path.join(base_dir, "static"),
            'debug':True,
            "xsrf_cookies": False,
        }
        
        tornado.web.Application.__init__(self, [
            tornado.web.url(r"/", MainHandler, name="main"),
            tornado.web.url(r'/login', LoginHandler, name="login"),
            tornado.web.url(r'/logout', LogoutHandler, name="logout"),
            tornado.web.url(r'/register', RegisterHandler, name="register"),
            tornado.web.url(r'/profile', ProfileHandler, name="profile"),
            tornado.web.url(r'/add_blog', ComposeHandler, name="composeblog"),
            tornado.web.url(r'/likes', LikeHandler, name="likepost"),
            tornado.web.url(r'/unlike', UnlikeHandler, name="unlikepost"),
            tornado.web.url(r'/dislike', DislikeHandler, name="dislikepost"),
            tornado.web.url(r'/undo_dislike', Undo_DislikeHandler, name="undo_dislikepost"),
            tornado.web.url(r'/viewpost', ViewpostHandler, name="viewpost"),
            tornado.web.url(r'/category/entertainment', EntHandler, name="entcategory"),
            tornado.web.url(r'/category/science', ScHandler, name="sccategory"),
            tornado.web.url(r'/category/political', PolHandler, name="polcategory"),
            tornado.web.url(r'/comment', CommentHandler, name="commentpost"),
            tornado.web.url(r'/deletepost', DeletePostHandler, name="deletepost"),
            tornado.web.url(r'/editpost', EditPostHandler, name="editpost"),
            

], **settings, default_handler_class=E404handler)

def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()