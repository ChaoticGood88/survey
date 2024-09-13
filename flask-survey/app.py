from surveys import satisfaction_survey

from flask import Flask, render_template, redirect, url_for, flash, request

app = Flask(__name__)

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# Set the secret key to a random value (this should be a secure and unpredictable key in production)
app.config['SECRET_KEY'] = 'mysecretkey'

# Enable debug mode
app.debug = True

# Set up Flask Debug Toolbar
toolbar = DebugToolbarExtension(app)


# List to store user responses
responses = []

@app.route('/')
def home():
    """Home page with survey title and start button."""
    return render_template('home.html', survey=satisfaction_survey)

@app.route('/questions/<int:qid>')
def questions(qid):
    """Show the current question with choices, protecting against invalid access."""
    # If the user has completed the survey, redirect to the thank-you page
    if len(responses) == len(satisfaction_survey.questions):
        flash("You've already completed the survey.")
        return redirect(url_for('thank_you'))

    # If the user tries to access a question that doesn't exist, redirect them and flash a message
    if qid < 0 or qid >= len(satisfaction_survey.questions):
        flash("Invalid question number. Redirecting to the correct question.")
        return redirect(url_for('questions', qid=len(responses)))

    # If the user tries to skip questions, redirect and flash a message
    if qid != len(responses):
        flash("You're trying to access a question out of order. Redirecting to the correct question.")
        return redirect(url_for('questions', qid=len(responses)))

    # If everything is fine, show the current question
    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question=question, qid=qid, survey=satisfaction_survey)



@app.route('/answer', methods=["POST"])
def answer():
    """Handle the submission of an answer."""
    # Get the selected answer from the form
    answer = request.form['answer']
    
    # Append the answer to the responses list
    responses.append(answer)

    # Check if all questions have been answered
    if len(responses) < len(satisfaction_survey.questions):
        # Redirect to the next question
        return redirect(url_for('questions', qid=len(responses)))
    else:
        # All questions answered, redirect to thank you page
        return redirect(url_for('thank_you'))


    
@app.route('/thank-you')
def thank_you():
    """Show a thank-you message after completing the survey."""
    return render_template('thank_you.html')
