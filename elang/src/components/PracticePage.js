import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/practice.css';
import flashcardImg from './images/flashcard.png';
import sentenceCorrectionImg from './images/sentence-correction.png';
import phoneticsImg from './images/phonetics.png';
import logoImg from './images/logo.png';

function PracticePage() {
  const navigate = useNavigate();
  const [navVisible, setNavVisible] = useState(false);

  const handleNavigate = (page) => {
    navigate(`/${page}`);
    setNavVisible(false); // Ensures the nav closes on navigation
  };

  const toggleNav = () => {
    setNavVisible(!navVisible);
  };

  return (
    <div className="practice-container">
      <header className="header">
        <div className="header-logo-container">
          <img src={logoImg} alt="Logo" className="header-logo" />
        </div>
        <div className="header-title">
          <h1>E-lang App</h1>
        </div>
        <div className="header-navigation">
          <div className="menu-icon" onClick={toggleNav}>☰</div>
          <nav className={`vertical-nav ${navVisible ? 'visible' : ''}`}>
            <ul>
              <li onClick={() => handleNavigate('home')}>Home</li>
              <li onClick={() => handleNavigate('mydeck')}>Word Deck</li>
              <li onClick={() => handleNavigate('userpage')}>User Page</li>
              <li onClick={() => handleNavigate('practice')}>Practice</li>
              <li onClick={() => handleNavigate('flashcards')}>Flash Cards</li>
              <li onClick={() => handleNavigate('reports')}>Reports</li>
              <li onClick={() => handleNavigate('')}>Exit</li>
            </ul>
          </nav>
        </div>
      </header>
      <main className="main-content">
        <h2>The best way to learn is by practicing.</h2>
        <p>Choose the right exercise for you right now.</p>
        <div className="sections-row">
          <div className="section" onClick={() => handleNavigate('flashcards')}>
            <img src={flashcardImg} alt="Flash Cards" className="section-image" />
            <h3>Flash Cards</h3>
            <p>Go through a set of flash cards to review your vocabulary by translating words.</p>
            <button className="btn">Practice</button>
          </div>
          <div className="section" onClick={() => handleNavigate('sentence-correction')}>
            <img src={sentenceCorrectionImg} alt="Sentence Correction" className="section-image" />
            <h3>Sentence Correction</h3>
            <p>Fill in the empty spaces in a sentence to learn how to properly use your acquired vocabulary.</p>
            <button className="btn">Practice</button>
          </div>
          <div className="section" onClick={() => handleNavigate('phonetics')}>
            <img src={phoneticsImg} alt="Phonetics" className="section-image" />
            <h3>Phonetics</h3>
            <p>Write the translation of the words you will hear to train your listening skills.</p>
            <button className="btn">Practice</button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default PracticePage;
