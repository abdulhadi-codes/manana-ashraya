const API_URL = 'https://manana-ashraya.onrender.com';

// ─── ENQUIRY FORM ───────────────────────────────────────
async function submitLead() {
    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const email = document.getElementById('email').value.trim();
    const budget = document.getElementById('budget').value;
    const bhk = document.getElementById('bhk').value;
    const message = document.getElementById('message').value.trim();
    const formMsg = document.getElementById('form-msg');

    if (!name || !phone) {
        formMsg.style.color = 'red';
        formMsg.textContent = 'Name and Phone are required.';
        return;
    }

    try {
        const response = await fetch(`${API_URL}/submit-lead`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, phone, email, budget, bhk, message })
        });

        const data = await response.json();

        if (data.status === 'success') {
            formMsg.style.color = 'green';
            formMsg.textContent = '✅ Thank you! We will contact you shortly.';
            document.getElementById('name').value = '';
            document.getElementById('phone').value = '';
            document.getElementById('email').value = '';
            document.getElementById('budget').value = '';
            document.getElementById('bhk').value = '';
            document.getElementById('message').value = '';
        }
    } catch (error) {
        formMsg.style.color = 'red';
        formMsg.textContent = '❌ Something went wrong. Please try again.';
    }
}

// ─── CHATBOT ─────────────────────────────────────────────
function toggleChat() {
    const box = document.getElementById('chatbot');
    box.classList.toggle('open');
}

function handleKey(event) {
    if (event.key === 'Enter') sendMessage();
}

const botResponses = {
    'price':    'Our units start at ₹4,990/sqft. 2BHK from ₹45L, 3BHK from ₹65L, 4BHK from ₹95L+.',
    'location': 'We are located in Attibele, on the Hosur Road corridor — close to STRR and Metro Yellow Line.',
    'bhk':      'We offer 2 BHK, 3 BHK, and 4 BHK units ranging from 950 to 2000+ sqft.',
    'amenities':'We have a swimming pool, gymnasium, clubhouse, landscaped gardens, 24/7 security and more.',
    'contact':  'Call us at +91 99999 99999 or fill the enquiry form on this page.',
    'rera':     'Our RERA registration is in process. Details will be updated shortly.',
    'possession': 'Expected possession is in 2027. Contact us for exact timelines.',
    'loan':     'We have tie-ups with leading banks for home loans. Our team will assist you.',
};

function getBotReply(input) {
    const lower = input.toLowerCase();
    for (const keyword in botResponses) {
        if (lower.includes(keyword)) {
            return botResponses[keyword];
        }
    }
    return "Thanks for your question! Please call us at +91 99999 99999 or fill the enquiry form and our team will get back to you.";
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    const messages = document.getElementById('chat-messages');
    const userText = input.value.trim();

    if (!userText) return;

    // User message
    const userDiv = document.createElement('div');
    userDiv.className = 'user-msg';
    userDiv.textContent = userText;
    messages.appendChild(userDiv);

    // Bot reply
    setTimeout(() => {
        const botDiv = document.createElement('div');
        botDiv.className = 'bot-msg';
        botDiv.textContent = getBotReply(userText);
        messages.appendChild(botDiv);
        messages.scrollTop = messages.scrollHeight;
    }, 500);

    input.value = '';
    messages.scrollTop = messages.scrollHeight;
}
