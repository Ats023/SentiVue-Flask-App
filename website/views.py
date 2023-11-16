from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .forms import ProjectForm
from .models import *
from . import db
from textblob import TextBlob
import pandas as pd
import json
import io

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def user_home():
    return render_template("user_home.html", user=current_user)

@views.route('/create-project', methods=['GET', 'POST'])
@login_required
def project_form():
    form = ProjectForm()
    return render_template('create_project.html', user=current_user, form=form, review_csv='')

@views.route('/delete-project', methods=['POST'])
def delete_project():
    project = json.loads(request.data)
    projId = project['projId']
    project = Project.query.get(projId)
    if project:
        if project.user_id==current_user.id:
            db.session.delete(project)
            db.session.commit()
    return jsonify({})

@views.route('/analyze-sentiment', methods=['GET', 'POST'])
@login_required
def analyze_sentiment():
    form = ProjectForm()
    if request.method == 'POST':
        csv_data = request.files['csv_data']
        if csv_data:
            csv_data = csv_data.read().decode('utf-8', errors='replace')
            csv_stream = io.StringIO(csv_data)
            output_df = analyze_sentiment(csv_stream)
            return render_template('display_sentiment.html', output=output_df, user=current_user, form=form, csv_data=output_df.to_csv(index=False))
    else:
        flash('POST not successful', category='error')
        return render_template('create_project.html', user=current_user)
    
@views.route('/save-sentiment', methods=['POST'])
@login_required
def save_sentiment():
    form = ProjectForm()
    title = request.form.get('title') 
    desc = request.form.get('desc')
    data = request.form.get('sentiment_data')
    if data:
        new_project = Project(title=title, desc=desc, csv_data=data, user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()
        flash('Sentiment data saved to the database!', category='success')
        url = url_for('views.project_view', project_id = new_project.id)
        return redirect(url)
    else:
        flash('Data is missing or empty. Sentiment data not saved.', category='error')

    return render_template('display_sentiment.html', user=current_user, form=form)

@views.route('/project-view/<int:project_id>')
@login_required
def project_view(project_id):
    project = Project.query.get(project_id)
    csv_data = project.csv_data
    n = len(csv_data)
    csv_data[:n-2]
    csv_stream = io.StringIO(csv_data)
    output_df = analyze_sentiment(csv_stream)
    return render_template('view_project.html', project=project, output = output_df, user=current_user)

def analyze_sentiment(csv_data):
    df = pd.read_csv(csv_data)
    polarity_scores = []
    subjectivity_scores = []
    for index, row in df.iterrows():
        review = row['Review']
        analysis = TextBlob(review)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity

        polarity_scores.append(polarity)
        subjectivity_scores.append(subjectivity)
    def scoreAnalysis(x):
        if x<0:
            return 'Negative'
        elif x>0:
            return 'Positive'
        else:
            return 'Neutral'
    df['Polarity'] = polarity_scores
    df['Subjectivity'] = subjectivity_scores
    df['Sentiment'] = df['Polarity'].apply(scoreAnalysis)
    return df

