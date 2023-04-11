import { Row, Col } from "react-bootstrap"

import { User } from "../../types"
import "./UserCard.scss"

const UserCard = (user: User) => {
  return (
    <div className="user-card">
      <Row>
        <Col className="profile-picture" md="2">
          <img src={user.picture} />
        </Col>
        <Col className="username">
          <p>{user.username}</p>
        </Col>
      </Row>
      <Row>
        <p>{user.bio}</p>
      </Row>
    </div>
  )
}

export default UserCard
