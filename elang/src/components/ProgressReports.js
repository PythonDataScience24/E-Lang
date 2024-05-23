import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './styles/progressreport.css';
import logoImg from './images/logo.png'; // Adjust path as necessary

function ProgressReports() {
    const [progressData, setProgressData] = useState(null);
    const [error, setError] = useState('');
    const [navVisible, setNavVisible] = useState(false);
    const navigate = useNavigate();

    const handleNavigate = (page) => {
        navigate(`/${page}`);
        setNavVisible(false); // Close the nav on navigation
    };

    const toggleNav = () => {
        setNavVisible(!navVisible);
    };

    useEffect(() => {
        document.title = "E-Lang Learning Assistant";

        const fetchProgressData = async () => {
            const token = localStorage.getItem('access_token');
            try {
                const response = await axios.get('http://127.0.0.1:5000/language_ns/progress_visualization/user_id', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    responseType: 'blob'
                });
                const imageUrl = URL.createObjectURL(response.data);
                setProgressData(imageUrl);
            } catch (error) {
                setError('Failed to fetch progress data');
            }
        };

        fetchProgressData();
    }, []);

    if (error) {
        return <p>{error}</p>;
    }

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
            </header>
            <div className="progress-reports-container">
                <h2>Your Progression Toward Your Goal</h2>
                <div className="progress-chart">
                    {progressData ? (
                        <img src={progressData} alt="Progression Toward Goal" style={{ width: '100%' }} />
                    ) : (
                        <p>Loading progress data...</p>
                    )}
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
