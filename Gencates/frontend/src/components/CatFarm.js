import React, { useState, useEffect } from 'react';

function CatFarm() {
  const [cats, setCats] = useState([]);
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    fetch('/api/cats/')
      .then(response => response.json())
      .then(data => setCats(data));

    fetch('/api/profiles/1/')  // Замените 1 на ID текущего пользователя
      .then(response => response.json())
      .then(data => setProfile(data));
  }, []);

  return (
    <div>
      <h1>Cat Farm</h1>
      {profile && <div>Coins: {profile.coins}</div>}
      <h2>Your Cats</h2>
      <ul>
        {cats.map(cat => (
          <li key={cat.id}>{cat.name} - Level {cat.level} - {cat.coins_per_minute} coins/min</li>
        ))}
      </ul>
    </div>
  );
}

export default CatFarm;
