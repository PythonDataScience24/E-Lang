// src/components/Phonetics.js
import React, { useState } from 'react';
import './styles/styles.css';

function Phonetics() {
    const [word, setWord] = useState('Bahnhof');
    const [translation, setTranslation] = useState('');
    const [correctAnswer, setCorrectAnswer] = useState(false);
    const [attempt, setAttempt] = useState('');

    const checkAnswer = () => {
        setCorrectAnswer(attempt.toLowerCase() === 'train station');
    };

    const nextQuestion = () => {
        // Example logic for next question
        setWord('Hungry');
        setTranslation('Hungrig');
        setCorrectAnswer(false);
        setAttempt('');
    };

    return (
        <div className="phonetics-container">
            <h2>Phonetics</h2>
            <div className="card">
                <p><strong>Word:</strong> {word}</p>
                <input
                    type="text"
                    value={attempt}
                    placeholder="Your translation"
                    onChange={(e) => setAttempt(e.target.value)}
                />
                {!correctAnswer ? (
                    <div>
                        <button onClick={checkAnswer}>Submit</button>
                        <button onClick={nextQuestion}>Next</button>
                    </div>
                ) : (
                    <div>
                        <p className="correct-answer">Right Answer! Well done, keep going 😊</p>
                        <button onClick={nextQuestion}>Next</button>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Phonetics;
