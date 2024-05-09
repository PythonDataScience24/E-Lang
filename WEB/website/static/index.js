document.getElementById('addWordForm').addEventListener('submit', function(e) {
  e.preventDefault();

  let word = document.getElementById('wordInput').value;
  let translation = document.getElementById('translationInput').value;

  fetch('/add-word', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // Include CSRF token header if required
    },
    body: JSON.stringify({
      word: word,
      translation: translation,
      sentence: sentence,
    })
  }).then(response => response.json())
  .then(data => {
    if (data.success) {
      // Append new word to vocab table
      let vocabList = document.getElementById('vocab-list');
      let row = vocabList.insertRow();
      let cell1 = row.insertCell(0);
      let cell2 = row.insertCell(1);
      let cell3 = row.insertCell(2);
      cell1.innerHTML = data.word;
      cell2.innerHTML = data.translation;
      cell3.innerHTML = '<button class="btn btn-danger" onclick="removeWord(this)">Remove</button>';

      // Clear the form fields and refocus on the word input for quick new entry
      document.getElementById('wordInput').value = "";
      document.getElementById('translationInput').value = "";
      document.getElementById('wordInput').focus();
    } else {
      alert('Error adding word: ' + data.error);
    }
  }).catch(error => {
    console.error('Error:', error);
  });
});

function removeWord(btn) {
  let row = btn.parentNode.parentNode;
  row.parentNode.removeChild(row);
}
