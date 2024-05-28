import React, { useState, useEffect } from 'react';
import { ProgressBar, Button, Alert, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './styles/flashcards.css';
import logo from './images/logo.png';  // Replace with your logo path
import userImage from './images/user.png';  // Replace with your user image path

const FlashCards = () => {
  const [word, setWord] = useState('');
  const [translation, setTranslation] = useState('');
  const [pronunciation, setPronunciation] = useState('');
  const [exampleUsage, setExampleUsage] = useState('');
  const [progress, setProgress] = useState(0);
  const [showDropdown, setShowDropdown] = useState(false);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const navigate = useNavigate();

  const getToken = () => localStorage.getItem('access_token');

  const handleSubmit = async () => {
    if (!word || !translation || !pronunciation || !exampleUsage) {
      alert('Please fill all fields before submitting.');
      return;
    }
    try {
      const payload = {
        word: word,
        translation: translation,
        pronunciation: pronunciation,
        example_usage: exampleUsage
      };
      const token = getToken();
      console.log('Submitting payload:', payload);
      console.log('Authorization token:', token);
      const response = await axios.post('http://127.0.0.1:5000/vocabulary_ns/vocabulary', payload, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      console.log('Response:', response.data);
      setProgress(oldProgress => Math.min(oldProgress + 20, 100));
      setWord('');
      setTranslation('');
      setPronunciation('');
      setExampleUsage('');
      setError('');
    } catch (error) {
      console.error('Error posting word:', error);

      if (error.response) {
        if (error.response.data && error.response.data.message) {
          setError(`Failed to submit. Error: ${error.response.data.message}`);
        } else {
          setError(`Failed to submit. Status code: ${error.response.status}`);
        }
      } else if (error.request) {
        setError('No response received from the server.');
      } else {
        setError(`Failed to submit. Error: ${error.message}`);
      }
    }
  };

  const handleNext = () => {
    setProgress(oldProgress => Math.min(oldProgress + 5, 100));
    setWord('Bahnhof');
    setTranslation('');
    setPronunciation('');
    setExampleUsage('');
  };

  const handleMenuClick = () => {
    setShowDropdown(!showDropdown);
  };

  const handleGoHome = () => {
    navigate('/home');
  };

  useEffect(() => {
    if (progress === 100) {
      setShowModal(true);
      setTimeout(() => {
        navigate('/home');
      }, 5000);  // Redirect to home after 3 seconds
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
        <h1 className="title">Flash Cards</h1>
        {error && <Alert variant="danger">{error}</Alert>}
        <div className="flash-card-content">
          <div className="word-input">
            <label>Word:</label>
            <input type="text" value={word} onChange={(e) => setWord(e.target.value)} />
          </div>
          <div className="translation-input">
            <label>Your Translation:</label>
            <input type="text" value={translation} onChange={(e) => setTranslation(e.target.value)} />
          </div>
          <div className="pronunciation-input">
            <label>Pronunciation:</label>
            <input type="text" value={pronunciation} onChange={(e) => setPronunciation(e.target.value)} />
          </div>
          <div className="example-usage-input">
            <label>Example Usage:</label>
            <input type="text" value={exampleUsage} onChange={(e) => setExampleUsage(e.target.value)} />
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
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Congratulations!</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          You have finished the words for today.
        </Modal.Body>
      </Modal>
    </div>
  );
};

export default FlashCards;
