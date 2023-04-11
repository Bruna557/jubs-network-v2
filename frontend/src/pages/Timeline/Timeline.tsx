import { useState } from "react"

import { Post } from "../../types"
import PostCard from "../../components/PostCard/PostCard"
import { fetchTimeline } from "../../services/mocks/timelineService"
import "./Timeline.scss"

const Timeline = () => {
  const [posts, setPosts] = useState<Post[]>([])

  fetchTimeline("bruna").then(result => {
    setPosts(result)
  })

  return (
    <>
      {posts.map((post: Post) => <PostCard {...post} />)}
    </>
  )
}

export default Timeline
