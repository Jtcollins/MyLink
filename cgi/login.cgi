#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import session
from datetime import datetime, date, time

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Get Databasedir
MYLOGIN="colli180"
DATABASE="/homes/"+MYLOGIN+"/MyLink/picture_share.db"
IMAGEPATH="/homes/"+MYLOGIN+"/MyLink/images"

##############################################################
# Define function to generate login HTML form.
def login_form():
    with open("login.html") as content_file:
        content = content_file.read()
    html="""
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>MyLink User Login</H2></center>

<H3>Log in:</H3>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="login.cgi">
<TR><TH>Username:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="login">
<INPUT TYPE=submit VALUE="Log In">
</FORM>

<H3>Not a user? Sign up here:</H3>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="signup.cgi">
<TR><TH>Username:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="sign" VALUE="signup">
<INPUT TYPE=submit VALUE="Sign Up">
</FORM>
</BODY>
</HTML>
"""
    print_html_content_type()
    print(content)

def display_user():
    #TODO
    print("hello")

def display_album():
    #TODO
    print("hello1")

###################################################################
# Define function to test the password.
def check_password(user, passwd):

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (user,)
    c.execute('SELECT * FROM users WHERE email=?', t)

    row = stored_password=c.fetchone()
    conn.close();

    if row != None: 
      stored_password=row[1]
      if (stored_password==passwd):
         return "passed"

    return "failed"

##########################################################
def new_user(user, passwd):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (user,)
    ver = verify_email(user)
    newuser = (user, passwd, "NULL", "NULL", "default.jpg", ver)
    c.execute('SELECT * FROM users WHERE email=?', t)
    row = stored_password=c.fetchone()
    if row == None:
        c.execute('INSERT INTO users VALUES (?,?,?,?,?,?)', newuser)
        conn.commit()
        return "passed"

    conn.close()
    return "failed"

##########################################################
def delete_user(user, passwd):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (user,)
    newuser = (user, passwd)
    c.execute('SELECT * FROM users WHERE email=?', t)
    conn.close()
    return "failed"

##########################################################
# Diplay the options of admin
def display_admin_options(user, ses):

    with open("settings.html") as content_file:
        content = content_file.read()
    html="""
        <H1> Picture Share Admin Options</H1>
        <ul>
        <li> <a href="login.cgi?action=new-album&user={user}&session={session}">Create new album</a>
        <li> <a href="login.cgi?action=upload&user={user}&session={session}">Upload Picture</a>
        <li> <a href="login.cgi?action=show_image&user={user}&session={session}">Show Image</a>
        <li> Delete album
        <li> Make album public
        <li> Change pasword
        </ul>
        """
        #Also set a session number in a hidden field so the
        #cgi can check that the user has been authenticated

    print_html_content_type()
    print_html_nav(form)
    print(content.format(user=user,session=ses))

def display_admin_options(form, statement="", color="green"):
    if (session.check_session(form) != "passed"):
        login_form()
        return

    user=form["user"].value
    ses=form["session"].value
    with open("settings.html") as content_file:
        content = content_file.read()

    print_html_content_type()
    print_html_nav(form)
    print(content.format(user=user,session=ses))
    if statement != "":
        print("<H3><font color=\color\statement</font></H3>")


#################################################################

def display_user_profile(form):
    if (session.check_session(form) != "passed"):
        login_form()
        return

    print_html_content_type()
    print_html_nav(form)

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    user=form["user"].value
    ses=form["session"].value
    with open("userprofile.html") as content_file:
        content = content_file.read()

    t = (user,)
    c.execute('SELECT * FROM users WHERE email=?', t)
    userdetails= c.fetchone()

    c.execute('SELECT * FROM posts WHERE user=? ORDER BY postDate DESC', t)
    posts = stored_posts=c.fetchall()

    print(content.format(user=user,session=ses,firstname=userdetails[2],lastname=userdetails[3],userpic=userdetails[4],verifykey=userdetails[5],currpage=user))
    
    for row in c.execute('SELECT * FROM posts WHERE user=? ORDER BY postDate DESC', t):
        display_post(row)

    with open("profilefoot.html") as content_file:
        content = content_file.read()

    print(content)

    conn.close()

    return "passed"

