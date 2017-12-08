# -*- coding: utf-8 -*-
from flask import session, url_for, request, render_template, redirect, flash
from .model import Model
from werkzeug.security import generate_password_hash, check_password_hash
import time
from .user_agent import browser


class Views:
    @staticmethod
    def init_views(app):
        @app.route('/')
        def index():
            UA = request.headers['User-Agent']
            if 'Android' in UA or 'iPhone' in UA:
                pass
            with Model.connect_db() as conn:
                cur = conn.cursor()
                cur.execute("""SELECT * FROM moods ORDER BY id DESC""")
                rows = cur.fetchall()
                cur.execute("""UPDATE moods SET browse_counter = browse_counter + 1""")
                conn.commit()
            return render_template('index.html', moods=rows)

        @app.route('/register', methods=['POST', 'GET'])
        def register():
            if request.method == 'GET':
                return render_template('register.html')
            name = request.form.get('name')
            password = generate_password_hash(request.form.get('password'))
            sex = request.form.get('sex') or 'male'
            info = request.form.get('info')
            try:
                with Model.connect_db() as conn:
                    conn.execute("""INSERT INTO users (name, password, sex, info) VALUES \
                                  (?, ?, ? ,?)""", (name, password, sex, info))
                    conn.commit()
            except:
                flash(u'用户名已存在，请重新输入')
                return render_template('register.html')
            flash(u'注册成功!')
            session['name'] = name
            session['my_sex'] = sex
            session['login_stat'] = True
            return redirect(url_for('user', name=session['name']))

        @app.route('/login', methods=['GET', 'POST'])
        def login():
            if session.get('login_stat'):
                return redirect(url_for('user', name=session['name']))
            elif request.method == 'GET':
                return render_template('login.html')
            name = request.form.get('name')
            password = request.form.get('password')
            with Model.connect_db() as conn:
                cur = conn.cursor()
                cur.execute("""SELECT password, sex FROM users WHERE name = (?)""", (name,))
                password_hash, sex = cur.fetchone()
            if check_password_hash(password_hash, password):
                flash(u'登录成功！')
                session['name'] = name
                session['login_stat'] = True
                session['my_sex'] = sex
                return redirect(url_for('user', name=name))
            flash(u'密码错误！请重新输入！')
            return redirect(url_for('login'))

        @app.route('/user/')
        @app.route('/user/<name>')
        def user(name=None):
            if session.get('login_stat'):
                if not name:
                    name = session['name']
                with Model.connect_db() as conn:
                    cur = conn.cursor()
                    cur.execute("""SELECT * FROM moods WHERE master = (?) ORDER BY birthday """, (name,))
                    moods = cur.fetchall()
                    cur.execute("""SELECT info FROM users WHERE name = (?)""", (session['name'],))
                    personal_info = cur.fetchone()[0]
                return render_template('user.html', moods=moods, personal_info=personal_info)
            flash(u"你还没有登录，已自动跳转到登录页面")
            return redirect(url_for('login'))

        @app.route('/logout')
        def logout():
            if session.get('login_stat') == True:
                session['login_stat'] = False
                session.pop('name', None)
                session.pop('my_sex', None)
                flash(u'注销成功！')
                return redirect(url_for('index'))
            flash(u'你还没有登录，不需要注销！')
            return redirect(url_for('index'))

        @app.route('/mood', methods=['GET', 'POST'])
        def mood():
            if request.method == 'GET':
                return render_template('mood.html')
            content = request.form['content']
            bgcolor = request.form.get('bgcolor') or 'white'
            master_sex = session.get('my_sex') or 'male'
            time_now = time.ctime()
            with Model.connect_db() as conn:
                conn.execute("""INSERT INTO moods (content, birthday, browse_counter, good_counter, bgcolor, master, master_sex) \
                            VALUES (?, ?, ?, ?, ?, ?, ?)""",
                             (content, time_now, 0, 0, bgcolor, (session.get('name') or 'uname'), master_sex))
                conn.commit()
            return redirect(url_for('index'))

        @app.route('/tourist')
        def tourist():
            with Model.connect_db() as conn:
                cur = conn.cursor()
                cur.execute("""SELECT * FROM moods ORDER BY birthday """)
                moods = cur.fetchall()
                cur.execute("""UPDATE moods SET browse_counter = browse_counter + 1""")
                conn.commit()
            return render_template('tourist.html', moods=moods)

        @app.route('/entry')
        @app.route('/entry/<id>', methods=['GET', 'POST'])
        def entry(id):
            with Model.connect_db() as conn:
                cur = conn.cursor()
                # change good_counter += 1
                cur.execute("""UPDATE moods SET good_counter = good_counter + 1 WHERE id = (?)""", (id,))
                conn.commit()

                cur.execute("""SELECT * FROM moods WHERE id = (?)""", (id,))
                mood = cur.fetchone()
                cur.execute("""SELECT MAX(id) AS max_id FROM moods""")
                max_id = cur.fetchone()[0]
                cur.execute("""SELECT * FROM comments WHERE towho = (?)""", (id,))
                comments = cur.fetchall()


            # If the id requested by GET method is bigger than the most biggest id, return 404
            # the type of id is unicode, so we need to convert it to int
            if int(id) > max_id:
                return redirect('404')
            if request.method == 'GET':
                return render_template('entry.html', id=id, mood=mood, comments=comments)
            content = request.form.get('comment')
            birthday = time.ctime()
            if not session.has_key('name'):
                name = "uname"
            else:
                name = session['name']
            with Model.connect_db() as conn:
                conn.execute("""INSERT INTO comments (content, birthday, master, towho, sex)\
                              VALUES (?, ?, ?, ?, ?)""", (content, birthday, name, id, (session.get('my_sex') or 'male')))
                conn.commit()
                cur = conn.cursor()
                cur.execute("""SELECT * FROM comments WHERE towho = (?)""", (id,))
                comments = cur.fetchall()
            return render_template('entry.html', id=id, mood=mood, comments=comments)

        @app.route('/balabala', methods=['GET', 'POST'])
        def balabala():
            if request.method == 'GET':
                return render_template('balabala.html')
            feedback = request.form.get('feedback')
            with Model.connect_db() as conn:
                cur = conn.cursor()
                cur.execute("""INSERT INTO feedback (content) VALUES (?)""", (feedback, ))
                conn.commit()
                cur.execute("""SELECT content FROM feedback ORDER BY id DESC""")
                feed_backs = cur.fetchall()
            return render_template('balabala.html', feedbacks=feed_backs)



        @app.route('/google', methods=['GET', 'POST'])
        def google():
            flash(u'此网站仅供学习之用，请勿搜索有损国家利益的信息，违者，一经发现，立即封杀！！！')
            UA = request.headers['User-Agent']
            # It is from PC or mobile device?
            if 'Android' in UA or 'iPhone' in UA:
                pass

            if request.method == 'GET':
                return render_template('google.html')
            #request.form['***'] return a unicode, but URL is utf-8 coding.
            q = request.form['q'].encode('utf-8')
            if not q:
                flash(u'请输入内容再搜索')
                return render_template('google.html')
            return get_google(q)

        def get_google(q, start=0, tbm=''):
            import urllib2
            import random
            if tbm == 'isch':
                return render_template('sorry_for_broadwidth.html')

            # Just need to convert q, start is digit and tbm is string, they two don't need to convert.
            q = urllib2.quote(q)
            url = 'https://www.google.com/search?q={0}&start={1}&tbm={2}'.format(q, start, tbm)
            req = urllib2.Request(url)
            req.add_header('User-Agent', random.choice(browser))
            html = urllib2.urlopen(req).read()

            for old, new in [
                ('images/branding/googlelogo/2x/googlelogo_color_120x44dp.png', '../static/images/googlelogo.png'),
                ('https://www.google.com.hk/webhp?', 'http://127.0.0.1:5000/google?'),
                ('https://www.google.com', 'http://127.0.0.1:5000'),
                ('https://maps.google.com/maps?', 'http://127.0.0.1:5000/search?tbm=map&')]:
                html = html.replace(old, new)
            return html

        @app.route('/search')
        def search():
            q = request.args.get('q').encode('utf-8')
            start = request.args.get('start') or 0
            tbm = request.args.get('tbm') or ''
            if tbm == 'map':
                return render_template('sorry_for_broadwidth.html')
            return get_google(q, start, tbm)

        @app.route('/justForFun')
        def just_for_fun():
            return render_template('just_for_fun.html')

        @app.errorhandler(404)
        def page_not_found(e):
            return render_template('404.html'), 404

        @app.errorhandler(500)
        def server_error(e):
            return "你请求的页面不存在"
