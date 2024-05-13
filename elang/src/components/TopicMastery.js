// src/components/TopicMastery.js
import React from 'react';
import './styles/styles.css';
import MasteryImg from'./images/mastery.png'

function TopicMastery() {
    return (
        <div className="topic-mastery-container">
            <h2>Topics Mastery</h2>
            <p>Here is an overview of your success rate based on the topics studied.</p>
            <div className="pie-chart">
                <img src={MasteryImg} alt="Topic Mastery Chart" />
            </div>
        </div>
    );
}

export default TopicMastery;