def display_post(row):
    if row is None:
        return
    user = row[0]
    circle = row[1]
    postDate = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f" )
    message = row[3]
    picture = row[4]

    if(picture == "Null"):
        html= """
        <div class="panel panel-warning">
            <div class="panel-heading">
                <h4 class="panel-title">{poster} on {postDate}</h4>
            </div>
            <div class="panel-body">{message}
                </div>
        </div><!-- /.blog-post -->
        """

        print(html.format(postDate=postDate.strftime("%D at %H:%M"),poster=user,message=message))
        return "passed"
    else:
        html= """
        <div class="panel panel-warning">
            <div class="panel-heading">
                <h4 class="panel-title">{poster} on {postDate}</h4>
            </div>
            <div class="panel-body">{message}<br><img src="login.cgi?action=show_postpic&addr={picture}" class="img-thumbnail" alt="Post Pic">
                </div>
        </div><!-- /.blog-post -->
        """

        print(html.format(postDate=postDate.strftime("%D at %H:%M"),poster=user,picture=picture,message=message))
        return "passed"

def display_user_profile_init(user, ses):

    print_html_content_type()
    print_html_nav_init(user, ses)

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    with open("userprofile.html") as content_file:
        content = content_file.read()

    t = (user,)
    c.execute('SELECT * FROM users WHERE email=?', t)
    userdetails= c.fetchone()

    c.execute('SELECT * FROM posts WHERE user=? ORDER BY postDate DESC', t)
    posts = stored_posts=c.fetchall()

    print(content.format(user=user,session=ses,firstname=userdetails[2],lastname=userdetails[3],userpic=userdetails[4],verifykey=userdetails[5],currpage=user))
    
    for row in c.execute('SELECT * FROM posts WHERE user=? ORDER BY postDate DESC', t):
        display_post(row)

    with open("profilefoot.html") as content_file:
        content = content_file.read()

    print(content)

    conn.close()

    return "passed"

def display_friend_profile(form):
    if (session.check_session(form) != "passed"):
        login_form()
        return

    print_html_content_type()
    print_html_nav(form)
    #TODO
    return "passed"

def display_feed(form):
    if (session.check_session(form) != "passed"):
        login_form()
        return

    print_html_content_type()
    print_html_nav(form)

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    user=form["user"].value
    ses=form["session"].value
    with open("newsfeed.html") as content_file:
        content = content_file.read()

    t = (user,)
    c.execute('SELECT * FROM users WHERE email=?', t)
    userdetails= c.fetchone()

    c.execute('SELECT * FROM posts WHERE user=? ORDER BY postDate DESC', t)
    posts = stored_posts=c.fetchall()

    print(content.format(user=user,session=ses,firstname=userdetails[2],lastname=userdetails[3],userpic=userdetails[4],verifykey=userdetails[5],currpage="feed"))
    
    for row in c.execute('SELECT * FROM posts ORDER BY postDate DESC'):
        display_post(row)

    with open("profilefoot.html") as content_file:
        content = content_file.read()

    print(content)

    conn.close()

    return "passed"

