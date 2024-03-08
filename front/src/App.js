import React, { useState } from 'react';
import Cell from './Cell';
import './App.css';
import PlayMyself from './PlayMyself';
import PlayAI from './PlayAI';
import RandomOpponents from './RandomOpponents';
import RoomNumber from './RoomNumber';

function App() {
  const [screen, setScreen] = useState('start');

  // Render screen based on current state
  const renderScreen = () => {
    switch (screen) {
      case 'start':
        return (
          <div className="start-screen">
            <h2>Choose Game Mode</h2>
            <button onClick={() => setScreen('me')}>1. Play with myself</button>
            <button onClick={() => setScreen('ai')}>2. Play with AI</button>
            <button onClick={() => setScreen('random')}>3. Play with random players</button>
            <button onClick={() => setScreen('room')}>4. Enter room number</button>
          </div>
        );
    case 'random':
        return (
          <RandomOpponents/>
        );
      case 'ai':
        return (
          <PlayAI/>
        );
      case 'me':
        return (
         <PlayMyself/>
        );
        case 'room':
          return (
           <RoomNumber/>
          );
      default:
        return null;
    }
  };

  return (
    <div className="App">
      {/* Render current screen */}
      {renderScreen()}
    </div>
  );
}

export default App;
