import React from 'react';

export default function Footer() {
  return (
    <div className="container">
      <footer className="py-3 my-4">
        <p className="text-center text-muted" style={{fontSize: '18px', fontFamily: 'Segoe UI, Helvetica Neue, Arial, sans-serif', color: 'black'}}>
          Made with <span style={{color: 'red', fontSize: '24px'}}>&#10084;&#65039;</span><br />by 
          <span>
            <a href="https://www.linkedin.com/in/bioenable/" target="_blank" rel="noopener noreferrer" className="mx-1" style={{color: '#0077b5'}}>Dr. Shyam Sundaram</a>, 
            <a href="https://www.linkedin.com/in/animesh2210/" target="_blank" rel="noopener noreferrer" className="mx-1" style={{color: '#0077b5'}}>Animesh Verma</a>,
            <a href="https://www.linkedin.com/in/prateek-balaji/" target="_blank" rel="noopener noreferrer" className="mx-1" style={{color: '#0077b5'}}>Prateek Balaji</a>,
            <a href="https://www.linkedin.com/in/kartikey-bhatnagar/" target="_blank" rel="noopener noreferrer" className="mx-1" style={{color: '#0077b5'}}>Kartikey Bhatnagar</a>, and
            <a href="https://www.linkedin.com/in/avi-gupta-a1679a94/" target="_blank" rel="noopener noreferrer" className="mx-1" style={{color: '#0077b5'}}>Avi Gupta</a>
          </span>
        </p>
      </footer>
    </div>
  );
}




// Add this Footer component in your React application where you want to display the footer.



