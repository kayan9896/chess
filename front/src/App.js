import React, { useState } from 'react';
import Cell from './Cell';
import './App.css';
import PlayMyself from './PlayMyself';
import PlayAI from './PlayAI';
import RandomOpponents from './RandomOpponents';
import RoomNumber from './RoomNumber';

function App() {
  const [screen, setScreen] = useState('start');
  const link1='https://shiny-eureka-9v76576wpgh9r95-5000.app.github.dev'
  const link='https://chess-owau.onrender.com/'
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
          <RandomOpponents link={link}/>
        );
      case 'ai':
        return (
          <PlayAI link={link}/>
        );
      case 'me':
        return (
         <PlayMyself link={link}/>
        );
        case 'room':
          return (
           <RoomNumber link={link}/>
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
