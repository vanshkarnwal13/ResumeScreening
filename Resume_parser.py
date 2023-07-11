import nltk as nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_text(text):
    # Tokenize the text into individual words
    tokens = nltk.word_tokenize(text)

    stemmer = nltk.stem.PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    # Remove stop words and punctuation
    stopwords = nltk.corpus.stopwords.words('english')
    filtered_tokens = [token for token in stemmed_tokens if token.lower() not in stopwords and token.isalpha()]

    # Join the filtered tokens back into a single string
    preprocessed_text = ' '.join(filtered_tokens)

    return preprocessed_text


def convert_to_string(texts):
    text = ""
    for i in texts:
        text += i + " "
    return text


# Preprocess the job description
java_developer = "BS/MS degree in Computer Science, Engineering or a related subject. Proven hands-on Software " \
                 "Development experience Proven working experience in Java development Hands on experience in " \
                 "designing and developing applications using Java EE platforms Object Oriented analysis and design " \
                 "using common design patterns. Profound insight of Java and JEE internals (Classloading, " \
                 "Memory Management, Transaction management etc) Excellent knowledge of Relational Databases, " \
                 "SQL and ORM technologies (JPA2, Hibernate) Experience in the Spring Framework Experience as a Sun " \
                 "Certified Java Developer Experience in developing web applications using at least one popular web " \
                 "framework (JSF, Wicket, GWT, Spring MVC) Experience with test-driven development"

ml_engineer = "Proven experience as a Machine Learning Engineer or similar role Understanding of data structures, " \
              "data modeling and software architecture Deep knowledge of math, probability, statistics and algorithms " \
              "Ability to write robust code in Python, Java and R Familiarity with machine learning frameworks (like " \
              "Keras or PyTorch) and libraries (like scikit-learn) Excellent communication skills Ability to work in a " \
              "team Outstanding analytical and problem-solving skills BSc in Computer Science, Mathematics or similar " \
              "field; Master’s degree is a plus"

ml_engineer = "Proficiency with a deep learning framework such as TensorFlow or Keras Proficiency with Python and " \
              "basic libraries for machine learning such as scikit-learn and pandas Expertise in visualizing and " \
              "manipulating big datasets Proficiency with OpenCV Familiarity with Linux Ability to select hardware to " \
              "run an ML model with the required latency"

salesforce_developer = "Experience with Apex, Visualforce and the Lightning Component Framework. Advanced knowledge of " \
                       "Salesforce permissions, roles, reports, dashboards, etc. Experience with APIs and integrations. " \
                       "Experience working on an Agile development team (if applicable).Experience with software " \
                       "development outside of the Salesforce ecosystem. Excellent communication and collaboration " \
                       "skills. Any additional technical requirements.Desired level of education."

job_description = "Looking for a tech-savvy and passionate Software Engineering Intern with knowledge of Linux and " \
                  "strong knowledge of software systems. Course work: Should have strong Computer Science " \
                  "fundamentals.Demonstrate good knowledge of the course work, e.g. Data Structures, Algorithmic " \
                  "complexity, TCP/IP stack, Operating Systems Education -Bachelor’s/Master's Degree in Computer " \
                  "Science OR anything relevant."


def calculate_similarity(job_description, resumes):
    # Create a CountVectorizer
    vectorizer = CountVectorizer()

    # Vectorize the job description and candidate resumes
    job_description_vector = vectorizer.fit_transform([job_description])
    resume_vectors = vectorizer.transform(resumes)

    # Calculate cosine similarity between the job description vector and each resume vector
    similarities = cosine_similarity(job_description_vector, resume_vectors)

    return similarities.flatten()
