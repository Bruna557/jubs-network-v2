import { useState } from "react"
import { Button, Row, Col, Card } from 'react-bootstrap'

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
      <Card>
        <Row>
          <Col md="2">
            <Card.Img variant="top" src={user.picture} />
          </Col>
          <Col className="username"><p>{user.username}</p></Col>
        </Row>
        <Card.Body>
          <form>
            <label>
            <textarea value={postBody} onChange={(e) => setPostBody(e.target.value)} />
            </label>
          </form>
          <Button variant="primary" onClick={handleSubmit}>Post</Button>
        </Card.Body>
      </Card>
    </>
  )
}

export default WritePost
