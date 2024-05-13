import React, { useState } from 'react';
import { ProgressBar, Button, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './styles/flashcards.css';
import logo from './images/logo.png';  // Replace with your logo path
import userImage from './images/user.png';  // Replace with your user image path

const FlashCards = () => {
  const [word, setWord] = useState('');
  const [translation, setTranslation] = useState('');
  const [sentence, setSentence] = useState('');
  const [difficulty, setDifficulty] = useState(1);
  const [progress, setProgress] = useState(0);
  const [showDropdown, setShowDropdown] = useState(false);
  const [error, setError] = useState(''); // To display error messages
  const navigate = useNavigate();

  const handleSubmit = async () => {
  if (!translation || !sentence || difficulty === 0) {
    alert('Please fill all fields before submitting.');
    return;
  }
  try {
    const payload = {
      word: word,
      translation: translation,
      sentence: sentence,
      difficulty: parseInt(difficulty, 10) // Ensure difficulty is sent as an integer
    };
    const response = await axios.post('http://127.0.0.1:5000/language_ns/languagemodel', payload);
    console.log('Response:', response.data);
    setProgress(oldProgress => Math.min(oldProgress + 20, 100));
    setWord("")
    setTranslation('');
    setSentence('');
    setDifficulty(1); // Reset difficulty to 1 as default
    setError(''); // Clear any previous errors
  } catch (error) {
    console.error('Error posting word:', error);
    setError('Failed to submit. Please try again.'); // Set error message for the user
  }
};

  const handleNext = () => {
    setProgress(oldProgress => Math.min(oldProgress + 5, 100));
    setWord('Bahnhof');
    setTranslation('');
    setSentence('');
    setDifficulty(1);
  };

  const handleMenuClick = () => {
    setShowDropdown(!showDropdown);
  };

  const handleGoHome = () => {
    navigate('/home');
  };

  return (
    <div className="container main-container">
      <nav className="navbar">
        <img src={logo} alt="Logo" className="navbar-logo" />
        <div className="navbar-menu-right">
          <div className="navbar-language-switch">Switch to English to German</div>
          <img src={userImage} alt="User" className="navbar-user-image" />
          <div className="navbar-menu-icon" onClick={handleMenuClick}>☰</div>
        </div>
        {showDropdown && (
          <div className="navbar-dropdown">
            <Button variant="light" onClick={handleGoHome}>Home</Button>
          </div>
        )}
      </nav>
      <main>
        <h1 className="title">Flash Cards</h1>
        {error && <Alert variant="danger">{error}</Alert>}  {/* Display error alert if there is an error */}
        <div className="flash-card-content">
          <div className="word-input">
            <label>Word:</label>
            <input type="text" value={word} onChange={(e) => setWord(e.target.value)} />
          </div>
          <div className="translation-input">
            <label>Your Translation:</label>
            <input type="text" value={translation} onChange={(e) => setTranslation(e.target.value)} />
          </div>
          <div className="sentence-input">
            <label>Sentence:</label>
            <input type="text" value={sentence} onChange={(e) => setSentence(e.target.value)} />
          </div>
          <div className="difficulty-input">
            <label>Difficulty (1-5):</label>
            <input type="number" value={difficulty} onChange={(e) => setDifficulty(e.target.value)} min="1" max="5" />
          </div>
          <div className="button-group">
            <Button variant="success" className="submit-button" onClick={handleSubmit}>
              Submit
            </Button>
            <Button variant="light" className="next-button" onClick={handleNext}>
              Next
            </Button>
          </div>
        </div>
        <ProgressBar now={progress} variant="info" className="progress-bar" />
      </main>
    </div>
  );
};

export default FlashCards;
