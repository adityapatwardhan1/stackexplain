import { useState, useEffect } from 'react';
import axios from 'axios';
import './styles.css';

function App() {
	const [error, setError] = useState('');
	const [model, setModel] = useState('deepseek/deepseek-chat-v3-0324:free');
	const [response, setResponse] = useState<{
		error_type?: string;
		explanation?: string;
		suggested_fix?: string;
		relevant_links?: string[];
	} | null>(null);

	const [darkMode, setDarkMode] = useState(false);

	const BACKEND_SERVER_URL = 'http://localhost:8000/explain';

	const handleSubmitError = async () => {
		try {
			const res = await axios.post(BACKEND_SERVER_URL, {
				error,
				model,
			});
			setResponse(res.data);
		} catch (err) {
			console.error(err);
			setResponse({
				error_type: 'RequestError',
				explanation: 'Failed to contact the backend server.',
				suggested_fix: 'Ensure the server is running on port 8000.',
				relevant_links: [],
			});
		}
	};

	useEffect(() => {
		document.body.classList.toggle('dark', darkMode);
	}, [darkMode]);

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

				<label htmlFor="model-select" style={{ display: 'block', marginBottom: '0.5rem', marginTop: '1rem' }}>
					Select model:
				</label>
				<select
					id="model-select"
					value={model}
					onChange={e => setModel(e.target.value)}
					style={{ marginBottom: '1rem' }}
				>
					<option value="deepseek/deepseek-chat-v3-0324:free">DeepSeek</option>
					<option value="google/gemini-2.0-flash-exp:free">Gemini</option>
					<option value="mistralai/mistral-small-3.2-24b-instruct:free">Mistral</option>
				</select>

				<br />

				<button onClick={handleSubmitError}>Explain Error</button>

				{response && (
					<div
						style={{
							marginTop: '2rem',
							whiteSpace: 'pre-wrap',
							padding: '1rem',
							borderRadius: '4px',
							maxWidth: '800px',
						}}
						className="content"
					>
						<h2>Explanation</h2>
						{response.error_type && (
							<p><strong>Error Type:</strong> {response.error_type}</p>
						)}
						{response.explanation && (
							<p><strong>Explanation:</strong> {response.explanation}</p>
						)}
						{response.suggested_fix && (
							<p><strong>Suggested Fix:</strong> {response.suggested_fix}</p>
						)}
						{response.relevant_links && response.relevant_links.length > 0 && (
							<p>
								<strong>More Info:</strong>
								<ul style={{ paddingLeft: '1.2em', marginTop: '0.5em' }}>
									{response.relevant_links.map((link, index) => (
										<li key={index}>
											<a href={link} target="_blank" rel="noopener noreferrer">
												{link}
											</a>
										</li>
									))}
								</ul>
							</p>
						)}
						{response.relevant_links && response.relevant_links.length === 0 && (
							<p><strong>More Info:</strong> No relevant links available.</p>
						)}
					</div>
				)}

			</div>
		</div>
	);
}

export default App;


// import { useState, useEffect } from 'react';
// import axios from 'axios';
// import './styles.css';

// function App() {
// 	const [error, setError] = useState('');
// 	const [response, setResponse] = useState<{
// 		error_type?: string;
// 		explanation?: string;
// 		suggested_fix?: string;
// 		relevant_links?: string[];
// 	} | null>(null);

// 	const [darkMode, setDarkMode] = useState(false);

// 	const BACKEND_SERVER_URL = 'http://localhost:8000/explain';

// 	const handleSubmitError = async () => {
// 		try {
// 			const res = await axios.post(BACKEND_SERVER_URL, { error });
// 			setResponse(res.data);
// 		} catch (err) {
// 			console.error(err);
// 			setResponse({
// 				error_type: 'RequestError',
// 				explanation: 'Failed to contact the backend server.',
// 				suggested_fix: 'Ensure the server is running on port 8000.',
// 				relevant_links: [],
// 			});
// 		}
// 	};

// 	useEffect(() => {
// 		document.body.classList.toggle('dark', darkMode);
// 	}, [darkMode]);

// 	return (
// 		<div className="app-container">
// 			<div className="content">
// 				<div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
// 					<h1 style={{ marginBottom: '1rem' }}>StackExplain</h1>
// 					<button onClick={() => setDarkMode(!darkMode)}>
// 						Toggle {darkMode ? 'Light' : 'Dark'} Mode
// 					</button>
// 				</div>

// 				<label htmlFor="error-input" style={{ display: 'block', marginBottom: '0.5rem' }}>
// 					Paste your error message:
// 				</label>

// 				<textarea
// 					id="error-input"
// 					rows={10}
// 					value={error}
// 					onChange={e => setError(e.target.value)}
// 				/>

// 				<br />

// 				<button onClick={handleSubmitError}>Explain Error</button>

// 				{response && (
// 					<div
// 						style={{
// 							marginTop: '2rem',
// 							whiteSpace: 'pre-wrap',
// 							padding: '1rem',
// 							borderRadius: '4px',
// 							maxWidth: '800px',
// 						}}
// 						className="content"
// 					>
// 						<h2>Explanation</h2>
// 						{response.error_type && (
// 							<p><strong>Error Type:</strong> {response.error_type}</p>
// 						)}
// 						{response.explanation && (
// 							<p><strong>Explanation:</strong> {response.explanation}</p>
// 						)}
// 						{response.suggested_fix && (
// 							<p><strong>Suggested Fix:</strong> {response.suggested_fix}</p>
// 						)}
// 						{response.relevant_links && response.relevant_links.length > 0 && (
// 							<p>
// 								<strong>More Info:</strong>
// 								<ul style={{ paddingLeft: '1.2em', marginTop: '0.5em' }}>
// 									{response.relevant_links.map((link, index) => (
// 										<li key={index}>
// 											<a href={link} target="_blank" rel="noopener noreferrer">
// 												{link}
// 											</a>
// 										</li>
// 									))}
// 								</ul>
// 							</p>
// 						)}
// 						{response.relevant_links && response.relevant_links.length === 0 && (
// 							<p><strong>More Info:</strong> No relevant links available.</p>
// 						)}
// 					</div>
// 				)}

// 			</div>
// 		</div>
// 	);
// }

// export default App;
