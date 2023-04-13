import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { Button, Row } from "react-bootstrap"

import { register } from "../../services/mocks/userService"
import "./Register.scss"

const Register = () => {
  const navigate = useNavigate()
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [bio, setBio] = useState("")
  const [picture, setPicture] = useState("")

  const handleSignUp = () => {
    register(username, password, bio, picture).then(success => {
      if(success) {
        navigate("/")
      }
    })
  }

  return (
    <div className="register">
      <form className="register-form">
        <Row><h3>Sign up</h3></Row>
        <Row className="username-label">Username:</Row>
        <Row>
          <input value={username} placeholder="username" onChange={(e) => setUsername(e.target.value)} />
        </Row>
        <Row className="password-label">Password:</Row>
        <Row>
          <input value={password} placeholder="password" onChange={(e) => setPassword(e.target.value)} />
        </Row>
        <Row className="picture-label">Picture:</Row>
        <Row>
          <input value={picture} placeholder="picture url" onChange={(e) => setPicture(e.target.value)} />
        </Row>
        <Row className="bio-label">Bio:</Row>
        <Row>
          <textarea value={bio} placeholder="let people know who you are" onChange={(e) => setBio(e.target.value)} />
        </Row>
        <Row className="buttons">
          <Button variant="primary" onClick={() => handleSignUp()}>Sign Up</Button>
        </Row>
        <Row className="yes-account">
          Already have an account?
        </Row>
        <Row className="login">
          <Link to="/login">Sign In</Link>
        </Row>
      </form>
    </div>
  )
}

export default Register