def display_requests(form):
    if (session.check_session(form) != "passed"):
        login_form()
        return

    print_html_content_type()
    print_html_nav(form)

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    user=form["user"].value
    ses=form["session"].value

    html= """
        <div class="container">

          <form METHOD=post ACTION="login.cgi" class="form-signin">

            <h3 class="form-requests-heading">Add a new friend</h3>
            <label for="inputEmail" class="sr-only">First Name</label>
            <input type="text" id="friend" NAME="friend" class="form-control" placeholder="Friend's Email Address" required autofocus>
            <INPUT TYPE=hidden NAME="action" VALUE="new-request">
            <INPUT TYPE=hidden NAME="user" VALUE="{user}">
            <INPUT TYPE=hidden NAME="session" VALUE="{session}">
            <INPUT TYPE=hidden NAME="currpage" VALUE="requests">
            <br>
            <button class="btn btn-md btn-primary btn-block" type="submit">Add Friend</button>
          </form>
          <br>
    </div>
    """

    t = (user,"request")
    c.execute('SELECT * FROM friendlist WHERE friend=? AND circle=?', t)
    friendlist= c.fetchall()

    c.execute('SELECT * FROM friendlist WHERE user=? AND circle=?', t)
    pending = c.fetchall()

    #if len(friendlist) == 0 and len(pending) == 0:
    #    print html
    #    print "  </body>"
    #    print "</html>"
    #    return "passed"

    html += """
        <h3 class="form-requests-heading">Friend Requests</h3>
        <div class="row">  
          <div class="col-md-6">
                  <table class="table table-striped">
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Add to circle</th>
                        <th>Delete</th>
                      </tr>
                    </thead>
                    <tbody>

    """

    for friend in friendlist:
        html += """
            <tr>
                <td>{firstname} {lastname}</td>
                <td>{user}</td>
                <td><a href="#">Add to circle</a></td>
                <td><a href="#">Delete</a></td>
              </tr> 
        """
        html.format(user=friend[2],firstname="Joe",lastname="bloggs")

    html += """</tbody>
                </table>
                </div>
            </div>
            <h3 class="form-requests-heading">Pending Requests</h3>
        <div class="row">  
          <div class="col-md-6">
        <table class="table table-striped">"""

    for friend in pending:
        html += """
            <tr>
                <td>{firstname} {lastname}</td>
                <td>{user}</td>
                <td><a href="#">Add to circle</a></td>
                <td><a href="#">Delete</a></td>
              </tr> 
        """
        html.format(user=friend[2],firstname="Joe",lastname="bloggs")

    html += """</tbody>
                </table>
                </div>
            </div>       
              </body>
</html>"""

    print html

    return "passed"

#################################################################
def change_name_page(form):
    if "user" in form and "session" in form and session.check_session(form) == "passed":
        user=form["user"].value
        ses=form["session"].value
        html = """
    <div class="container">

          <form METHOD=post ACTION="login.cgi" class="form-signin">
            <h1>MyLink</h1>

            <h2 class="form-changeinfo-heading">Change Your Personal Info</h2>
            <label for="inputEmail" class="sr-only">First Name</label>
            <input type="text" id="firstname" NAME="firstname" class="form-control" placeholder="New First Name" required autofocus>
            <label for="lastname" class="sr-only">Last Name</label>
            <input type="text" id="lastname" NAME="lastname" class="form-control" placeholder="New Last Name" required>
            <INPUT TYPE=hidden NAME="action" VALUE="change-name">
            <INPUT TYPE=hidden NAME="user" VALUE="{user}">
            <INPUT TYPE=hidden NAME="session" VALUE="{session}">
            <br>
            <button class="btn btn-md btn-primary btn-block" type="submit">Submit Changes</button>
          </form>
    </div>
    """

        print_html_content_type()
        print_html_nav(form)
        print(html.format(user=user,session=ses))
        print_settings_footer()
        return "passed"
    login_form()
    return "failed"

def change_name(form):
    user=form["user"].value
    ses=form["session"].value
    firstname = form["firstname"].value
    lastname = form["lastname"].value
    
    if (session.check_session(form) != "passed"):
        login_form()
        return

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    ts = (firstname,lastname,user,)
    
    c.execute('UPDATE users SET firstName = ?, lastName = ? WHERE email=?', ts)
    conn.commit()
    conn.close()
    return "Name Changed"


