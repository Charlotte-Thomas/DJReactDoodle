
import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Auth from '../lib/auth'
import { makeStyles } from '@material-ui/core/styles'
import TextField from '@material-ui/core/TextField'
import Button from '@material-ui/core/Button'
import Link from '@material-ui/core/Link'



const Guess = (props) => {

  console.log('GUESS')
  const [data, setData] = useState([])
  const [form, updateForm] = useState()
  const [answer, setAnswer] = useState()
  const [guess1, setGuess1] = useState()
  const [guess2, setGuess2] = useState()
  const [guess3, setGuess3] = useState()


  useEffect(() => {
    // console.log(props.match.params.id)
    fetch(`/api/images/${props.match.params.id}`)
      .then(resp => resp.json())
      .then(resp => {
        setData(resp)
        getAnswer(resp)
        setDisable1(false); setDisable2(false); setDisable3(false)
        setClose1(false); setClose2(false), setClose3(false)
      })
    return () => console.log('Unmounting component')
  }, [props.match.params.id])


  function getAnswer(resp) {
    axios.get(`/api/answers/${resp.correct_answer}`)
      .then(res => {
        setAnswer(res.data.correct_answer)
        // console.log(res.data.correct_answer)
      })
  }

  const useStyles = makeStyles(theme => ({
    root: {
      '& > *': {
        margin: theme.spacing(1),
        width: 200
      }
    }
  }))


  const classes = useStyles()


  function handleInput(e) {
    updateForm(e.target.value)
  }

  const route = `/guess/${parseInt(props.match.params.id) + 1}`
  const [close1, setClose1] = useState(false)
  const [close2, setClose2] = useState(false)
  const [close3, setClose3] = useState(false)
  const [disable1, setDisable1] = useState(false)
  const [disable2, setDisable2] = useState(false)
  const [disable3, setDisable3] = useState(false)

  function checkMatch(ev, ans, input, num) {
    if (ev.key === 'Enter') {
      if (num === 1) setGuess1(input.toLowerCase()); else if (num === 2) setGuess2(input.toLowerCase()); else if (num === 3) setGuess3(input.toLowerCase())
      axios.post('/api/useranswers/', { 'user_answer': input, 'image': parseInt(props.match.params.id) }, {
        headers: { Authorization: `Bearer ${Auth.getToken()}` }
      })
        .then(() => console.log('success'))
      if (ans.toLowerCase() === input.toLowerCase()) {
        console.log(props.match.params.id)
        setDisable1(true); setDisable2(true); setDisable3(true)
      } else if (num === 1) setClose1(true), setDisable1(true); else if (num === 2) setClose2(true), setDisable2(true); else if (num === 3) setClose3(true), setDisable3(true)
      updateForm('')
      ev.preventDefault()
    }
  }

  function checkFail(g1, g2, g3, ans) {
    if (ans) {
      const lower = ans.toLowerCase()
      if (g1 === lower || g2 === lower || g3 === lower) {
        return 'Correct!'
      } else if (g1 && g2 && g3) {
        return `:( Correct answer is: ${ans}`
      }
    }
  }


  const [username, setUser] = useState('unknown')

  function findArtist(user) {
    if (!user) return
    axios.get(`/api/users/${user}`)
      .then((resp) => {
        setUser(resp.data.username)
      })
  }


  
  var small = document.querySelector('small')
  var label = document.querySelector('label')
  var input = document.querySelectorAll('input')[0]
  var input1 = document.querySelectorAll('input')[1]

  label.classList.add('noShow')
  input.classList.add('noShow')
  input1.classList.add('noShow')
  small.classList.add('noShow')

  return (<div className="wholePage">
    <div className="imgColumn">
      <h2 className="artistName">Drawn by {findArtist(data.user_artist)}{username}</h2>
      <img className="guessImage" src={`${data.user_drawn_image}`} alt='drawing not found' width="700px" height="600px" />
    </div>
    <div>
      <div className="formColumn">
        <form className={classes.root} noValidate autoComplete="off">
          <TextField id="outlined-basic" label="guess one" variant="filled" disabled={disable1} error={close1}
            onChange={(e) => handleInput(e)}
            onKeyPress={(ev) => {
              checkMatch(ev, answer, form, 1)
            }}
          />
          <TextField id="outlined-basic2" label="guess two" variant="filled" disabled={disable2} error={close2}
            onChange={(e) => handleInput(e)}
            onKeyPress={(ev) => {
              checkMatch(ev, answer, form, 2)
            }}
          />
          <TextField id="outlined-basic3" label="guess three" variant="filled" disabled={disable3} error={close3}
            onChange={(e) => handleInput(e)}
            onKeyPress={(ev) => {
              checkMatch(ev, answer, form, 3)
            }}
          />
        </form>
        <p className="result">{checkFail(guess1, guess2, guess3, answer)}</p>
      </div>
      <button className="guessButton buttonC" onClick={() => props.history.push(route)}>
        {'Next Painting'}
      </button>
    </div>
  </div>
  )

}

export default Guess