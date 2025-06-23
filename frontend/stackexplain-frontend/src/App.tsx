// To run: npm run dev

import { useState, useEffect } from 'react';
import axios from 'axios';
import './styles.css';

function App() {
	const [error, setError] = useState('');
	const [explanation, setExplanation] = useState('');
	const [darkMode, setDarkMode] = useState(false);

	const BACKEND_SERVER_URL = 'http://localhost:8000/explain';

	const handleSubmitError = async () => {
		try {
			const response = await axios.post(BACKEND_SERVER_URL, { error });
			setExplanation(response.data.explanation);
		} catch (err) {
			setExplanation('An error occurred while contacting the server.');
		}
	};

	// Toggle dark mode class on <body>
	useEffect(() => {
		document.body.classList.toggle('dark', darkMode);
	}, [darkMode]);

	// Horribly ChatGPT'd
	return (
		<div className="app-container">
			<div className="content">
				<div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
					<h1 style={{ marginBottom: '1rem' }}>StackExplain</h1>
					<button onClick={() => setDarkMode(!darkMode)}>
						Toggle {darkMode ? 'Light' : 'Dark'} Mode
					</button>
				</div>

				<label htmlFor="error-input" style={{ display: 'block', marginBottom: '0.5rem' }}>
					Paste your error message:
				</label>

				<textarea
					id="error-input"
					rows={10}
					value={error}
					onChange={e => setError(e.target.value)}
				/>

				<br />

				<button onClick={handleSubmitError}>Explain Error</button>

				{explanation && (
					<div className="explanation">
						<h2>Explanation:</h2>
						<p>{explanation}</p>
					</div>
				)}
			</div>
		</div>
	);
}

export default App;