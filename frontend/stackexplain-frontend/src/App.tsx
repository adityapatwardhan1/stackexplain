// To run: npm run dev

import { useState } from 'react';
import axios from 'axios';
import './styles.css';

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

	// Horribly ChatGPT'd
	return (
		<div className="app-container">
			<div className="content">
				<h1 style={{ marginBottom: '1rem' }}>StackExplain</h1>

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
	// return (
	// 	<div style={{
	// 		minHeight: '100vh',
	// 		width: '100vw', // fill the full screen width
	// 		fontFamily: 'sans-serif',
	// 		backgroundColor: '#f8f9fa',
	// 		color: '#212529',
	// 		display: 'flex',
	// 		justifyContent: 'center',
	// 		alignItems: 'flex-start',
	// 		padding: '2rem',
	// 		boxSizing: 'border-box' // ensures padding doesn't shrink the box
	// 	}}>
	// 		<div style={{
	// 		width: '100%',
	// 		maxWidth: '800px',
	// 		}}>
	// 		<h1 style={{ marginBottom: '1rem' }}>StackExplain</h1>

	// 		<label htmlFor="error-input" style={{ display: 'block', marginBottom: '0.5rem' }}>
	// 			Paste your error message:
	// 		</label>

	// 		<textarea
	// 			id="error-input"
	// 			rows={10}
	// 			value={error}
	// 			onChange={e => setError(e.target.value)}
	// 			style={{
	// 			width: '100%',
	// 			padding: '1rem',
	// 			fontFamily: 'monospace',
	// 			fontSize: '1rem',
	// 			border: '1px solid #ced4da',
	// 			borderRadius: '4px',
	// 			backgroundColor: '#ffffff',
	// 			color: '#212529',
	// 			boxSizing: 'border-box'
	// 			}}
	// 		/>

	// 		<br />

	// 		<button
	// 			onClick={handleSubmitError}
	// 			style={{
	// 			marginTop: '1rem',
	// 			padding: '0.5rem 1rem',
	// 			fontSize: '1rem',
	// 			cursor: 'pointer',
	// 			backgroundColor: '#0d6efd',
	// 			color: 'white',
	// 			border: 'none',
	// 			borderRadius: '4px',
	// 			}}
	// 		>
	// 			Explain Error
	// 		</button>

	// 		{explanation && (
	// 			<div style={{
	// 			marginTop: '2rem',
	// 			whiteSpace: 'pre-wrap',
	// 			backgroundColor: '#e9ecef',
	// 			padding: '1rem',
	// 			borderRadius: '4px',
	// 			}}>
	// 			<h2>Explanation:</h2>
	// 			<p>{explanation}</p>
	// 			</div>
	// 		)}
	// 		</div>
	// 	</div>
	// );
}

export default App;