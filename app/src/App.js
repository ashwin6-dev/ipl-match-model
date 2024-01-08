import './App.css';
import { useState } from "react";

function Batsman(props) {
  const { score } = props
  const { runs, balls } = score

  return (
    <p>{ runs } ({ balls })</p>
  )
}

function Bowler(props) {
  const { figures } = props
  const { runs, balls, wickets } = figures 

  return (
    <p>{ wickets } - { runs } ({ Math.floor(balls / 6)})</p>
  )
}

function Innings(props) {
  const { inningsData } = props
  const { total, wickets, balls, batting, bowling } = inningsData
  console.log(total, wickets)

  return (
    <div style={{ float: "left", marginRight: "2vw"}}>
      <h3>{ total } - { wickets } ({ Math.floor(balls / 6) } overs)</h3>
      {
        batting.map( batsmanScore => <Batsman score = { batsmanScore } />)
      }
      {
        bowling.map( bowlingFigs => <Bowler figures = { bowlingFigs } />)
      }
    </div>
  )
}

function Scorecard(props) {
  const { scorecard } = props
  
  return (
    <div>
      { 
        scorecard.innings.map( innings => <Innings inningsData = { innings }/> ) 
      }
    </div>
  )
}

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
