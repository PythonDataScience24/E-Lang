import React, { useState, useEffect } from 'react';
import { Button, Alert, ProgressBar } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './styles/sentence.css';
import logo from './images/logo.png';  // Replace with your logo path
import userImage from './images/user.png';  // Replace with your user image path

const SentenceCorrection = () => {
  const [word, setWord] = useState('');
  const [sentence, setSentence] = useState('');
  const [input, setInput] = useState('');
  const [feedback, setFeedback] = useState('');
  const [progress, setProgress] = useState(0);
  const [showDropdown, setShowDropdown] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const getToken = () => localStorage.getItem('access_token');

  const fetchData = async () => {
    const token = getToken();
    if (!token) {
      setError('No access token found. Please log in.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/quiz_ns/generate', {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = response.data;
      setSentence(data.question.replace('_____', '_____ (fill in the blank)'));
      setWord(data.correct_word);
      setError('');
    } catch (error) {
      console.error('Fetch error:', error);
      setError('Failed to load data. Please try again later.');
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const checkAnswer = async () => {
    if (!input) {
      setFeedback('Please enter a word before submitting.');
      return;
    }

    if (!word) {
      setFeedback('No question data available. Please try again.');
      return;
    }

    const isCorrect = input.trim().toLowerCase() === word.trim().toLowerCase();
    const token = getToken();
    if (!token) {
      setFeedback('No access token found. Please log in.');
      return;
    }

    try {
      const payload = {
        responses: [
          {
            question_id: word,
            user_answer: input,
            is_correct: isCorrect
          }
        ]
      };

      const response = await axios.post(`http://127.0.0.1:5000/quiz_ns/submit/${word}`, payload, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (isCorrect) {
        setFeedback('Right Answer! Well done, keep going 😊');
        setProgress(oldProgress => Math.min(oldProgress + 20, 100));
        fetchData();
      } else {
        setFeedback('Wrong Answer! Review this later, practice makes perfect 😞');
      }
    } catch (error) {
      console.error('Submission error:', error);
      setFeedback('Failed to submit answer. Please try again later.');
    }

    setInput('');
  };

  const handleNext = () => {
    fetchData();
    setFeedback('');
    setInput('');
  };

  const handleMenuClick = () => {
    setShowDropdown(!showDropdown);
  };

  const handleGoHome = () => {
    navigate('/home');
  };

  useEffect(() => {
    if (progress === 100) {
      setTimeout(() => {
        navigate('/home');
      }, 5000);
    }
  }, [progress, navigate]);

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
        <h1 className="title">Sentence Correction</h1>
        {error && <Alert variant="danger">{error}</Alert>}
        {feedback && <Alert variant={feedback.includes('Right') ? 'success' : 'danger'}>{feedback}</Alert>}
        <div className="sentence-correction-content">
          <div className="word-input">
            <label>Word:</label>
            <input type="text" value={input} onChange={(e) => setInput(e.target.value)} />
          </div>
          <div className="sentence-input">
            <label>Sentence:</label>
            <p>{sentence}</p>
          </div>
          <div className="button-group">
            <Button variant="success" className="submit-button" onClick={checkAnswer}>
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

export default SentenceCorrection;
