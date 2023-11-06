# SentiVue-Flask-App
A Sentiment Analysis Webapp made using Flask, html, Bootstrap 5 and JavaScript as a part of my 3rd Year B.Tech Software Engineering Project. (Under progress)

# Tech Stack
Flask, HTML5, CSS3, Bootstrap 4.6.2, JavaScript
For Sentiment Analysis: TextBlob, pandas
Database: Flask-SQLAlchemy

# Features so far:
1. User account handling: Registration and login.
2. CSV file preview: Upon uploading the desired csv file, it generates a preview for the user. [Dependencies: i.CSV data must have fields 'Product' and 'Review']
3. Sentiment Analysis Output: Uploaded CSV data is converted to a pandas dataframe. The 'Review' field is analyzed by TextBlob, fields 'Polarity', 'Subjectivity', and 'Sentiment' are added. Chart.js generates a polarity vs subjectivity scatterplot and a bar chart demonstrating the sentiment count for each product.
4. Project Creation: User may choose to finalize and save the Sentiment Analysis Output with a title and description, or return to home page to discard the output.
5. View and Delete: User can access their saved projects from their homepage. Delete functionalites aare available in homepage and project view page.

# Screenshots:

![sentivue 1](https://github.com/Ats023/SentiVue-Flask-App/assets/122550503/fd9efdad-7c9a-4050-b696-0126e64ff067)
![sentivue 2](https://github.com/Ats023/SentiVue-Flask-App/assets/122550503/32c9dc1f-76d4-4539-aba6-f3179ba3acb5)
![sentivue 3](https://github.com/Ats023/SentiVue-Flask-App/assets/122550503/ff181075-5579-4e32-a6a6-5af8a656c69d)

