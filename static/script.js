const image = document.getElementById('image');
const imageContainer = document.querySelector(".img-container"); // Get the page container element

let cropper = null; // Initialize Cropper to null
const btnCrop = document.getElementById('btn-crop');
const btnToggleCropper = document.getElementById('btn-toggle-cropper');
const numberInput = document.getElementById("numberInput");
const submitButton = document.getElementById("submitButton");

submitButton.addEventListener("click", handleButtonClick);

let pgno=1;
const totalpages=248;

let isClickListenerDisabled = false;
let summaries=""; // Initialize an empty dictionary


class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
        };

        this.state = false;
        this.messages = [];
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));
        sendButton.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') this.onSendButton(chatBox);
        });
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const node = chatBox.querySelector('input');
        node.addEventListener('keyup', ({ key }) => {
            if (key === 'Enter') {
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;

        if (this.state) {
            chatbox.classList.add('chatbox--active');
        } else {
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox) {
        const textField = chatbox.querySelector('input');
        const text1 = textField.value;

        if (text1 === "") {
            return;
        }

        const msg1 = { name: "user", message: text1 };
        this.messages.push(msg1);

        fetch('/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            const msg2 = { name: "Sam", message: r.answer };
            this.messages.push(msg2);
            this.updateChatText(chatbox);
            textField.value = '';
        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox);
            textField.value = '';
        });
    }

    updateChatText(chatbox) {
        let html = '';
        this.messages.slice().reverse().forEach(function(item) {
            if (item.name === "Sam") {
                html += `<div class="messages__item messages__item--visitor"><pre class="message-content">${item.message}</pre></div>`;
            } else {
                html += `<div class="messages__item messages__item--operator"><pre class="message-content">${item.message}</pre></div>`;
            }
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

function sendCurrentPageToFlask(pgno) {
    const url = `/${pgno}`;  // Replace with your Flask route
    fetch(url)
      .then(response => response.text())
      .then(data => {
        if (data.error) {
          console.error("Error fetching page content:", data.error);
          alert("Failed to load page content!");
        } else {
          //Summary = data; // Assign fetched data to Summary
          //console.log("Page:", Summary);
          summaries = data; // Store data for the current page
          console.log(summaries);
        }
      })
      .catch(error => {
        console.error("Error loading page content:", error);
        alert("Failed to load page content!");
      });
  }
  
  sendCurrentPageToFlask(pgno)
  function handleButtonClick() {
    const enteredNumber = numberInput.value;
    // Call your function to process the entered number
    processNumber(enteredNumber); 
  }
  
  // Replace this with your actual function that uses the entered number
  function processNumber(number) {
    console.log("You entered:", number);
    pgno=number;
    document.getElementById("image").src = `/static/converted_images/page${pgno}.png`;
    sendCurrentPageToFlask(pgno);
  
    // Perform your desired operations using the number variable
  }
  
  imageContainer.addEventListener("click", (event) => {
    // Check if the click is on the left or right half of the container
    if (!isClickListenerDisabled) {
      const isLeftClick = event.offsetX < imageContainer.offsetWidth / 2;
  
      if (isLeftClick & pgno > 1) {
        pgno--;
        document.getElementById("image").src = `/static/converted_images/page${pgno}.png`;
        sendCurrentPageToFlask(pgno);
        
      } else if (!isLeftClick & pgno < totalpages) {
        pgno++;
        document.getElementById("image").src = `/static/converted_images/page${pgno}.png`;
        sendCurrentPageToFlask(pgno);
      }
    }
  });
  
  
  btnToggleCropper.addEventListener('click', function() {
    if (cropper) {
      // Cropper is already initialized, destroy it
      cropper.destroy();
      cropper = null;
      btnCrop.disabled = true; // Disable crop button when cropper is off
      btnToggleCropper.textContent = 'Turn on Cropper';
      isClickListenerDisabled = false;
    } else {
      // Cropper is not initialized, create it
      cropper = new Cropper(image, {
        // Cropper options (aspectRatio, etc.)
      });
      btnCrop.disabled = false; // Enable crop button when cropper is on
      btnToggleCropper.textContent = 'Turn off Cropper';
      isClickListenerDisabled = true; // Disable click event listener
  
    }
  });
  
  btnCrop.addEventListener('click', function() {
    // Ensure Cropper is initialized before getting data
    if (!cropper) {
      console.error('Cropper not initialized. Please wait for image loading or turn on Cropper.');
      return;
    }
  
    const data = cropper.getData(); // Get cropping data
  
    // Extract coordinates
    const { x, y, width, height } = data;
    const x1 = x;
    const y1 = y;
    const x2 = x + width;
    const y2 = y + height;
    const coordinates = [x1, y1, x2, y2,pgno];
  
    // Print coordinates
    console.log(coordinates);
    console.log('Cropped image coordinates: (x, y, width, height)');
    console.log(`(${x1}, ${y1}, ${x2}, ${y2}, ${pgno})`);
  
    // Send coordinates to Flask backend for OCR processing
    getOcrText(coordinates);
  });
  
  function getOcrText(coordinates) {
    const url = '/coordinate';
  
    fetch(url, {
      method: 'POST', // Specify POST for sending data
      headers: { 'Content-Type': 'application/json' }, // Set JSON content type
      body: JSON.stringify(coordinates) // Convert coordinates to JSON string
    })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          console.error('Error fetching OCR text:', data.error);
          alert('Failed to get OCR text!');
        } else {
          const receivedText = data.answer;
          navigator.clipboard.writeText(receivedText).then(() => {
            console.log(receivedText);
            /* Resolved - text copied to clipboard successfully */
          },() => {
            console.error('Failed to copy');
            /* Rejected - text failed to copy to the clipboard */
          });
          
          console.log(receivedText);
          // Update UI or display OCR text here (e.g., using innerText)
        }
      })
      .catch(error => {
        console.error('Error fetching OCR text:', error);
        alert('Failed to get OCR text!');
      });
  }
  

const chatbox = new Chatbox();
chatbox.display();
