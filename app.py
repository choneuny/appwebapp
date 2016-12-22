from flask import Flask
from flask import render_template
from flask import request
import sys
app = Flask(__name__, static_url_path='')

reload(sys)
sys.setdefaultencoding('utf-8')


from flask import redirect, url_for
import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', passwd='donnhh16', db='myblog', charset='utf8')


@app.route("/")
def hello():
	c=conn.cursor()

	c.execute('SELECT * FROM `article`')
	list = c.fetchall()

	return render_template('index.html', list=list)

@app.route("/signup")
def signup():
	return render_template('signup.html')


@app.route("/signup_ok", methods=['POST'])
def signup_ok():
	c=conn.cursor()

	c.execute("INSERT INTO `userinfo`(`username`, `userid`, `userpw`) VALUES(\'%s\', \'%s\', \'%s\')"%(request.form['user_name'], request.form['user_id'], request.form['user_pw']))
	conn.commit()

	return redirect(url_for('.hello'))


@app.route("/write")
def write():
	return render_template('write.html')


@app.route("/write_ok", methods=['POST'])
def write_ok():
	c = conn.cursor()

	c.execute("INSERT INTO `article`(`title`, `body`) VALUES(\'%s\', \'%s\')"%(request.form['title'], request.form['body']))
	conn.commit()

	return redirect(url_for("hello"))


@app.route("/login_ok")
def login_ok():
	return redirect(url_for("hello"))



@app.route("/edit/<int:id>")
def edit(id):
	c = conn.cursor()

	c.execute('SELECT * FROM `article` WHERE id=%d' % (id))
	article = c.fetchone()
	return render_template("edit.html", article=article, id=id)

# %s = string
# %d = digit

@app.route("/edit_ok/<int:id>", methods=['POST'])
def edit_ok(id):
	c = conn.cursor()

	c.execute("UPDATE `article` SET title=\'%s\', body=\'%s\' where id=%d"%(request.form['title'], request.form['body'], id))
	conn.commit()

	return redirect(url_for("hello"))
	
@app.route("/delete/<int:id>")
def delete(id):
 	c = conn.cursor()
	c.execute('delete FROM `article` WHERE id=%d' % id)
	conn.commit()

	return redirect(url_for(".hello"))

@app.route("/view/<int:id>")
def view(id):
	c = conn.cursor()
	c.execute('SELECT * FROM `article` WHERE id=%d' % (id))
	article = c.fetchone()

	return render_template("view.html", article=article, id=id)

@app.route("/view/<int:id>/comment_ok", methods=['POST'])
def comment_ok():
	c = conn.cursor()

	c.execute("INSERT INTO `comment`(`body`, `nickname`) VALUES(\'%s\', \'%s\')"%(request.form['commentbody'], request.form['nickname'], articleid))
	conn.commit()

	return redirect(url_for(".hello"))




if __name__ == "__main__":
	app.run(debug=True)