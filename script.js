
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
    