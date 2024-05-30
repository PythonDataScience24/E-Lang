import React from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import HomePage from './components/HomePage';
import FlashCards from './components/FlashCards';
import MyWordDeck from './components/MyWordDeck';
import PracticePage from './components/PracticePage';
import SentenceCorrection from './components/SentenceCorrection';
import ProgressReports from './components/ProgressReports';
import RegisterPage from "./components/RegisterPage";
import './components/styles/styles.css';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/home" element={<HomePage />} />
                <Route path="/flashcards" element={<FlashCards />} />
                <Route path="/mydeck" element={<MyWordDeck />} />
                <Route path="/practice" element={<WrapperComponent />} />
                <Route path="/practice/sentence-correction" element={<SentenceCorrection />} />
                <Route path="/sentence-correction" element={<SentenceCorrection />} />
                <Route path="/reports" element={<ProgressReports />} />
            </Routes>
        </Router>
    );
}

// Wrapper component to provide navigation capabilities
function WrapperComponent() {
    const navigate = useNavigate();

    const handleNavigate = (path) => {
        navigate(path);
    };

    return <PracticePage onNavigate={handleNavigate} />;
}

export default App;
