from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import connect_db, db, User, Feedback
from forms import LoginForm, RegisterForm, DeleteForm, FeedbackForm


app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)



@app.route("/")
def homepage():
    """Homepage / Redirect to /register."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    return redirect("/register")



@app.route("/register", methods=['GET', 'POST'])
def register():
    """Form to register user. Password input hides character that the user is typing"""

    if "username" in session:
        flash("You are already logged in!")
        return redirect(f"/users/{session['username']}")
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        

        user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()
        flash("Your Account has been created!")
        session['username'] = user.username

        return redirect(f"/users/{user.username}")
    
    else:
        return render_template("users/register.html", form=form)
    



@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show a form that when submitted will login a user.
    Password inputs are hidden."""

    if "username" in session:
        flash("User is already logged in")
        return redirect(f"/users/{session['username']}")
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password"]
            return render_template("users/login.html, form=form")
        
    return render_template("users/login.html", form=form)



@app.route("/logout")
def logout():
    """Logs users off"""

    session.pop("username")
    session.pop("is_admin")
    flash("You have logged out!")
    return redirect("/login")


# This was the secret
@app.route("/users/<username>")
def show_user(username):
    """Show information about the given user.
       Shows all feedback and links to more feedback.
       Only logged in users can successfully view this page"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    if session["is_admin"] == True:
        admin = User.query.filter_by(username=username)
        all_users = User.query.all()
        all_feedback = Feedback.query.all()
        return render_template("users/admin.html", users=all_users, feedback=all_feedback, admin=admin)
    
    user = User.query.filter_by(username=username).first()
    feedback = Feedback.query.filter_by(username=username).all()
    form = DeleteForm()

    return render_template("users/show.html", user=user, feedback=feedback, form=form)



@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user and their feedback
       Redirect to main page.
       Only user who is logged in can successfully delete their account"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")



@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Displays a form for adding feedback"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        title = form.title.data
        content = form.content.data
        username = user.username

        feedback = Feedback(
            title=title,
            content=content,
            username=username
        )

        db.session.add(feedback)
        db.session.commit()

        flash("Feedback has been added!")
        return redirect(f"/users/{feedback.username}")
    
    else:
        return render_template("feedback/addfeedback.html", form=form)
    



@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Display a form to edit feedback.
       Update redirects to /users/<username>"""
    
    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        flash("Feedback has been edited!")
        return redirect(f"/users/{feedback.username}")
    
    return render_template("/feedback/editfeedback.html", form=form, feedback=feedback)



@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete Feedback"""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback Deleted")
        
    return redirect(f"/users/{feedback.username}")



@app.errorhandler(404)
def page_not_found(e):
    """404 error page"""

    return render_template("404.html", 404)