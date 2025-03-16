import { gsap } from "gsap";

document.addEventListener('DOMContentLoaded', function() {
    gsap.fromTo('header', {y: '-100%'}, {y: '0%', duration: 1});

    gsap.fromTo('#hero', {opacity: 0}, {opacity: 1, duration: 1, delay: 0.5});

    gsap.fromTo('#about', {x: '-100%'}, {x: '0%', duration: 1, scrollTrigger: {
        trigger: '#about',
        start: 'top bottom',
        end: 'bottom bottom',
        scrub: true
    }});

    gsap.fromTo('#prediction', {x: '100%'}, {x: '0%', duration: 1, scrollTrigger: {
        trigger: '#prediction',
        start: 'top bottom',
        end: 'bottom bottom',
        scrub: true
    }});

    gsap.fromTo('#contact', {opacity: 0}, {opacity: 1, duration: 1, scrollTrigger: {
        trigger: '#contact',
        start: 'top bottom',
        end: 'bottom bottom',
        scrub: true
    }});

    (function() {
        emailjs.init("YOUR_EMAILJS_USER_ID"); // Replace with your EmailJS user ID
    })();

    const contactForm = document.querySelector('#contact form');

    contactForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const name = contactForm.querySelector('input[type="text"]').value;
        const email = contactForm.querySelector('input[type="email"]').value;
        const message = contactForm.querySelector('textarea').value;

        const templateParams = {
            from_name: name,
            from_email: email,
            message: message
        };

        emailjs.send('YOUR_EMAILJS_SERVICE_ID', 'YOUR_EMAILJS_TEMPLATE_ID', templateParams) // Replace with your EmailJS service and template IDs
            .then(function(response) {
                console.log('SUCCESS!', response.status, response.text);
                alert('Message sent successfully!');
                contactForm.reset(); // Clear the form after successful submission
            }, function(error) {
                console.error('FAILED...', error);
                alert('Failed to send message. Please try again later.');
            });
    });
});

function getHealthRecommendation() {
    const age = document.getElementById('age').value;
    const height = document.getElementById('height').value / 100; // Convert cm to meters
    const weight = document.getElementById('weight').value;
    const smokingStatus = document.getElementById('smoking').value;
    const recommendationResult = document.getElementById('recommendation-result');
    const fatigueLevel = document.getElementById('fatigue').value;
    const dietType = document.getElementById('diet').value;
    const physicalActivity = document.getElementById('physicalActivity').value;

    const bmi = weight / (height * height);
    let recommendation = "";

    if (bmi < 18.5) {
        recommendation = "You are underweight. Consider consulting a nutritionist to develop a healthy eating plan to gain weight.";
    } else if (bmi >= 18.5 && bmi < 25) {
        recommendation = "Your BMI is in the normal range. Maintain a balanced diet and regular exercise.";
    } else if (bmi >= 25 && bmi < 30) {
        recommendation = "You are overweight. Focus on a calorie-controlled diet and increase physical activity.";
    } else {
        recommendation = "You are obese. Consult a healthcare professional for personalized advice on weight management and overall health.";
    }

    if (smokingStatus === 'Smoker') {
        recommendation += " As a smoker, it's highly recommended to quit smoking to improve your overall health and reduce the risk of various diseases, including cervical cancer.";
    } else {
        recommendation += " Keep up the good work as a non-smoker! Maintaining a smoke-free lifestyle is crucial for your health.";
    }

    if (fatigueLevel === 'High') {
        recommendation += " Ensure you get adequate sleep, manage stress, and consult a healthcare professional if fatigue persists.";
    } else if (fatigueLevel === 'Medium') {
        recommendation += " Try incorporating relaxation techniques into your daily routine. If fatigue persists, consult a healthcare professional.";
    } else {
        recommendation += " Keep maintaining healthy habits."
    }

    if (dietType === 'High Sugar') {
        recommendation += " A diet high in sugar can increase inflammation in the body. Consider reducing your sugar intake and focusing on a balanced diet.";
    } else if (dietType === 'Vegetarian') {
        recommendation += " As a vegetarian, ensure you're getting all the necessary nutrients, including B12, iron, and omega-3 fatty acids.";
    } else {
        recommendation += " Maintain a balanced diet with plenty of fruits, vegetables, and whole grains."
    }

    if (physicalActivity === 'Sedentary') {
        recommendation += " A sedentary lifestyle can increase the risk of various health issues. Try to incorporate at least 30 minutes of moderate exercise into your daily routine.";
    } else if (physicalActivity === 'Moderate') {
        recommendation += " Continue to stay active and consider increasing the intensity or duration of your workouts.";
    } else {
        recommendation += " Keep maintaining regular exercise."
    }

    recommendationResult.innerHTML = `<p>Your BMI is ${bmi.toFixed(2)}.</p>
                                     <p>Recommendation:</p>
                                     <ul>${recommendation.split('. ').map(item => `<li>${item}</li>`).join('')}</ul>`;
}

window.getHealthRecommendation = getHealthRecommendation;