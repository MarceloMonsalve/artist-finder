import { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';
import ArtistTable from './ArtistTable';
import './App.css';

const supabaseUrl = 'https://ebwkprvicnnscxhesdez.supabase.co';
const supabaseKey =
	'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVid2twcnZpY25uc2N4aGVzZGV6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc3ODY0MjUsImV4cCI6MjAyMzM2MjQyNX0.uN086LfUsLBTu0WSJ9OOJoDYYb1tERWk7-iqBqLmzTU';
const supabase = createClient(supabaseUrl, supabaseKey);

const App = () => {
	const [artists, setArtists] = useState([]);

	useEffect(() => {
		fetchArtists();
	}, []);

	const fetchArtists = async () => {
		const { data, error } = await supabase
			.from('artists')
			.select('unique_id, date, visible')
			.eq('visible', true);

		if (error) {
			console.error(error);
			return;
		}

		setArtists(data);
	};

	const removeArtist = async (unique_id) => {
		const confirmation = window.confirm(
			`Are you sure you want to remove ${unique_id}?`
		);

		if (confirmation) {
			const { error } = await supabase
				.from('artists')
				.update({ visible: false })
				.eq('unique_id', unique_id);

			if (error) {
				console.error(error);
				return;
			}

			fetchArtists();
		}
	};

	return (
		<div className="App">
			<h1>TikTok Artist Finder</h1>
			<ArtistTable artists={artists} removeArtist={removeArtist} />
		</div>
	);
};

export default App;
