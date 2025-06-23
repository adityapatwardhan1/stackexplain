// To run: npm run dev

import { useState } from 'react';
import axios from 'axios';

function App() {
	const [error, setError] = useState('');
	const [explanation, setExplanation] = useState('');

	const BACKEND_SERVER_URL = 'http://localhost:8000/explain';

	const handleSubmitError = async () => {
		try {
			const response = await axios.post(BACKEND_SERVER_URL, { error });
			setExplanation(response.data.explanation);
		} catch (err) {
			setExplanation('An error occurred while contacting the server.');
		}
	};

	// This is horribly ChatGPT'd, make it my own.
	return (
		<div style={{
			padding: '2rem',
			fontFamily: 'sans-serif',
			backgroundColor: '#f8f9fa', // light background
			color: '#212529',            // dark text
			minHeight: '100vh'
		}}>
			<h1 style={{ marginBottom: '1rem' }}>StackExplain</h1>

			<label htmlFor="error-input" style={{ display: 'block', marginBottom: '0.5rem' }}>
				Paste your error message:
			</label>

			<textarea
				id="error-input"
				rows={10}
				cols={80}
				value={error}
				onChange={e => setError(e.target.value)}
				style={{
					width: '100%',
					maxWidth: '800px',
					padding: '1rem',
					fontFamily: 'monospace',
					fontSize: '1rem',
					border: '1px solid #ced4da',
					borderRadius: '4px',
					backgroundColor: '#ffffff',
					color: '#212529',
				}}
			/>

			<br />

			<button
				onClick={handleSubmitError}
				style={{
					marginTop: '1rem',
					padding: '0.5rem 1rem',
					fontSize: '1rem',
					cursor: 'pointer',
					backgroundColor: '#0d6efd',
					color: 'white',
					border: 'none',
					borderRadius: '4px',
				}}
			>
				Explain Error
			</button>

			{explanation && (
				<div style={{
					marginTop: '2rem',
					whiteSpace: 'pre-wrap',
					backgroundColor: '#e9ecef',
					padding: '1rem',
					borderRadius: '4px',
					maxWidth: '800px'
				}}>
					<h2>Explanation:</h2>
					<p>{explanation}</p>
				</div>
			)}
		</div>
	);
}

export default App;