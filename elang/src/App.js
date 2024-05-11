// src/App.js
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import HomePage from './components/HomePage';
import FlashCards from './components/FlashCards';
import MyWordDeck from './components/MyWordDeck';
import PracticePage from './components/PracticePage';
import SentenceCorrection from './components/SentenceCorrection';
import ProgressReports from './components/ProgressReports';
import './components/styles.css';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path="/home" element={<HomePage />} />
                <Route path="/flashcards" element={<FlashCards />} />
                <Route path="/mydeck" element={<MyWordDeck />} />
                <Route path="/practice" element={<PracticePage />} />
                <Route path="/sentence-correction" element={<SentenceCorrection />} />
                <Route path="/reports" element={<ProgressReports />} />
            </Routes>
        </Router>
    );
}

export default App;