def change_password_page(form):
    user=form["user"].value
    ses=form["session"].value
    html = """
<div class="container">

      <form METHOD=post ACTION="login.cgi" class="form-changeinfo">
        <h1>MyLink</h1>

        <h2 class="form-changeinfo-heading">Change your password</h2>
        <label for="inputEmail" class="sr-only">Email</label>
        <input type="password" id="old-pw" NAME="old-pw" class="form-control" placeholder="Old Password" required autofocus>
        <label for="inputPassword" class="sr-only">New Password</label>
        <input type="password" id="npw" NAME="npw" class="form-control" placeholder="New Password" required>
        <label for="inputPassword" class="sr-only">New Password Again</label>
        <input type="password" id="npw-ver" NAME="npw-ver" class="form-control" placeholder="New Password Again" required>
        <INPUT TYPE=hidden NAME="action" VALUE="change-pw">
        <INPUT TYPE=hidden NAME="user" VALUE="{user}">
        <INPUT TYPE=hidden NAME="session" VALUE="{session}">
        <br>
        <button class="btn btn-md btn-primary btn-block" type="submit">Submit Changes</button>
      </form>
</div>
"""

    print_html_content_type()
    print_html_nav(form)
    print(html.format(user=user,session=ses))
    print_settings_footer()
    return "passed"

def change_password(form):
    ##user, ses, oldPW, newPW, newPWVer
    user=form["user"].value
    ses=form["session"].value
    oldPW = form["old-pw"].value
    newPW = form["npw"].value
    newPWVer = form["npw-ver"].value

    if (session.check_session(form) != "passed"):
        login_form()
        return

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (user,)
    c.execute('SELECT * FROM users WHERE email=?', t)
    ts = (newPW,user,)
    row = stored_password=c.fetchone()
    if(row[1]== oldPW and newPW == newPWVer):
        c.execute('UPDATE users SET password = ? WHERE email=?', ts)
        conn.commit()
        conn.close()
        return "Password Changed"
    else:

        conn.close()
        return "failed"

def upload_user_pic_page(form):
    if session.check_session(form) != "passed":
       login_form()
       return

    html="""
        <HTML>

        <FORM ACTION="login.cgi" METHOD="POST" enctype="multipart/form-data">
            <input type="hidden" name="user" value="{user}">
            <input type="hidden" name="session" value="{session}">
            <input type="hidden" name="action" value="change-profile-pic">
            <BR><I>Browse Picture:</I> <INPUT TYPE="FILE" NAME="file">
            <br>
            <input type="submit" value="Press"> to upload the picture!
            </form>
        </HTML>
    """

    user=form["user"].value
    s=form["session"].value
    print_html_content_type()
    print_html_nav(form)
    print(html.format(user=user,session=s))

def verify_page(form):
    print_html_content_type()
    print_html_nav(form)

    user=form["user"].value
    ses=form["session"].value
    html_unverified = """
<div class="container">

      <form METHOD=post ACTION="login.cgi" class="form-changeinfo">
        <h1>MyLink</h1>

        <h2 class="form-changeinfo-heading">Verify Account</h2>
        <label for="inputEmail" class="sr-only">Verification Code</label>
        <input type="text" id="verif" NAME="verif" class="form-control" placeholder="Verification Code" required autofocus>
        <INPUT TYPE=hidden NAME="action" VALUE="verificate">
        <INPUT TYPE=hidden NAME="user" VALUE="{user}">
        <INPUT TYPE=hidden NAME="session" VALUE="{session}">
        <br>
        <button class="btn btn-md btn-primary btn-block" type="submit">Submit Changes</button>
      </form>
</div>
"""
    html_verified = """
<div class="container">

      <form METHOD=post ACTION="login.cgi" class="form-changeinfo">
        <h1>MyLink</h1>

        <h2 class="form-changeinfo-heading">Your account has been verified!</h2>
        <INPUT TYPE=hidden NAME="action" VALUE="view_settings">
        <INPUT TYPE=hidden NAME="user" VALUE="{user}">
        <INPUT TYPE=hidden NAME="session" VALUE="{session}">
        <br>
        <button class="btn btn-md btn-primary btn-block" type="submit">Go Back</button>
      </form>
</div>
"""
    if (session.check_session(form) != "passed"):
        login_form()
        return

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (user,)
    c.execute('SELECT * FROM users WHERE email=?', t)
    row = stored_password=c.fetchone()
    if row[5] == 1:
        print(html_verified.format(user=user,session=ses))
        print_settings_footer()
        conn.close()
        return "passed"
    else:
        print(html_unverified.format(user=user,session=ses))
        print_settings_footer()
        conn.close()
        return "passed"

