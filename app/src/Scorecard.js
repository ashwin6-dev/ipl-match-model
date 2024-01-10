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

export default Scorecard;