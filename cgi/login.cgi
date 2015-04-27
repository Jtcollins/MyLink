#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import session
import Cookie, os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Get Databasedir
MYLOGIN="chanthor"
DATABASE="/homes/"+MYLOGIN+"/MyLink/picture_share.db"
IMAGEPATH="/homes/"+MYLOGIN+"/MyLink/images"
VERIFY_KEY = None

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
    newuser = (user, passwd, "NULL", "NULL", "NULL")
    c.execute('SELECT * FROM users WHERE email=?', t)
    row = stored_password=c.fetchone()
    if row == None:
        c.execute('INSERT INTO users VALUES (?,?,?,?,?)', newuser)
        conn.commit()
        verify_email(user)
        return "passed"

    conn.close();
    return "failed"

##########################################################
def delete_user(user, passwd):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (user,)
    newuser = (user, passwd)
    c.execute('SELECT * FROM users WHERE email=?', t)
    return "passed"

##########################################################
# Diplay the options of admin
def display_admin_options(user, session):
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
    print_html_nav(user, session)
    print(content.format(user=user,session=session))


#################################################################

def display_user_profile(user, session):
    if check_cookie(user, session) == "passed":
        print_html_content_type()
    else:
        create_cookie(user, session)

    print_html_nav(user, session)
    return "passed"

def display_friend_profile(user, friend, session):
    print_html_content_type()
    print_html_nav(user, session)
    #TODO
    return "passed"

#################################################################
def change_user_info(user, session):
    #TODO
    return "failed"

def upload_user_pic(user, session):
    #TODO
    return "failed"

#################################################################
def friend_request(user, session):
    #TODO
    return "failed"

def request_response(user, session):
    #TODO
    return "failed"

def create_circle(user, session):
    #TODO
    return "failed"

def friend_to_circle(user, session):
    #TODO
    return "failed"

def remove_friend_from_circle(user, friend, session):
    #TODO
    return "failed"

#################################################################
def create_new_post(user, session):
    #TODO
    return "failed"

#################################################################
def create_new_session(user):
    #return session.create_session(user)
    # Store random string as session number
    # Number of characters in session string
    n = 20
    char_set = string.ascii_uppercase + string.digits
    session = ''.join(random.sample(char_set,n))
    create_cookie(user, session)
    return session

#################################################################
def check_session(user, session):
    return check_cookie(user, session)

#################################################################
def create_cookie(user, session):
    cookie = Cookie.SimpleCookie()
    cookie["session"] = session
    print "Content-type: text/plain"
    print cookie.output()
    print

def check_cookie(user, session):
    cookieString = os.environ.get("HTTP_COOKIE")
    if not cookieString:
        return "failed"
    cookie = Cookie.SimpleCookie()
    cookie.load(cookieString)
    if cookie["session"] == session:
        return "passed"
    else:
        return "failed"

#################################################################

def verify_email(useremail):
    sender = 'jtc@purdue.edu'
    receiver=useremail
    VERIFY = random.randint(10000,99999)
    body = """
    We just need to verify your email, please click this link:
        
    Or go to your settings page and input this code: %d
    """ % VERIFY
    msg = MIMEText(body)
    msg['Subject'] = 'Please Verify your email'
    msg['From'] ="NoReply@MyLink.cs.purdue.edu"
    msg['To'] =receiver

    smtpObj = smtplib.SMTP('localhost')

    smtpObj.sendmail(sender, receiver, msg.as_string())

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

    #username=form["username"].value

    # Read image
    with open(IMAGEPATH+'/user1/test.jpg', 'rb') as content_file:
       content = content_file.read()

    # Send header and image content
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
    print(html.format(user=user,session=s))

#######################################################

def upload_pic_data(form):
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
        open(IMAGEPATH+'/user1/test.jpg', 'wb').write(fileInfo.file.read())
        image_url="login.cgi?action=show_image&user={user}&session={session}".format(user=user,session=s)
        print_html_content_type()
	print ('<H2>The picture ' + fileName + ' was uploaded successfully</H2>')
        print('<image src="'+image_url+'">')
    else:
        message = 'No file was uploaded'

def print_html_content_type():
	# Required header that tells the browser how to render the HTML.
	print("Content-Type: text/html\n\n")

def print_html_nav(user, session):
    with open("nav.html") as content_file:
        content = content_file.read()

        #Also set a session number in a hidden field so the
        #cgi can check that the user has been authenticated

    print(content.format(user=user,session=session))

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
                   session=create_new_session(username)
                   display_user_profile(username, session)
                   #display_admin_options(username, session)
                else:
                   login_form()
                   print("<H3><font color=\"red\">Incorrect user/password</font></H3>")
        elif (action == "signup"):
            if "signup-username" in form and "signup-password" in form:
                #Test password
                username=form["signup-username"].value
                password=form["signup-password"].value
                if new_user(username, password)=="passed":
                   session=create_new_session(username)
                   display_user_profile(username, session)
                   #display_admin_options(username, session)
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
        elif action == "view_settings":
            display_admin_options(username, session)
        elif action == "view_profile":
            display_user_profile(username, session)
        else:
            login_form()
    else:
        login_form()

###############################################################
# Call main function.
main()
