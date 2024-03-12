import React, { useState } from 'react';
import Cell from './Cell';
import './App.css';

function PlayMyself({link}) {
  const [board, setBoard] = useState(null);
  const [selectedCell, setSelectedCell] = useState(null);
  const [message, setMessage] = useState('');
  const [id,setId]=useState('')
  const time = Math.floor(new Date().getTime()/ 1000); // Get current time in ISO format
  // Function to start the game and fetch the initial board state
  const startGame = async () => {
    try {
      const response = await fetch(link+'/start');
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
        let promo=''
        if(board[selectedCell.row][selectedCell.col]==='p'&&selectedCell.row===6) promo='q'
        if(board[selectedCell.row][selectedCell.col]==='P'&&selectedCell.row===1) promo='Q'
        const move = `${String.fromCharCode(97 + selectedCell.col)}${8-selectedCell.row}-${String.fromCharCode(97 + col)}${8-row}${promo}`;
        const response = await fetch(link+'/mov', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ move,id,time })
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
      {!board?<button onClick={startGame} style={{marginTop:'10%'}}>Start Game</button>:null}

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
