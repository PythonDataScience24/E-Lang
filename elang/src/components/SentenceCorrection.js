import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Updated import
import './styles/sentence.css'; // Ensure this CSS file is updated accordingly
import logoImg from './images/logo.png';  // Assuming logo image is stored here
import menuIcon from './images/user.png';  // Assuming menu icon is stored here
import backIcon from './images/back.png';  // Assuming back icon is stored here

function SentenceCorrection() {
    const [word, setWord] = useState('');
    const [sentence, setSentence] = useState('');
    const [input, setInput] = useState('');
    const [feedback, setFeedback] = useState('');
    const [progress, setProgress] = useState(0);
    const [total, setTotal] = useState(5); // Total number of questions
    const [questionData, setQuestionData] = useState(null); // Store question data
    const navigate = useNavigate(); // Use navigate for navigation

    // Function to fetch data from the Flask API
    const fetchData = async () => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            setFeedback('No access token found. Please log in.');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/quiz_ns/generate', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to fetch data.');
            }

            const data = await response.json();
            setSentence(data.question.replace('_____', '_____ (fill in the blank)'));
            setWord(data.correct_word);
            setQuestionData(data); // Store the question data for later use
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

        if (!questionData) {
            setFeedback('No question data available. Please try again.');
            return;
        }

        const isCorrect = input.trim().toLowerCase() === questionData.correct_word.trim().toLowerCase();
        const token = localStorage.getItem('access_token');
        if (!token) {
            setFeedback('No access token found. Please log in.');
            return;
        }

        try {
            const payload = {
                responses: [
                    {
                        question_id: questionData.question_id,
                        user_answer: input,
                        is_correct: isCorrect
                    }
                ]
            };

            console.log('Submitting payload:', payload); // Log payload for debugging

            const response = await fetch(`http://127.0.0.1:5000/quiz_ns/submit/${questionData.quiz_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Response error:', errorData);
                throw new Error(errorData.message || 'Failed to submit answer.');
            }

            const result = await response.json();
            console.log('Submission result:', result); // Log result for debugging

            if (isCorrect) {
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

    const handleBack = () => {
        navigate(-1); // Navigate to the previous page
    };

    return (
        <div className="app-container">
            <div className="app-content">
                <header className="app-header">
                    <div className="header-left">
                        <img src={logoImg} alt="App Logo" className="logo" />
                        <h1 className="app-title">E'lang</h1>
                    </div>
                    <div className="header-right">
                        <img src={backIcon} alt="Back Icon" className="back-icon" onClick={handleBack} />
                        <img src={menuIcon} alt="Menu Icon" className="menu-icon" />
                    </div>
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
        </div>
    );
}

export default SentenceCorrection;
