import React, { useState,useEffect } from 'react';
import Cell from './Cell';
import './App.css';
import PlayMyself from './PlayMyself';
import PlayAI from './PlayAI';
import RandomOpponents from './RandomOpponents';
import RoomNumber from './RoomNumber';

function App() {
  const [screen, setScreen] = useState('start');
  const link1='https://shiny-eureka-9v76576wpgh9r95-5000.app.github.dev'
  const link=link1//'https://chess-owau.onrender.com'
  // Render screen based on current state
  window.addEventListener("beforeunload", (ev) => 
{  
    ev.preventDefault();
    clear();
    return ev.returnValue = 'Are you sure you want to close?';
});
async function clear() {
  try {
    const response = await fetch(link+'/clear');
  } catch (error) {
    console.error('Error fetching board:', error);
  }
};
  const renderScreen = () => {
    switch (screen) {
      case 'start':
        return (
          <div className="start-screen">
            <h2>Choose Game Mode</h2>
            <button onClick={() => setScreen('me') } className="home-button">Play myself</button>
            <button onClick={() => setScreen('ai')} className="home-button">Play with AI</button>
            <button onClick={() => setScreen('random')} className="home-button">Find random players</button>
            <button onClick={() => setScreen('room')} className="home-button">Enter room number</button>
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
      <button onClick={function(){setScreen('start')}}>Main page</button>
      {/* Render current screen */}
      {renderScreen()}
    </div>
  );
}

export default App;
