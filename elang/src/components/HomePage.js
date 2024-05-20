import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/homepage.css';
import flashcardImg from './images/flashcard.png';
import practiceImg from './images/practice.png';
import progressImg from './images/progress.png';
import logoImg from './images/logo.png';

function HomePage() {
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
    <div className="home-container">
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
        <h1>Welcome to your language learning platform</h1>
        <div className="sections-row">
          <div className="section" onClick={() => handleNavigate('flashcards')}>
            <img src={flashcardImg} alt="Flashcards" className="section-image" />
            <h2>Flash Cards</h2>
            <p>Go through a set of flash cards to review your vocabulary by translating words.</p>
            <button className="btn">My Deck</button>
          </div>
          <div className="section" onClick={() => handleNavigate('practice')}>
            <img src={practiceImg} alt="Practice" className="section-image" />
            <h2>Get Some Practice Here</h2>
            <p>Practice makes perfect. Regularly review your vocabulary.</p>
            <button className="btn">Study</button>
          </div>
          <div className="section" onClick={() => handleNavigate('reports')}>
            <img src={progressImg} alt="Progress" className="section-image" />
            <h2>Get an Overview of Your Progress</h2>
            <p>Seeing your progress will keep you motivated.</p>
            <button className="btn">My Reports</button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default HomePage;
