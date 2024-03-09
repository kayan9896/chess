import React, { useState } from 'react';
import Cell from './Cell';
import './App.css';

function PlayMyself() {
  const [board, setBoard] = useState(null);
  const [selectedCell, setSelectedCell] = useState(null);
  const [message, setMessage] = useState('');
  const [id,setId]=useState('')

  // Function to start the game and fetch the initial board state
  const startGame = async () => {
    try {
      const response = await fetch('https://shiny-eureka-9v76576wpgh9r95-5000.app.github.dev/start');
      if (response.ok) {
        const data = await response.json();
        setBoard(data.board);
        setId(data.id)
        setMessage(data.message);
      } else {
        throw new Error('Failed to fetch board');
      }
    } catch (error) {
      console.error('Error fetching board:', error);
    }
  };

  // Function to handle cell click
  const handleCellClick = async (row, col) => {
    if (!selectedCell) {
      // First cell clicked, store the position
      setSelectedCell({ row, col });
    } else {
      // Second cell clicked, send move request
      try {
        const move = `${String.fromCharCode(97 + selectedCell.col)}${8-selectedCell.row}-${String.fromCharCode(97 + col)}${8-row}`;
        const response = await fetch('https://shiny-eureka-9v76576wpgh9r95-5000.app.github.dev/mov', {
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
          setMessage('Invalid move.');
          throw new Error('Failed to make move');
        }
      } catch (error) {
        console.error('Error making move:', error);
      }
      setSelectedCell(null); // Reset selected cell
      
    }
  };

  return (
    <div className="App">
      {/* Start button */}
      <button onClick={startGame}>Start Game</button>

      {/* Render board if available */}
      {board && (
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

export default PlayMyself;
