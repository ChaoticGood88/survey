from surveys import satisfaction_survey
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_debugtoolbar import DebugToolbarExtension

# Define the Flask app first
app = Flask(__name__)

# Set the secret key for session management
app.config['SECRET_KEY'] = 'mysecretkey'  # Replace 'mysecretkey' with a strong, random key in production

# Enable debug mode and set up the Flask Debug Toolbar
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # Prevent toolbar from disappearing on redirects

# Set up the Debug Toolbar
toolbar = DebugToolbarExtension(app)

# Route to begin the survey and initialize the session
@app.route('/begin', methods=["POST"])
def begin():
    """Clear the session of responses and start the survey."""
    session['responses'] = []  # Initialize the session with an empty responses list
    return redirect(url_for('questions', qid=0))

@app.route('/')
def home():
    """Home page with survey title and start button."""
    return render_template('home.html', survey=satisfaction_survey)

@app.route('/questions/<int:qid>')
def questions(qid):
    """Show the current question with choices, protecting against invalid access."""
    responses = session.get('responses', [])

    # If the user has completed the survey, redirect to the thank-you page
    if len(responses) == len(satisfaction_survey.questions):
        return redirect(url_for('thank_you'))

    # If the user tries to access an invalid question id
    if qid < 0 or qid >= len(satisfaction_survey.questions):
        flash("Invalid question number. Redirecting to the correct question.")
        return redirect(url_for('questions', qid=len(responses)))

    # If the user tries to skip questions
    if qid != len(responses):
        flash("You're trying to access a question out of order. Redirecting to the correct question.")
        return redirect(url_for('questions', qid=len(responses)))

    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question=question, qid=qid, survey=satisfaction_survey)

@app.route('/answer', methods=["POST"])
def answer():
    """Handle the submission of an answer and redirect to the next question."""
    # Get the answer from the form
    answer = request.form['answer']

    # Retrieve the current responses from the session
    responses = session.get('responses', [])
    responses.append(answer)

    # Update the session with the new responses list
    session['responses'] = responses

    # If all questions are answered, redirect to the thank-you page
    if len(responses) == len(satisfaction_survey.questions):
        return redirect(url_for('thank_you'))

    # Otherwise, redirect to the next question
    return redirect(url_for('questions', qid=len(responses)))

@app.route('/thank-you')
def thank_you():
    """Show a thank-you message after completing the survey."""
    return render_template('thank_you.html')

if __name__ == "__main__":
    app.run(debug=True)
