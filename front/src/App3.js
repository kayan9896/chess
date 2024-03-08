import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import PlayMyself from './PlayMyself';
import PlayAI from './PlayAI';
import RandomOpponents from './RandomOpponents';
import RoomNumber from './RoomNumber';

function App() {
  return (
    
      <div className="App">
        
        <Routes>
          <Route path="/play-myself" element={<PlayMyself/>} />
          <Route path="/play-ai" element={<PlayAI />}/>
          <Route path="/random-opponents" element={<RandomOpponents />}/>
          <Route path="/room-number" element={<RoomNumber />}/>
    
          <Route path="/" element={<Home />}/>
          
        </Routes>
      </div>
    
  );
}

function Home() {
  return (
    <>
      <nav>
        <ul>
          <li>
            <Link to="/play-myself">Play Myself</Link>
          </li>
          <li>
            <Link to="/play-ai">Play AI</Link>
          </li>
          <li>
            <Link to="/random-opponents">Random Opponents</Link>
          </li>
          <li>
            <Link to="/room-number">Room Number</Link>
          </li>
        </ul>
      </nav>
      <h2>Welcome to the Chess Game!</h2>
    </>
  );
}

export default App;
