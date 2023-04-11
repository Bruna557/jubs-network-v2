import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

import { Post } from "../../types"
import "./PostCard.scss"

const PostCard = (post: Post) => {
  return (
    <>
      <Card>
        <Card.Img variant="top" src={post.picture} />
        <Card.Body>
          <Card.Text>{post.body}</Card.Text>
          <Button variant="primary">Like</Button>
        </Card.Body>
      </Card>
    </>
  )
}

export default PostCard
