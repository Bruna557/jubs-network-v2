import { useState } from "react"
import { useSelector } from "react-redux"

import { Post } from "../../types"
import PostCard from "../../components/PostCard/PostCard"
import WritePost from "../../components/WritePost/WritePost"
import { getUser } from "../../store/userSlice"
import { fetchTimeline } from "../../services/mocks/timelineService"
import "./Timeline.scss"

const Timeline = () => {
  const [posts, setPosts] = useState<Post[]>([])
  const user = useSelector(getUser)

  fetchTimeline("bruna").then(result => {
    setPosts(result)
  })

  return (
    <>
      <WritePost {...user}/>
      {posts.map((post: Post) => <PostCard {...post} />)}
    </>
  )
}

export default Timeline
