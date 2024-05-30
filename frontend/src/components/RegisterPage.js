import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/login.css'; // Reusing the same CSS
import { FaUserCircle } from 'react-icons/fa';
import login_image from './images/login_image.jpg';
import logoImage from './images/logo.png';

function RegisterPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();

        if (password !== confirmPassword) {
            setError('Passwords do not match.');
            return;
        }

        if (username && password) {
            try {
                const response = await fetch('http://127.0.0.1:5000/auth_ns/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });

                const result = await response.json();

                if (response.ok) {
                    navigate('/');
                } else {
                    setError(result.message || 'Registration failed. Please try again.');
                }
            } catch (error) {
                setError('Error occurred. Try again.');
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
                        <h1>Create an account</h1>
                        <p>Register to get started</p>
                        <form onSubmit={handleRegister}>
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
                            <input
                                type="password"
                                placeholder="Confirm Password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                            />
                            <button type="submit">Register</button>
                            {error && <p className="error">{error}</p>}
                        </form>
                        <button onClick={() => navigate('/')} className="register-button">Back to Login</button>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default RegisterPage;
