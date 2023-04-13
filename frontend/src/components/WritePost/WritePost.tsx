import { useState } from "react"
import { Button, Row, Col, Card } from "react-bootstrap"

import { User } from "../../types"
import { post } from "../../services/mocks/postService"
import "./WritePost.scss"

const WritePost = (user: User) => {
  const [postBody, setPostBody] = useState("")

  const handleSubmit = () => {
    post(user.username, postBody)
    setPostBody("")
  }

  return (
    <>
      <Card className="write-post">
        <Row>
          <Col md="2">
            <Card.Img variant="top" src={user.picture} />
          </Col>
          <Col className="username"><p>{user.username}</p></Col>
        </Row>
        <Card.Body>
          <Row>
            <form>
              <textarea value={postBody} placeholder="Write a post..." onChange={(e) => setPostBody(e.target.value)} />
            </form>
          </Row>
          <Row className="button-row">
            <Button variant="primary" onClick={handleSubmit}>Post</Button>
          </Row>
        </Card.Body>
      </Card>
    </>
  )
}

export default WritePost
