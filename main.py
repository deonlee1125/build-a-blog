from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y2k2000'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(150))
    
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    #redirects to blog page "/blog"
    return redirect('/blog')

@app.route('/blog', methods=['GET'])
def blog():
    #retrieves and displays all blog posts (title, body) from DB
    # !!Not done!! Contains hyperlinks on titles to allow navigation..
    #..to single page ("/blog?ID=#")
    blogs = Blog.query.all()
    return render_template('blog.html', title='Build a Blog', blogs=blogs)
#You shouldn't have a separate route to handle showing individual entries,
#it should all be handled in your main `/blog` route.
#With an if statement that determines whether or not you should display the 
# list of all blogs or a single blog depending on whether or not
# the `id` query parameter was part of the GET request.
#your `/blog` handler should be able to see the `id` query parameter, and then render
# your single entry _template_.
# If there's no `id` query parameter, it should render your main blog list template.
#

@app.route('/newpost', methods=['POST', 'GET'])
def newpost(): 
    #Displays form allowing users to input blog title and body
    #POSTS blogpost (title, body) to DB
    #Verify: If title or body blank, reload w/error ms..
            #..If OK, redirect to singlepage '/blog?ID=#' and display
    #If GET, display singlepage; if POST posts blogs to DB

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
                
        if title != "" and body != "":
            blog_post = Blog(title, body)
            db.session.add(blog_post)
            db.session.commit() 
            return render_template('singlepage.html', title=title, body=body)
        else:
            flash('Title and body cannot be blank.', 'error')
            return render_template('newpost.html')
    return render_template('newpost.html', title='Add a Blog Entry')
        
if __name__ == '__main__':
    app.run()