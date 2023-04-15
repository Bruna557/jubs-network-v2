import { useState, useEffect } from "react"
import { useSelector } from "react-redux"
import InfiniteScroll from "react-infinite-scroll-component"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faSpinner } from "@fortawesome/free-solid-svg-icons"

import { Post } from "../../types"
import PostCard from "../../components/PostCard/PostCard"
import WritePost from "../../components/WritePost/WritePost"
import { getUser } from "../../store/userSlice"
import { fetchTimeline } from "../../services/mocks/timelineService"
import "./Timeline.scss"

const Timeline = () => {
  const [posts, setPosts] = useState<Post[]>([])
  const [hasMore, setHasMore] = useState(true)
  const user = useSelector(getUser)

  useEffect(() => {
    nextPage()
  }, [])

  const nextPage = () => {
    fetchTimeline(user.username, posts.slice(-1)[0].posted_on).then(result => {
      setPosts([...posts, ...result.posts])
      setHasMore(result.has_more)
    })
  }

  return (
    <div className="timeline">
      <WritePost {...user}/>
      <InfiniteScroll
        dataLength={posts.length}
        next={nextPage}
        hasMore={hasMore}
        loader={<FontAwesomeIcon className="spinner" icon={faSpinner} spin/>}
        endMessage={
          <p className="end">
            <b>Yay! You have seen it all</b>
          </p>
        }
        scrollableTarget="scrollableDiv"
      >
        {posts.map((post: Post, i: number) => <PostCard key={i} {...post} />)}
      </InfiniteScroll>
    </div>
  )
}

export default Timeline
