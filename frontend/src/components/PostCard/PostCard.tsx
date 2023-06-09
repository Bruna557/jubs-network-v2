import { useState} from "react"
import { useNavigate } from "react-router-dom"
import { Button, Row, Col, Card } from "react-bootstrap"
import { faThumbsUp } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"

import { Post } from "../../types"
import { like } from "../../services/postService"
import "./PostCard.scss"

const PostCard = (p: Post) => {
  const navigate = useNavigate()
  const [post, setPost] = useState(p)

  const handleLike = () => {
    like(post.username, post.posted_on)
      .then(response => {
        if (response) {
          setPost(post => ({...post, likes: post.likes + 1}))
        }
      })
      .catch(() => {
        navigate("/login")
      })
  }

  return (
    <>
      <Card>
        <Row>
          <Col md="2">
            <Card.Img variant="top" src={post.picture} />
          </Col>
          <Col className="username"><p>{post.username}</p></Col>
          <Col className="posted-on">{post.posted_on.substring(5, 25)}</Col>
        </Row>
        <Card.Body>
          <Card.Text>{post.body}</Card.Text>
          <Row>
            <Col lg="12" className="likes">
              {post.likes}
              <Button className="like-button" onClick={handleLike}>
                <FontAwesomeIcon icon={faThumbsUp} />
              </Button>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    </>
  )
}

export default PostCard
