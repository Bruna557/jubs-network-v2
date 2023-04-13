import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
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

  return (
    <div className="login">
      <form className="login-form">
        <Row><h3>Sign in</h3></Row>
        <Row className="username-label">Username:</Row>
        <Row>
          <input value={username} placeholder="username" onChange={(e) => setUsername(e.target.value)} />
        </Row>
        <Row className="password-label">Password:</Row>
        <Row>
          <input value={password} placeholder="password" onChange={(e) => setPassword(e.target.value)} />
        </Row>
        <Row className="buttons">
          <Button variant="primary" onClick={() => handleSignIn()}>Sign In</Button>
        </Row>
        <Row className="no-account">
          Don't have an account?
        </Row>
        <Row className="register">
          <Link to="/register">Register</Link>
        </Row>
      </form>
    </div>
  )
}

export default Login
