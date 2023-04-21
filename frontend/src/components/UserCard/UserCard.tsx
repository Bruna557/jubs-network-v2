import { useSelector } from "react-redux"
import { useNavigate } from "react-router-dom"
import { Row, Col, Button } from "react-bootstrap"

import { User } from "../../types"
import { follow } from "../../services/mocks/followService"
import { getUser } from "../../store/userSlice"

import "./UserCard.scss"

const UserCard = (user: User) => {
  const navigate = useNavigate()
  const u = useSelector(getUser)

  const handleFollow = (username: string, followed: string) => {
    follow(username, followed)
      .catch(() => {
        navigate("/login")
      })
  }

  return (
    <div className="user-card">
      <Row>
        <Col className="profile-picture" md="2">
          <img src={user.picture} alt="profile"/>
        </Col>
        <Col className="username">
          <p>{user.username}</p>
        </Col>
        {user.follow &&
          <Col>
            <Button onClick={() => handleFollow(u.username, user.username)}>Follow</Button>
          </Col>}
      </Row>
      <Row className="bio">
        <p>{user.bio}</p>
      </Row>
    </div>
  )
}

export default UserCard
