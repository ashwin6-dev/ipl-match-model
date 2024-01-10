import './App.css';
import { useState } from "react";
import Scorecard from './Scorecard';

function App() {
  const [scorecard, setScorecard] = useState(0)

  const sim = async () => {
    let response = await fetch("http://localhost:5000/sim")
    let simScorecard = await response.json()

    setScorecard(simScorecard)
  }

  return (
    <div>
      <button onClick = { sim }>Simulate match</button>
      { scorecard != 0 && <Scorecard scorecard={ scorecard }/> }
    </div>
  );
}

export default App;
