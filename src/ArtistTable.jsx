const ArtistTable = ({ artists, removeArtist }) => (
	<table>
		<thead>
			<tr>
				<th>Username</th>
				<th>Date Found</th>
				<th>Remove</th>
			</tr>
		</thead>
		<tbody>
			{artists.map((artist) => (
				<tr key={artist.unique_id}>
					<td>
						<a
							href={`https://www.tiktok.com/@${artist.unique_id}`}
							target="_blank"
						>
							@{artist.unique_id}
						</a>
					</td>
					<td>{artist.date}</td>
					<td>
						<button
							className="remove-button"
							onClick={() => removeArtist(artist.unique_id)}
						>
							Remove
						</button>
					</td>
				</tr>
			))}
		</tbody>
	</table>
);

export default ArtistTable;
