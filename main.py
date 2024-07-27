#import necessary libararis
import os
from flask import Flask, render_template_string, request
from boltiotai import openai

#set api key for openai api using OPENAI_API_KEY environment variable
api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = api_key


#This function generates objectives, syllabus, assessment methods, outcomes and recommended text books and reading of a course provided as argument using open ai
def generate_response(course):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # use model as gpt-3.5-turbo
        messages=[{
            "role": "system",
            "content": "You are a helpful assistant."
        }, {
            "role":
            "user",
            "content":
            f"Provide Objective that describe goal and purpose of course, Detailed Syllabus for school or college with 5-7 Topics, 3 Assessment Methods, 3 Outcomes, and 4 Recommended Text Books and Readings only for {course}. Explain each point in detail and underline headings.Leave a line when one point is completed.Seprate each para with lines.Don't end answer with any conclusion and generate answer with proper spaces"
        }])
    return response['choices'][0]['message']['content']


## Create a Flask web application object with name as  app and define a route for the root URL and set methods as GET and POST
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
#This function renders the html template. It includes input box for user where he can enter name of course and three javascript functions in the html template(generateDetails(), copyContent() and  containNumbers()). Custom CSS is added in style tag to beautify html page.
def hello():
    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Designer</title>
    
    <!-- CSS -->
    <style>
    
        /* Sets margin and padding as zero and box-sizing as border box for every html element*/

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Sets background of html page */
        
        body {
            /* Url of image is set according to replit environment */
            background-image:url('static/images/background.png');
            background-repeat: no-repeat;
            background-size: cover;
            height: 100vh;
            width: 100vw;
            background-attachment: fixed;
            overflow-x: hidden;
        }
        
        /* Sets CSS for container */
        
        .container {
            display: flex;
            flex-direction: column;
            margin-top: 7%;
            align-items: center;
            row-gap: 40px;
            width: 100%;

        }

        .container h2 {
            font-size: 50px;
            color: white;
            font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
            text-transform: capitalize;
            word-spacing: 2px;
            font-weight: bold;
        }

        .container h2 .main-heading {
            color: yellow;
        }

        
        /* Sets CSS for input box */
        .input {
            display: flex;
            align-items: center;
            column-gap: 5rem;
            margin-left: 11.5rem;
        }

        .input input {
            padding: 20px 15px;
            width: 40rem;
            height: 4rem;
            background: transparent;
            border: 1px solid white;
            outline: none;
            color: white;
            font-size: 24px;
            border-radius: 5px;
            margin-right:5rem;
        }
        
        /* CSS for generate button */
        
        #generate-btn {
            background-color: yellow;
            padding: 0px 5rem;
            border-radius: 5px;
            border: none;
            outline: none;
            font-size: 25px;
            height: 4rem;
            font-weight: 500;
            cursor: pointer;
        }
        
        /*Set CSS for teacher in page */

        #teacher {
            height: 45%;
            width: 20%;
            position: fixed;
            right: 4rem;
            bottom: 50px;
            display: none;
            z-index: 2;
        }
        
         /*Set CSS for output box */
         
        .output {
            display: none;
            border: 5px solid white;
            height:auto;
            width: 50rem;
            position: relative;
            margin-bottom:5rem;
        }

        .response {
            color: white;
            font-size: 20px;
            font-family: Arial, Helvetica, sans-serif;
            padding: 15px;
            text-align: justify;
            margin-top: 40px;
            white-space:pre-wrap;
        }
         /*Set CSS for copy btn */
        #copy-btn {
            cursor: pointer;
            position: absolute;
            top: 9px;
            right: 9px;
            padding: 10px;
            background-color: transparent;
            font-size: 20px;
            border: 1px solid white;
            outline: none;
            color: white;
        }
    </style>
</head>
<body>
    
    <!-- This div container include input box, generate button and output box ,teachers image and copy button. -->
    
    <div class="container">
        <div class="heading">
            <h2><span class="main-heading">Course Designer:</span> Get <span class="auto-type"></span> of any Course</h2>
        </div>
        <form id="input-form">
            <div class="input">
                <label for="course"></label>
                <input type="text" id="course" name="course">
                <button type="button" onclick="generateDetails()" id="generate-btn">Generate</button>
            </div>
        </form>
        
        <!--Url of image is set according to replit environment -->
        
        <img src="{{ url_for('static', filename='images/teacher.png') }}" alt="" id="teacher" style="display: none;">
        <div class="output" style="display: none;">
            <div class="response"></div>
            <button id="copy-btn" onclick="copyContent()">Copy</button>
        </div>
    </div>
    
    <!-- Script for Auto Typing Effect -->
    <script src="https://unpkg.com/typed.js@2.1.0/dist/typed.umd.js"></script>

    
    <!--JavaScript-->
    <script>
    
        //It sets the text to be typed in the auto-type div.
        let typed = new Typed(".auto-type", {
            strings: ["Objectives", "Sample Syllabus", "Outcomes", "Assessment Methods", "Text Books"],
            typeSpeed: 150,
            backSpeed: 150,
            loop: true
        });
        
        //This function return true if string contain numbers else return false
        function containNumbers(str) {
            return /[0-9]/.test(str);
        }
        
        //This async function generates details of course using openai api
        async function generateDetails() {
            const output = document.querySelector('.output');
            const teacher = document.querySelector('#teacher');
            const course = document.querySelector('#course').value;
            const ans = document.querySelector('.response');
            const generateBtn = document.querySelector('#generate-btn');
            //It checks if course is empty or not or it conatins numbers
            if (course.length<2 || containNumbers(course)) {
                alert('Please Write A Valid Course');
                return;
            }
            generateBtn.disabled = true;
            generateBtn.textContent = 'Loading...';
            const response = await fetch('/generate', {
                method: 'POST',
                body: new URLSearchParams(new FormData(document.querySelector('#input-form')))
            });

            const data = await response.text();
            ans.innerHTML = data;
            output.style.display = "block";
            teacher.style.display = 'block';
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate';
        }
        
        //This function copies the content of response div to clipboard
        function copyContent() {
            const ans = document.querySelector('.response').innerHTML;
            const textarea = document.createElement('textarea');
            textarea.value = ans;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            alert('Copied to clipboard');
        }
    </script>
</body>
</html>
    ''')


#This code defines a route for the URL "/generate" that only accepts POST requests.
@app.route('/generate', methods=['POST'])

# This function 'takes a POST request containing a 'course' field and returns the result of calling the 'generate_response' function with the provided course as input.
def generate():
    course = request.form['course']
    return generate_response(course)


## These code lines starts the Flask application with  the IP address  as '0.0.0.0' and port number as 8080.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
