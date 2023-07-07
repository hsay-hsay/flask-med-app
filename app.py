from flask import Flask, render_template, request, redirect, url_for, jsonify
import speech_recognition as sr
import main as main

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    answer = ''
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            question = recognizer.recognize_google(data, key=None)

    else:
        # pdf_text = "Sudip has difficulty climbing stairs, difficulty with airline seats, tying shoes,used to public seating, difficulty walking, high cholesterol, and high blood pressure. He has asthmaand difficulty walking two blocks or going eight to ten steps. He has sleep apnea and snoring. He is adiabetic, on medication. He has joint pain, knee pain, back pain, foot and ankle pain, leg and footswelling. He has hemorrhoids"
        pdf_text = main.extract_text_multiple(pdfs_folder=['file_directory/sample1.pdf'])
        # to be searched in the vector database of all the documents
        doc_search = main.get_docsearch(pdf_text)
        
        question = "describe the patient"
        
        # sending the question to get answers
        # pdf_text = main.extract_text_multiple(pdf_folder='user_input_folder')
        # answer = main.get_answer(query=query, doc_search=doc_search) -> call get_answer fumnction
        # answer = main.get_answer(query=question, doc_search=doc_search)
        answer = 'as'
        # answer to be sent to the ui

    return render_template('index.html', transcript=answer)





# # testing
# @app.route("/test/<string:member>/<string:question>/<string:pdf_loc>", methods=["GET", "POST"])
@app.route("/test", methods=["GET", "POST"])
# def test(member, question, pdf_loc):
def test():
    # answer = ''
    # pdf_text = ''
    # if request.method == "POST":
    #     print("FORM DATA RECEIVED")

    #     if "file" not in request.files:
    #         return redirect(request.url)
        
    #     uploaded_files = request.files.getlist('file')
    #     pdf_text = main.extract_text_multiple(pdfs_folder=uploaded_files)
    #     return redirect(request.url)
    # print(member, question, pdf_loc)
    # print([(k, v) for k, v in request.get_json().items()])
    
    # if request is in json format
    query = request.get_json()['question'] if 'question' in request.get_json() else ""
    pdf_folder = request.get_json()['pdf_loc'] if 'pdf_loc' in request.get_json() else ""
    member_name = request.get_json()['member'] if 'member' in request.get_json() else ""
    
    # if request is sent as url parameters
    # pdf_folder = pdf_loc
    # member_name = member
    # query = question
    
    if query=="" or pdf_folder=="" or member_name=="":
        result ={'error_message': "datalist is empty send positive number list "}
        return jsonify(result), 400
    
    pdf_text = main.extract_text_multiple(pdfs_folder=[pdf_folder])
    doc_search = main.get_docsearch(pdf_text)
    answer = main.get_answer(query=query, doc_search=doc_search)
    
    result = {'member':member_name,
              'question':query, 
              'pdf':pdf_folder, 
              'answer':answer}
    
    return jsonify(result), 200
    # return render_template('index2.html', member=member)
    


if __name__ == "__main__":
    app.run(host='localhost', port=80, debug=True, threaded=True)


