// src/components/SentenceCorrection.js
import React, { useState } from 'react';
import './styles.css';

function SentenceCorrection() {
    const [sentence, setSentence] = useState('Ich habe ____.');
    const [correct, setCorrect] = useState(false);

    const submitAnswer = () => {
        setCorrect(true);
    };

    return (
        <div className="sentence-correction-container">
            <h2>Sentence Correction</h2>
            <div className="sentence-card">
                <p><strong>Word:</strong> Bahnhof</p>
                <p><strong>Sentence:</strong> {sentence}</p>
                {!correct ? (
                    <button onClick={submitAnswer}>Submit</button>
                ) : (
                    <p className="correct-answer">Right Answer! Well done, keep going 😊</p>
                )}
            </div>
        </div>
    );
}

export default SentenceCorrection;
