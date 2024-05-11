// src/components/LoginPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './login.css';
import { FaUserCircle } from 'react-icons/fa';
import login_image from './login_image.jpg';
import logoImage from './logo.png';

function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate(); // Initialize useNavigate

    const handleLogin = async (e) => {
        e.preventDefault(); // Prevent page reload

        if (username && password) {
            try {
                const response = await fetch('http://127.0.0.1:5000/auth_ns/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });

                const result = await response.json();

                if (response.ok) {
                    navigate('/home'); // Redirect to HomePage on successful login
                } else {
                    setError(result.message || 'Login failed. Please try again.');
                }
            } catch (error) {
                setError('An error occurred. Please try again later.');
            }
        } else {
            setError('Please enter a username and password.');
        }
    };

    return (
        <div className="login-container">
            <header className="header">
                <div className="header-logo">
                    <img src={logoImage} alt="Logo" />
                </div>
                <div className="header-profile">
                    <FaUserCircle size="32px" />
                </div>
            </header>
            <main className="login-main">
                <div className="welcome-container">
                    <div className="welcome-image">
                        <img src={login_image} alt="Welcome" />
                    </div>
                    <div className="login-form">
                        <h1>Welcome back!</h1>
                        <p>Login to continue</p>
                        <form onSubmit={handleLogin}>
                            <input
                                type="text"
                                placeholder="Username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                            <input
                                type="password"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                            <button type="submit">Login</button>
                            <a href="/forgot-password">Forget Password?</a>
                            {error && <p className="error">{error}</p>}
                        </form>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default LoginPage;
