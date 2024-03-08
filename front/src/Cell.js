import React from 'react';
import './App.css';

function Cell({ row, col, p, isSelected, onClick}) {
  // Determine cell color based on row and column index
  const isEvenRow = row % 2 === 0;
  const isEvenCol = col % 2 === 0;
  const isWhiteCell = (isEvenRow && isEvenCol) || (!isEvenRow && !isEvenCol);

  // Function to render chess piece pattern based on p prop
  const renderPiece = () => {
    if (p === '.') {
      return null; // No piece, cell remains empty
    } else {
        const pieceUnicodeMap = {
            'P': '\u2659', // Pawn
            'N': '\u2658', // Knight
            'B': '\u2657', // Bishop
            'R': '\u2656', // Rook
            'Q': '\u2655', // Queen
            'K': '\u2654', // King
            'p': '\u265F', // Pawn (black)
            'n': '\u265E', // Knight (black)
            'b': '\u265D', // Bishop (black)
            'r': '\u265C', // Rook (black)
            'q': '\u265B', // Queen (black)
            'k': '\u265A'  // King (black)
          };
          p=pieceUnicodeMap[p]
      return (
        <span role="img" aria-label="chess-piece">
          {p}
        </span>
      );
    }
  };
  const cellClass = `cell ${isWhiteCell ? 'white-cell' : 'black-cell'} ${isSelected ? 'selected-cell' : ''}`;
  return (
    <div className={cellClass} onClick={onClick}>
      {renderPiece()}
    </div>
  );
}

export default Cell;

