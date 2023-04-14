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
  const [pageNumber, setPageNumber] = useState(1)
  const user = useSelector(getUser)

  useEffect(() => {
    nextPage()
  })

  const nextPage = () => {
    fetchTimeline(user.username, pageNumber).then(result => {
      setPosts(result)
      setPageNumber(pageNumber + 1)
    })
  }

  return (
    <div className="timeline">
      <WritePost {...user}/>
      <InfiniteScroll
        dataLength={posts.length}
        next={nextPage}
        style={{ display: 'flex', flexDirection: 'column-reverse' }} //To put endMessage and loader to the top.
        inverse={true}
        hasMore={true}
        loader={<FontAwesomeIcon icon={faSpinner} spin />}
        endMessage={
          <p style={{ textAlign: 'center' }}>
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