def verify_final(form):
    user=form["user"].value
    ses=form["session"].value
    verif = form["verif"].value

    if (session.check_session(form) != "passed"):
        login_form()
        return

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (user,)
    ts = (1,user,)
    c.execute('SELECT * FROM users WHERE email=?', t)
    row = stored_key=c.fetchone()
    if(int(verif) == row[5]):
        c.execute('UPDATE users SET verifyKey= ? WHERE email=?', ts)
        conn.commit()
        conn.close()
        return "Account Verified"

    conn.close()
    return "Verification Failed"

def check_verified(form):
    user=form["user"].value
    ses=form["session"].value
    verif = form["verif"].value

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (user,)
    c.execute('SELECT * FROM users WHERE email=?', t)

    row = stored_key=c.fetchone()
    conn.close()

    if(row[5] == 1):
        return True
    return False


#################################################################
def friend_request(form):
    user=form["user"].value
    friend=form["friend"].value
    ses=form["session"].value

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (user,"request",friend,)
    c.execute('INSERT INTO friendlist VALUES (?,?,?)', t)

    conn.commit()
    conn.close()

    return "success"

def request_response(form):
    #TODO
    return "failed"

def create_circle(form):
    #TODO
    return "failed"

def friend_to_circle(form):
    #TODO
    return "failed"

def remove_friend_from_circle(form):
    #TODO
    return "failed"

#################################################################
def create_new_post(form):
    user=form["user"].value
    cir=form["circle"].value
    mess=form["newpost"].value
    fileInfo = form['file']
    postDate= datetime.now()

    if (session.check_session(form) != "passed"):
        login_form()
        return

    if (if mess == "" and fileInfo == ""):
        return

    postconn = sqlite3.connect(DATABASE)
    postc = postconn.cursor()

    picid = upload_post_pic(form)

    t = (user,cir,postDate,mess,picid,)
    postc.execute('INSERT INTO posts VALUES (?,?,?,?,?)', t)
    postconn.commit()
    postconn.close()
    return "post successful"

#################################################################
def create_new_session(user):
    return session.create_session(user)

def logout(form):
    user=form["user"].value
    ses=form["session"].value

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    ts = (user,ses,)
    
    c.execute('DELETE FROM sessions WHERE user=? AND session=?', ts)
    conn.commit()
    conn.close()
    return "logout success"

#################################################################
def create_cookie(user, ses):
    #TODO
    return "failed"

def check_cookie(user, ses):
    #TODO
    return "failed"

#################################################################

def verify_email(useremail):
    sender = 'jtc@purdue.edu'
    receiver=useremail
    VERIFY = random.randint(10000,99999)
    body = """
    We just need to verify your email, please go to your settings page and input this code: %d
    """ % VERIFY
    msg = MIMEText(body)
    msg['Subject'] = 'Please Verify your email'
    msg['From'] ="NoReply@MyLink.cs.purdue.edu"
    msg['To'] =receiver

    smtpObj = smtplib.SMTP('localhost')

    smtpObj.sendmail(sender, receiver, msg.as_string())
    return VERIFY

##############################################################
def new_album(form):
    #Check session
    if session.check_session(form) != "passed":
       return

    html="""
        <H1> New Album</H1>
        """
    print_html_content_type()
    print(html);

##############################################################
def show_image(form):
    #Check session
    if session.check_session(form) != "passed":
       login_form()
       return

    # Your code should get the user album and picture and verify that the image belongs to this
    # user and this album before loading it

    username=form["username"].value

    # Read image
    picconn = sqlite3.connect(DATABASE)
    picc = postconn.cursor()

    with open(IMAGEPATH+'/user1/test.jpg', 'rb') as content_file:
       content = content_file.read()

    # Send header and image content
    hdr = "Content-Type: image/jpeg\nContent-Length: %d\n\n" % len(content)
    print hdr+content


