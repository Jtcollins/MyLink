#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import session

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
    newuser = (user, passwd, "NULL", "NULL", "NULL", ver)
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

def display_admin_options(form):
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


#################################################################

def display_user_profile(form):
    if (session.check_session(form) != "passed"):
        login_form()
        return

    print_html_content_type()
    print_html_nav(form)
    return "passed"

def display_user_profile(user, ses):

    print_html_content_type()
    print_html_nav_init(user, ses)
    return "passed"

def display_friend_profile(form):
    if (session.check_session(form) != "passed"):
        login_form()
        return

    print_html_content_type()
    print_html_nav(form)
    #TODO
    return "passed"

#################################################################
def change_name_page(form):
    if "user" in form and "session" in form and session.check_session(form) == "passed":
        user=form["user"].value
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
            <button class="btn btn-lg btn-primary btn-block" type="submit">Submit Changes</button>
          </form>
    </div>
    """
        print_html_content_type()
        print_html_nav(form)
        print(html)
        print_settings_footer()
        return "passed"
    return "failed"

def change_name(user, firstname, lastname):
    #TODO
    return "failed"

def change_email_page(form):
    html = """
<div class="container">

      <form METHOD=post ACTION="login.cgi" class="form-signin">
        <h1>MyLink</h1>

        <h2 class="form-changeinfo-heading">Change Your Email/Username</h2>
        <label for="inputEmail" class="sr-only">Email</label>
        <input type="text" id="username" NAME="username" class="form-control" placeholder="New Email" required autofocus>
        <INPUT TYPE=hidden NAME="action" VALUE="change-email">
        <button class="btn btn-lg btn-primary btn-block" type="submit">Submit Changes</button>
      </form>
</div>
"""
    print_html_content_type()
    print_html_nav(form)
    print(html)
    print_settings_footer()
    return "passed"

def change_email(user, email):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    conn.close()
    return "failed"


def change_password_page(form):
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
        <button class="btn btn-lg btn-primary btn-block" type="submit">Submit Changes</button>
      </form>
</div>
"""
    print_html_content_type()
    print_html_nav(form)
    print(html)
    print_settings_footer()
    return "passed"

def change_password(form):
    ##user, ses, oldPW, newPW, newPWVer
    if (session.check_session(form) != "passed"):
        login_form()
        return

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (user,)
    c.execute('SELECT * FROM users WHERE email=?', t)
    row = stored_password=c.fetchone()
    if(row[1]== oldPW and newPW == newPWVer and check_session(form) == "passed"):
        c.execute('UPDATE users SET password = newPW WHERE email=?', t)

        conn.close()
        return "passed"
    else:

        conn.close()
        return "failed"

def upload_user_pic_page(form):
    print_html_content_type()
    print_html_nav(form)
    #TODO
    return "failed"

def verify_page(form):
    print_html_content_type()
    print_html_nav(form)
    
    return "failed"

#################################################################
def friend_request(form):
    #TODO
    return "failed"

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
    #TODO
    return "failed"

#################################################################
def create_new_session(user):
    return session.create_session(user)

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

def print_html_nav(form):
    if (session.check_session(form) != "passed"):
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
                   display_user_profile(username, ses)
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
                   ses=create_new_ses(username)
                   display_user_profile(username, ses)
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

          ## PAGE VIEW/NAV BAR OPTIONS
        elif action == "view_settings":
          display_admin_options(form)
        elif action == "view_profile":
          display_user_profile(form)

          ##SETTINGS OPTIONS
        elif action == "ch-name":
            change_name_page(form)
        elif action == "ch-email":
            change_email_page(form)
        elif action == "ch-prof-pic":
            #TODO
            login_form()
        elif action == "verify-acc":
            verify_page(form)
        elif action == "ch-pw":
            change_password_page(form)
        elif action == "logout":
            #TODO
            login_form()
        else:
            login_form()
    else:
        login_form()

###############################################################
# Call main function.
main()
