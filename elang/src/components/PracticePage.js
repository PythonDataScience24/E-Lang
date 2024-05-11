// src/components/PracticePage.js
import React from 'react';
import './styles.css';

function PracticePage({ onNavigate }) {
    return (
        <div className="practice-container">
            <h2>The best way to learn is by practicing.</h2>
            <p>Choose the right exercise for you right now.</p>
            <div className="practice-options">
                <div className="option">
                    <h3>Flash Cards</h3>
                    <p>Review vocabulary by translating words.</p>
                    <button onClick={() => onNavigate('flashcards')}>Practice</button>
                </div>
                <div className="option">
                    <h3>Sentence Correction</h3>
                    <p>Fill in empty spaces to learn how to use vocabulary.</p>
                    <button onClick={() => onNavigate('sentence-correction')}>Practice</button>
                </div>
                <div className="option">
                    <h3>Phonetics</h3>
                    <p>Write translations to train listening skills.</p>
                    <button onClick={() => onNavigate('phonetics')}>Practice</button>
                </div>
            </div>
        </div>
    );
}

export default PracticePage;