def show_profilepic(form):

    # Your code should get the user album and picture and verify that the image belongs to this
    # user and this album before loading it

    user=form["user"].value

    # Read image
    picconn = sqlite3.connect(DATABASE)
    picc = picconn.cursor()

    t = (user,)
    picc.execute('SELECT * FROM users WHERE email=?',t)
    ipath = picc.fetchone()[4]
    with open(IMAGEPATH+'/profiles/'+ipath, 'rb') as content_file:
       content = content_file.read()

    hdr = "Content-Type: image/jpeg\nContent-Length: %d\n\n" % len(content)
    print hdr+content

def show_postpic(form):
    # Your code should get the user album and picture and verify that the image belongs to this
    # user and this album before loading it
    picaddr = form["addr"].value

    with open(IMAGEPATH+'/posts/'+picaddr, 'rb') as content_file:
       content = content_file.read()

    hdr = "Content-Type: image/jpeg\nContent-Length: %d\n\n" % len(content)
    print hdr+content

###############################################################################

def upload(form):
    if session.check_session(form) != "passed":
       login_form()
       return

    html="""
        <HTML>

        <FORM ACTION="login.cgi" METHOD="POST" enctype="multipart/form-data">
            <input type="hidden" name="user" value="{user}">
            <input type="hidden" name="session" value="{session}">
            <input type="hidden" name="action" value="upload-pic-data">
            <BR><I>Browse Picture:</I> <INPUT TYPE="FILE" NAME="file">
            <br>
            <input type="submit" value="Press"> to upload the picture!
            </form>
        </HTML>
    """

    user=form["user"].value
    s=form["session"].value
    print_html_content_type()
    print_html_nav(form)
    print(html.format(user=user,session=s))

#######################################################

def upload_pic_data(form):
    #Check session is correct
    if (check_session(form) != "passed"):
        login_form()
        return

    #Get file info
    fileInfo = form['file']

    #Get user
    user=form["user"].value
    s=form["session"].value

    # Check if the file was uploaded
    if fileInfo.filename:
        # Remove directory path to extract name only
        fileName = os.path.basename(fileInfo.filename)
        open(IMAGEPATH+'/user1/test.jpg', 'wb').write(fileInfo.file.read())
        image_url="login.cgi?action=show_image&user={user}&session={session}".format(user=user,session=s)
        print_html_content_type()
        print ('<H2>The picture ' + fileName + ' was uploaded successfully</H2>')
        print('<image src="'+image_url+'">')
    else:
        message = 'No file was uploaded'

def upload_post_pic(form):
    #Check session is correct
    if (session.check_session(form) != "passed"):
        login_form()
        return

    #Get file info
    fileInfo = form['file']

    #Get user
    user=form["user"].value
    s=form["session"].value

    # Check if the file was uploaded
    if fileInfo.filename:
        # Remove directory path to extract name only
        fileName = os.path.basename(fileInfo.filename)

        n = 20
        char_set = string.ascii_uppercase + string.digits
        filen = ''.join(random.sample(char_set,n))
        filen += '.jpg'

        open(IMAGEPATH+'/posts/'+filen, 'wb').write(fileInfo.file.read())

        return filen    
    else:
        message = 'No file was uploaded'
        return "Null"


def new_profile_pic(form):
    #Check session is correct
    if (session.check_session(form) != "passed"):
        login_form()
        return

    #Get file info
    fileInfo = form['file']

    #Get user
    user=form["user"].value
    s=form["session"].value

    # Check if the file was uploaded
    if fileInfo.filename:
        # Remove directory path to extract name only
        fileName = os.path.basename(fileInfo.filename)
        picconn = sqlite3.connect(DATABASE)
        picc = picconn.cursor()

        n = 20
        char_set = string.ascii_uppercase + string.digits
        filen = ''.join(random.sample(char_set,n))
        filen += '.jpg'

        open(IMAGEPATH+'/profiles/'+filen, 'wb').write(fileInfo.file.read())

        t = (filen,user,)

        picc.execute('UPDATE users set picture=? WHERE email=?', t)
        picconn.commit()
        picconn.close()

        image_url="login.cgi?action=show_profilepic&user={user}".format(user=user,session=s)
        print_html_content_type()
        print ('<H2>The picture ' + fileName + ' was uploaded successfully</H2>')
        print('<image src="'+image_url+'">')
    else:
        message = 'No file was uploaded'

