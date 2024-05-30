import React from 'react';
import './styles/DisplayPage.css';
import logo from './images/logo.png';
import userIcon from './images/user.png';
import languageImage from './images/languageImage.png';

const DisplayPage = () => {
  return (
    <div className="container">
      <header className="header">
        <img src={logo} alt="E'Lang Logo" className="logo" />
        <nav className="navbar">
          <ul>
            <li><a href="/login">Login</a></li>
            <li><a href="/register">Register</a></li>
            <li><img src={userIcon} alt="User Icon" className="user-icon" /></li>
          </ul>
        </nav>
      </header>
      <main className="main-content">
        <div className="text-content">
          <h1>Learn a language on the go.</h1>
          <p>We make it easy for you to learn, study and practice a new language.</p>
          <p>We are introducing an easy and effective way to learn a language. Write the new words you learn, review them, and get our feedback on how you can improve.</p>
        </div>
        <div className="image-content">
          <img src={languageImage} alt="Learning Language" />
        </div>
      </main>
      <footer className="footer">
        <button className="app-store-button">Soon on the App Store</button>
        <button className="google-play-button">Soon on Google Play</button>
      </footer>
    </div>
  );
};

export default DisplayPage;
