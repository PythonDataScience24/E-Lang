import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/progressreport.css';
import logoImg from './images/logo.png'; // Adjust path as necessary
import userImg from './images/user.png'; // Adjust path as necessary

function ProgressReports() {
    const [navVisible, setNavVisible] = useState(false);
    const navigate = useNavigate();

    const handleNavigate = (page) => {
        navigate(`/${page}`);
        setNavVisible(false); // Close the nav on navigation
    };

    const toggleNav = () => {
        setNavVisible(!navVisible);
    };

    return (
        <div className="app-container">
            <header className="header">
                <div className="header-logo-container">
                    <img src={logoImg} alt="Logo" className="header-logo" />
                </div>
                <div className="header-title">
                    <h1>E-lang Learning Assistant</h1>
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
                <div className="header-user-container">
                    <img src={userImg} alt="User" className="header-user" />
                </div>
            </header>
            <div className="progress-reports-container">
                <h2>Your Practice Performance</h2>
                <div className="progress-chart">
                    <iframe
                        src="http://127.0.0.1:5000/dash/"
                        style={{ width: '100%', height: '800px', border: 'none' }}
                        title="Progress Chart"
                    />
                </div>
                <p>
                    You have reached 45% of your goal to learn German at A2 level. You have learned around X of the X number of words required for that level.
                </p>
                <p>Keep going, you will be at 100% before you realize it!</p>
            </div>
        </div>
    );
}

export default ProgressReports;
