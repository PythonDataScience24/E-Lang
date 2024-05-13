import React, { useState, useEffect } from 'react';
import axios from 'axios';
import logoImg from './images/logo.png'; // Make sure the path matches where you store your image files
import './styles/worddeck.css'; // Make sure the path matches the location of your CSS file

const WordDeck = () => {
  const [word, setWord] = useState('');
  const [translation, setTranslation] = useState('');
  const [sentence, setSentence] = useState('');
  const [words, setWords] = useState([]);

  useEffect(() => {
    fetchWords();
  }, []);

  const fetchWords = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/language_ns/languagemodel');
      setWords(response.data);
    } catch (error) {
      console.error('Error fetching words', error);
    }
  };

  const addWord = async () => {
    if (!word || !translation || !sentence) {
      alert('Please fill in all fields');
      return;
    }
    try {
      const postData = { word, translation, sentence };
      const response = await axios.post('http://127.0.0.1:5000/language_ns/languagemodel', postData);
      setWords([...words, response.data]);
      setWord('');
      setTranslation('');
      setSentence('');
      // Fetch words again to update the table
      fetchWords();
    } catch (error) {
      console.error('Failed to add word', error);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <img src={logoImg} alt="Logo" className="logo" /> {/* Logo image */}
        <div className="title">My Word Deck</div>
      </div>
      <div className="form-table-container">
        <div className="input-form">
          <input
            type="text"
            placeholder="Word"
            value={word}
            onChange={(e) => setWord(e.target.value)}
          />
          <input
            type="text"
            placeholder="Translation"
            value={translation}
            onChange={(e) => setTranslation(e.target.value)}
          />
          <input
            type="text"
            placeholder="Sentence"
            value={sentence}
            onChange={(e) => setSentence(e.target.value)}
          />
          <button onClick={addWord}>Add word</button>
        </div>
        <div className="word-table">
          <table>
            <thead>
              <tr>
                <th>Word</th>
                <th>Translation</th>
                <th>Sentence</th>
              </tr>
            </thead>
            <tbody>
              {words.map((item, index) => (
                <tr key={index}>
                  <td>{item.word}</td>
                  <td>{item.translation}</td>
                  <td>{item.sentence}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default WordDeck;
