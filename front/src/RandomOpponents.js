import React, { useState,useEffect } from 'react';
import Cell from './Cell';
import './App.css';

function RandomOpponents({link}) {
  const [board, setBoard] = useState(null);
  const [selectedCell, setSelectedCell] = useState(null);
  const [message, setMessage] = useState('');
  const [gameid, setGameid] = useState('');
  const [waiting, setWaiting] = useState(false);
  const [side,setSide] = useState(null);
  const white = new Set(["P","R","N",'B','Q','K']);
  const black = new Set(["p","r","n",'b','q','k']);
  const time = Math.floor(new Date().getTime()/ 1000);

  useEffect(() => {
    const interval = setInterval(fetchBoard, 5000);
    return () => clearInterval(interval);
  });

  async function joinGame(){
    try {
      setWaiting(true);
      const response = await fetch(link+'/find', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({  })
      });
      if (response.ok) {
        const data = await response.json();
        setBoard(data.board);
        setWaiting(false);
        setSide(data.side)
        setGameid(data.gameid)
      } else {
        throw new Error('Failed to join game');
      }
    } catch (error) {
      console.error('Error joining game:', error);
      setWaiting(false);
    }
  };

  async function fetchBoard(){
    if(!board) return;
    try {
      const response = await fetch(link+'/board', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'number':gameid })
      });
      if (response.ok) {
        const data = await response.json();
        setBoard(data.board);
        if (data.message) setMessage(data.message);
      } else {
        setMessage('Gameover')
        throw new Error('Failed to fetch board');
      }
    } catch (error) {
      console.error(error);
    }
  }

  // Function to handle cell click
  const handleCellClick = async (row, col) => {
    if (!selectedCell) {
      // First cell clicked, store the position
      console.log(board[row][col] in black)
      console.log(side)
      if((black.has(board[row][col]) && side===false) ||(white.has(board[row][col]) && side===true))
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
          body: JSON.stringify({ move,'id':gameid,time })
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
      {board? (
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
      ): (
        <div className="waiting-window">
          
          <button onClick={joinGame} disabled={waiting} >
            Start searching
          </button>
          {waiting && <p>Waiting for another player...</p>}
        </div>
      )}
    </div>
  );
}
export default RandomOpponents;
