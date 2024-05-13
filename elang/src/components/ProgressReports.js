// src/components/ProgressReports.js
import React from 'react';
import './styles/styles.css';

function ProgressReports() {
    return (
        <div className="progress-reports-container">
            <h2>Your Progression Toward Your Goal</h2>
            <p>
                You have reached 45% of your goal to learn German at A2 level. You have learned around X of the X number of words required for that level.
            </p>
            <div className="progress-chart">
                <img src="Reports_Progression toward goal.png" alt="Progression Toward Goal" />
            </div>
        </div>
    );
}

export default ProgressReports;
