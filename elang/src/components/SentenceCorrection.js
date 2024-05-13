import React, { useState, useEffect } from 'react';
import './styles/sentence.css'; // Ensure this CSS file is updated accordingly
import logoImg from './images/logo.png';  // Assuming logo image is stored here
import menuIcon from './images/user.png';  // Assuming menu icon is stored here

function SentenceCorrection() {
    const [word, setWord] = useState('');
    const [sentence, setSentence] = useState('');
    const [input, setInput] = useState('');
    const [feedback, setFeedback] = useState('');
    const [progress, setProgress] = useState(0);
    const [total, setTotal] = useState(5); // Total number of questions

    // Function to fetch data from the Flask API
    const fetchData = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/translations_ns/generate_sentence');
            const data = await response.json();
            setSentence(data.german_sentence.replace('_____', '_____ (fill in the blank)'));
            setWord(data.correct_word);
        } catch (error) {
            console.error('Fetch error:', error);
            setFeedback('Failed to load data. Please try again later.');
        }
    };

    // Fetch data on component mount
    useEffect(() => {
        fetchData();
    }, []);

    // Function to check the user's answer
    const checkAnswer = async () => {
        if (!input) {
            setFeedback('Please enter a word before submitting.');
            return;
        }

        try {
            const payload = {
                user_input: input,
                correct_word: word
            };
            const response = await fetch('http://127.0.0.1:5000/translations_ns/validate_answer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();
            if (response.ok) {
                setFeedback('Right Answer! Well done, keep going 😊');
                setProgress(progress + 100 / total); // Increase progress
                fetchData(); // Fetch new sentence and word
            } else {
                setFeedback('Wrong Answer! Review this later, practice makes perfect 😞');
            }
        } catch (error) {
            console.error('Submission error:', error);
            setFeedback('Failed to submit answer. Please try again later.');
        }

        setInput(''); // Reset input field
    };

    const handleNext = () => {
        fetchData(); // Fetch new data
        setFeedback(''); // Reset feedback
        setInput(''); // Reset input field
    };

    return (
        <div className="app-container">
            <header className="app-header">
                <img src={logoImg} alt="App Logo" className="logo" />
                <img src={menuIcon} alt="Menu Icon" className="menu-icon" />
            </header>
            <div className="content">
                <h1>Sentence Correction</h1>
                <div className="input-group">
                    <label>Word:</label>
                    <input type="text" value={input} onChange={(e) => setInput(e.target.value)} />
                </div>
                <div className="input-group">
                    <label>Sentence:</label>
                    <p>{sentence}</p>
                </div>
                {feedback && <p className="feedback">{feedback}</p>}
                <button onClick={checkAnswer} className="btn-submit">Submit</button>
                <button onClick={handleNext} className="btn-next">Next</button>
                <div className="progress-bar">
                    <div className="progress" style={{ width: `${progress}%` }}></div>
                </div>
            </div>
        </div>
    );
}

export default SentenceCorrection;
