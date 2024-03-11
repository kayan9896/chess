import React, { useState } from 'react';
import Cell from './Cell';
import './App.css';

function PlayAI({link}) {
  const [board, setBoard] = useState(null);
  const [selectedCell, setSelectedCell] = useState(null);
  const [message, setMessage] = useState('');
  const [screen, setScreen] = useState('start');
  const [id,setId]=useState('')

  // Function to start the game and fetch the initial board state
  async function startGame (n){
  
    try {
      const response = await fetch(link+'/startai',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "diff":n })
      });
      if (response.ok) {
        const data = await response.json();
        setBoard(data.board);
        setId(data.id)
      } else {
        throw new Error('Failed to fetch board');
      }
    } catch (error) {
      console.error('Error fetching board:', error);
    }
  };
  const renderScreen = () => {
    
        return (
          <div className="difficulty-screen">
            <h2>Select Difficulty</h2>
            <button onClick={() => startGame(1)}>Beginner</button>
            <button onClick={() => startGame(3)}>Amateur</button>
            <button onClick={() => startGame(5)}>Professional</button>
            
          </div>
        );
      }
  // Function to handle cell click
  const handleCellClick = async (row, col) => {
    if (!selectedCell) {
      // First cell clicked, store the position
      setSelectedCell({ row, col });
    } else {
      // Second cell clicked, send move request
      try {
        let promo=''
        if(board[selectedCell.row][selectedCell.col]==='p'&&selectedCell.row===6) promo='q'
        if(board[selectedCell.row][selectedCell.col]==='P'&&selectedCell.row===1) promo='Q'
        const move = `${String.fromCharCode(97 + selectedCell.col)}${8-selectedCell.row}-${String.fromCharCode(97 + col)}${8-row}${promo}`;
        const response = await fetch(link+'/move', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ move,id })
        });
        if (response.ok) {
          const data = await response.json();
          setBoard(data.board);
          setMessage(data.message);
        } else {
          setMessage('Invalid move.')
          throw new Error('Failed to make move');
        }
      } catch (error) {
        console.error('Error making move:', error);
      }
      setSelectedCell(null); // Reset selected cell
      try {
        const response = await fetch(`${link}/getmove/${id}`);
        if (response.ok) {
          const data = await response.json();
          setBoard(data.board);
          setMessage(data.message);
        } else {
          throw new Error('Failed to fetch board');
        }
      } catch (error) {
        console.error('Error fetching board:', error);
      }
    }
  };

  return (
    <div className="App">
      {!board?renderScreen():

      
      (
        <div className="board-container">
          {board.map((row, rowIndex) => (
            <div key={rowIndex} className="row">
              {row.map((p, colIndex) => (
                <Cell
                  key={`${rowIndex}-${colIndex}`}
                  row={rowIndex}
                  col={colIndex}
                  p={p}
                  onClick={() => handleCellClick(rowIndex, colIndex)}
                  isSelected={selectedCell && selectedCell.row === rowIndex && selectedCell.col === colIndex}
                />
              ))}
            </div>
          ))}
          <div className="message">{message}</div>
        </div>
      )}
    </div>
  );
}

export default PlayAI;
