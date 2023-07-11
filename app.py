from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pyresparser import ResumeParser
from Resume_parser import preprocess_text, convert_to_string, calculate_similarity, java_developer, ml_engineer, salesforce_developer
import smtplib

#
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()

# give ur email and generated password for sending mails from application down below
s.login("gamesvanshu12@gmail.com", "uoafimmvicohnkgc")

SUBJECT = "Interview Call"

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/jobs')
def jobs():
    return render_template('jobs.html')


@app.route('/form')
def form():
    job_title = request.args.get('jobtitle')
    return render_template('form.html', job_title=job_title)


@app.route('/uploader', methods=["GET", "POST"])
def upload_file():
    job_title = ""
    preprocessed_resumes = []
    candidate_name = []
    candidate_email_id = []
    candidate_mobile_number = []
    if request.method == "POST":
        f = request.files['resume'];
        f.save(secure_filename(f.filename))
        job_title = request.form['jobtitle']
        # job_title = "hello"
        print(job_title)
        data = ResumeParser(f.filename).get_extracted_data()
        print(data)
        # data, job_title
        candidate_name.append(data['name'])
        candidate_email_id.append(data['email'])
        candidate_mobile_number.append(data['mobile_number'])
        print(candidate_name, candidate_email_id, candidate_mobile_number)

        job_description = ""
        job_score = 0
        if job_title == "mleng":
            job_description = ml_engineer
            job_score = 0.45
        elif job_title == "javadev":
            job_description = java_developer
            job_score = 0.55
        else:
            job_description = salesforce_developer
            job_score = 0.55

        preprocessed_job_description = preprocess_text(job_description)

        resume_text = []
        if "skills" in data:
            if data['skills'] is not None:
                resume_text += data['skills']
        if "education" in data:
            if data['education'] is not None:
                resume_text += data['education']
        if "experience" in data:
            if data['experience'] is not None:
                resume_text += data['experience']
        resume_text = convert_to_string(resume_text)
        preprocessed_resume = preprocess_text(resume_text)
        preprocessed_resumes.append(preprocessed_resume)
        similarity_scores = calculate_similarity(preprocessed_job_description, preprocessed_resumes)

        for score in similarity_scores:
            if (score >= job_score):
                print("Eligible")
                TEXT = "Hello " + candidate_name[0] + "\n\n" + "Thanks for applying to the job post." \
                                                               "Your Skills match our requirement." \
                                                               "Kindly let us know your availability for next round " \
                                                               "of interview. " \
                                                               "\n\n\n\n Thanks and regards, " \
                                                               "\n\n Talent acquisition team."
                message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
                # give the same mail here also
                s.sendmail("gamesvanshu@gmail.com", candidate_email_id[0], message)
                # s.quit()
                return render_template("form.html",
                                       prediction=str(
                                           round(score * 10,
                                                 2)) + "\n\nThanks for applying you will be emailed about your candidature")
            else:
                print("Sorry we cannot further process your candidature")
                TEXT = "Hello " + candidate_name[0] + "\n\n" + "Thanks for applying to the job post." \
                                                               "Unfortunately, we cannot further your candidature " \
                                                               "\n\n\n\n Thanks and regards, " \
                                                               "\n\n Talent acquisition team."
                message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
                # give the same mail here also
                s.sendmail("gamesvanshu@gmail.com", candidate_email_id[0], message)
                # s.quit()
                return render_template("form.html",
                                       prediction=str(
                                           round(score * 10,
                                                 2)) + "\n\nThanks for applying you will be emailed about your candidature")
    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