def print_html_content_type():
	# Required header that tells the browser how to render the HTML.
	print("Content-Type: text/html\n\n")

def print_html_nav(form):
    if (session.check_session(form) == "passed"):
        user = form["user"].value
        ses = form["session"].value
        with open("nav.html") as content_file:
            content = content_file.read()

            #Also set a session number in a hidden field so the
            #cgi can check that the user has been authenticated

        print(content.format(user=user,session=ses))
        return "passed"
    return "failed"

def print_html_nav_init(user, ses):
    with open("nav.html") as content_file:
        content = content_file.read()

        #Also set a session number in a hidden field so the
        #cgi can check that the user has been authenticated

    print(content.format(user=user,session=ses))
    return "passed"

def print_settings_footer():
    with open("setfooter.html") as content_file:
        content = content_file.read()
    print(content)


##############################################################
# Define main function.
def main():
    form = cgi.FieldStorage()
    if "action" in form:
        action=form["action"].value
        #print("action=",action)
        if action == "login":
            if "username" in form and "password" in form:
                #Test password
                username=form["username"].value
                password=form["password"].value
                if check_password(username, password)=="passed":
                   ses=create_new_session(username)
                   display_user_profile_init(username, ses)
                   #display_admin_options(username, ses)
                else:
                   login_form()
                   print("<H3><font color=\"red\">Incorrect user/password</font></H3>")
        elif (action == "signup"):
            if "signup-username" in form and "signup-password" in form:
                #Test password
                username=form["signup-username"].value
                password=form["signup-password"].value
                if new_user(username, password)=="passed":
                   ses=create_new_session(username)
                   display_user_profile_init(username, ses)
                   #display_admin_options(username, ses)
                else:
                   login_form()
                   print("<H3><font color=\"red\">User already exists please sign in instead.</font></H3>")
        elif (action == "new-album"):
	       new_album(form)
        elif (action == "upload"):
           upload(form)
        elif (action == "show_image"):
          show_image(form)
        elif action == "upload-pic-data":
          upload_pic_data(form)
        elif action == "change-profile-pic":
          new_profile_pic(form)

          ## PAGE VIEW/NAV BAR OPTIONS
        elif action == "view_settings":
          display_admin_options(form)
        elif action == "view_profile":
          display_user_profile(form)
        elif action == "view_requests":
          display_requests(form)
        elif action == "view_news":
            display_feed(form)

          ##SETTINGS OPTIONS PAGES
        elif action == "ch-name":
            change_name_page(form)
        elif action == "ch-email":
            change_email_page(form)
        elif action == "ch-prof-pic":
            upload_user_pic_page(form)
        elif action == "verify-acc":
            verify_page(form)
        elif action == "ch-pw":
            change_password_page(form)
        elif action == "logout":
            logout(form)
            login_form()

        ## SETTINGS COMMIT PAGES
        elif action == "change-pw":
            change_password(form)
            statement = change_password(form)
            if statement != "failed":
                display_admin_options(form,statement,"green")
            else:
                display_admin_options(form,statement,"red")
        elif action == "change-name":
            statement = change_name(form)
            if statement != "failed":
                display_admin_options(form,statement,"green")
            else:
                display_admin_options(form,statement,"red")
        elif action == "verificate":
            statement = verify_final(form)
            if statement != "failed":
                display_admin_options(form,statement,"green")
            else:
                display_admin_options(form,statement,"red")

        ##Other actions
        elif action == "makepost":
            create_new_post(form)
            if(form["currpage"].value==form["user"].value):
                display_user_profile(form)
            elif(form["currpage"].value=="feed"):
                display_feed(form)
        elif action =="new-request":
            friend_request(form)
            if(form["currpage"].value==form["friend"].value):
                display_friend_profile(form)
            else:
                display_requests(form)
        elif action == "show_profilepic":
            show_profilepic(form)
        elif action == "show_postpic":
            show_postpic(form)
        else:
            login_form()
    else:
        login_form()

###############################################################
# Call main function.
main()
