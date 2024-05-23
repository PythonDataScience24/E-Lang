import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/login.css';
import { FaUserCircle } from 'react-icons/fa';
import login_image from './images/login_image.jpg';
import logoImage from './images/logo.png';

function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();

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
                    console.log('Access Token:', result.access_token); // Log the token
                    localStorage.setItem('access_token', result.access_token);
                    localStorage.setItem('refresh_token', result.refresh_token);
                    navigate('/home');
                } else {
                    setError(result.message || 'Login failed. Please try again.');
                }
            } catch (error) {
                setError('Wrong User details. Try again');
            }
        } else {
            setError('Please enter a username and password.');
        }
    };

    return (
        <div className="login-container">
            <header className="header">
                <div className="header-logo">
                    <img src={logoImage} alt="Logo" loading="lazy" />
                </div>
                <div className="header-title">
                    <h1>E-lang App</h1>
                </div>
                <div className="header-profile">
                    <FaUserCircle size="32px" />
                </div>
            </header>
            <main className="login-main">
                <div className="welcome-container">
                    <div className="welcome-image">
                        <img src={login_image} alt="Welcome" loading="lazy" />
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
                        <button onClick={() => navigate('/register')} className="register-button">Register</button>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default LoginPage;
