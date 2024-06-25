import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CatFarm from './components/CatFarm';
import Demo from './components/Demo';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Demo />} />
        <Route path="/demo" element={<Demo />} /> {/* Новый маршрут для демо-версии */}
        <Route path="/catfarm" element={<CatFarm />} />
      </Routes>
    </Router>
  );
}
c

export default App;