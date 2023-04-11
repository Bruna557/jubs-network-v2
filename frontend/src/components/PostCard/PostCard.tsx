import { Button, Row, Col } from 'react-bootstrap';
import Card from 'react-bootstrap/Card';
import { faThumbsUp } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"

import { Post } from "../../types"
import "./PostCard.scss"

const PostCard = (post: Post) => {
  return (
    <>
      <Card>
        <Row>
          <Col>
            <Card.Img variant="top" src={post.picture} />
          </Col>
          <Col className="posted-on">{post.posted_on.substring(5, 25)}</Col>
        </Row>
        <Card.Body>
          <Card.Text>{post.body}</Card.Text>
          <Row>
            <Col lg="12" className="likes">
              {post.likes}
              <Button className="like-button"><FontAwesomeIcon icon={faThumbsUp} /></Button>
            </Col>

          </Row>
        </Card.Body>
      </Card>
    </>
  )
}

export default PostCard
