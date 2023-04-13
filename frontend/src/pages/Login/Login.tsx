import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { Button, Row } from "react-bootstrap"

import { login, register } from "../../services/mocks/userService"
import "./Login.scss"

const Login = () => {
  const navigate = useNavigate()
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const handleSignIn = () => {
    login(username, password).then(success => {
      if(success) {
        navigate("/")
      }
    })
  }

  const handleSignUp = () => {
    register(username, password).then(success => {
      if(success) {
        navigate("/")
      }
    })
  }

  return (
    <div className="login">
      <form className="login-form">
        <Row><h3>Sign in or sign up</h3></Row>
        <Row className="username-label">Username:</Row>
        <Row>
          <input value={username} placeholder="username" onChange={(e) => setUsername(e.target.value)} />
        </Row>
        <Row className="password-label">Password:</Row>
        <Row>
          <input value={password} placeholder="password" onChange={(e) => setPassword(e.target.value)} />
        </Row>
        <Row className="buttons">
          <Button variant="primary" onClick={() => handleSignUp()}>Sign Up</Button>
          <Button variant="primary" onClick={() => handleSignIn()}>Sign In</Button>
        </Row>
      </form>
    </div>
  )
}

export default Login
