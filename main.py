from flask import Flask, render_template, request, redirect, url_for, session, make_response
import pymysql
import os, glob
import datetime, flask_login

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.permanent_session_lifetime = datetime.timedelta(hours=2)

@app.route('/', methods=['GET', 'POST'])
def home():
    work = {}
    work['WorkName'] = ['aaa', 'test', 'bbb']
    work['Writer']   = ['hoge', 'tel', 'mev']
    work['pos']      = ['70', '80', '90']
    work['office']   = ['765AS', 'SD', 'milion']
    work['Name']     = ['AmamiHaruka','ShimamuraUzuki','KasugaMirai']
    work['Number']   = ['1','1','1']
    if not session.get('Name') == None:
        return render_template('homepage.html',work=work)
    else:
        return render_template('homepage.html',work=work)

@app.route('/Login', methods=['GET', 'POST'])
def LoginForm():
    if not session.get('Name') ==  None:
        return redirect(url_for('Compleat', username = session.get('Name')))
    return render_template('login.html')

@app.route('/accountcheck', methods=['POST'])
def Checkaccount():
    if request.method == 'POST':
        Username = request.form['username']
        Pass     = request.form['pass']
        if Username == 'hoge': # Now only 'hoge' can login. After a while pymysql is used.
            session.permanent = True
            session.modified = True
            app.user = flask_login.current_user
            session['Name'] = Username
            return redirect(url_for('Compleat', username = Username))
        else:
            return redirect(url_for('LoginForm'))
    else:
        return redirect(url_for('LoginForm'))

@app.route('/mypage/<username>', methods=['GET', 'POST'])
def Compleat(username):
    if not session.get('Name') ==  username:
        return render_template('home.html', name=username)
    else:
        return render_template('home.html', name=username, select='true')

@app.route('/v', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        return render_template('writePage.html')
    elif not session.get('Name') == None:
        return render_template('writePage.html')
    else:
        return redirect(url_for('LoginForm'))

@app.route('/workURL', methods=['GET', 'POST'])
def inURLworks():
    return render_template('works2URL.html')

@app.route('/URLcheck', methods=['GET','POST'])
def URL2Check():
    if 'ss456p.com' in request.form['Link']:
        return render_template('works2URL.html', CheckRes=True, Links=request.form['Link'], title=request.form['title'])
    else:
        return render_template('works2URL.html')

@app.route('/Write', methods=['GET', 'POST'])
def Storage():
    fileName = request.form['title']
    with open('works/'+fileName+'.txt','w+',encoding="utf-8") as f:
        f.write(request.form['MainIdea'])
        # return redirect(url_for('Compleat', username = session.get('Name')))
        return redirect(url_for('FacePic'))

@app.route('/selecttop')
def FacePic():
    NameList = sorted(glob.glob('./FolderNames/Names*'))
    FileList = sorted(glob.glob('./FolderNames/File*'))
    Offices = ['765AS','SD','milion']
    OfficeNames = {'765AS':'アイドルマスター','milion':'ミリオンライブ', 'SD':'シンデレラガールズ'}
    filnums = {}
    TagNames = []
    FolNames = []
    idolcount = {}
    LastNum   = 0
    idolbecon = {}

    for num in range(len(NameList)):
        with open(NameList[num] ,'r', encoding="utf-8") as t:
            TagName = t.readlines()
        with open(FileList[num], 'r', encoding="utf-8") as f:
            FolName = f.readlines()
        imgpass = './static/images/' + Offices[num] +'/'
        idolbecon[Offices[num]] = LastNum
        for count in range(len(TagName)):
            TagNames.append(TagName[count].replace("\n",""))
            FolNames.append(FolName[count].replace("\n",""))
            filnums[FolNames[-1]] = os.listdir(imgpass+FolNames[-1])
            LastNum += 1
        idolcount[Offices[num]] = LastNum
    print(idolcount)
    return render_template('figselect.html',FolNames=FolNames, TagNames=TagNames, filnums=filnums, Offices=Offices, OfficeNames=OfficeNames, idolcount=idolcount, idolbecon=idolbecon)

@app.route('/promotion', methods=['POST'])
def promotion():
    if request.method == 'POST':
        return render_template('promotion.html')

@app.route('/logout')
def logout():
    session.pop('Name',None)
    return redirect(url_for('LoginForm'))

@app.route('/createaccount', methods=['GET', 'POST'])
def creacc():
    return render_template('createaccount.html')

@app.route('/createcheck', methods=['POST', 'GET'])
def checreate():
    if request.method == 'POST':
        if not request.form['accName'] == 'hoge':
            return 'OK'
        return render_template('createaccount.html', error='That account already exists. Please try another account name etc.')
    return render_template('createaccount.html', error='Please come in the correct order')


@app.route('/read/<titName>')
def project(titName):
    fileName = titName
    with open('works/'+fileName+'.txt','r',encoding="utf-8") as f:
        Main = f.readlines()
    return render_template('projection.html', Main = Main, Title = fileName)

@app.route('/rewrite/<titNum>')
def rewriteproject(titNum):
    fileName = titNum
    with open('works/'+fileName+'.txt','r',encoding="utf-8") as f:
        Main = f.readlines()
    return render_template('rewritepage.html', Main = Main, Title=fileName)

@app.route('/topbar')
def topbar():
    if not session.get('Name') == None:
        print('hoge')
        return render_template('topbar.html',check='hoge')
    else:
        print('hogehoge')
        return render_template('topbar.html')

@app.route("/robots.txt")
def display_robots_txt():
    return app.send_static_file("robots.txt")

if __name__ == "__main__":
    app.run(debug=True)
